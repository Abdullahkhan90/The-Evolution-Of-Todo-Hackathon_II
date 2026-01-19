'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/lib/auth';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import ChatInterface from '@/components/ChatInterface';
import { Task } from '@/types/task';
import { useTaskContext } from '@/contexts/TaskContext';

const DashboardPage = () => {
  const { state, fetchTasks, addTask, updateTask, completeTask, deleteTask } = useTaskContext();
  const { tasks, loading } = state;
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showChat, setShowChat] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
      return;
    }

    fetchTasks();
  }, [router]); // Removed fetchTasks from dependencies to prevent infinite loop

  const handleCreateTask = async (taskData: any) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      // Convert taskData to match the API format
      const apiTaskData = {
        ...taskData,
        title: taskData.title || '',
        user_id: userId
      };

      await addTask(apiTaskData);
      setShowForm(false);
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleUpdateTask = async (taskData: any) => {
    if (!editingTask) return;

    try {
      await updateTask({ ...editingTask, ...taskData });
      setEditingTask(null);
      setShowForm(false);
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await deleteTask(taskId);
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleLogout = async () => {
    await authService.logout();
    router.push('/login');
  };

  // Memoize the task count display to prevent unnecessary re-renders
  const taskCountDisplay = useMemo(() => (
    <p className="text-indigo-100 mt-1">You have {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} to complete today.</p>
  ), [tasks.length]);

  const taskTotalBadge = useMemo(() => (
    <span className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-3 py-1 rounded-full">
      {tasks.length} total
    </span>
  ), [tasks.length]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Enhanced Navigation Bar */}
      <nav className="bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 shadow-lg shadow-indigo-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="bg-white/20 p-2 rounded-lg backdrop-blur-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h1 className="ml-3 text-2xl font-bold text-white tracking-tight">Todo Dashboard</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => {
                  setEditingTask(null);
                  setShowForm(true);
                }}
                className="bg-white text-indigo-600 px-6 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5"
              >
                <div className="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span>Add Task</span>
                </div>
              </button>
              <button
                onClick={handleLogout}
                className="text-white/90 hover:text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-white/10 transition-all duration-200"
              >
                <div className="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span>Logout</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-1 gap-8">
          {/* Welcome Banner - Memoized to prevent re-renders */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-6 text-white shadow-xl">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="bg-white/20 p-3 rounded-full backdrop-blur-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h2 className="text-2xl font-bold">Welcome Back!</h2>
                {taskCountDisplay}
              </div>
            </div>
          </div>

          {/* Tasks Section */}
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-800 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Your Tasks
              </h2>
              {taskTotalBadge}
            </div>
            <div className="bg-gray-50/50 rounded-xl p-4 min-h-[400px]">
              <TaskList
                tasks={tasks}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
              />
            </div>
          </div>
        </div>
      </main>

      {/* Floating Chat Button - Enhanced with gradient and animation */}
      <button
        onClick={() => setShowChat(true)}
        className="fixed bottom-8 right-8 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white p-5 rounded-full shadow-2xl hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600 focus:outline-none focus:ring-4 focus:ring-purple-300 z-50 transform transition-all duration-300 hover:scale-110 animate-pulse-slow border-2 border-white"
        aria-label="Open AI Chatbot"
      >
        <div className="flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </div>
      </button>

      {/* Enhanced Chat Panel - Modern glassmorphism */}
      <div
        className={`fixed bottom-24 right-8 w-full max-w-md h-[70vh] backdrop-blur-2xl bg-gradient-to-br from-indigo-50/90 to-purple-50/90 rounded-2xl shadow-2xl z-50 overflow-hidden transform transition-all duration-300 ease-in-out border border-white/40 shadow-indigo-100/30 ${
          showChat ? 'opacity-100 translate-y-0 pointer-events-auto' : 'opacity-0 translate-y-4 pointer-events-none'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 p-5 flex justify-between items-center backdrop-blur-md">
            <div className="flex items-center space-x-2">
              <div className="bg-white/20 p-1.5 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h2 className="text-white text-lg font-bold">AI Assistant</h2>
            </div>
            <button
              onClick={() => setShowChat(false)}
              className="text-white/90 hover:text-white hover:bg-white/20 p-1.5 rounded-lg focus:outline-none transition-all duration-200"
              aria-label="Close chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 bg-white/30 backdrop-blur-sm">
            <ChatInterface />
          </div>
        </div>
      </div>

      {/* Enhanced Modal Form */}
      {showForm && (
        <div className="fixed inset-0 bg-black/30 backdrop-blur-sm overflow-y-auto h-full w-full flex items-center justify-center p-4 z-50">
          <div className="relative mx-auto w-full max-w-md transform transition-all duration-300 scale-100">
            <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-2xl border border-gray-200/50 overflow-hidden">
              <div className="px-6 pt-6 pb-4">
                <div className="flex justify-between items-center pb-4 border-b border-gray-200/50">
                  <div className="flex items-center space-x-3">
                    <div className="bg-indigo-100 p-2 rounded-lg">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-bold text-gray-900">
                      {editingTask ? 'Edit Task' : 'Create New Task'}
                    </h3>
                  </div>
                  <button
                    onClick={() => {
                      setShowForm(false);
                      setEditingTask(null);
                    }}
                    className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-1 rounded-lg transition-all duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
              <div className="px-6 pb-6">
                <TaskForm
                  task={editingTask || undefined}
                  onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
                  onCancel={() => {
                    setShowForm(false);
                    setEditingTask(null);
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;