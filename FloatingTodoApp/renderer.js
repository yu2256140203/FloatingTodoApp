const { ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

// 应用状态
let todos = [];
let currentFilter = 'all';
let currentAudio = null;
let reminderIntervals = [];

// DOM元素
const todoInput = document.getElementById('todoInput');
const reminderTime = document.getElementById('reminderTime');
const musicPath = document.getElementById('musicPath');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const filterBtns = document.querySelectorAll('.filter-btn');
const minimizeBtn = document.getElementById('minimizeBtn');
const closeBtn = document.getElementById('closeBtn');
const playBtn = document.getElementById('playBtn');
const pauseBtn = document.getElementById('pauseBtn');
const stopBtn = document.getElementById('stopBtn');
const currentTrack = document.getElementById('currentTrack');

// 初始化
function init() {
  loadTodos();
  renderTodos();
  setupEventListeners();
  startReminderCheck();
}

// 加载待办事项
function loadTodos() {
  try {
    const dataPath = path.join(__dirname, 'todos.json');
    if (fs.existsSync(dataPath)) {
      const data = fs.readFileSync(dataPath, 'utf8');
      todos = JSON.parse(data);
    }
  } catch (error) {
    console.error('加载待办事项失败:', error);
    todos = [];
  }
}

// 保存待办事项
function saveTodos() {
  try {
    const dataPath = path.join(__dirname, 'todos.json');
    fs.writeFileSync(dataPath, JSON.stringify(todos, null, 2), 'utf8');
  } catch (error) {
    console.error('保存待办事项失败:', error);
  }
}

// 生成唯一ID
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// 添加待办事项
function addTodo() {
  const text = todoInput.value.trim();
  if (!text) return;

  const todo = {
    id: generateId(),
    text: text,
    completed: false,
    reminder: reminderTime.value || null,
    musicPath: musicPath.value || null,
    createdAt: new Date().toISOString()
  };

  todos.push(todo);
  saveTodos();
  renderTodos();

  // 清空输入
  todoInput.value = '';
  reminderTime.value = '';
  musicPath.value = '';

  // 设置提醒
  if (todo.reminder) {
    setReminder(todo);
  }
}

// 删除待办事项
function deleteTodo(id) {
  todos = todos.filter(todo => todo.id !== id);
  saveTodos();
  renderTodos();
}

// 切换完成状态
function toggleTodo(id) {
  const todo = todos.find(todo => todo.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    saveTodos();
    renderTodos();
  }
}

// 渲染待办列表
function renderTodos() {
  const filteredTodos = todos.filter(todo => {
    if (currentFilter === 'active') return !todo.completed;
    if (currentFilter === 'completed') return todo.completed;
    return true;
  });

  todoList.innerHTML = filteredTodos.map(todo => `
    <div class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
      <div class="todo-main">
        <div class="todo-checkbox ${todo.completed ? 'checked' : ''}" onclick="toggleTodo('${todo.id}')"></div>
        <span class="todo-text">${escapeHtml(todo.text)}</span>
        <div class="todo-actions">
          ${todo.musicPath ? `<button class="btn-icon" onclick="playMusic('${escapeHtml(todo.musicPath)}')" title="播放音乐">🎵</button>` : ''}
          <button class="btn-icon" onclick="deleteTodo('${todo.id}')" title="删除">🗑️</button>
        </div>
      </div>
      ${todo.reminder ? `
        <div class="todo-info">
          <span>提醒: ${formatDateTime(todo.reminder)}</span>
        </div>
      ` : ''}
    </div>
  `).join('');
}

// HTML转义
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// 格式化日期时间
function formatDateTime(dateTimeStr) {
  const date = new Date(dateTimeStr);
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// 设置提醒
function setReminder(todo) {
  if (!todo.reminder) return;

  const reminderDate = new Date(todo.reminder);
  const now = new Date();
  const delay = reminderDate.getTime() - now.getTime();

  if (delay > 0) {
    setTimeout(() => {
      if (!todo.completed) {
        // 发送通知
        ipcRenderer.send('show-notification', {
          title: 'ToDo 提醒',
          body: todo.text
        });

        // 如果有音乐，播放音乐
        if (todo.musicPath) {
          playMusic(todo.musicPath);
        }
      }
    }, delay);
  }
}

// 启动提醒检查
function startReminderCheck() {
  // 每分钟检查一次
  setInterval(() => {
    const now = new Date();
    todos.forEach(todo => {
      if (todo.reminder && !todo.completed) {
        const reminderDate = new Date(todo.reminder);
        const diff = reminderDate.getTime() - now.getTime();

        // 如果提醒时间已到（在1分钟内）
        if (diff >= 0 && diff < 60000) {
          ipcRenderer.send('show-notification', {
            title: 'ToDo 提醒',
            body: todo.text
          });

          if (todo.musicPath) {
            playMusic(todo.musicPath);
          }
        }
      }
    });
  }, 60000);
}

// 播放音乐
function playMusic(filePath) {
  try {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio = null;
    }

    if (!fs.existsSync(filePath)) {
      console.error('音乐文件不存在:', filePath);
      return;
    }

    currentAudio = new Audio(filePath);
    currentAudio.play();
    currentTrack.textContent = path.basename(filePath);
  } catch (error) {
    console.error('播放音乐失败:', error);
  }
}

// 暂停音乐
function pauseMusic() {
  if (currentAudio) {
    currentAudio.pause();
  }
}

// 停止音乐
function stopMusic() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
    currentTrack.textContent = '未播放';
  }
}

// 设置事件监听器
function setupEventListeners() {
  // 添加按钮
  addBtn.addEventListener('click', addTodo);

  // 回车添加
  todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
  });

  // 筛选按钮
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter;
      renderTodos();
    });
  });

  // 窗口控制
  minimizeBtn.addEventListener('click', () => {
    ipcRenderer.send('window-minimize');
  });

  closeBtn.addEventListener('click', () => {
    ipcRenderer.send('window-close');
  });

  // 音乐控制
  playBtn.addEventListener('click', () => {
    if (currentAudio) {
      currentAudio.play();
    }
  });

  pauseBtn.addEventListener('click', pauseMusic);
  stopBtn.addEventListener('click', stopMusic);

  // 窗口拖动
  const header = document.getElementById('header');
  let isDragging = false;
  let startX, startY;

  header.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.screenX - window.screenX;
    startY = e.screenY - window.screenY;
  });

  document.addEventListener('mousemove', (e) => {
    if (isDragging) {
      const x = e.screenX - startX;
      const y = e.screenY - startY;
      ipcRenderer.send('window-drag', { x, y });
    }
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
  });
}

// 初始化应用
init();
