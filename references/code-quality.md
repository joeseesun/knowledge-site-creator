# 代码质量标准

> **目标**：生成健壮、可维护、高性能的网站代码

## 一级标准（必须达到）🔴

这些是**必须遵守**的规则，不遵守会导致 bug 或安全问题。

### 1. 错误处理

#### ❌ 错误示例
```javascript
// 没有错误处理，localStorage 可能返回 null
const progress = JSON.parse(localStorage.getItem('progress'));
progress.masteredRoots.forEach(...); // 💥 崩溃
```

#### ✅ 正确示例
```javascript
function getProgress() {
  try {
    const data = localStorage.getItem('progress');
    if (!data) {
      return getDefaultProgress();
    }
    const parsed = JSON.parse(data);
    // 验证数据结构
    if (!parsed.masteredRoots || !Array.isArray(parsed.masteredRoots)) {
      return getDefaultProgress();
    }
    return parsed;
  } catch (error) {
    console.error('Failed to load progress:', error);
    return getDefaultProgress();
  }
}

function getDefaultProgress() {
  return {
    masteredRoots: [],
    currentRootIndex: 0,
    lastStudyDate: null
  };
}
```

**规则**：
- LocalStorage 读取必须有 try-catch
- JSON.parse 必须有错误处理
- 必须提供默认值 fallback

---

### 2. XSS 防护

#### ❌ 危险示例
```javascript
// 直接插入用户数据，有 XSS 风险
container.innerHTML = `
  <div class="root-name">${root.root}</div>
  <div class="root-meaning">${root.meaning}</div>
`;
// 如果 root.root = "<script>alert('XSS')</script>"，脚本会被执行！
```

#### ✅ 安全示例（方案1：textContent）
```javascript
// 使用 textContent（推荐）
function createRootCard(root) {
  const card = document.createElement('div');
  card.className = 'root-card';

  const nameDiv = document.createElement('div');
  nameDiv.className = 'root-name';
  nameDiv.textContent = root.root; // 安全：textContent 会自动转义

  const meaningDiv = document.createElement('div');
  meaningDiv.className = 'root-meaning';
  meaningDiv.textContent = root.meaning;

  card.appendChild(nameDiv);
  card.appendChild(meaningDiv);

  return card;
}
```

#### ✅ 安全示例（方案2：escapeHtml）
```javascript
// 如果必须使用 innerHTML，先转义
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

container.innerHTML = `
  <div class="root-name">${escapeHtml(root.root)}</div>
  <div class="root-meaning">${escapeHtml(root.meaning)}</div>
`;
```

**规则**：
- **优先使用 textContent/createElement**
- 如果必须用 innerHTML，先用 escapeHtml 转义
- 永远不要直接插入未经处理的用户数据

---

### 3. DOM 安全查询

#### ❌ 不安全示例
```javascript
// 没有检查元素是否存在
document.getElementById('rootName').textContent = root.root; // 💥 如果元素不存在会崩溃
```

#### ✅ 安全示例
```javascript
// 方案1：检查元素存在
function updateRootName(text) {
  const element = document.getElementById('rootName');
  if (element) {
    element.textContent = text;
  } else {
    console.warn('Element #rootName not found');
  }
}

// 方案2：使用可选链（Optional Chaining）
document.getElementById('rootName')?.textContent = root.root;
```

**规则**：
- 所有 DOM 操作前检查元素是否存在
- 或使用可选链 `?.` 语法

---

### 4. 边界检查

#### ❌ 重复的边界检查
```javascript
// 每个函数都检查边界
function loadRoot(index) {
  if (index < 0 || index >= WordRoots.length) return;
  // ...
}

function nextRoot() {
  if (currentIndex < WordRoots.length - 1) {
    loadRoot(currentIndex + 1);
  }
}
```

#### ✅ 消除边界检查（Linus 的"好品味"）
```javascript
// 使用环形索引，消除边界情况
function normalizeIndex(index, length) {
  return ((index % length) + length) % length;
}

function loadRoot(index) {
  const safeIndex = normalizeIndex(index, WordRoots.length);
  const root = WordRoots[safeIndex];
  // ... 不再需要边界检查
}

function nextRoot() {
  loadRoot(currentIndex + 1); // 自动循环到开头
}

function prevRoot() {
  loadRoot(currentIndex - 1); // 自动循环到末尾
}
```

**Linus 视角**：
> "消除特殊情况，让代码无条件执行。边界检查是糟糕设计的补丁。"

---

### 5. 避免全局变量污染

#### ❌ 全局变量污染
```javascript
// 污染全局作用域
let currentIndex = 0;
let currentRoot = null;

function loadRoot(index) { ... }
function nextRoot() { ... }
```

#### ✅ 模块化封装
```javascript
// 使用 IIFE 或模块模式
const AppState = (() => {
  let currentIndex = 0;
  let currentRoot = null;

  return {
    getCurrentIndex() { return currentIndex; },
    setCurrentIndex(index) { currentIndex = index; },
    getCurrentRoot() { return currentRoot; },
    setCurrentRoot(root) { currentRoot = root; }
  };
})();

// 或者使用现代 ES6 模块（如果支持）
class AppState {
  #currentIndex = 0;
  #currentRoot = null;

  getCurrentIndex() { return this.#currentIndex; }
  setCurrentIndex(index) { this.#currentIndex = index; }
}
```

**规则**：
- 避免全局变量，使用模块封装
- 或至少使用命名空间（如 `window.APP = {}`）

---

## 二级标准（建议遵守）🟡

这些规则提升代码质量，但不是强制的。

### 6. 性能优化

#### ❌ 重复查询 DOM
```javascript
function updateProgress(index) {
  document.getElementById('progressBar').style.width = '50%';
  document.getElementById('progressBar').setAttribute('aria-valuenow', 50);
  document.getElementById('progressBar').textContent = '50%';
}
```

#### ✅ 缓存 DOM 引用
```javascript
// 初始化时缓存
const DOM = {
  progressBar: document.getElementById('progressBar'),
  rootName: document.getElementById('rootName'),
  // ...
};

function updateProgress(percentage) {
  if (DOM.progressBar) {
    DOM.progressBar.style.width = `${percentage}%`;
    DOM.progressBar.setAttribute('aria-valuenow', percentage);
    DOM.progressBar.textContent = `${percentage}%`;
  }
}
```

#### ✅ 使用事件委托
```javascript
// ❌ 为每个按钮添加监听器
buttons.forEach(btn => {
  btn.addEventListener('click', handleClick);
});

// ✅ 事件委托
document.getElementById('container').addEventListener('click', (e) => {
  if (e.target.classList.contains('quiz-option')) {
    handleClick(e.target);
  }
});
```

---

### 7. 代码可读性

#### ✅ 函数单一职责
```javascript
// ❌ 函数做太多事情
function loadRoot(index) {
  const root = WordRoots[index];
  updateUI(root);
  updateProgress(index);
  saveToLocalStorage(index);
  logAnalytics(index);
}

// ✅ 拆分职责
function loadRoot(index) {
  const root = getRoot(index);
  renderRoot(root);
  updateProgress(index);
}

function renderRoot(root) {
  updateRootUI(root);
  renderExamples(root.examples);
  renderQuiz(root.quiz);
}
```

#### ✅ 语义化命名
```javascript
// ❌ 缩写和不清晰的命名
const idx = 0;
const r = getRt(idx);
const m = r.m;

// ✅ 清晰的命名
const currentIndex = 0;
const root = getRoot(currentIndex);
const meaning = root.meaning;
```

#### ✅ 配置与逻辑分离
```javascript
// ❌ 魔法数字硬编码
setInterval(updateDemo, 4000);
const examples = WordRoots.slice(0, 5);

// ✅ 提取为配置
const CONFIG = {
  ANIMATION_INTERVAL: 4000,
  DEMO_EXAMPLES_COUNT: 5
};

setInterval(updateDemo, CONFIG.ANIMATION_INTERVAL);
const examples = WordRoots.slice(0, CONFIG.DEMO_EXAMPLES_COUNT);
```

---

### 8. 现代化 JavaScript

#### ✅ 使用 const/let 代替 var
```javascript
// ❌ 使用 var（作用域混乱）
var currentIndex = 0;

// ✅ 使用 const/let
let currentIndex = 0;
const maxIndex = WordRoots.length - 1;
```

#### ✅ 使用解构赋值
```javascript
// ❌ 逐个取值
const root = WordRoots[index];
const name = root.root;
const meaning = root.meaning;
const origin = root.origin;

// ✅ 解构赋值
const { root: name, meaning, origin } = WordRoots[index];
```

#### ✅ 使用箭头函数
```javascript
// 简洁的箭头函数
const getMasteredCount = () => {
  const progress = getProgress();
  return progress.masteredRoots.length;
};

// 数组操作更简洁
const masteredRoots = WordRoots.filter(root =>
  progress.masteredRoots.includes(root.id)
);
```

---

## 检查清单 ✅

生成代码后，必须检查：

### 一级标准（强制）
- [ ] 所有 LocalStorage 读取有 try-catch
- [ ] 所有 DOM 操作前检查元素存在
- [ ] 没有直接使用 innerHTML 插入未转义数据
- [ ] 边界情况已消除或有检查
- [ ] 没有全局变量污染

### 二级标准（建议）
- [ ] DOM 引用已缓存
- [ ] 使用事件委托代替多个监听器
- [ ] 函数职责单一（<20行）
- [ ] 变量命名语义化
- [ ] 魔法数字提取为配置
- [ ] 使用现代 JavaScript 语法

---

## 快速参考

| 问题 | 解决方案 |
|------|----------|
| LocalStorage 崩溃 | try-catch + fallback 默认值 |
| XSS 攻击 | 使用 textContent 或 escapeHtml |
| DOM 查询失败 | 检查元素存在 或 `?.` |
| 重复边界检查 | 重新设计数据结构 |
| 全局变量冲突 | 模块封装 或 IIFE |
| 重复 DOM 查询 | 缓存 DOM 引用 |
| 多个事件监听器 | 事件委托 |
| 函数太长 | 拆分职责（单一职责原则）|

---

## Linus 语录

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."
>
> "消除特殊情况，让代码无条件执行。边界检查是糟糕设计的补丁。"
>
> "如果你需要超过3层缩进，你就已经完蛋了，应该修复你的程序。"
