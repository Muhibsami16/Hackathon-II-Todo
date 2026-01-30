'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '../../services/api-client';
import authService from '../../services/auth';
import TodoList from '../../components/Todo/TodoList';
import TodoForm from '../../components/Todo/TodoForm';

export default function DashboardPage() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  // Check if user is authenticated
  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  // Load todos
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getTodos();
        setTodos(data);
      } catch (err) {
        setError(err.message || 'Failed to load todos');
      } finally {
        setLoading(false);
      }
    };

    if (authService.isAuthenticated()) {
      fetchTodos();
    }
  }, []);

  const handleAddTodo = async (todoData) => {
    try {
      const newTodo = await apiClient.createTodo(todoData);
      setTodos([newTodo, ...todos]);
    } catch (err) {
      setError(err.message || 'Failed to add todo');
    }
  };

  const handleToggleComplete = async (id, completed) => {
    try {
      const updatedTodo = await apiClient.toggleTodoComplete(id, !completed);
      setTodos(todos.map(todo =>
        todo.id === id ? updatedTodo : todo
      ));
    } catch (err) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const handleUpdateTodo = async (id, todoData) => {
    try {
      const updatedTodo = await apiClient.updateTodo(id, todoData);
      setTodos(todos.map(todo =>
        todo.id === id ? updatedTodo : todo
      ));
    } catch (err) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await apiClient.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError(err.message || 'Failed to delete todo');
    }
  };

  const handleLogout = async () => {
    await authService.logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading todos...</p>
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
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="ml-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
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
            {error && (
              <div className="mb-4 rounded-md bg-red-50 p-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            <TodoForm onAddTodo={handleAddTodo} />

            <div className="mt-8">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Your Todos</h2>
              <TodoList
                todos={todos}
                onToggleComplete={handleToggleComplete}
                onUpdateTodo={handleUpdateTodo}
                onDeleteTodo={handleDeleteTodo}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}