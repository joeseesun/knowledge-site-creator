# 核心学习模式 - 功能参考

> 通用的学习功能模式，在所有知识网站中保持一致

## 0. 用户反馈系统原则 ⚠️ 强制规范

**❌ 禁止使用系统对话框**：
- `alert()` - 阻塞式、难看、不可定制
- `confirm()` - 仅在真正需要确认时保留（如重置进度）
- `prompt()` - 从不使用

**✅ 正确的反馈方式**：

1. **成功/错误提示** → 使用 `showFeedback(message, isSuccess)`
   ```javascript
   // ✓ 正确
   showFeedback('✓ 回答正确！', true);
   showFeedback('✗ 操作失败', false);

   // ✗ 错误
   alert('回答正确！');
   ```

2. **错误跳转前的提示** → 使用 `console.warn()` 静默记录
   ```javascript
   // ✓ 正确
   if (!data) {
     console.warn('数据未找到，跳转回首页');
     window.location.href = '/';
     return;
   }

   // ✗ 错误
   if (!data) {
     alert('数据未找到');
     window.location.href = '/';
   }
   ```

3. **确认操作（谨慎使用）** → 仅保留 `confirm()` 用于破坏性操作
   ```javascript
   // ✓ 可接受（破坏性操作）
   if (confirm('确定要删除所有数据吗？此操作无法撤销。')) {
     localStorage.clear();
     showFeedback('✓ 数据已清除', true);
   }
   ```

**`showFeedback()` 函数定义**（每个需要反馈的页面都要包含）：
```javascript
function showFeedback(message, isSuccess) {
  const toast = document.createElement('div');
  toast.className = `feedback-toast ${isSuccess ? 'success' : 'error'}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}
```

---

## 1. 数据结构（通用）

所有知识网站使用相同的数据结构：

```javascript
// js/wordData.js
const WordRoots = [
  {
    id: 1,
    root: "知识点名称",
    origin: "分类/来源",
    meaning: "一句话解释",
    description: "详细说明（200-300字）",
    examples: [
      {
        word: "例子名称",
        meaning: "例子含义",
        breakdown: { root: "知识点名称" },
        explanation: "详细解释"
      }
    ],
    quiz: {
      question: "测试问题？",
      options: ["选项A", "选项B", "选项C", "选项D"],
      correctAnswer: 2  // 正确答案索引（0-3）
    }
  }
];
```

## 2. 网站配置（AI创作）

```javascript
// js/siteConfig.js
const siteConfig = {
  topic: "主题名称",
  siteName: "网站名称",
  itemName: "知识点名称",
  itemCount: 30,

  hero: {
    title: ["第一行", "第二行", "第三行"],
    subtitle: "副标题",
    animation: {
      enabled: true,
      demoCount: 5
    }
  },

  stats: [
    { value: "30", label: "核心概念" },
    { value: "100+", label: "应用场景" },
    { value: "15分钟", label: "每日学习" }
  ],

  footer: {
    tagline: "一句话口号",
    description: "2-3句介绍"
  },

  cta: {
    primary: "开始第一个概念 →",
    secondary: "闪卡复习"
  }
};
```

## 3. 本地存储（进度管理）⚠️ 代码质量标准

**关键原则**：
- ✅ 错误处理：try-catch 包裹所有 LocalStorage 操作
- ✅ 数据验证：检查数据结构完整性
- ✅ 默认值：提供安全的 fallback

```javascript
// js/storage.js
const StorageManager = {
  // 获取默认进度
  _getDefaultProgress() {
    return {
      masteredRoots: [],
      currentRootIndex: 0,
      lastStudyDate: null
    };
  },

  // 验证进度数据结构
  _validateProgress(data) {
    return (
      data &&
      typeof data === 'object' &&
      Array.isArray(data.masteredRoots) &&
      typeof data.currentRootIndex === 'number'
    );
  },

  // 获取进度（带错误处理）
  getProgress() {
    try {
      const data = localStorage.getItem('progress');
      if (!data) {
        return this._getDefaultProgress();
      }

      const parsed = JSON.parse(data);
      if (!this._validateProgress(parsed)) {
        console.warn('Invalid progress data, using default');
        return this._getDefaultProgress();
      }

      return parsed;
    } catch (error) {
      console.error('Failed to load progress:', error);
      return this._getDefaultProgress();
    }
  },

  // 保存进度（带错误处理）
  _saveProgress(progress) {
    try {
      localStorage.setItem('progress', JSON.stringify(progress));
      return true;
    } catch (error) {
      console.error('Failed to save progress:', error);
      return false;
    }
  },

  // 标记为已掌握
  markRootAsMastered(rootId) {
    const progress = this.getProgress();
    if (!progress.masteredRoots.includes(rootId)) {
      progress.masteredRoots.push(rootId);
      progress.lastStudyDate = new Date().toISOString();
      this._saveProgress(progress);
    }
    return progress;
  },

  // 更新学习进度
  updateProgress(rootIndex) {
    const progress = this.getProgress();
    progress.currentRootIndex = rootIndex;
    progress.lastStudyDate = new Date().toISOString();
    this._saveProgress(progress);
    return progress;
  }
};
```

## 4. 闪卡模式（Flashcard）

### 4.1 核心功能

- **卡片翻转**：正面显示知识点名称，背面显示详细信息
- **键盘控制**：←→切换卡片，空格翻转
- **进度显示**：当前进度 + 已掌握数量
- **标记功能**：标记为已掌握

### 4.2 实现模式

```javascript
// 卡片翻转
function flipCard() {
  const card = document.getElementById('flashcard');
  card.classList.toggle('flipped');
}

// 加载卡片
function loadCard(index) {
  const root = WordRoots[index];

  // 正面
  document.getElementById('frontRoot').textContent = root.root;
  document.getElementById('frontMeaning').textContent = root.meaning;
  document.getElementById('frontOrigin').textContent = root.origin;

  // 背面
  document.getElementById('backRoot').textContent = root.root;
  document.getElementById('backDescription').textContent = root.description;

  // 更新进度
  updateProgress(index);
}

// 键盘控制
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft') prevCard();
  if (e.key === 'ArrowRight') nextCard();
  if (e.key === ' ') flipCard();
});
```

### 4.3 HTML结构

```html
<div class="flashcard" id="flashcard" onclick="flipCard()">
  <div class="flashcard-inner">
    <!-- 正面 -->
    <div class="flashcard-front">
      <div class="flashcard-root" id="frontRoot">-</div>
      <div class="flashcard-meaning" id="frontMeaning">-</div>
      <div class="flashcard-origin" id="frontOrigin">-</div>
    </div>

    <!-- 背面 -->
    <div class="flashcard-back">
      <div class="flashcard-root" id="backRoot">-</div>
      <div class="flashcard-description" id="backDescription">-</div>
      <div class="flashcard-examples" id="backExamples">
        <!-- 动态生成 -->
      </div>
    </div>
  </div>
</div>
```

## 5. 渐进学习模式（Learn）

### 5.1 核心功能

- **渐进式展示**：一次一个知识点
- **上一个/下一个**：顺序学习
- **标记已掌握**：学习过程中可标记
- **自动保存进度**：记录当前位置

### 5.2 实现模式

```javascript
// 加载知识点
function loadRoot(index) {
  if (index < 0 || index >= WordRoots.length) return;

  const root = WordRoots[index];
  currentIndex = index;

  // 更新标题
  document.getElementById('rootName').textContent = root.root;
  document.getElementById('rootMeaning').textContent = root.meaning;

  // 更新详细说明
  document.getElementById('description').textContent = root.description;

  // 渲染例子
  renderExamples(root.examples);

  // 渲染测试题
  renderQuiz(root.quiz);

  // 更新进度
  updateProgress(index);
}

// 导航
function nextRoot() {
  if (currentIndex < WordRoots.length - 1) {
    loadRoot(currentIndex + 1);
  }
}

function prevRoot() {
  if (currentIndex > 0) {
    loadRoot(currentIndex - 1);
  }
}
```

## 6. 测试题模式（Quiz）

### 6.1 实现模式

```javascript
// 渲染测试题（安全方法）
function renderQuiz(quiz) {
  const questionElement = document.getElementById('quizQuestion');
  if (questionElement) {
    questionElement.textContent = quiz.question;
  }

  const optionsContainer = document.getElementById('quizOptions');
  if (!optionsContainer) {
    console.warn('Element #quizOptions not found');
    return;
  }

  // 清空容器
  optionsContainer.innerHTML = '';

  // 创建选项按钮（安全方法）
  quiz.options.forEach((option, index) => {
    const button = document.createElement('button');
    button.className = 'quiz-option';
    button.textContent = option; // textContent 安全
    button.onclick = () => checkAnswer(index);
    optionsContainer.appendChild(button);
  });
}

// 显示反馈提示（Toast）⚠️ 不要用 alert！
function showFeedback(message, isSuccess) {
  const toast = document.createElement('div');
  toast.className = `feedback-toast ${isSuccess ? 'success' : 'error'}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// 检查答案
function checkAnswer(selectedIndex) {
  const quiz = currentRoot.quiz;
  const isCorrect = selectedIndex === quiz.correctAnswer;

  // 更新选项样式
  const options = document.querySelectorAll('.quiz-option');
  options.forEach((btn, index) => {
    btn.disabled = true;
    if (index === quiz.correctAnswer) {
      btn.classList.add('correct');
    } else if (index === selectedIndex && !isCorrect) {
      btn.classList.add('wrong');
    }
  });

  // 显示反馈（使用优雅的 toast，不要用 alert！）
  if (isCorrect) {
    setTimeout(() => {
      showFeedback('✓ 回答正确！', true);
    }, 300);
  } else {
    setTimeout(() => {
      showFeedback('✗ 回答错误，正确答案是：' + quiz.options[quiz.correctAnswer], false);
    }, 300);
  }
}
```

## 7. 索引模式（Index）

### 7.1 核心功能

- **搜索**：按名称搜索知识点
- **筛选**：按分类筛选
- **卡片展示**：网格布局显示所有知识点
- **已掌握标记**：显示学习状态

### 7.2 实现模式

```javascript
// 搜索功能
function searchRoots(query) {
  const filtered = WordRoots.filter(root =>
    root.root.toLowerCase().includes(query.toLowerCase()) ||
    root.meaning.toLowerCase().includes(query.toLowerCase())
  );
  renderRoots(filtered);
}

// 筛选功能
function filterByOrigin(origin) {
  if (origin === 'all') {
    renderRoots(WordRoots);
  } else {
    const filtered = WordRoots.filter(root => root.origin === origin);
    renderRoots(filtered);
  }
}

// 渲染知识点卡片（XSS 安全）
function renderRoots(roots) {
  const container = document.getElementById('rootsGrid');
  if (!container) {
    console.warn('Element #rootsGrid not found');
    return;
  }

  const progress = StorageManager.getProgress();
  const masteredIds = new Set(progress.masteredRoots);

  // 清空容器
  container.innerHTML = '';

  // 创建卡片（使用 createElement 避免 XSS）
  roots.forEach(root => {
    const card = createRootCard(root, masteredIds.has(root.id));
    container.appendChild(card);
  });
}

// 创建单个卡片（安全方法）
function createRootCard(root, isMastered) {
  const card = document.createElement('div');
  card.className = `root-card ${isMastered ? 'mastered' : ''}`;
  card.onclick = () => viewDetail(root.id);

  const nameDiv = document.createElement('div');
  nameDiv.className = 'root-name';
  nameDiv.textContent = root.root; // textContent 自动转义，安全

  const meaningDiv = document.createElement('div');
  meaningDiv.className = 'root-meaning';
  meaningDiv.textContent = root.meaning;

  const originDiv = document.createElement('div');
  originDiv.className = 'root-origin';
  originDiv.textContent = root.origin;

  card.appendChild(nameDiv);
  card.appendChild(meaningDiv);
  card.appendChild(originDiv);

  if (isMastered) {
    const badge = document.createElement('span');
    badge.className = 'mastered-badge';
    badge.textContent = '✓ 已掌握';  // 明确的文字标识
    card.appendChild(badge);
  }

  return card;
}
```

## 8. 进度追踪模式（Progress）

### 8.1 实现模式

```javascript
// 加载进度
function loadProgress() {
  const progress = StorageManager.getProgress();
  const masteredCount = progress.masteredRoots.length;
  const totalCount = WordRoots.length;
  const percentage = Math.round((masteredCount / totalCount) * 100);

  // 更新统计
  document.getElementById('masteredCount').textContent = masteredCount;
  document.getElementById('totalCount').textContent = totalCount;
  document.getElementById('percentage').textContent = percentage;

  // 更新进度条
  document.getElementById('progressBar').style.width = `${percentage}%`;

  // 显示已掌握列表
  renderMasteredList(progress.masteredRoots);
}
```

## 9. 首页动画（自动适配）

### 9.1 动态加载示例

```javascript
// 从数据自动提取前5个作为动画示例
const examples = WordRoots.slice(0, 5).map(root => {
  const firstExample = root.examples[0];
  return {
    word: root.root,
    prefix: firstExample?.breakdown?.prefix || '',
    prefixMeaning: '',
    root: root.root,
    rootMeaning: root.meaning,
    meaning: firstExample?.meaning || root.description.substring(0, 30) + '...'
  };
});

// 动画循环
let currentIndex = 0;
function updateDemo() {
  const example = examples[currentIndex];

  // 更新内容
  document.getElementById('demoWord').textContent = example.word;
  document.getElementById('demoPrefix').textContent = example.prefix;
  document.getElementById('demoRoot').textContent = example.root;
  document.getElementById('demoMeaning').textContent = example.meaning;

  // 切换下一个
  currentIndex = (currentIndex + 1) % examples.length;
}

// 每4秒切换
setInterval(updateDemo, 4000);
```

## 10. 关键原则

1. **数据驱动**：所有页面从 WordRoots 数据加载，不硬编码
2. **进度持久化**：使用 LocalStorage 保存学习进度
3. **键盘友好**：支持键盘快捷键（←→空格）
4. **响应式设计**：适配移动端和桌面端
5. **极简交互**：清晰的反馈，最少的操作步骤
