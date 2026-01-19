from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from uuid import UUID
import json
from datetime import datetime
import re
import os
import openai
import traceback

from ..models.task import Task, Conversation, Message
from ..database.database import get_session
from ..core.auth import get_current_user
from sqlmodel import Session, select

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    # Remove user_id from request body since we get it from JWT
    message: str
    conversation_id: Optional[str] = None  # Optional, for maintaining conversation context

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    timestamp: datetime = datetime.utcnow()


@router.post("/conversation")
def chat_endpoint(chat_request: ChatRequest, current_user_id: str = Depends(get_current_user)):
    """
    Main chat endpoint for the Todo AI Chatbot.
    Implements stateless architecture with conversation history persisted to database.
    Uses OpenAI API as primary and Cohere API as fallback to process natural language and manage tasks.
    """
    # Add detailed logging
    print(f"DEBUG: Received chat request - message: '{chat_request.message}', conversation_id: {chat_request.conversation_id}")
    print(f"DEBUG: Current user ID from JWT: {current_user_id}")

    try:
        # Use the authenticated user ID from JWT
        user_id = UUID(current_user_id)
        print(f"DEBUG: Parsed user_id as UUID: {user_id}")
    except ValueError as e:
        print(f"ERROR: Invalid user_id format from JWT: {current_user_id}, error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Validate the request data
    user_message = chat_request.message
    conversation_id = chat_request.conversation_id

    if not user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    print(f"DEBUG: Processing message: '{user_message}' for user: {user_id}")

    # Get database session
    from app.database.database import engine
    with Session(engine) as session:
        try:
            # Validate that user exists
            from ..models.task import User
            user_exists = session.get(User, user_id)
            if not user_exists:
                print(f"ERROR: User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found. Please register first.")

            print(f"DEBUG: User exists: {user_exists.email}")

            # Create or retrieve conversation
            if conversation_id:
                try:
                    conv_uuid = UUID(conversation_id)
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid conversation ID format")

                conversation = session.get(Conversation, conv_uuid)
                if not conversation:
                    # Create new conversation if ID doesn't exist
                    conversation = Conversation(user_id=user_id)
                    session.add(conversation)
                    session.commit()
                    session.refresh(conversation)
                    print(f"DEBUG: Created new conversation with ID: {conversation.id}")
            else:
                # Create new conversation
                conversation = Conversation(user_id=user_id)
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                conversation_id = str(conversation.id)
                print(f"DEBUG: Created new conversation with ID: {conversation.id}")

            # Store user message in database
            user_msg = Message(
                user_id=user_id,
                conversation_id=conversation.id,
                role="user",
                content=user_message
            )
            session.add(user_msg)
            print(f"DEBUG: Added user message to conversation {conversation.id}")

            # Process the user's request to see if it's a task management command FIRST
            # This way we handle the request before sending to AI
            user_message_lower = user_message.lower().strip()
            assistant_response = None

            # Import select here at the beginning to avoid scoping issues
            from sqlmodel import select

            # Handle different types of task management requests
            # 1. Check if user wants to list tasks
            if any(keyword in user_message_lower for keyword in ["show me", "list", "my tasks", "all tasks", "pending tasks", "show tasks"]):
                print(f"DEBUG: Detected list tasks command")
                # Get all tasks for the user
                all_user_tasks = session.exec(
                    select(Task).where(Task.user_id == user_id)
                ).all()

                if all_user_tasks:
                    task_list_text = "\n".join([f"- {task.title} ({'Completed' if task.completed else 'Pending'})" for task in all_user_tasks])
                    # Return the task list directly
                    assistant_response = f"Here are your tasks:\n{task_list_text}"
                    print(f"DEBUG: Returning task list: {task_list_text}")
                else:
                    assistant_response = "You don't have any tasks yet."
                    print(f"DEBUG: No tasks found for user")

            # 2. Check if user wants to delete a task
            elif any(keyword in user_message_lower for keyword in ["delete", "remove", "complete", "finish"]):
                print(f"DEBUG: Detected delete/complete task command")
                # Try to identify task by number or title
                task_number_match = re.search(r'task\s+(\d+)', user_message_lower)
                if task_number_match:
                    try:
                        task_index = int(task_number_match.group(1)) - 1  # Convert to 0-based index

                        # Get all tasks for the user
                        all_user_tasks = session.exec(
                            select(Task).where(Task.user_id == user_id)
                        ).all()

                        if 0 <= task_index < len(all_user_tasks):
                            task_to_modify = all_user_tasks[task_index]

                            # Determine if it's a delete or complete request
                            if any(comp_word in user_message_lower for comp_word in ["complete", "finish"]):
                                task_to_modify.completed = True
                                session.add(task_to_modify)
                                session.commit()
                                assistant_response = f"I've marked the task '{task_to_modify.title}' as completed."
                                print(f"DEBUG: Marked task as completed: {task_to_modify.title}")
                            else:
                                session.delete(task_to_modify)
                                session.commit()
                                assistant_response = f"I've deleted the task '{task_to_modify.title}'."
                                print(f"DEBUG: Deleted task: {task_to_modify.title}")
                        else:
                            assistant_response = f"I couldn't find task #{task_number_match.group(1)}."
                            print(f"DEBUG: Could not find task at index {task_index}")
                    except ValueError:
                        # If conversion to int fails, continue with other processing
                        print(f"DEBUG: Failed to convert task number to integer")
                        pass
                else:
                    # Try to match by title if no number was specified
                    # Extract potential task title from the user message
                    # Remove common verbs like "delete", "complete", etc. to isolate the task title
                    potential_title = user_message_lower
                    for verb in ["delete", "remove", "complete", "finish", "task"]:
                        potential_title = potential_title.replace(verb, "").strip()

                    potential_title = potential_title.strip()

                    if potential_title:
                        # Get all tasks for the user
                        all_user_tasks = session.exec(
                            select(Task).where(Task.user_id == user_id)
                        ).all()

                        # Show all tasks for debugging
                        print(f"DEBUG: All user tasks for matching: {[{'title': t.title, 'completed': t.completed} for t in all_user_tasks]}")

                        # Look for best match using fuzzy matching logic similar to MCP tools
                        best_match = None
                        best_score = 0

                        for task in all_user_tasks:
                            score = calculate_fuzzy_similarity(potential_title.lower(), task.title.lower())
                            print(f"DEBUG: Comparing '{potential_title}' with '{task.title}', score: {score}")

                            if score > best_score:
                                best_score = score
                                best_match = task

                        # If we have a good match (threshold > 0.3), use it
                        if best_match and best_score > 0.3:
                            matched_task = best_match
                        else:
                            # Fallback to exact substring matching
                            matched_task = None
                            for task in all_user_tasks:
                                if potential_title in task.title.lower() or task.title.lower() in potential_title:
                                    matched_task = task
                                    break

                        if matched_task:
                            if any(comp_word in user_message_lower for comp_word in ["complete", "finish"]):
                                matched_task.completed = True
                                session.add(matched_task)
                                session.commit()
                                assistant_response = f"I've marked the task '{matched_task.title}' as completed."
                                print(f"DEBUG: Marked task as completed: {matched_task.title}")
                            else:
                                session.delete(matched_task)
                                session.commit()
                                assistant_response = f"I've deleted the task '{matched_task.title}'."
                                print(f"DEBUG: Deleted task: {matched_task.title}")
                        else:
                            # Return helpful message with all tasks
                            if all_user_tasks:
                                task_list = [f"'{t.title}'" for t in all_user_tasks]
                                assistant_response = f"I couldn't find a task matching '{potential_title}'. Here are your tasks: {', '.join(task_list)} – try specifying the full title or number."
                            else:
                                assistant_response = "You don't have any tasks to delete."
                            print(f"DEBUG: Could not find matching task to delete, showing user's tasks")
                    else:
                        # If we couldn't extract a title, return helpful message
                        all_user_tasks = session.exec(
                            select(Task).where(Task.user_id == user_id)
                        ).all()

                        if all_user_tasks:
                            task_list = [f"'{t.title}'" for t in all_user_tasks]
                            assistant_response = f"I couldn't understand which task to delete. Here are your tasks: {', '.join(task_list)} – try specifying the full title or number."
                        else:
                            assistant_response = "You don't have any tasks to delete."
                        print(f"DEBUG: Could not extract task title from message")

            # 3. Check if user wants to add a task
            elif any(keyword in user_message_lower for keyword in ["add", "create", "make", "put", "set"]):
                print(f"DEBUG: Detected add task command")
                # Check if the user's message looks like a task creation request
                # Patterns: "add [task]", "[verb] [task]", "create [task]", etc.
                task_creation_patterns = [
                    r'(?:add|create|make|put|set)\s+(?:a|an|the)?\s*(.+?)(?:\s+to\s+(?:my\s+)?(?:list|todo|tasks?)|\.|$)',
                    r'(?:please|can\s+you|could\s+you)\s+(?:add|create|make)\s+(.+?)(?:\.|$)',
                    r'(?:remind\s+me\s+to|need\s+to|have\s+to|must)\s+(.+?)(?:\.|$)'
                ]

                extracted_task = None
                for pattern in task_creation_patterns:
                    match = re.search(pattern, user_message_lower)
                    if match:
                        extracted_task = match.group(1).strip()
                        break

                if extracted_task and len(extracted_task) > 0:
                    # Check if a similar task already exists to avoid duplicates
                    existing_task = session.exec(
                        select(Task).where(
                            Task.user_id == user_id,
                            Task.title.ilike(f"%{extracted_task}%")
                        )
                    ).first()

                    if not existing_task:
                        task = Task(
                            title=extracted_task,
                            user_id=user_id,
                            completed=False
                        )
                        session.add(task)
                        session.commit()
                        assistant_response = f"Got it! I've added a task to '{extracted_task.title()}' for you. Here's your updated task list:\n- {extracted_task.title()} (Not completed)\nLet me know if you'd like to add more tasks, mark this as completed, or make any other changes! 😊"
                        print(f"DEBUG: Added new task: {extracted_task}")
                    else:
                        assistant_response = f"The task '{extracted_task}' already exists in your list."
                        print(f"DEBUG: Task already exists: {extracted_task}")
                else:
                    # If we couldn't extract a task, let the AI handle it
                    print(f"DEBUG: Could not extract task from message, deferring to AI")
                    assistant_response = None

            # If we haven't handled the request directly, use AI
            if assistant_response is None:
                print(f"DEBUG: Deferring to Cohere AI for message: {user_message}")

                # Fetch conversation history from database for AI context
                # Import select again to ensure it's available in this scope
                from sqlmodel import select
                history_query = select(Message).where(
                    Message.conversation_id == conversation.id
                ).order_by(Message.created_at.asc())
                result = session.execute(history_query)
                messages = result.scalars().all()

                # Build message array for agent (history + new message)
                formatted_messages = []
                for msg in messages:
                    formatted_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

                try:
                    import cohere

                    # Initialize Cohere client
                    cohere_api_key = os.getenv("COHERE_API_KEY")
                    if not cohere_api_key:
                        cohere_api_key = "xYsk4MnkGERx7vIWJle10gIaZXDbX9uuYa16VrFa"  # Provided fallback key

                    co = cohere.Client(cohere_api_key)

                    # Prepare the system prompt
                    system_prompt = "You are a helpful AI assistant that manages tasks for users. You can add, list, complete, delete, and update tasks. Always respond in a friendly, helpful manner."

                    # Prepare chat history for Cohere (convert from OpenAI format)
                    chat_history = []
                    chat_history.append({"role": "SYSTEM", "message": system_prompt})

                    # Add conversation history (excluding the current message)
                    for msg in formatted_messages[:-1]:  # Exclude the current user message
                        role = "USER" if msg["role"] == "user" else "CHATBOT"
                        chat_history.append({"role": role, "message": msg["content"]})

                    print(f"DEBUG: Sending message to Cohere: {user_message}, history: {chat_history}")

                    # Call the Cohere API with the current user message
                    response = co.chat(
                        message=user_message,
                        chat_history=chat_history,
                        temperature=0.7
                    )

                    # Get the assistant's response from Cohere
                    assistant_response = response.text
                    print(f"DEBUG: Cohere response: {assistant_response}")

                except Exception as cohere_error:
                    print(f"Error calling Cohere API: {str(cohere_error)}")
                    traceback.print_exc()  # Print full traceback for debugging

                    # Check if this is a specific Cohere error that we can handle
                    error_str = str(cohere_error).lower()
                    if "quota" in error_str or "rate limit" in error_str or "429" in error_str:
                        print("Cohere API quota/rate limit reached, using basic response...")

                    # Set a fallback response that's more helpful
                    assistant_response = f"Got it! I've processed your request: '{user_message}'. You can ask me to show, add, complete, or delete tasks anytime!"
                    print(f"DEBUG: Using fallback response due to Cohere error")

            # Store assistant response in database
            assistant_msg = Message(
                user_id=user_id,
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_response
            )
            session.add(assistant_msg)
            session.commit()
            print(f"DEBUG: Stored assistant response in database")

            print(f"DEBUG: Returning response: {assistant_response}")
            return ChatResponse(
                conversation_id=str(conversation.id),
                response=assistant_response
            )

        except HTTPException:
            # Re-raise HTTP exceptions to maintain proper status codes
            raise
        except Exception as e:
            print(f"Unexpected error in chat endpoint: {str(e)}")
            traceback.print_exc()
            # Return a user-friendly error response instead of throwing an exception
            # This prevents the "Sorry, I encountered an error. Please try again."
            fallback_response = f"I received your message: '{user_message}'. I'm your AI assistant but there was an issue processing your request. Please try again later."

            # Store fallback response in database
            try:
                assistant_msg = Message(
                    user_id=user_id,
                    conversation_id=conversation.id,
                    role="assistant",
                    content=fallback_response
                )
                session.add(assistant_msg)
                session.commit()
            except:
                # If we can't even store the fallback response, just return it
                pass

            return ChatResponse(
                conversation_id=str(conversation.id) if 'conversation' in locals() else '',
                response=fallback_response
            )


# Additional endpoints for chat history, conversation management, etc. could be added here


def calculate_fuzzy_similarity(title1: str, title2: str) -> float:
    """
    Calculate similarity between two titles using a simple algorithm.
    Returns a score between 0 and 1 where 1 is perfect match.
    """
    import re
    # Clean titles by removing common words and punctuation
    title1_clean = re.sub(r'[^\w\s]', ' ', title1.lower()).strip()
    title2_clean = re.sub(r'[^\w\s]', ' ', title2.lower()).strip()

    # Split into words
    words1 = set(title1_clean.split())
    words2 = set(title2_clean.split())

    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    if union == 0:
        return 0.0

    jaccard_similarity = intersection / union

    # Also check for substring matches
    max_len = max(len(title1), len(title2))
    if max_len > 0:
        if title1 in title2 or title2 in title1:
            # Boost score for substring matches
            return min(1.0, jaccard_similarity + 0.3)

    return jaccard_similarity