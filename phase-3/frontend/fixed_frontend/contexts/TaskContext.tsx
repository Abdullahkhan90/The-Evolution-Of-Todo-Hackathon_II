'use client';

import React, { createContext, useContext, useReducer, ReactNode, useCallback } from 'react';
import { Task } from '@/types/task';
import { authService } from '@/lib/auth';
import { apiClient } from '@/lib/api';

interface TaskState {
  tasks: Task[];
  loading: boolean;
}

type TaskAction =
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'COMPLETE_TASK'; payload: string }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean };

const TaskContext = createContext<{
  state: TaskState;
  fetchTasks: () => Promise<void>;
  addTask: (task: Task) => Promise<void>;
  updateTask: (task: Task) => Promise<void>;
  completeTask: (taskId: string) => Promise<void>;
  deleteTask: (taskId: string) => Promise<void>;
} | undefined>(undefined);

const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'SET_TASKS':
      return { ...state, tasks: action.payload };
    case 'ADD_TASK':
      return {
        ...state,
        tasks: [...state.tasks, action.payload]
      };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        )
      };
    case 'COMPLETE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload ? { ...task, completed: true } : task
        )
      };
    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload)
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    default:
      return state;
  }
};

export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(taskReducer, { tasks: [], loading: false });

  const fetchTasks = useCallback(async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      const data = await apiClient.getTasks(userId);
      dispatch({ type: 'SET_TASKS', payload: data });
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, []);

  const addTask = useCallback(async (task: Task) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      const newTask = await apiClient.createTask(userId, task);
      dispatch({ type: 'ADD_TASK', payload: newTask });
    } catch (error) {
      console.error('Error adding task:', error);
      throw error;
    }
  }, []);

  const updateTask = useCallback(async (task: Task) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      const updatedTask = await apiClient.updateTask(userId, task.id, task);
      dispatch({ type: 'UPDATE_TASK', payload: updatedTask });
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }, []);

  const completeTask = useCallback(async (taskId: string) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      // Update the task status to completed
      await apiClient.updateTask(userId, taskId, { completed: true });
      dispatch({ type: 'COMPLETE_TASK', payload: taskId });
    } catch (error) {
      console.error('Error completing task:', error);
      throw error;
    }
  }, []);

  const deleteTask = useCallback(async (taskId: string) => {
    try {
      const userId = authService.getCurrentUserId();
      if (!userId) return;

      await apiClient.deleteTask(userId, taskId);
      dispatch({ type: 'DELETE_TASK', payload: taskId });
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }, []);

  return (
    <TaskContext.Provider value={{ state, fetchTasks, addTask, updateTask, completeTask, deleteTask }}>
      {children}
    </TaskContext.Provider>
  );
};

export const useTaskContext = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};