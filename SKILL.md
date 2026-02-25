---
name: knowledge-site-creator
description: 一句话生成任何领域的知识学习网站。AI自动理解主题、创作内容、生成页面、部署上线。适用于任何需要系统学习的知识领域：进化心理学、大模型术语、化学元素、历史事件等。
user_invocable: true
---

# Knowledge Site Creator - 通用知识学习网站生成器

**AI理解主题，自动创作内容，生成网站，一键部署。**

## 核心理念

**设计系统优先**：
- 复用设计语言（极简主义、配色、布局、交互模式）
- 不复用具体页面代码
- AI根据主题重新创作所有内容

**通用学习模式**（核心功能）：
- **闪卡（Flashcard）** - 快速记忆
- **学习（Learn）** - 渐进式学习
- **测试（Quiz）** - 知识检验
- **索引（Index）** - 快速查找
- **进度（Progress）** - 学习追踪

**零模板依赖**：
- 不再 `cp -r` 复制模板
- AI参考设计系统，生成新页面
- 所有文案、统计、介绍都由AI创作

## 触发方式

- "生成一个XXX学习网站"
- "创建XXX知识网站"
- "做个XXX学习工坊"

示例：
- "生成一个进化心理学概念学习网站"
- "创建量子力学基础概念网站"
- "做个中医经络穴位学习工坊"

## 工作流程

### 用户视角（一句话）

```
用户："生成一个进化心理学学习网站"

AI自动执行：
✓ 分析"进化心理学"特点和价值
✓ 生成30个核心概念数据
✓ 创作首页文案、统计、介绍
✓ 参考设计系统生成页面
✓ 部署到 Vercel
✓ 返回：https://evolutionary-psychology.vercel.app

完成！
```

---

## 实施流程（AI执行）

### Step 1: 理解主题

AI深入分析主题，输出主题分析：

```javascript
主题分析 {
  领域: "进化心理学",
  特点: "跨学科（生物学+心理学），解释人类行为的底层逻辑",
  价值: "理解人性、改善关系、优化决策",
  受众: "心理学爱好者、自我提升者、教育工作者",
  表达: "科学严谨 + 生活化案例，避免学术术语堆砌"
}
```

**思考问题**：
- 这是什么领域？（学科分类、知识特点）
- 为什么重要？（学习价值、应用场景）
- 目标受众是谁？（背景、需求、痛点）
- 如何表达更好？（语言风格、案例选择）

---

### Step 2: 生成数据 + 网站配置

⚠️ **关键**：生成两个文件，不只是数据！

#### 2.1 生成数据（wordData.js）

**通用数据结构**：
```javascript
const WordRoots = [
  {
    id: 1,
    root: "适应性 (Adaptation)",     // 知识点名称
    origin: "核心理论",               // 分类/来源
    meaning: "通过自然选择进化出的有利特征",  // 一句话解释
    description: "详细说明（200-300字）...",
    examples: [                       // 应用案例/例子（3个）
      {
        word: "恐高症",
        meaning: "对高处的恐惧",
        breakdown: { root: "适应性" },
        explanation: "详细解释..."
      }
    ],
    quiz: {                           // 小测试（4选1）
      question: "以下哪个不是适应性的特征？",
      options: ["选项A", "选项B", "选项C", "选项D"],
      correctAnswer: 2                // 正确答案索引（0-3）
    }
  }
];
```

**生成数量**：默认20-30个，根据主题复杂度调整

#### 2.2 生成配置（siteConfig.js）🆕

**AI创作，完全适配主题**：
```javascript
const siteConfig = {
  // 基础信息
  topic: "进化心理学",
  siteName: "进化心理学概念工坊",
  itemName: "概念",                    // 单个知识点的称呼
  itemCount: 30,

  // 首页Hero区（AI创作）
  hero: {
    title: [
      "30个核心概念",
      "理解人类行为",
      "的底层逻辑"
    ],
    subtitle: "从适应性到配偶选择，系统掌握进化心理学核心框架",
    animation: {
      enabled: true,                   // 是否显示动画
      demoCount: 5                     // 动画展示几个概念
    }
  },

  // 统计卡片（AI生成，匹配主题特点）
  stats: [
    { value: "30", label: "核心概念" },
    { value: "100+", label: "生活应用" },
    { value: "15分钟", label: "每日学习" }
  ],

  // 底部介绍（AI创作）
  footer: {
    tagline: "像理解自己一样理解人性",
    description: "基于进化心理学的科学框架，用30个核心概念解释人类行为背后的生物学逻辑。从配偶选择到亲子关系，从群体合作到情绪反应，让你看懂人性的深层原因。"
  },

  // 按钮文案（AI适配）
  cta: {
    primary: "开始第一个概念 →",
    secondary: "闪卡复习"
  }
};
```

**AI创作原则**：
- `hero.title`: 简洁有力，3行，突出核心价值
- `hero.subtitle`: 具体说明学什么，为什么学
- `stats`: 真实、有说服力的数字，匹配主题特点
- `footer.tagline`: 一句话点题，朗朗上口
- `footer.description`: 2-3句，说清楚是什么、学什么、有什么用

---

### Step 3: 参考设计系统，生成页面

⚠️ **不再复制模板！AI参考设计规范，生成新页面**

#### 3.1 设计系统参考

⚠️ **参考文档**：`references/design-system.md` - 完整的设计规范

**核心要点**：
- **配色**：黄色主题色 (#FBBF24)，灰色系文字和背景
- **字体**：Inter字体族，代码用Courier New
- **风格**：极简主义，大留白，清晰层级
- **组件**：圆角卡片（12px），极浅阴影
- **间距**：8px网格系统，Hero区96px留白

详细配色、字体、间距、组件样式见 `design-system.md`

#### 3.2 生成页面清单

⚠️ **功能参考**：
- `references/core-patterns.md` - 核心学习模式实现
- `references/code-quality.md` - **代码质量标准（必须遵守）**
- `references/seo-best-practices.md` - **SEO优化指南** 🆕
- `references/pwa-setup.md` - PWA配置指南

**代码质量要求**（强制）：
- ✅ **错误处理**：所有 LocalStorage 操作必须有 try-catch
- ✅ **XSS 防护**：使用 textContent/createElement，禁止直接 innerHTML 插入未转义数据
- ✅ **DOM 安全**：所有 DOM 操作前检查元素存在
- ✅ **避免全局污染**：使用模块封装或 IIFE

详细规则见 `references/code-quality.md`。

AI参考设计系统，从零生成以下页面：

1. **index.html** - 首页 🆕
   - Hero区：使用 `siteConfig.hero.title/subtitle`
   - 动画演示：从 `WordRoots` 动态加载前5个（见core-patterns.md §9）
   - 统计卡片：使用 `siteConfig.stats`
   - CTA按钮：使用 `siteConfig.cta`
   - Footer：使用 `siteConfig.footer`

2. **learn.html** - 学习页（见core-patterns.md §5）
   - 渐进式卡片展示
   - 上一个/下一个导航
   - 标记已掌握功能

3. **flashcard.html** - 闪卡页（见core-patterns.md §4）
   - 卡片翻转动画
   - 键盘快捷键（←→翻页，空格翻转）
   - 进度显示

4. **roots.html** - 索引页（见core-patterns.md §7）
   - 标题适配：`${itemName}索引`
   - 搜索框 + 筛选器
   - 卡片网格布局

5. **progress.html** - 进度页（见core-patterns.md §8）
   - 学习统计
   - 已掌握列表
   - 成就系统

6. **root-detail.html** - 详情页
   - 概念详细说明
   - 例子展示
   - 测试题（见core-patterns.md §6）

7. **css/minimal.css** - 样式文件（见design-system.md）
   - 统一设计系统
   - 响应式布局

8. **js/storage.js** - 存储逻辑（见core-patterns.md §3）
   - LocalStorage 进度管理

9. **manifest.json** - PWA 配置（见pwa-setup.md §1）🆕
   - App 名称、图标、主题色
   - 支持安装到主屏幕

10. **sw.js** - Service Worker（见pwa-setup.md §2）🆕
    - 缓存静态资源
    - 支持离线访问

11. **icon-192.png / icon-512.png** - PWA 图标 🆕
    - **自动生成**：使用 PIL 从配置生成（黄色背景 + 主题文字）
    - **不要手动创建**：AI 应自动用 Python PIL 生成

12. **sitemap.xml** - 网站地图（见seo-best-practices.md §4）🆕
    - 列出所有页面URL
    - 提交到搜索引擎

13. **robots.txt** - 爬虫指令（见seo-best-practices.md §5）🆕
    - 允许/禁止抓取规则
    - Sitemap 位置声明

**⚠️ 强制要求：所有 HTML 文件必须包含完整的 meta 标签**

每个 HTML 文件的 `<head>` 必须包含：

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${siteConfig.siteName}</title>

  <!-- SEO 基础 -->
  <meta name="description" content="${siteConfig.footer.description}">
  <meta name="keywords" content="${siteConfig.topic},学习,知识,${siteConfig.itemName}">
  <meta name="author" content="乔木">
  <meta name="language" content="zh-CN">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="${currentPageUrl}">

  <!-- Open Graph (社交分享) -->
  <meta property="og:title" content="${siteConfig.siteName}">
  <meta property="og:description" content="${siteConfig.footer.description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${currentPageUrl}">
  <meta property="og:image" content="${siteBaseUrl}/icon-512.png">
  <meta property="og:site_name" content="${siteConfig.siteName}">
  <meta property="og:locale" content="zh_CN">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@vista8">
  <meta name="twitter:creator" content="@vista8">
  <meta name="twitter:title" content="${siteConfig.siteName}">
  <meta name="twitter:description" content="${siteConfig.footer.description}">
  <meta name="twitter:image" content="${siteBaseUrl}/icon-512.png">

  <!-- Favicon (简单的 emoji data URI) -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>">

  <!-- PWA 支持 🆕 -->
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#FBBF24">

  <!-- iOS Safari PWA 支持 -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="${siteConfig.itemName}学习">
  <link rel="apple-touch-icon" href="/icon-192.png">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <!-- 样式 -->
  <link rel="stylesheet" href="css/minimal.css">
</head>
```

**关键原则**：
- ✅ 核心学习模式（闪卡、学习、测试）保持一致 - 参考 core-patterns.md
- ✅ 设计风格（配色、字体、布局）保持一致 - 参考 design-system.md
- ✅ 所有文案、标题、描述由AI根据主题创作
- ✅ **代码质量**：必须遵守 code-quality.md 标准（错误处理、XSS防护、DOM安全）🆕
- ✅ **PWA 支持**：manifest.json + Service Worker + 图标（离线访问、可安装）🆕
- ✅ **SEO 优化**：完整的 meta 标签 + sitemap.xml + robots.txt + 结构化数据 🆕
- ✅ **语义化 HTML**：正确使用 header, main, article, section 等标签 🆕
- ✅ **移动端优先**：响应式设计 + viewport meta + 快速加载（< 3秒）🆕
- ❌ 不要硬编码特定领域的内容

---

### Step 4: 创建项目结构

```bash
# 项目位置
mkdir -p "/Users/joe/Dropbox/code/${topic}-workshop"
cd "/Users/joe/Dropbox/code/${topic}-workshop"

# 创建目录结构
mkdir -p js css

# 写入数据
cat > js/wordData.js << 'EOF'
const WordRoots = [...];
EOF

# 写入配置 🆕
cat > js/siteConfig.js << 'EOF'
const siteConfig = {...};
EOF

# 写入页面（AI生成的HTML）
cat > index.html << 'EOF'
[AI生成的index.html]
EOF

# 写入其他页面...

# 🆕 自动生成 PWA 图标（用 PIL）
python3 << 'PYEOF'
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename, text):
    # 创建黄色背景
    img = Image.new('RGB', (size, size), color='#FBBF24')
    draw = ImageDraw.Draw(img)

    # 尝试使用系统字体
    try:
        font_size = int(size * 0.25)
        font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', font_size)
    except:
        font = ImageFont.load_default()

    # 获取文字边界框
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # 居中位置
    x = (size - text_width) / 2
    y = (size - text_height) / 2

    # 绘制文字（深灰色）
    draw.text((x, y), text, font=font, fill='#1F2937')

    # 保存
    img.save(filename, 'PNG')

# 从主题生成图标文字（取前2-3个字）
icon_text = "${siteConfig.itemName}"[:3]  # 例如："概念" → "概念"、"历史知识点" → "历史知"

# 生成两种尺寸
create_icon(192, 'icon-192.png', icon_text)
create_icon(512, 'icon-512.png', icon_text)
print("✓ PWA 图标生成完成")
PYEOF
```

---

### Step 5: 数据验证（强制质量检查）

⚠️ **关键**：AI 生成的数据必须经过完整验证，确保质量和一致性

```bash
# ========================================
# 阶段 1：基础结构验证
# ========================================

echo "🔍 验证数据结构..."

# 1.1 检查数据文件存在且变量名正确
if ! grep -q "const WordRoots" js/wordData.js; then
  echo "❌ 错误：数据变量名不正确（应为 const WordRoots）"
  exit 1
fi

# 1.2 检查配置文件存在且变量名正确
if ! grep -q "const siteConfig" js/siteConfig.js; then
  echo "❌ 错误：配置文件缺失（应为 const siteConfig）"
  exit 1
fi

# ========================================
# 阶段 2：数据完整性验证
# ========================================

echo "🔍 验证数据完整性..."

# 2.1 使用 Node.js 进行深度验证
node -e "
const fs = require('fs');

// 读取数据文件
const dataContent = fs.readFileSync('js/wordData.js', 'utf-8');
eval(dataContent);  // 加载 WordRoots

let errors = [];
let warnings = [];

// 验证数据存在
if (typeof WordRoots === 'undefined') {
  console.error('❌ 严重错误：WordRoots 未定义');
  process.exit(1);
}

if (!Array.isArray(WordRoots) || WordRoots.length === 0) {
  console.error('❌ 严重错误：WordRoots 为空或不是数组');
  process.exit(1);
}

console.log(\`📊 数据量：\${WordRoots.length} 个知识点\`);

// 遍历每个知识点进行验证
WordRoots.forEach((item, index) => {
  const itemLabel = \`Item #\${item.id || index}\`;

  // 必需字段检查
  if (!item.id) errors.push(\`\${itemLabel}: 缺少 id\`);
  if (!item.root || item.root.trim() === '') errors.push(\`\${itemLabel}: 缺少 root（知识点名称）\`);
  if (!item.origin) warnings.push(\`\${itemLabel}: 缺少 origin（分类）\`);
  if (!item.meaning || item.meaning.trim() === '') errors.push(\`\${itemLabel}: 缺少 meaning（简短解释）\`);
  if (!item.description || item.description.trim() === '') errors.push(\`\${itemLabel}: 缺少 description（详细说明）\`);

  // 描述长度检查（应该详细但不过长）
  if (item.description && item.description.length < 50) {
    warnings.push(\`\${itemLabel}: description 太短（<50字），建议扩展为200-300字\`);
  }
  if (item.description && item.description.length > 1000) {
    warnings.push(\`\${itemLabel}: description 太长（>1000字），建议精简\`);
  }

  // 例子检查
  if (!item.examples || !Array.isArray(item.examples)) {
    errors.push(\`\${itemLabel}: 缺少 examples 数组\`);
  } else if (item.examples.length < 3) {
    errors.push(\`\${itemLabel}: examples 少于3个（当前 \${item.examples.length}）\`);
  } else {
    // 验证每个例子的结构
    item.examples.forEach((ex, exIndex) => {
      if (!ex.word) errors.push(\`\${itemLabel}.examples[\${exIndex}]: 缺少 word\`);
      if (!ex.meaning) errors.push(\`\${itemLabel}.examples[\${exIndex}]: 缺少 meaning\`);
      if (!ex.explanation) warnings.push(\`\${itemLabel}.examples[\${exIndex}]: 缺少 explanation\`);
    });
  }

  // 测试题检查
  if (!item.quiz) {
    warnings.push(\`\${itemLabel}: 缺少 quiz（测试题）\`);
  } else {
    if (!item.quiz.question || item.quiz.question.trim() === '') {
      errors.push(\`\${itemLabel}.quiz: 缺少 question\`);
    }
    if (!item.quiz.options || !Array.isArray(item.quiz.options)) {
      errors.push(\`\${itemLabel}.quiz: 缺少 options 数组\`);
    } else if (item.quiz.options.length !== 4) {
      errors.push(\`\${itemLabel}.quiz: options 必须是4个（当前 \${item.quiz.options.length}）\`);
    }
    if (typeof item.quiz.correctAnswer !== 'number') {
      errors.push(\`\${itemLabel}.quiz: correctAnswer 必须是数字\`);
    } else if (item.quiz.correctAnswer < 0 || item.quiz.correctAnswer > 3) {
      errors.push(\`\${itemLabel}.quiz: correctAnswer 越界（必须是0-3，当前 \${item.quiz.correctAnswer}）\`);
    }
  }
});

// 输出验证结果
if (errors.length > 0) {
  console.error('\\n❌ 发现 ' + errors.length + ' 个错误：');
  errors.slice(0, 10).forEach(e => console.error('  - ' + e));
  if (errors.length > 10) console.error(\`  ... 还有 \${errors.length - 10} 个错误\`);
  process.exit(1);
}

if (warnings.length > 0) {
  console.warn('\\n⚠️  发现 ' + warnings.length + ' 个警告：');
  warnings.slice(0, 5).forEach(w => console.warn('  - ' + w));
  if (warnings.length > 5) console.warn(\`  ... 还有 \${warnings.length - 5} 个警告\`);
}

console.log('\\n✓ 数据验证通过');
" || exit 1

# ========================================
# 阶段 3：配置验证
# ========================================

echo "🔍 验证配置..."

node -e "
const fs = require('fs');
const configContent = fs.readFileSync('js/siteConfig.js', 'utf-8');
eval(configContent);

if (typeof siteConfig === 'undefined') {
  console.error('❌ siteConfig 未定义');
  process.exit(1);
}

// 验证必需字段
const required = ['topic', 'siteName', 'itemName', 'itemCount', 'hero', 'stats', 'footer', 'cta'];
const missing = required.filter(key => !siteConfig[key]);

if (missing.length > 0) {
  console.error('❌ siteConfig 缺少字段：' + missing.join(', '));
  process.exit(1);
}

// 验证 hero 结构
if (!siteConfig.hero.title || !Array.isArray(siteConfig.hero.title) || siteConfig.hero.title.length !== 3) {
  console.error('❌ siteConfig.hero.title 必须是3行数组');
  process.exit(1);
}

console.log('✓ 配置验证通过');
" || exit 1

echo ""
echo "✅ 所有验证通过！"
```

---

### Step 6: 部署（强制安全检查）

⚠️ **关键**：每个项目必须独立部署，绝不共享 GitHub 仓库

**部署流程（必须严格按顺序执行）**：

```bash
# ========================================
# 阶段 1：部署前安全检查（必须执行）
# ========================================

# 1.1 检查并移除 Git 远程仓库（防止关联到其他项目的仓库）
if git remote -v 2>/dev/null | grep -q 'origin'; then
  echo "⚠️ 警告：检测到 Git 远程仓库，立即移除以避免冲突"
  git remote remove origin
  echo "✓ 已移除 Git 远程仓库"
fi

# 1.2 初始化本地 Git（仅本地，不推送到 GitHub）
git init
git add .
git commit -m "Initial commit: ${siteName}"

# 1.3 列出所有现有 workshop 项目（用于后续验证）
echo "📋 现有项目列表："
ls -d /Users/joe/Dropbox/code/*-workshop 2>/dev/null | while read dir; do
  PROJECT_NAME=$(basename "$dir")
  if [ -f "$dir/.vercel/project.json" ]; then
    PROJECT_ID=$(cat "$dir/.vercel/project.json" | jq -r '.projectId' 2>/dev/null || echo "unknown")
    echo "  - $PROJECT_NAME (projectId: $PROJECT_ID)"
  fi
done

# ========================================
# 阶段 2：执行部署
# ========================================

echo "🚀 开始部署到 Vercel..."
vercel --prod --yes 2>&1 | tee /tmp/vercel-deploy-${projectName}.log

DEPLOY_STATUS=$?
if [ $DEPLOY_STATUS -ne 0 ]; then
  echo "❌ 部署失败，请检查日志：/tmp/vercel-deploy-${projectName}.log"
  exit 1
fi

# ========================================
# 阶段 3：部署后强制验证（必须执行）
# ========================================

echo ""
echo "🔍 部署后验证..."

# 3.1 验证 projectId 已生成
if [ ! -f ".vercel/project.json" ]; then
  echo "❌ 错误：未找到 .vercel/project.json"
  exit 1
fi

NEW_PROJECT_ID=$(cat .vercel/project.json | jq -r '.projectId')
NEW_PROJECT_NAME=$(cat .vercel/project.json | jq -r '.projectName')
echo "✓ 新项目："
echo "  名称: $NEW_PROJECT_NAME"
echo "  ID: $NEW_PROJECT_ID"

# 3.2 提取部署 URL
DEPLOY_URL=$(grep -E "Production:|https://.*vercel.app" /tmp/vercel-deploy-${projectName}.log | grep -o "https://[^ ]*vercel.app" | head -1)
echo "✓ 部署 URL: $DEPLOY_URL"

# 3.3 验证新网站可访问
echo "🌐 验证新网站..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$DEPLOY_URL" || echo "000")
if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "304" ]; then
  echo "✓ 新网站可正常访问 (HTTP $HTTP_STATUS)"
else
  echo "⚠️ 警告：新网站返回 HTTP $HTTP_STATUS"
fi

# 3.4 检查其他项目是否受影响（关键步骤）
echo ""
echo "🔍 检查其他项目是否受影响..."
AFFECTED_PROJECTS=0

for dir in /Users/joe/Dropbox/code/*-workshop; do
  if [ "$dir" = "/Users/joe/Dropbox/code/${projectName}" ]; then
    continue  # 跳过当前项目
  fi

  if [ -f "$dir/.vercel/project.json" ]; then
    OLD_PROJECT_NAME=$(basename "$dir")
    OLD_PROJECT_ID=$(cat "$dir/.vercel/project.json" | jq -r '.projectId' 2>/dev/null)

    # 检查是否有相同的 projectId（这表示冲突）
    if [ "$OLD_PROJECT_ID" = "$NEW_PROJECT_ID" ]; then
      echo "❌ 严重错误：项目 $OLD_PROJECT_NAME 的 projectId 与新项目相同！"
      echo "   这意味着新项目覆盖了旧项目，需要立即修复。"
      AFFECTED_PROJECTS=$((AFFECTED_PROJECTS + 1))
    fi
  fi
done

if [ $AFFECTED_PROJECTS -gt 0 ]; then
  echo ""
  echo "❌ 检测到 $AFFECTED_PROJECTS 个项目受影响，部署失败！"
  echo "   请手动检查并修复冲突。"
  exit 1
fi

echo "✓ 所有现有项目未受影响"

# ========================================
# 阶段 3.5：移动端和 SEO 验证 🆕
# ========================================

echo ""
echo "📱 验证移动端适配..."

# 检查 viewport meta 标签（移动端必需）
VIEWPORT_CHECK=$(curl -s "$DEPLOY_URL" | grep -c 'viewport')
if [ "$VIEWPORT_CHECK" -gt 0 ]; then
  echo "✓ 移动端 viewport 配置正确"
else
  echo "⚠️ 警告：缺少 viewport meta 标签，移动端可能显示异常"
fi

# 检查 SEO meta 标签
echo "🔍 验证 SEO 配置..."
META_DESCRIPTION=$(curl -s "$DEPLOY_URL" | grep -c 'meta name="description"')
META_OG=$(curl -s "$DEPLOY_URL" | grep -c 'property="og:')

if [ "$META_DESCRIPTION" -gt 0 ]; then
  echo "✓ SEO description 已配置"
else
  echo "⚠️ 警告：缺少 SEO description"
fi

if [ "$META_OG" -gt 0 ]; then
  echo "✓ Open Graph 标签已配置（社交分享优化）"
else
  echo "⚠️ 警告：缺少 Open Graph 标签"
fi

# 模拟移动设备访问测试
echo "📱 模拟移动设备访问..."
MOBILE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" \
  "$DEPLOY_URL")

if [ "$MOBILE_STATUS" = "200" ] || [ "$MOBILE_STATUS" = "304" ]; then
  echo "✓ 移动端访问正常 (HTTP $MOBILE_STATUS)"
else
  echo "⚠️ 警告：移动端访问异常 (HTTP $MOBILE_STATUS)"
fi

# ========================================
# 阶段 4：成功总结
# ========================================

echo ""
echo "✅ 部署成功！"
echo ""
echo "📊 部署信息："
echo "  项目名称: $NEW_PROJECT_NAME"
echo "  项目 ID: $NEW_PROJECT_ID"
echo "  部署 URL: $DEPLOY_URL"
echo "  日志文件: /tmp/vercel-deploy-${projectName}.log"
```

---

**安全原则（必须遵守）**：

1. ✅ **禁止 GitHub 关联**：默认不连接 GitHub，避免仓库共享
2. ✅ **强制前置检查**：部署前必须移除所有 Git 远程仓库
3. ✅ **强制后置验证**：部署后必须检查 projectId 唯一性
4. ✅ **冲突自动检测**：发现冲突立即报错，不允许继续
5. ✅ **完整日志记录**：所有部署操作记录到 /tmp/

---

**如果仍然发生冲突（极端情况）**：

如果验证通过但实际仍有问题，执行紧急修复：

```bash
# 1. 立即列出所有 Vercel 项目
vercel ls

# 2. 检查每个本地项目的部署状态
cd /Users/joe/Dropbox/code
for dir in *-workshop; do
  echo "=== $dir ==="
  cd "$dir"
  if [ -f ".vercel/project.json" ]; then
    cat .vercel/project.json | jq -r '.projectName, .projectId'
  fi
  cd ..
done

# 3. 重新部署受影响的项目
cd /path/to/affected-project
vercel --prod --yes

# 4. 向用户报告冲突详情和修复结果
```

---

## 成功输出模板

```markdown
✅ ${siteName} 已生成并部署！

📁 项目位置：${projectPath}
🌐 网站名称：${siteName}
📚 知识点数量：${itemCount}个
🔗 访问链接：${deployUrl}

🎯 核心特性：
- ✅ AI创作首页：根据主题生成标题、副标题、统计
- ✅ 动态动画：自动从数据加载，完全适配
- ✅ 通用学习模式：闪卡、渐进学习、测试、索引
- ✅ 极简设计：清晰的视觉层级，专注内容

🔧 下一步：
1. 打开网站查看效果
2. 审核AI生成的内容
3. 配置自定义域名（Vercel后台）
```

---

## 实施检查清单

AI 执行此 skill 时，**必须严格按顺序**完成：

- [ ] 1. **理解主题** - 分析领域特点、价值、受众、表达方式
- [ ] 2. **生成数据** - 创建 wordData.js（const WordRoots）
- [ ] 3. **生成配置** 🆕 - 创建 siteConfig.js（AI创作首页文案）
- [ ] 4. **生成页面** 🆕 - 参考设计系统，从零生成HTML（不复制模板）
- [ ] 5. **创建项目** - mkdir + 写入所有文件
- [ ] 6. **验证数据** - 检查数据和配置文件完整性
- [ ] 7. **安全部署** 🔒 - 执行 Step 6 的完整部署流程（含前置检查 + 部署 + 后置验证）
- [ ] 8. **返回信息** - 项目路径 + URL + 核心特性 + 安全检查结果

---

## 关键改进（相比旧版）

### ❌ 旧版问题
- 依赖模板复制（`cp -r word-root-workshop`）
- 用 sed 粗暴替换文案
- 首页文案硬编码，不适配主题
- 动画示例写死英文单词

### ✅ 新版优势
- 零模板依赖，AI从零生成页面
- AI理解主题后创作所有文案
- 首页完全适配主题特点
- 动画自动从数据加载

### 🎯 核心理念转变
```
旧版：复制 + 替换
新版：理解 + 创作

旧版：模板驱动
新版：设计系统驱动

旧版：硬编码文案
新版：AI创作内容
```

---

## 注意事项

⚠️ **数据结构不变**：
- 仍然使用 `const WordRoots` 和固定字段结构
- 这是核心学习模式（闪卡、学习、测试）的基础

⚠️ **设计风格保持**：
- 极简主义、黄色主题色、Inter字体
- 这些是品牌识别度的保证

⚠️ **AI自由发挥**：
- 首页文案、统计数据、介绍文本
- 根据主题特点创作，不要千篇一律

---

## Vercel 部署最佳实践 🆕

### 问题背景

Vercel 在部署时可能会自动连接 GitHub 仓库，导致多个项目共享同一个仓库，引发部署冲突：
- 新项目覆盖旧项目的部署
- 旧项目的 URL 失效
- GitHub 仓库关联混乱

### 解决方案

**1. 默认不连接 GitHub**
```bash
# 仅使用本地 Git，不推送到 GitHub
git init
git add .
git commit -m "Initial commit"
vercel --prod --yes  # 只部署，不连接 GitHub
```

**2. 部署后验证**
```bash
# 检查生成的 projectId 是否唯一
cat .vercel/project.json

# 应该看到类似：
# {"projectId":"prj_UNIQUE_ID_HERE",...}
```

**3. 发现冲突时的补救**

如果部署后发现旧项目受影响：

```bash
# 立即进入旧项目目录
cd /Users/joe/Dropbox/code/旧项目名称

# 重新部署旧项目
vercel --prod --yes

# 确认旧项目恢复正常
curl -I https://旧项目URL
```

### 故障排查清单

部署新项目后，必须检查：

- [ ] 新项目的 `.vercel/project.json` 中的 `projectId` 是否唯一
- [ ] 新项目的 Production URL 是否可以访问（HTTP 200）
- [ ] 旧项目（如果存在）的 URL 是否仍然可访问
- [ ] 部署日志中的 "Linked to" 信息是否正确

### 经验教训（真实生产事故）

**事故时间线**：2026-02-25

**事故描述**：
1. 生成 `evolutionary-psychology-workshop`（进化心理学），成功部署
2. 生成 `design-aesthetics-workshop`（设计美学），成功部署
3. 用户发现 **word.qiaomu.ai**（原词根词缀网站）显示的是进化心理学内容
4. 检查发现 `word-root-workshop` 项目的 Git 仓库被进化心理学内容覆盖

**根本原因分析**：

```bash
# 事故前的状态
evolutionary-psychology-workshop → origin: https://github.com/joeseesun/word-root-workshop.git
word-root-workshop              → origin: https://github.com/joeseesun/word-root-workshop.git
                                   ↑↑↑ 两个项目共享同一个 GitHub 仓库
```

**为什么会发生**：
- 旧版 skill 使用 `cp -r word-root-workshop` 复制模板
- 复制时连 `.git/` 目录也一起复制了（包含远程仓库配置）
- 部署时 Vercel 检测到 Git 远程仓库，自动关联
- 多个项目关联同一个 GitHub 仓库，后部署的覆盖先部署的

**损害范围**：
- ⛔ word.qiaomu.ai（生产域名）显示错误内容
- ⛔ word-root-workshop 的 Git 历史被污染
- ⛔ 用户体验受损，需要紧急修复

**紧急修复步骤**：
```bash
# 1. 恢复 word-root-workshop 到原始状态
cd /Users/joe/Dropbox/code/word-root-workshop
git log --oneline  # 找到原始提交
git reset --hard 14cc7b0  # 恢复到原始词根词缀内容

# 2. 修复 vercel.json 配置冲突
# 移除不兼容的 routes 配置

# 3. 重新部署
vercel --prod --yes

# 4. 验证恢复
curl -sL https://word.qiaomu.ai/ | grep "词根词缀记忆工坊"

# 5. 清理其他项目的 Git 远程仓库
cd /Users/joe/Dropbox/code/evolutionary-psychology-workshop
git remote remove origin
```

**彻底解决方案**（已在 Step 6 实施）：

1. **强制前置检查**：部署前自动移除所有 Git 远程仓库
2. **强制后置验证**：部署后检查 projectId 唯一性
3. **冲突自动检测**：遍历所有项目，发现相同 projectId 立即报错
4. **完整日志记录**：所有部署操作记录到 /tmp/
5. **零容忍策略**：任何检测到的冲突都不允许继续

**长期防范措施**：
- ✅ 废弃模板复制机制（`cp -r`），改用从零生成
- ✅ 在 Step 6 中实施强制安全检查
- ✅ 更新实施检查清单，明确"安全部署"步骤
- ✅ 文档中增加"经验教训"章节，防止后人重蹈覆辙

**教训总结**：
> "Copy + Paste 是万恶之源。模板驱动看似高效，实则埋下了隐患。只有从零生成（设计系统驱动），才能确保每个项目真正独立。"

**影响**：
- 促使 skill 从"模板驱动"彻底重构为"设计系统驱动"
- 确立了"零模板依赖"的核心原则
- 建立了完善的部署安全检查机制

---

## 批量更新机制 🔄

### 使用场景

当 skill 的设计系统有更新（如 CSS bug 修复、样式改进）时，需要将更新同步到所有已部署的 workshop 项目。

**典型场景**：
- CSS 样式修复：修复了响应式布局问题
- 设计改进：优化了卡片阴影、间距、配色
- 功能增强：添加了新的交互动效
- 安全更新：修复了 XSS 漏洞或其他安全问题

### 更新脚本

**脚本位置**：`scripts/update-css.sh`

**使用方法**：

```bash
# 1. 演练模式（仅列出将更新的项目）
bash scripts/update-css.sh --dry-run

# 2. 执行更新
bash scripts/update-css.sh
```

### 工作流程

**脚本自动执行以下步骤**：

1. **扫描项目**：自动扫描 `/Users/joe/Dropbox/code/*-workshop`
2. **智能对比**：使用 `cmp` 命令对比 CSS 文件，跳过已是最新版本的项目
3. **安全备份**：更新前自动备份旧 CSS 为 `.backup` 文件
4. **Git 提交**：自动 commit CSS 变更（commit message: `chore: update CSS from skill template`）
5. **重新部署**：调用 `vercel --prod --yes` 重新部署到生产环境
6. **失败回滚**：如果部署失败，自动恢复备份的 CSS
7. **统计报告**：输出更新统计（成功/跳过/失败项目数量）

### 使用示例

**步骤 1：准备最新的 CSS**

在 skill 目录中修复或改进 `templates/minimal.css`：

```bash
cd /Users/joe/.claude/skills/knowledge-site-creator
# 编辑 templates/minimal.css
# 修复 bug 或改进样式
```

**步骤 2：预览将更新的项目**

```bash
bash scripts/update-css.sh --dry-run
```

输出示例：
```
🔍 演练模式（不会实际更新）

📁 CSS 源文件：/path/to/templates/minimal.css
📊 文件大小：12345 bytes

🔍 扫描 workshop 项目...

================================================
📦 项目：evolutionary-psychology-workshop
📝 将更新：/path/to/evolutionary-psychology-workshop/css/minimal.css
📝 将重新部署到 Vercel

================================================
📦 项目：word-root-workshop
✓ 跳过：CSS 已是最新版本

================================================
📊 更新总结

  ✅ 成功更新：1 个项目
  ⚠️  跳过：1 个项目

💡 这是演练模式，没有实际执行任何操作
   要实际执行，请运行：bash scripts/update-css.sh
```

**步骤 3：执行批量更新**

```bash
bash scripts/update-css.sh
```

输出示例：
```
================================================
📦 项目：evolutionary-psychology-workshop
💾 已备份旧 CSS：/path/to/css/minimal.css.backup
✓ 已更新 CSS
🚀 重新部署到 Vercel...
✅ 部署成功

================================================
📊 更新总结

  ✅ 成功更新：1 个项目
  ⚠️  跳过：1 个项目
```

### 安全特性

1. **智能跳过**：自动跳过已是最新版本的项目，避免不必要的部署
2. **自动备份**：更新前备份旧 CSS 为 `.backup` 文件
3. **失败回滚**：部署失败时自动恢复备份
4. **Git 记录**：所有更新都有 Git commit，可追溯历史
5. **演练模式**：`--dry-run` 模式让你先看看会更新什么

### 注意事项

⚠️ **更新前检查**：
- 确保 `templates/minimal.css` 已经过测试
- 使用 `--dry-run` 先预览将更新的项目
- 检查是否有项目正在被用户访问（避免高峰期更新）

⚠️ **更新后验证**：
- 脚本完成后，随机抽查 2-3 个项目的网站
- 确认新样式生效且没有破坏布局
- 检查移动端显示是否正常

⚠️ **失败处理**：
- 如果某个项目部署失败，脚本会自动回滚该项目的 CSS
- 失败的项目不影响其他项目的更新
- 可以手动进入失败的项目目录，使用 `vercel --prod --yes` 重试

### 扩展性

**未来可扩展的更新类型**：

当前脚本仅支持 CSS 更新，但同样的机制可以扩展到：
- JavaScript 文件更新（`js/storage.js` 等）
- HTML 模板更新（如修复 meta 标签缺失）
- 配置文件更新（`vercel.json` 等）
- 批量迁移（如数据结构变更）

**扩展方法**：参考 `update-css.sh` 创建类似脚本，如 `update-storage.sh`、`update-meta-tags.sh` 等。
