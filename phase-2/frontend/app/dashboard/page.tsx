'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/lib/auth';
import { apiClient } from '@/lib/api';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import { Task } from '@/types/task';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
      return;
    }

    fetchTasks();
  }, [router]);

  const fetchTasks = async () => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) {
        router.push('/login');
        return;
      }

      const data = await apiClient.getTasks(userId);
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = (taskData: any) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      // Convert taskData to match the API format
      const apiTaskData = {
        ...taskData,
        title: taskData.title || '',
        user_id: userId
      };

      apiClient.createTask(userId, apiTaskData).then(newTask => {
        setTasks([...tasks, newTask]);
        setShowForm(false);
      }).catch(error => {
        console.error('Error creating task:', error);
      });
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleUpdateTask = (taskData: any) => {
    if (!editingTask) return;

    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      apiClient.updateTask(userId, editingTask.id, taskData).then(updatedTask => {
        setTasks(tasks.map(task =>
          task.id === editingTask.id ? updatedTask : task
        ));

        setEditingTask(null);
        setShowForm(false);
      }).catch(error => {
        console.error('Error updating task:', error);
      });
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      await apiClient.deleteTask(userId, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
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
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => {
                  setEditingTask(null);
                  setShowForm(true);
                }}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Add Task
              </button>
              <button
                onClick={handleLogout}
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-6">
            <TaskList
              tasks={tasks}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
            />
          </div>
        </div>
      </main>

      {showForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center pb-3 border-b">
                <h3 className="text-lg font-medium text-gray-900">
                  {editingTask ? 'Edit Task' : 'Create New Task'}
                </h3>
                <button
                  onClick={() => {
                    setShowForm(false);
                    setEditingTask(null);
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
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
      )}
    </div>
  );
}