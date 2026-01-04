"""
Helper functions for the CLI Todo Application.
"""
import re
from typing import Tuple, Dict, Any, List, Optional


class IDGenerator:
    """
    Generates unique IDs for tasks.
    """
    def __init__(self):
        self._current_id = 0

    def generate_id(self) -> int:
        """
        Generate the next unique ID.
        """
        self._current_id += 1
        return self._current_id


# Global ID generator instance
id_generator = IDGenerator()


def get_next_id() -> int:
    """
    Get the next unique ID for a task.
    """
    return id_generator.generate_id()


def parse_command_flags(command: str) -> Tuple[str, List[str], Dict[str, Any]]:
    """
    Parse a command string into base command, arguments, and flags.
    Returns a tuple of (base_command, args, flags_dict)
    """
    # Split command using regex that respects quoted strings
    # This pattern matches either quoted strings or non-whitespace sequences
    pattern = r'"([^"]*)"|(\S+)'
    matches = re.findall(pattern, command.strip())
    
    # Each match is a tuple where either the quoted part [0] or unquoted part [1] is present
    parts = [match[0] if match[0] else match[1] for match in matches]
    
    if not parts:
        return None, [], {}
    
    base_cmd = parts[0].lower()
    args = []
    flags = {}

    i = 1
    while i < len(parts):
        part = parts[i]
        if part.startswith('--'):
            # This is a flag
            flag_name = part[2:]  # Remove '--' prefix
            if i + 1 < len(parts) and not parts[i + 1].startswith('--'):
                # Next part is the flag value
                flags[flag_name] = parts[i + 1]
                i += 2  # Skip both flag and its value
            else:
                # Flag without value (like a boolean flag)
                flags[flag_name] = True
                i += 1
        else:
            # Regular argument
            args.append(part)
            i += 1

    return base_cmd, args, flags


def validate_priority(priority: str) -> bool:
    """
    Validate the priority value.
    """
    if priority is None:
        return True
    
    valid_priorities = ["high", "medium", "low", "h", "m", "l", "1", "2", "3"]
    if priority.lower() not in valid_priorities:
        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
    return True


def validate_due_date(due_date: str) -> bool:
    """
    Validate the due date format (YYYY-MM-DD).
    """
    if due_date is None:
        return True
    
    import re
    # Check if date matches YYYY-MM-DD format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
        raise ValueError("Due date must be in YYYY-MM-DD format")
    
    # Additional validation to check if it's a valid date
    try:
        import datetime
        datetime.datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Due date must be a valid date in YYYY-MM-DD format")
    
    return True


def validate_tags(tags_str: str) -> List[str]:
    """
    Validate and parse tags from a comma-separated string.
    """
    if tags_str is None:
        return []
    
    tags = [tag.strip() for tag in tags_str.split(',')]
    
    for tag in tags:
        if not tag:
            raise ValueError("Tags cannot be empty")
        if len(tag) > 50:
            raise ValueError("Each tag must be 50 characters or less")
        # Check for valid tag characters (alphanumeric, hyphens, underscores)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', tag):
            raise ValueError(f"Tag '{tag}' contains invalid characters. Only alphanumeric, hyphens, and underscores are allowed.")
    
    return tags