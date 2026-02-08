// API Client Service for Todo Application
class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080';
  }

  // Set JWT token for authentication
  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('jwt_token', token);
    }
  }

  // Get JWT token from storage
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      if (!this.token) {
        this.token = localStorage.getItem('jwt_token');
      }
      return this.token;
    }
    return this.token;
  }

  // Remove JWT token
  removeToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('jwt_token');
    }
  }

  // Prepare headers with JWT token
  getHeaders(includeContentType = true) {
    const headers: Record<string, string> = {};

    if (includeContentType) {
      headers['Content-Type'] = 'application/json';
    }

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Generic request method
  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized
      if (response.status === 401) {
        this.removeToken();
        throw new Error('Unauthorized: Please log in again');
      }

      // Attempt to parse response as JSON
      const contentType = response.headers.get('content-type');
      let data;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // For responses without JSON (like DELETE 204), return empty object
        if (response.status === 204) {
          data = {};
        } else {
          data = await response.text();
        }
      }

      if (!response.ok) {
        // Handle FastAPI validation errors (422)
        if (response.status === 422 && Array.isArray((data as any).detail)) {
          const errors = (data as any).detail.map((err: any) => err.msg).join(', ');
          throw new Error(errors);
        }
        throw new Error((data as any).detail || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Authentication methods
  async register(userData: { email: string; password: string }) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { email: string; password: string }) {
    const response = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.access_token) {
      this.setToken(response.access_token);
    }

    return response;
  }

  async logout() {
    this.removeToken();
  }

  // Todo methods
  async getTodos() {
    return this.request('/api/todos/');
  }

  async createTodo(todoData: { title: string; description?: string; completed?: boolean }) {
    return this.request('/api/todos/', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  }

  async getTodoById(id: number) {
    return this.request(`/api/todos/${id}`);
  }

  async updateTodo(id: number, todoData: { title?: string; description?: string; completed?: boolean }) {
    return this.request(`/api/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  }

  async toggleTodoComplete(id: number, completed: boolean) {
    return this.request(`/api/todos/${id}/complete?completed=${completed}`, {
      method: 'PATCH',
    });
  }

  async deleteTodo(id: number) {
    return this.request(`/api/todos/${id}`, {
      method: 'DELETE',
    });
  }
}

// Create singleton instance
const apiClient = new ApiClient();

export default apiClient;
