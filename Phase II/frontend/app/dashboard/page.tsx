'use client';

import React, { useEffect } from 'react';
import ProtectedRoute from '@/src/components/auth/ProtectedRoute';
import TodoList from '@/src/components/todo/TodoList';
import TodoForm from '@/src/components/todo/TodoForm';
import useTodos from '@/src/hooks/useTodos';

export default function DashboardPage() {
  const { fetchTodos, createTodo, todos, loading, error } = useTodos();

  useEffect(() => {
    // Fetch todos when the component mounts
    fetchTodos();
  }, [fetchTodos]);

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900">My Tasks</h1>
            <p className="mt-2 text-gray-600">Manage your daily tasks efficiently</p>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              Error: {error}
            </div>
          )}

          <TodoForm onCreateTodo={createTodo} />

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-gray-600">Loading tasks...</p>
              </div>
            </div>
          ) : (
            <TodoList todos={todos} />
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
