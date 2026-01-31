# 🚀 Полный мануал по JavaScript Frameworks: От основ до продвинутых практик

## 📋 Содержание

1. [Введение в JavaScript Frameworks](#введение-в-javascript-frameworks)
2. [React.js](#reactjs)
3. [Vue.js](#vuejs)
4. [Angular](#angular)
5. [Svelte](#svelte)
6. [Next.js](#nextjs)
7. [Nuxt.js](#nuxtjs)
8. [Express.js](#expressjs)
9. [Node.js Frameworks](#nodejs-frameworks)
10. [State Management](#state-management)
11. [Routing](#routing)
12. [Testing](#testing)
13. [Performance Optimization](#performance-optimization)
14. [Deployment](#deployment)
15. [Best Practices](#best-practices)

## Введение в JavaScript Frameworks

**JavaScript Frameworks** — это готовые решения, которые предоставляют структуру и инструменты для разработки веб-приложений. Они помогают организовать код, ускоряют разработку и обеспечивают лучшую поддержку проектов.

### Почему использовать фреймворки?

✅ **Преимущества:**
- **Структура и организация кода**
- **Повторное использование компонентов**
- **Быстрая разработка**
- **Сообщество и экосистема**
- **Решения для типичных задач**
- **Производительность из коробки**

❌ **Когда фреймворки могут быть избыточными:**
- Очень простые landing pages
- Статические сайты
- Микросервисы без UI
- Когда нужен полный контроль над каждым аспектом

### Популярные категории фреймворков:

#### Frontend Frameworks:
- **React** — библиотека от Facebook
- **Vue** — прогрессивный фреймворк
- **Angular** — полноценный фреймворк от Google
- **Svelte** — компилятор нового поколения

#### Fullstack Frameworks:
- **Next.js** — React фреймворк
- **Nuxt.js** — Vue фреймворк
- **SvelteKit** — Svelte фреймворк

#### Backend Frameworks:
- **Express.js** — минималистичный Node.js фреймворк
- **Fastify** — высокопроизводительный фреймворк
- **Koa** — современная замена Express
- **NestJS** — enterprise-grade фреймворк

## React.js

### Основы React:

```jsx
// Основной компонент
import React, { useState, useEffect } from 'react';

function App() {
  const [count, setCount] = useState(0);
  const [data, setData] = useState([]);

  // Эффект при монтировании
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('/api/data');
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <h1>React Counter: {count}</h1>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
      
      <div>
        <h2>Data List:</h2>
        <ul>
          {data.map(item => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
```

### Хуки React:

```jsx
import React, { useState, useEffect, useContext, useReducer, useCallback, useMemo } from 'react';

// Custom Hook
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.log(error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.log(error);
    }
  };

  return [storedValue, setValue];
}

// Context
const ThemeContext = React.createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Использование
function ThemedComponent() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  
  return (
    <div className={`theme-${theme}`}>
      <p>Current theme: {theme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}
```

### Компоненты высшего порядка (HOC):

```jsx
// HOC для добавления логирования
function withLogging(WrappedComponent) {
  return function EnhancedComponent(props) {
    useEffect(() => {
      console.log(`Component ${WrappedComponent.name} mounted`);
      return () => {
        console.log(`Component ${WrappedComponent.name} unmounted`);
      };
    }, []);

    return <WrappedComponent {...props} />;
  };
}

// HOC для авторизации
function withAuth(WrappedComponent) {
  return function AuthComponent(props) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      checkAuth();
    }, []);

    const checkAuth = async () => {
      try {
        const response = await fetch('/api/auth/check');
        const data = await response.json();
        setIsAuthenticated(data.authenticated);
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    if (loading) {
      return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
      return <div>Please log in to view this content</div>;
    }

    return <WrappedComponent {...props} />;
  };
}

// Использование HOC
const ProtectedDashboard = withAuth(Dashboard);
const LoggedUserProfile = withLogging(UserProfile);
```

## Vue.js

### Основы Vue 3:

```vue
<template>
  <div class="app">
    <h1>{{ title }}</h1>
    <Counter :initial-value="0" @increment="handleIncrement" />
    <TodoList />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Counter from './components/Counter.vue';
import TodoList from './components/TodoList.vue';

// Реактивные данные
const title = ref('Vue 3 Application');
const count = ref(0);

// Вычисляемые свойства
const doubledCount = computed(() => count.value * 2);

// Методы
const handleIncrement = (value) => {
  count.value += value;
};

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted');
});
</script>

<style scoped>
.app {
  padding: 20px;
  font-family: Arial, sans-serif;
}
</style>
```

### Composition API:

```vue
<!-- UserProfile.vue -->
<template>
  <div class="user-profile">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <h2>{{ user.name }}</h2>
      <p>Email: {{ user.email }}</p>
      <p>Posts: {{ posts.length }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Реактивное состояние
const user = ref(null);
const posts = ref([]);
const loading = ref(false);
const error = ref(null);

// Методы
const fetchUser = async (userId) => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`/api/users/${userId}`);
    user.value = await response.json();
  } catch (err) {
    error.value = 'Failed to fetch user';
  } finally {
    loading.value = false;
  }
};

const fetchUserPosts = async (userId) => {
  try {
    const response = await fetch(`/api/users/${userId}/posts`);
    posts.value = await response.json();
  } catch (err) {
    console.error('Failed to fetch posts:', err);
  }
};

// Lifecycle
onMounted(async () => {
  const userId = 1; // или из props/route
  await fetchUser(userId);
  await fetchUserPosts(userId);
});
</script>
```

### Vuex Store:

```javascript
// store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null,
    isAuthenticated: false,
    cart: [],
    products: []
  },
  
  mutations: {
    SET_USER(state, user) {
      state.user = user;
      state.isAuthenticated = !!user;
    },
    
    ADD_TO_CART(state, product) {
      const existing = state.cart.find(item => item.id === product.id);
      if (existing) {
        existing.quantity++;
      } else {
        state.cart.push({ ...product, quantity: 1 });
      }
    },
    
    REMOVE_FROM_CART(state, productId) {
      state.cart = state.cart.filter(item => item.id !== productId);
    },
    
    CLEAR_CART(state) {
      state.cart = [];
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        });
        
        const user = await response.json();
        commit('SET_USER', user);
        return user;
      } catch (error) {
        throw new Error('Login failed');
      }
    },
    
    async logout({ commit }) {
      await fetch('/api/logout');
      commit('SET_USER', null);
    },
    
    async fetchProducts({ commit }) {
      const response = await fetch('/api/products');
      const products = await response.json();
      commit('SET_PRODUCTS', products);
    }
  },
  
  getters: {
    cartTotal: (state) => {
      return state.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
    
    cartItemCount: (state) => {
      return state.cart.reduce((count, item) => count + item.quantity, 0);
    },
    
    isAuthenticated: (state) => state.isAuthenticated
  }
});
```

## Angular

### Основы Angular:

```typescript
// app.component.ts
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Angular App';
  items: any[] = [];
  newItem = '';
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.loadItems();
  }
  
  loadItems() {
    this.http.get<any[]>('/api/items')
      .subscribe(
        data => this.items = data,
        error => console.error('Error loading items:', error)
      );
  }
  
  addItem() {
    if (this.newItem.trim()) {
      this.http.post('/api/items', { name: this.newItem })
        .subscribe(
          () => {
            this.loadItems();
            this.newItem = '';
          },
          error => console.error('Error adding item:', error)
        );
    }
  }
  
  deleteItem(id: number) {
    this.http.delete(`/api/items/${id}`)
      .subscribe(
        () => this.loadItems(),
        error => console.error('Error deleting item:', error)
      );
  }
}
```

```html
<!-- app.component.html -->
<div class="container">
  <h1>{{ title }}</h1>
  
  <form (ngSubmit)="addItem()">
    <input [(ngModel)]="newItem" name="newItem" placeholder="Add new item">
    <button type="submit">Add</button>
  </form>
  
  <ul>
    <li *ngFor="let item of items">
      {{ item.name }}
      <button (click)="deleteItem(item.id)">Delete</button>
    </li>
  </ul>
</div>
```

### Services:

```typescript
// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface User {
  id: number;
  name: string;
  email: string;
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = '/api';
  private usersSubject = new BehaviorSubject<User[]>([]);
  public users$ = this.usersSubject.asObservable();
  
  constructor(private http: HttpClient) {}
  
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users`)
      .pipe(
        tap(users => this.usersSubject.next(users))
      );
  }
  
  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/${id}`);
  }
  
  createUser(user: Partial<User>): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/users`, user)
      .pipe(
        tap(newUser => {
          const currentUsers = this.usersSubject.value;
          this.usersSubject.next([...currentUsers, newUser]);
        })
      );
  }
  
  updateUser(id: number, user: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/${id}`, user)
      .pipe(
        tap(updatedUser => {
          const currentUsers = this.usersSubject.value;
          const index = currentUsers.findIndex(u => u.id === id);
          if (index !== -1) {
            currentUsers[index] = updatedUser;
            this.usersSubject.next([...currentUsers]);
          }
        })
      );
  }
  
  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/users/${id}`)
      .pipe(
        tap(() => {
          const currentUsers = this.usersSubject.value;
          this.usersSubject.next(currentUsers.filter(u => u.id !== id));
        })
      );
  }
}
```

### Guards:

```typescript
// auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    if (this.authService.isAuthenticated()) {
      return true;
    }
    
    // Перенаправление на страницу логина
    this.router.navigate(['/login'], {
      queryParams: { returnUrl: state.url }
    });
    return false;
  }
}

// role.guard.ts
@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  canActivate(
    route: ActivatedRouteSnapshot
  ): boolean {
    const requiredRoles = route.data['roles'] as Array<string>;
    const userRole = this.authService.getUserRole();
    
    if (requiredRoles && requiredRoles.includes(userRole)) {
      return true;
    }
    
    this.router.navigate(['/unauthorized']);
    return false;
  }
}
```

## Svelte

### Основы Svelte:

```svelte
<!-- Counter.svelte -->
<script>
  import { onMount, onDestroy } from 'svelte';
  
  let count = 0;
  let doubled;
  
  // Реактивные выражения
  $: doubled = count * 2;
  $: console.log(`Count is now ${count}`);
  
  // Функции
  function increment() {
    count += 1;
  }
  
  function decrement() {
    count -= 1;
  }
  
  // Lifecycle
  onMount(() => {
    console.log('Component mounted');
    return () => {
      console.log('Component destroyed');
    };
  });
</script>

<div class="counter">
  <h2>Count: {count}</h2>
  <p>Doubled: {doubled}</p>
  
  <button on:click={increment}>+</button>
  <button on:click={decrement}>-</button>
</div>

<style>
  .counter {
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    margin: 0 5px;
    padding: 8px 16px;
    font-size: 16px;
  }
</style>
```

### Stores:

```javascript
// stores/userStore.js
import { writable, derived, readable } from 'svelte/store';

// Writable store
export const user = writable(null);

// Derived store
export const isLoggedIn = derived(user, $user => !!$user);

// Readable store (например, для времени)
export const time = readable(new Date(), function start(set) {
  const timer = setInterval(() => {
    set(new Date());
  }, 1000);
  
  return function stop() {
    clearInterval(timer);
  };
});

// Custom store с методами
function createCount() {
  const { subscribe, set, update } = writable(0);
  
  return {
    subscribe,
    increment: () => update(n => n + 1),
    decrement: () => update(n => n - 1),
    reset: () => set(0)
  };
}

export const count = createCount();

// Async store
export const todos = writable([]);

export async function fetchTodos() {
  const response = await fetch('/api/todos');
  const data = await response.json();
  todos.set(data);
}

export async function addTodo(text) {
  const response = await fetch('/api/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  
  const newTodo = await response.json();
  todos.update(items => [...items, newTodo]);
}
```

### Использование stores:

```svelte
<!-- TodoApp.svelte -->
<script>
  import { todos, fetchTodos, addTodo } from './stores/todoStore.js';
  import { isLoggedIn } from './stores/userStore.js';
  
  let newTodo = '';
  
  // Автоматически подписываемся на изменения
  $: todoList = $todos;
  $: userLoggedIn = $isLoggedIn;
  
  onMount(async () => {
    await fetchTodos();
  });
  
  async function handleSubmit() {
    if (newTodo.trim()) {
      await addTodo(newTodo);
      newTodo = '';
    }
  }
</script>

{#if userLoggedIn}
  <div>
    <h1>Todo List</h1>
    
    <form on:submit|preventDefault={handleSubmit}>
      <input bind:value={newTodo} placeholder="Add new todo">
      <button type="submit">Add</button>
    </form>
    
    <ul>
      {#each todoList as todo (todo.id)}
        <li class:completed={todo.completed}>
          {todo.text}
          <button on:click={() => removeTodo(todo.id)}>Delete</button>
        </li>
      {/each}
    </ul>
  </div>
{:else}
  <p>Please log in to view todos</p>
{/if}
```

## Next.js

### Основы Next.js:

```javascript
// pages/index.js
import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';

export default function Home() {
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    fetchPosts();
  }, []);
  
  const fetchPosts = async () => {
    const res = await fetch('/api/posts');
    const data = await res.json();
    setPosts(data);
  };
  
  return (
    <div className="container">
      <Head>
        <title>My Blog</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main>
        <h1 className="title">Welcome to My Blog!</h1>
        
        <div className="grid">
          {posts.map(post => (
            <Link key={post.id} href={`/posts/${post.slug}`}>
              <a className="card">
                <h3>{post.title}</h3>
                <p>{post.excerpt}</p>
              </a>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
```

### API Routes:

```javascript
// pages/api/posts.js
export default function handler(req, res) {
  const posts = [
    {
      id: 1,
      slug: 'first-post',
      title: 'First Post',
      excerpt: 'This is my first post'
    },
    {
      id: 2,
      slug: 'second-post',
      title: 'Second Post',
      excerpt: 'This is my second post'
    }
  ];
  
  if (req.method === 'GET') {
    res.status(200).json(posts);
  } else if (req.method === 'POST') {
    const { title, content } = req.body;
    const newPost = {
      id: posts.length + 1,
      slug: title.toLowerCase().replace(/\s+/g, '-'),
      title,
      content
    };
    posts.push(newPost);
    res.status(201).json(newPost);
  } else {
    res.setHeader('Allow', ['GET', 'POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
```

### getStaticProps и getServerSideProps:

```javascript
// pages/posts/[slug].js
import { useRouter } from 'next/router';

export default function Post({ post }) {
  const router = useRouter();
  
  if (router.isFallback) {
    return <div>Loading...</div>;
  }
  
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// Static Site Generation
export async function getStaticPaths() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  
  const paths = posts.map(post => ({
    params: { slug: post.slug }
  }));
  
  return {
    paths,
    fallback: true // или false для static generation
  };
}

export async function getStaticProps({ params }) {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`);
  const post = await res.json();
  
  return {
    props: { post },
    revalidate: 10 // ISR - обновление каждые 10 секунд
  };
}

// Server-side Rendering (альтернатива)
export async function getServerSideProps({ params }) {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`);
  const post = await res.json();
  
  return {
    props: { post }
  };
}
```

## Nuxt.js

### Основы Nuxt 3:

```vue
<!-- pages/index.vue -->
<template>
  <div>
    <h1>Welcome to Nuxt 3</h1>
    <Counter />
    <ProductList />
  </div>
</template>

<script setup>
// SEO meta tags
useHead({
  title: 'My Nuxt App',
  meta: [
    { name: 'description', content: 'My amazing Nuxt application' }
  ]
});
</script>
```

### Composables:

```javascript
// composables/useApi.js
export const useApi = () => {
  const apiBase = 'https://api.example.com';
  
  const get = async (endpoint) => {
    const response = await $fetch(`${apiBase}${endpoint}`);
    return response;
  };
  
  const post = async (endpoint, data) => {
    const response = await $fetch(`${apiBase}${endpoint}`, {
      method: 'POST',
      body: data
    });
    return response;
  };
  
  return { get, post };
};

// composables/useAuth.js
export const useAuth = () => {
  const user = useState('user', () => null);
  const { get, post } = useApi();
  
  const login = async (credentials) => {
    try {
      const userData = await post('/auth/login', credentials);
      user.value = userData;
      return userData;
    } catch (error) {
      throw new Error('Login failed');
    }
  };
  
  const logout = async () => {
    await post('/auth/logout');
    user.value = null;
  };
  
  const isAuthenticated = computed(() => !!user.value);
  
  return { user, login, logout, isAuthenticated };
};
```

### Server Routes:

```javascript
// server/api/users.get.js
export default defineEventHandler(async (event) => {
  const users = [
    { id: 1, name: 'John Doe' },
    { id: 2, name: 'Jane Smith' }
  ];
  
  return users;
});

// server/api/users.post.js
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  
  // Валидация
  if (!body.name) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Name is required'
    });
  }
  
  const newUser = {
    id: Date.now(),
    name: body.name
  };
  
  // Сохранение в базу данных
  // await db.users.create(newUser);
  
  return newUser;
});
```

## Express.js

### Основы Express:

```javascript
// app.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet()); // Security headers
app.use(cors());   // Cross-origin requests
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Hello World!' });
});

app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/users', async (req, res) => {
  try {
    const { name, email } = req.body;
    
    // Validation
    if (!name || !email) {
      return res.status(400).json({ error: 'Name and email are required' });
    }
    
    const user = new User({ name, email });
    await user.save();
    
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Middleware:

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.sendStatus(401);
  }
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.sendStatus(403);
    }
    
    req.user = user;
    next();
  });
};

const authorizeRole = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.sendStatus(401);
    }
    
    if (!roles.includes(req.user.role)) {
      return res.sendStatus(403);
    }
    
    next();
  };
};

module.exports = { authenticateToken, authorizeRole };
```

### Database Integration:

```javascript
// models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
  }
}, {
  timestamps: true
});

// Pre-save hook для хеширования пароля
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Метод для проверки пароля
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

## Node.js Frameworks

### Fastify:

```javascript
// server.js
const fastify = require('fastify')({ logger: true });

// Регистрация плагинов
fastify.register(require('@fastify/cors'));
fastify.register(require('@fastify/helmet'));
fastify.register(require('@fastify/rate-limit'));

// Роуты
fastify.get('/', async (request, reply) => {
  return { hello: 'world' };
});

fastify.get('/users', async (request, reply) => {
  const users = await User.find();
  return users;
});

fastify.post('/users', {
  schema: {
    body: {
      type: 'object',
      required: ['name', 'email'],
      properties: {
        name: { type: 'string' },
        email: { type: 'string', format: 'email' }
      }
    }
  }
}, async (request, reply) => {
  const { name, email } = request.body;
  const user = new User({ name, email });
  await user.save();
  return user;
});

// Запуск сервера
const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: '0.0.0.0' });
    fastify.log.info(`server listening on ${fastify.server.address().port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
```

### NestJS:

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersModule } from './users/users.module';
import { AuthModule } from './auth/auth.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'postgres',
      password: 'password',
      database: 'mydb',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: true,
    }),
    UsersModule,
    AuthModule,
  ],
})
export class AppModule {}

// users.controller.ts
import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(+id);
  }
}

// users.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';
import { CreateUserDto } from './dto/create-user.dto';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }

  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  findOne(id: number): Promise<User> {
    return this.usersRepository.findOneBy({ id });
  }
}
```

## State Management

### Redux Toolkit (React):

```javascript
// store/store.js
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import userReducer from '../features/user/userSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
});

// features/counter/counterSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  value: 0,
};

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;

// features/user/userSlice.js
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const fetchUserById = createAsyncThunk(
  'users/fetchByIdStatus',
  async (userId, thunkAPI) => {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: { entities: [], loading: 'idle' },
  reducers: {
    // стандартные редьюсеры
  },
  extraReducers: (builder) => {
    builder.addCase(fetchUserById.pending, (state, action) => {
      state.loading = 'pending';
    });
    builder.addCase(fetchUserById.fulfilled, (state, action) => {
      state.entities.push(action.payload);
      state.loading = 'idle';
    });
  },
});

export default userSlice.reducer;
```

### Pinia (Vue):

```javascript
// stores/counter.js
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Eduardo'
  }),
  
  getters: {
    doubleCount: (state) => state.count * 2,
    doubleCountPlusOne(): number {
      return this.doubleCount + 1
    }
  },
  
  actions: {
    reset() {
      this.count = 0
    },
    randomizeCounter() {
      this.count = Math.round(100 * Math.random())
    }
  }
});

// stores/user.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    userData: null,
    isAuthenticated: false
  }),
  
  actions: {
    async login(credentials) {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        });
        
        const data = await response.json();
        this.userData = data.user;
        this.isAuthenticated = true;
        
        return data;
      } catch (error) {
        throw new Error('Login failed');
      }
    },
    
    logout() {
      this.userData = null;
      this.isAuthenticated = false;
    }
  }
});
```

## Routing

### React Router:

```jsx
// App.js
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="app">
        <nav>
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/dashboard">Dashboard</Link>
        </nav>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route 
            path="/dashboard" 
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } 
          />
          <Route path="/users/:id" element={<UserProfile />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
}

// UserProfile.jsx
import { useParams, useSearchParams } from 'react-router-dom';

function UserProfile() {
  const { id } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  
  const tab = searchParams.get('tab') || 'profile';
  
  return (
    <div>
      <h1>User Profile: {id}</h1>
      <div>
        <button 
          onClick={() => setSearchParams({ tab: 'profile' })}
          className={tab === 'profile' ? 'active' : ''}
        >
          Profile
        </button>
        <button 
          onClick={() => setSearchParams({ tab: 'settings' })}
          className={tab === 'settings' ? 'active' : ''}
        >
          Settings
        </button>
      </div>
    </div>
  );
}
```

### Vue Router:

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users/:id',
    name: 'UserProfile',
    component: () => import('@/views/UserProfile.vue'),
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' });
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'Dashboard' });
  } else {
    next();
  }
});

export default router;
```

## Testing

### Jest + React Testing Library:

```javascript
// __tests__/Counter.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from '../components/Counter';

describe('Counter', () => {
  test('renders counter with initial value 0', () => {
    render(<Counter />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  test('increments count when button is clicked', () => {
    render(<Counter />);
    const button = screen.getByText('Increment');
    
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
    
    fireEvent.click(button);
    expect(screen.getByText('Count: 2')).toBeInTheDocument();
  });

  test('decrements count when decrement button is clicked', () => {
    render(<Counter />);
    const incrementButton = screen.getByText('Increment');
    const decrementButton = screen.getByText('Decrement');
    
    // First increment
    fireEvent.click(incrementButton);
    
    // Then decrement
    fireEvent.click(decrementButton);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
});

// __tests__/api.test.js
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { getUsers } from '../api/users';

const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json([
      { id: 1, name: 'John Doe' },
      { id: 2, name: 'Jane Smith' }
    ]));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API functions', () => {
  test('fetches users successfully', async () => {
    const users = await getUsers();
    expect(users).toHaveLength(2);
    expect(users[0]).toEqual({ id: 1, name: 'John Doe' });
  });
});
```

### Vitest + Vue Test Utils:

```javascript
// __tests__/Counter.spec.js
import { mount } from '@vue/test-utils';
import Counter from '../src/components/Counter.vue';

describe('Counter', () => {
  test('renders counter with initial value 0', () => {
    const wrapper = mount(Counter);
    expect(wrapper.text()).toContain('Count: 0');
  });

  test('increments count when button is clicked', async () => {
    const wrapper = mount(Counter);
    const button = wrapper.find('button');
    
    await button.trigger('click');
    expect(wrapper.text()).toContain('Count: 1');
    
    await button.trigger('click');
    expect(wrapper.text()).toContain('Count: 2');
  });
});

// __tests__/api.spec.js
import { vi, beforeEach, afterEach } from 'vitest';
import { fetchUsers } from '../src/api/users';

global.fetch = vi.fn();

describe('API functions', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('fetches users successfully', async () => {
    const mockUsers = [
      { id: 1, name: 'John Doe' },
      { id: 2, name: 'Jane Smith' }
    ];

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockUsers)
    });

    const users = await fetchUsers();
    expect(users).toEqual(mockUsers);
    expect(fetch).toHaveBeenCalledWith('/api/users');
  });
});
```

## Performance Optimization

### Lazy Loading:

```javascript
// React lazy loading
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}

// Route-based code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));

<Route 
  path="/dashboard" 
  element={
    <Suspense fallback={<LoadingSpinner />}>
      <Dashboard />
    </Suspense>
  } 
/>
```

### Memoization:

```javascript
// React memoization
import { useMemo, useCallback } from 'react';

function ExpensiveComponent({ items, searchTerm }) {
  // Мемоизируем отфильтрованные данные
  const filteredItems = useMemo(() => {
    return items.filter(item => 
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [items, searchTerm]);

  // Мемоизируем callback
  const handleItemClick = useCallback((itemId) => {
    console.log('Clicked item:', itemId);
  }, []);

  return (
    <div>
      {filteredItems.map(item => (
        <Item 
          key={item.id} 
          item={item} 
          onClick={handleItemClick}
        />
      ))}
    </div>
  );
}

// Vue memoization
import { computed, memo } from 'vue';

export default {
  setup(props) {
    // Computed свойства автоматически мемоизированы
    const expensiveCalculation = computed(() => {
      return props.items.filter(item => 
        item.name.toLowerCase().includes(props.searchTerm.toLowerCase())
      );
    });

    return {
      expensiveCalculation
    };
  }
};
```

## Deployment

### Docker для React/Vue приложений:

```dockerfile
# Dockerfile
FROM node:16-alpine as build

WORKDIR /app

# Копируем package файлы
COPY package*.json ./
RUN npm ci --only=production

# Копируем исходный код
COPY . .

# Сборка приложения
RUN npm run build

# Production stage
FROM nginx:alpine

# Копируем собранное приложение
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем nginx конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    types_hash_max_size 2048;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend:3000/;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
```

### CI/CD Pipeline:

```yaml
# .github/workflows/deploy.yml
name: Deploy Application

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '16'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Build application
      run: npm run build
    
    - name: Deploy to production
      run: |
        # Your deployment script here
        # Example for Firebase:
        # firebase deploy --token $FIREBASE_TOKEN
```

## Best Practices

### 1. Component Structure:

```jsx
// Good component structure
function UserProfile({ userId }) {
  // 1. State declarations
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // 2. Refs
  const profileRef = useRef(null);
  
  // 3. Effects
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);
  
  // 4. Callbacks and handlers
  const handleSave = useCallback(async (userData) => {
    try {
      await updateUser(userData);
      setUser(prev => ({ ...prev, ...userData }));
    } catch (err) {
      setError(err.message);
    }
  }, []);
  
  // 5. Derived state
  const displayName = useMemo(() => {
    return user?.firstName && user?.lastName 
      ? `${user.firstName} ${user.lastName}`
      : user?.username || 'Unknown User';
  }, [user]);
  
  // 6. Render
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <div ref={profileRef}>
      <h1>{displayName}</h1>
      {/* Rest of component */}
    </div>
  );
}
```

### 2. Error Boundaries:

```jsx
// ErrorBoundary.jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error reporting service
    // logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
          </details>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary>
      <MyComponentThatMightThrow />
    </ErrorBoundary>
  );
}
```

### 3. Performance Monitoring:

```javascript
// performance-monitoring.js
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
  }
  
  measureRender(componentName) {
    const start = performance.now();
    
    return () => {
      const end = performance.now();
      const duration = end - start;
      
      this.metrics[componentName] = this.metrics[componentName] || [];
      this.metrics[componentName].push(duration);
      
      // Report slow renders (>16ms)
      if (duration > 16) {
        console.warn(`${componentName} took ${duration.toFixed(2)}ms to render`);
      }
    };
  }
  
  getAverageTime(componentName) {
    const times = this.metrics[componentName] || [];
    if (times.length === 0) return 0;
    
    return times.reduce((sum, time) => sum + time, 0) / times.length;
  }
  
  report() {
    Object.keys(this.metrics).forEach(component => {
      const avgTime = this.getAverageTime(component);
      console.log(`${component}: ${avgTime.toFixed(2)}ms average`);
    });
  }
}

// Usage in components
const perfMonitor = new PerformanceMonitor();

function ExpensiveComponent() {
  const measure = perfMonitor.measureRender('ExpensiveComponent');
  
  // Component logic here
  
  useEffect(() => {
    measure(); // Record render time
  });
  
  return <div>Expensive Component</div>;
}

// Report metrics periodically
setInterval(() => {
  perfMonitor.report();
}, 30000);
```

> Этот мануал охватывает основные аспекты популярных JavaScript фреймворков. Для более глубокого изучения рекомендуется практиковаться на реальных проектах и изучать официальную документацию каждого фреймворка.