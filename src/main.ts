// 1. Types
type Todo = {
  id: number;
  text: string;
  isCompleted: boolean;
};

type FilterType = 'all' | 'active' | 'completed';

// 2. State Management
let todos: Todo[] = [];
let currentFilter: FilterType = 'all';

// 3. DOM Elements
const inputEl = document.getElementById('todo-input') as HTMLInputElement;
const addButtonEl = document.getElementById('add-button') as HTMLButtonElement;
const listEl = document.getElementById('todo-list') as HTMLUListElement;
const emptyStateEl = document.getElementById('empty-state') as HTMLDivElement;
const filterButtons = document.querySelectorAll('.filter-btn');

// 4. Persistence
const STORAGE_KEY = 'ts-todo-app-v1';

const saveTodos = () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
};

const loadTodos = () => {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try {
      todos = JSON.parse(stored);
    } catch (e) {
      console.error('Failed to load todos', e);
      todos = [];
    }
  }
};

// 5. Rendering
const renderTodos = () => {
  // Filter todos
  const filteredTodos = todos.filter((todo) => {
    if (currentFilter === 'active') return !todo.isCompleted;
    if (currentFilter === 'completed') return todo.isCompleted;
    return true;
  });

  // Toggle empty state
  if (filteredTodos.length === 0) {
    emptyStateEl.classList.remove('hidden');
    listEl.innerHTML = '';
    return;
  } else {
    emptyStateEl.classList.add('hidden');
  }

  // Clear list
  listEl.innerHTML = '';

  // Render items
  filteredTodos.forEach((todo) => {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.isCompleted ? 'completed' : ''}`;

    // Checkbox (Visual only, click handled by container or specific area)
    const checkbox = document.createElement('div');
    checkbox.className = 'checkbox';

    // Content Container
    const content = document.createElement('div');
    content.className = 'todo-content';
    content.appendChild(checkbox);

    // Text
    const textSpan = document.createElement('span');
    textSpan.className = 'todo-text';
    textSpan.textContent = todo.text;
    content.appendChild(textSpan);

    // Click to toggle
    content.addEventListener('click', () => toggleTodo(todo.id));

    // Double click to edit
    textSpan.addEventListener('dblclick', (e) => {
      e.stopPropagation(); // Prevent toggle
      enableEditing(todo.id, textSpan);
    });

    // Delete Button
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn';
    deleteBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`;
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteTodo(todo.id);
    });

    li.appendChild(content);
    li.appendChild(deleteBtn);
    listEl.appendChild(li);
  });
};

const updateFilterButtons = () => {
  filterButtons.forEach(btn => {
    const filter = btn.getAttribute('data-filter') as FilterType;
    if (filter === currentFilter) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
};

// 6. Logic
const addTodo = () => {
  const text = inputEl.value.trim();
  if (text === '') return;

  const newTodo: Todo = {
    id: Date.now(),
    text: text,
    isCompleted: false,
  };

  todos.push(newTodo);
  saveTodos();
  inputEl.value = '';
  renderTodos();
};

const toggleTodo = (id: number) => {
  const todo = todos.find((t) => t.id === id);
  if (todo) {
    todo.isCompleted = !todo.isCompleted;
    saveTodos();
    renderTodos();
  }
};

const deleteTodo = (id: number) => {
  if (confirm('Are you sure you want to delete this task?')) {
    todos = todos.filter((t) => t.id !== id);
    saveTodos();
    renderTodos();
  }
};

const enableEditing = (id: number, spanEl: HTMLElement) => {
  const todo = todos.find((t) => t.id === id);
  if (!todo) return;

  const input = document.createElement('input');
  input.type = 'text';
  input.value = todo.text;
  input.className = 'edit-input'; // We can style this if needed, or rely on default

  // Style inline to match
  input.style.fontSize = '1rem';
  input.style.padding = '4px';
  input.style.border = '1px solid #ccc';
  input.style.borderRadius = '4px';
  input.style.width = '100%';

  const saveEdit = () => {
    const newText = input.value.trim();
    if (newText) {
      todo.text = newText;
      saveTodos();
    }
    renderTodos();
  };

  input.addEventListener('blur', saveEdit);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      saveEdit();
    }
  });

  spanEl.replaceWith(input);
  input.focus();
};

const setFilter = (filter: FilterType) => {
  currentFilter = filter;
  updateFilterButtons();
  renderTodos();
};

// 7. Event Listeners
addButtonEl.addEventListener('click', addTodo);

inputEl.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    addTodo();
  }
});

filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.getAttribute('data-filter') as FilterType;
    setFilter(filter);
  });
});

// Initialization
loadTodos();
renderTodos();
updateFilterButtons();