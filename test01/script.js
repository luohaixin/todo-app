// 任务数组
let todos = [];

// DOM元素
const todoInput = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');
const pendingCount = document.getElementById('pending-count');
const completedCount = document.getElementById('completed-count');
const clearCompletedBtn = document.getElementById('clear-completed');
const clearAllBtn = document.getElementById('clear-all');
const prioritySelect = document.getElementById('priority-select');

// 初始化应用
function init() {
    // 从本地存储加载任务
    loadTodos();
    // 渲染任务列表
    renderTodos();
    // 更新统计
    updateStats();
    // 绑定事件
    addBtn.addEventListener('click', addTodo);
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    });
    clearCompletedBtn.addEventListener('click', clearCompleted);
    clearAllBtn.addEventListener('click', clearAll);
}

// 从本地存储加载任务
function loadTodos() {
    const storedTodos = localStorage.getItem('todos');
    if (storedTodos) {
        todos = JSON.parse(storedTodos);
    }
}

// 保存任务到本地存储
function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

// 添加新任务
function addTodo() {
    const text = todoInput.value.trim();
    if (text) {
        const todo = {
            id: Date.now(),
            text: text,
            completed: false,
            priority: prioritySelect.value
        };
        todos.push(todo);
        saveTodos();
        renderTodos();
        updateStats();
        todoInput.value = '';
        prioritySelect.value = 'medium';
    }
}

// 渲染任务列表
function renderTodos() {
    todoList.innerHTML = '';
    
    if (todos.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = '🎉 太棒了！没有待办任务。\n添加一些任务来开始吧！';
        todoList.appendChild(emptyState);
        return;
    }
    
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''} ${todo.priority}`;
        li.innerHTML = `
            <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} data-id="${todo.id}">
            <span class="todo-text">${todo.text}</span>
            <button class="edit-btn" data-id="${todo.id}">编辑</button>
            <button class="delete-btn" data-id="${todo.id}">删除</button>
        `;
        todoList.appendChild(li);
    });
    
    // 绑定事件
    bindEvents();
}

// 绑定事件
function bindEvents() {
    // 绑定复选框事件
    document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', toggleTodo);
    });
    
    // 绑定删除按钮事件
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', deleteTodo);
    });
    
    // 绑定编辑按钮事件
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', startEdit);
    });
}

// 切换任务完成状态
function toggleTodo(e) {
    const id = parseInt(e.target.dataset.id);
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.completed = !todo.completed;
        saveTodos();
        renderTodos();
        updateStats();
    }
}

// 删除任务
function deleteTodo(e) {
    const id = parseInt(e.target.dataset.id);
    todos = todos.filter(t => t.id !== id);
    saveTodos();
    renderTodos();
    updateStats();
}

// 更新统计
function updateStats() {
    const pending = todos.filter(t => !t.completed).length;
    const completed = todos.filter(t => t.completed).length;
    pendingCount.textContent = pending;
    completedCount.textContent = completed;
}

// 清空已完成任务
function clearCompleted() {
    todos = todos.filter(t => !t.completed);
    saveTodos();
    renderTodos();
    updateStats();
}

// 全部清空
function clearAll() {
    if (confirm('确定要清空所有任务吗？')) {
        todos = [];
        saveTodos();
        renderTodos();
        updateStats();
    }
}

// 开始编辑任务
function startEdit(e) {
    const id = parseInt(e.target.dataset.id);
    const todo = todos.find(t => t.id === id);
    if (todo) {
        const li = e.target.closest('.todo-item');
        li.innerHTML = `
            <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} data-id="${todo.id}">
            <input type="text" class="edit-input" value="${todo.text}" data-id="${todo.id}">
            <button class="save-btn" data-id="${todo.id}">保存</button>
            <button class="cancel-btn" data-id="${todo.id}">取消</button>
        `;
        // 绑定新按钮的事件
        li.querySelector('.save-btn').addEventListener('click', saveEdit);
        li.querySelector('.cancel-btn').addEventListener('click', renderTodos);
        li.querySelector('.edit-input').focus();
    }
}

// 保存编辑后的任务
function saveEdit(e) {
    const id = parseInt(e.target.dataset.id);
    const todo = todos.find(t => t.id === id);
    if (todo) {
        const input = e.target.closest('.todo-item').querySelector('.edit-input');
        const newText = input.value.trim();
        if (newText) {
            todo.text = newText;
            saveTodos();
        }
        renderTodos();
        updateStats();
    }
}

// 初始化应用
init();