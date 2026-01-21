export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_date?: string; // ISO date string
  recurrence?: string;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskInput {
  title: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_date?: string;
  recurrence?: string;
  user_id: string;
}