import { useState, useCallback } from 'react';
import todoService from '@/src/services/todo-service';
import { Todo } from '../types/todo';

interface TodosState {
  todos: Todo[];
  loading: boolean;
  error: string | null;
}

const useTodos = () => {
  const [state, setState] = useState<TodosState>({
    todos: [],
    loading: false,
    error: null,
  });

  // Fetch all todos
  const fetchTodos = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const todos = await todoService.getAllTodos();
      setState({
        todos,
        loading: false,
        error: null,
      });
    } catch (error) {
      setState({
        todos: [],
        loading: false,
        error: (error as Error).message || 'Failed to fetch todos',
      });
    }
  }, []);

  // Create a new todo
  const createTodo = async (todoData: Omit<Todo, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const newTodo = await todoService.createTodo(todoData);
      setState(prev => ({
        ...prev,
        todos: [...prev.todos, newTodo],
        loading: false,
      }));
      return newTodo;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: (error as Error).message || 'Failed to create todo',
      }));
      throw error;
    }
  };

  // Update a todo
  const updateTodo = async (id: number, todoData: Partial<Todo>) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const updatedTodo = await todoService.updateTodo(id, todoData);
      setState(prev => ({
        ...prev,
        todos: prev.todos.map(todo => (todo.id === id ? updatedTodo : todo)),
        loading: false,
      }));
      return updatedTodo;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: (error as Error).message || 'Failed to update todo',
      }));
      throw error;
    }
  };

  // Toggle todo completion status
  const toggleTodoComplete = async (id: number, completed: boolean) => {
    try {
      const updatedTodo = await todoService.toggleTodoComplete(id, completed);
      setState(prev => ({
        ...prev,
        todos: prev.todos.map(todo => (todo.id === id ? updatedTodo : todo)),
      }));
      return updatedTodo;
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: (error as Error).message || 'Failed to toggle todo completion',
      }));
      throw error;
    }
  };

  // Delete a todo
  const deleteTodo = async (id: number) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      await todoService.deleteTodo(id);
      setState(prev => ({
        ...prev,
        todos: prev.todos.filter(todo => todo.id !== id),
        loading: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: (error as Error).message || 'Failed to delete todo',
      }));
      throw error;
    }
  };

  return {
    ...state,
    fetchTodos,
    createTodo,
    updateTodo,
    toggleTodoComplete,
    deleteTodo,
  };
};

export default useTodos;
