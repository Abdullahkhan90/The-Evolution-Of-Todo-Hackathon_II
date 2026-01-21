import { Task } from '@/types/task';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export default function TaskItem({ task, onEdit, onDelete }: TaskItemProps) {
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <li className="bg-white hover:bg-gray-50">
      <div className="px-4 py-4 sm:px-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => {}}
              className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
              disabled
            />
            <p className={`ml-4 text-sm font-medium ${
              task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
            }`}>
              {task.title}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            {task.priority && (
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                {task.priority}
              </span>
            )}
            {task.due_date && (
              <span className="text-xs text-gray-500">
                {formatDate(task.due_date)}
              </span>
            )}
          </div>
        </div>
        <div className="mt-2 sm:flex sm:justify-between">
          <div className="sm:flex">
            {task.tags && (
              <div className="flex items-center text-sm text-gray-500">
                <span className="mr-2">#</span>
                <span>{task.tags}</span>
              </div>
            )}
          </div>
          <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
            <span>Created: {formatDate(task.created_at)}</span>
          </div>
        </div>
        <div className="mt-2 text-sm text-gray-600">
          {task.description}
        </div>
        <div className="mt-4 flex justify-end space-x-3">
          <button
            onClick={() => onEdit(task)}
            className="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
}