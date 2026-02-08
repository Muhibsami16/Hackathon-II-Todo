import apiClient from './api-client';
import { Todo, TodoCreate, TodoUpdate } from '../types/todo';

class TodoService {
  // Get all todos for the authenticated user
  async getAllTodos(): Promise<Todo[]> {
    try {
      const response = await apiClient.getTodos();
      return response;
    } catch (error) {
      console.error('Error fetching todos:', error);
      throw error;
    }
  }

  // Get a single todo by ID
  async getTodoById(id: number): Promise<Todo> {
    try {
      const response = await apiClient.getTodoById(id);
      return response;
    } catch (error) {
      console.error(`Error fetching todo ${id}:`, error);
      throw error;
    }
  }

  // Create a new todo
  async createTodo(todoData: TodoCreate): Promise<Todo> {
    try {
      const response = await apiClient.createTodo(todoData);
      return response;
    } catch (error) {
      console.error('Error creating todo:', error);
      throw error;
    }
  }

  // Update an existing todo
  async updateTodo(id: number, todoData: TodoUpdate): Promise<Todo> {
    try {
      const response = await apiClient.updateTodo(id, todoData);
      return response;
    } catch (error) {
      console.error(`Error updating todo ${id}:`, error);
      throw error;
    }
  }

  // Toggle todo completion status
  async toggleTodoComplete(id: number, completed: boolean): Promise<Todo> {
    try {
      const response = await apiClient.toggleTodoComplete(id, completed);
      return response;
    } catch (error) {
      console.error(`Error toggling todo ${id} completion:`, error);
      throw error;
    }
  }

  // Delete a todo
  async deleteTodo(id: number): Promise<void> {
    try {
      await apiClient.deleteTodo(id);
    } catch (error) {
      console.error(`Error deleting todo ${id}:`, error);
      throw error;
    }
  }
}

// Create singleton instance
const todoService = new TodoService();

export default todoService;
