---
name: knowledge-site-creator
description: "一句话生成任意主题的知识学习网站（HTML/CSS/JS/PWA/SEO）。AI自动完成：主题分析→知识数据生成→页面编码→Vercel部署→返回链接。支持学科知识/技术术语/历史文化/科学概念/设计美学等领域。触发词：生成/创建/做一个XXX学习网站/知识网站/学习工坊/概念网站/术语速查。"
version: 2.0.0
author: Joe (向阳乔木)
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [web-development, education, content-generation, pwa, seo, vercel]
    category: creative
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

## 成本与资源约束

| 资源 | 免费层限制 | 说明 |
|------|-----------|------|
| Vercel 部署数 | 无硬限制 | 每个项目独立 projectId，免费层支持无限静态站点 |
| Vercel 带宽 | 100GB/月 | 每个站点独立计费，学习类站点流量极低 |
| Vercel 构建时长 | 6000 分钟/月 | 静态站点无需构建，不消耗构建配额 |
| PWA 图标生成 | 无限制 | 本地 PIL 生成，不调用外部 API |
| 知识点数量 | 10-50 个 | 默认 20-30，简单主题 10-15，复杂主题上限 50 |

**注意事项**：
- 每个主题独立部署为一个 Vercel 项目，不会互相覆盖
- 已部署的站点可通过 `vercel ls` 查看，通过 `vercel rm <project>` 删除
- CSS 更新需要重新部署所有站点（用 `scripts/update-css.sh`）

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

🔴 **CHECKPOINT 0（入口）**：逐项验证（复制执行）：

```bash
# 1. 依赖检查
node --version          # 期望 ≥18
python -c "import PIL"  # 期望无报错（Pillow 可用）
vercel whoami           # 期望返回用户名（已登录）
jq --version            # 期望 ≥1.8

# 2. 目录检查
echo "${KNOWLEDGE_SITE_OUTPUT_DIR:-$HOME/hermes-generated-sites}"
mkdir -p "${KNOWLEDGE_SITE_OUTPUT_DIR:-$HOME/hermes-generated-sites}"

# 3. 主题提取
echo "用户请求: <在此填入用户的原始请求>"
echo "提取主题: <在此填入你分析出的主题名>"
```

🛑 上述 3 项任一失败 → **停止**，修复依赖后再继续。

### 流程总览

| Step | 名称 | 输入 | 输出 | 估算 |
|------|------|------|------|------|
| 1 | 理解主题 | 用户一句话 | 主题分析对象（领域/特点/价值/受众/表达）| ~2min |
| 2 | 生成数据+配置 | 主题分析 | `js/wordData.js` + `js/siteConfig.js` | ~5min |
| 3 | 参考设计生成页面 | references/*.md | 6 HTML + 1 CSS + 1 JS + PWA + SEO 文件 | ~10min |
| 4 | 创建项目结构 | 所有文件内容 | 磁盘上的完整项目目录 | ~2min |
| 5 | 数据验证 | 项目目录 | Node.js 验证报告 | ~1min |
| 6 | 部署到 Vercel | 验证通过的项目 | 生产 URL | ~2min |

---

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

🔴 **CHECKPOINT 1**：回答以下 5 个问题（缺一不可进入 Step 2）：

1. 主题英文/拼音 slug：______（用于目录名，如 `evolutionary-psychology`）
2. `itemName`：______（单个知识点的称呼，如"概念"/"命令"/"术语"/"穴位"）
3. 目标受众：______（如"编程初学者"/"心理学爱好者"）
4. 语言风格：______（如"科学严谨+生活案例"/"极简技术文档风"）
5. 估算知识点数：______个（默认 20，复杂主题 30-50）

🛑 5 题未全部回答 → **回到 Step 1** 重新分析。

---

### Step 2: 生成数据 + 网站配置

⚠️ **关键**：生成两个文件，不只是数据！

#### 2.1 生成数据（wordData.js）

⚠️ **写入方式**：不要用 bash heredoc (`cat > file << 'EOF'`) 写含中文的 JS 数据——heredoc 会静默损坏输出（丢失冒号、替换直引号为弯引号）。用 `write_file` 工具或 Python `open().write()`。详见 `references/heredoc-encoding-pitfalls.md`。

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

### Step 3: 生成页面

⚠️ **使用 Python 生成器，不要手动 sed 替换或复制旧 HTML**

**主方案（推荐）**：运行 `scripts/gen-html.py` 从 siteConfig.js 动态生成所有 HTML。每个页面的 meta description、OG title、页面标题全部来自配置数据，从源头消除语义残留。设计原理见 `references/html-generator-pattern.md`，语义验证方法见 `references/seo-semantic-verification.md`。

```bash
# 生成 6 个 HTML + manifest.json（依赖：js/siteConfig.js 已存在）
python "$SKILL_DIR/scripts/gen-html.py" .
```

生成后验证：
```bash
# 检查 SEO description 是否与 siteConfig 一致
node -e "var c=require('fs').readFileSync('js/siteConfig.js','utf-8').replace(/const siteConfig/,'var siteConfig');eval(c);console.log('expected:',siteConfig.footer.description)"
grep -o 'meta name="description"[^>]*' index.html | head -1
# 两者的 content 值应完全一致
```

**备选方案**：AI 从零生成每个 HTML 页面（创造性更强，但需要更仔细地验证 meta 标签内容）。如果用此方案，必须在 Step 5 增加内容一致性验证。

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
- `references/full-validation-and-stale-topic.md` - **全量验收与旧主题残留回归检查**（HTTP 200 不等于内容正确）

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

### 📋 数据模板速查

**wordData.js 硬性约束**：
| 字段 | 类型 | 最小长度 | 最大长度 |
|------|------|---------|---------|
| root | string | 2 字 | 30 字 |
| meaning | string | 5 字 | 50 字 |
| description | string | 150 字 | 500 字 |
| examples | array | 3 个 | 5 个 |
| quiz.options | array | 恰好 4 个 | — |
| quiz.correctAnswer | number | 0 | 3 |

**siteConfig.js 硬性约束**：
| 字段 | 要求 |
|------|------|
| hero.title | 恰好 3 个字符串，每个 ≤12 字 |
| hero.subtitle | 15-40 字 |
| stats | 恰好 3 个对象 {value, label} |
| footer.tagline | ≤20 字 |
| footer.description | 80-200 字 |
| cta.primary | ≤15 字 |
| cta.secondary | ≤10 字 |

**HTML 必须使用的 CSS class**（来自 `templates/minimal.css`）：
`nav` `nav-container` `nav-brand` `nav-link` `hero` `hero-title` `hero-subtitle` `container` `stat-grid` `stat-card` `stat-value` `stat-label` `card` `btn` `btn-primary` `btn-large` `flashcard` `flashcard-inner` `flashcard-front` `flashcard-back` `quiz-option` `feedback-toast` `roots-grid` `root-card` `root-name` `root-meaning` `root-origin` `mastered-badge` `learn-container` `learn-nav` `progress-bar-bg` `progress-bar-fill` `search-bar` `filter-bar` `footer` `footer-tagline`

### 🛑 HTML 内容一致性强制检查

**主方案：使用 `scripts/gen-html.py` 从 siteConfig.js 动态生成所有 HTML**（见 Step 3）。此方案从源头消除语义残留，不需要后续 stale-topic 检查。

**备选方案：如果用 sed 替换或手动编辑 HTML**，必须在写入后跑以下检查：

```bash
# 将这些旧主题替换成你历史上生成过的站点关键词
# Maintain this list as new topics are generated — add each new topic after deploying
STALE_TOPICS="Git 命令|Python 装饰器|摄影构图|咖啡品鉴|词根词缀|时间管理|谈判|潜意识|认知偏差|博弈论|思维模型|行为经济学|谈判心理学"
if grep -R -E "$STALE_TOPICS" *.html manifest.json; then
  echo "❌ HTML/manifest 中存在旧主题残留，必须重新生成页面，不能部署"
  exit 1
fi

# 当前主题必须出现在全部 HTML 页面中
for page in index.html learn.html flashcard.html roots.html progress.html root-detail.html; do
  grep -q "$siteConfig.topic" "$page" || {
    echo "❌ $page 缺少当前主题关键词：$siteConfig.topic"
    exit 1
  }
done

# 语义级验证：逐字读 SEO description，确认与当前主题一致
desc_in_html=$(grep -o 'meta name="description"[^>]*' index.html | head -1)
echo "SEO description: $desc_in_html"
# 人工确认：描述内容是否与当前主题匹配？不是→必须重写 HTML
```

**验收标准**：HTTP 200 只代表站点能打开，不代表内容正确。必须通过 5 层验证：

| 层级 | 检查项 | 工具 |
|------|--------|------|
| 文件级 | 6 HTML + 3 JS + 2 icons + PWA + SEO 文件存在 | `ls` |
| 语法级 | wordData / siteConfig / manifest 语法正确 | `node -c` / `python -m json.tool` |
| 内容级 | topic 出现在所有 HTML，stale 关键词 = 0 | `grep` |
| 语义级 | SEO description 内容与当前主题一致 | 人工逐字读 `meta name="description"` |
| 运行时级 | Hermes skills list 显示 enabled | `hermes skills list` |

---

### Step 4: 创建项目结构

```bash
# 项目位置（跨平台）
BASE_DIR="${KNOWLEDGE_SITE_OUTPUT_DIR:-$HOME/hermes-generated-sites}"
projectName="${topic}-workshop"
mkdir -p "$BASE_DIR/$projectName"
cd "$BASE_DIR/$projectName"

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
python << 'PYEOF'
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
const vm = require('vm');

// 读取数据文件并执行（使用 vm 模块解决 eval 中 const 作用域问题）
let dataContent = fs.readFileSync('js/wordData.js', 'utf-8');
// 浏览器环境用 eval 直接可用；Node.js 中 const 在 eval 有作用域隔离，需替换为 var
dataContent = dataContent.replace(/const\s+WordRoots\s*=/, 'var WordRoots =');
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
let configContent = fs.readFileSync('js/siteConfig.js', 'utf-8');
configContent = configContent.replace(/const\s+siteConfig\s*=/, 'var siteConfig =');
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

# ========================================
# 阶段 4：gen-html.py 输出验证（如果使用了 gen-html.py）
# ========================================

echo "🔍 验证 gen-html.py 生成的 HTML..."

# 4.1 检查所有 HTML 文件存在
for page in index.html learn.html flashcard.html roots.html progress.html root-detail.html; do
  if [ ! -f "$page" ]; then
    echo "❌ 错误：$page 不存在（gen-html.py 未生成）"
    exit 1
  fi
done

# 4.2 验证 SEO description 与 siteConfig 一致
EXPECTED_DESC=$(node -e "var c=require('fs').readFileSync('js/siteConfig.js','utf-8').replace(/const siteConfig/,'var siteConfig');eval(c);console.log(siteConfig.footer.description)")
ACTUAL_DESC=$(grep -o 'content="[^"]*"' index.html | head -2 | tail -1 | sed 's/content="//;s/"$//')
if [ "$EXPECTED_DESC" != "$ACTUAL_DESC" ]; then
  echo "❌ 错误：SEO description 与 siteConfig 不一致"
  echo "  期望: $EXPECTED_DESC"
  echo "  实际: $ACTUAL_DESC"
  exit 1
fi
echo "✓ SEO description 与 siteConfig 一致"

# 4.3 验证 topic 出现在所有 HTML 中
TOPIC=$(node -e "var c=require('fs').readFileSync('js/siteConfig.js','utf-8').replace(/const siteConfig/,'var siteConfig');eval(c);console.log(siteConfig.topic)")
for page in index.html learn.html flashcard.html roots.html progress.html root-detail.html; do
  if ! grep -q "$TOPIC" "$page"; then
    echo "❌ 错误：$page 缺少主题关键词：$TOPIC"
    exit 1
  fi
done
echo "✓ 主题关键词出现在所有 HTML 中"

echo ""
echo "✅ 所有验证通过！"
```

---

### Step 6: 部署（强制安全检查）

🔴 **CHECKPOINT 2（部署前 — 最关键）**：逐项验证（每一项不通过则 🛑 停止部署）：

```bash
# 1. 数据验证通过
node -e "var c=require('fs').readFileSync('js/wordData.js','utf-8').replace(/const WordRoots/,'var WordRoots');eval(c);console.log(WordRoots.length+' items OK')"
# 期望: "N items OK"（N>0）

# 2. 配置文件完整
node -e "var c=require('fs').readFileSync('js/siteConfig.js','utf-8').replace(/const siteConfig/,'var siteConfig');eval(c);console.log(siteConfig.topic,siteConfig.itemCount+' items')"
# 期望: "主题名 N items"

# 3. Vercel 已认证
vercel whoami
# 期望: 返回用户名（非 "No credentials"）

# 4. 输出目录正确
echo "BASE_DIR=$BASE_DIR"
echo "projectName=$projectName"
ls "$BASE_DIR/$projectName/index.html"
# 期望: 显示 index.html 路径
```

🛑 以上 4 项**任意一项失败 → 停止部署**，回到对应步骤修正。

---

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
ls -d $BASE_DIR/*-workshop 2>/dev/null | while read dir; do
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

for dir in $BASE_DIR/*-workshop; do
  if [ "$dir" = "$BASE_DIR/${projectName}" ]; then
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
cd $BASE_DIR
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

## 部署回滚流程

当部署后发现内容错误（如数据不完整、SEO 描述错误、主题残留）时：

```bash
# 1. 定位问题项目
cd "$BASE_DIR/$projectName"

# 2. 修复数据/配置
# 修改 js/wordData.js 或 js/siteConfig.js

# 3. 重新生成 HTML（使用 gen-html.py）
python "$SKILL_DIR/scripts/gen-html.py" .

# 4. 重新验证
node -e "var c=require('fs').readFileSync('js/wordData.js','utf-8').replace(/const WordRoots/,'var WordRoots');eval(c);console.log(WordRoots.length+' items')"
# stale-topic 检查
grep -rE "旧主题词" *.html manifest.json 2>/dev/null || echo "clean"

# 5. 重新部署
rm -rf .git .vercel; git init; git config user.name o; git config user.email o@o
echo .vercel>.gitignore; git add -A; git commit -qm "fix: re-deploy after content fix"
vercel --prod --yes

# 6. 验证修复
curl -s "$URL" | grep -o 'meta name="description"[^>]*'
```

**注意**：Vercel 的 `--prod` 部署会自动替换生产 URL，旧版本会被保留在预览 URL。不需要手动删除旧版本。

---

## 失败模式与修复方案

| 触发条件 | 一线修复（复制执行） | 仍失败则（复制执行） |
|---------|---------|---------|
| `vercel whoami` 报 "No credentials" | `vercel login` | `export VERCEL_TOKEN="<token>"` 并重试部署 |
| `python -c "import PIL"` 报 ModuleNotFoundError | `pip install pillow` | 用 SVG favicon 替代：`printf '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#FBBF24"/><text x="50" y="65" text-anchor="middle" font-size="40" fill="#1F2937">📚</text></svg>' > icon-192.png` 跳过 PIL |
| `jq --version` 返回 command not found | Win: `winget install jqlang.jq`; Mac: `brew install jq`; Linux: `sudo apt install jq -y` | 用 `python -c "import json;print(json.load(open('.vercel/project.json'))['projectId'])"` 替代 jq 操作 |
| `node -e "eval(fs.readFileSync('js/wordData.js','utf-8'))"` 报 ReferenceError | 改用 `const`→`var` 替换：`node -e "var fs=require('fs');var c=fs.readFileSync('js/wordData.js','utf-8').replace(/const WordRoots/,'var WordRoots');eval(c);console.log(WordRoots.length)"` | `node -e "console.log(JSON.stringify(require('fs').readFileSync('js/wordData.js','utf-8').match(/id:\s*(\d+)/g)))"` 正则提取 id 列表 |
| `.vercel/project.json` 的 projectId 和其他项目冲突 | `cd $BASE_DIR/旧项目 && vercel --prod --yes` | `vercel ls \| grep -v "projectId"` 列出全部项目，逐个重部署 |
| `git commit` 报 "Author identity unknown" | `git config user.name "temp"; git config user.email "temp@local"` | `GIT_AUTHOR_NAME="temp" GIT_AUTHOR_EMAIL="temp@local" GIT_COMMITTER_NAME="temp" GIT_COMMITTER_EMAIL="temp@local" git commit -m "..."` |
| 浏览器 SW 缓存旧版本 | 递增 `sw.js` 顶部 `CACHE_VERSION` 从 `'v1'` 到 `'v2'` | 手动清除：Chrome DevTools → Application → Clear storage → Clear site data |
| Pillow 字体 `truetype()` 报 OSError | Python 中 catch 后 `font = ImageFont.load_default()` | `printf '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" fill="#FBBF24"/><text x="256" y="320" text-anchor="middle" font-size="120" fill="#1F2937">$TEXT</text></svg>' > icon-512.png` |
| Vercel 部署超时 (>2min) | `export HTTP_PROXY=http://127.0.0.1:15556 HTTPS_PROXY=http://127.0.0.1:15556` | `vercel --prod --yes` 重试，最多 3 次；仍失败用 `vercel deploy --prebuilt --prod` |
| `mkdir "$BASE_DIR/$projectName"` 报 Permission denied | `mkdir -p "$HOME/hermes-generated-sites/$projectName"` 回退到默认路径 | 检查磁盘空间：`df -h "$HOME"` |
| `curl -s "$URL"` 返回 000 | 代理未设置：`export HTTP_PROXY=http://127.0.0.1:15556 HTTPS_PROXY=http://127.0.0.1:15556` | `curl --noproxy '*' -s "$URL"` 跳过代理直连 |
| bash heredoc 写 wordData.js 后 Node.js 报 `SyntaxError: Unexpected string` | MSYS 编码问题，用 `write_file` 工具替代 bash heredoc 重写文件 | 详见 `references/heredoc-encoding-pitfalls.md` |

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
- [ ] 3. **生成配置** - 创建 siteConfig.js（AI创作首页文案）
- [ ] 4. **生成页面** - 运行 `python "$SKILL_DIR/scripts/gen-html.py" .` 从 siteConfig 动态生成 6 个 HTML + manifest.json
- [ ] 5. **创建项目** - mkdir + 写入所有文件
- [ ] 6. **验证数据** - 检查数据和配置文件完整性（含 Step 5 阶段 4 gen-html.py 输出验证）
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

## 反例与常见错误

⚠️ 以下是在使用本 skill 时**必须避免**的错误：

| # | ❌ 反模式 | ✅ 正确做法 |
|---|----------|-----------|
| 1 | `cp -r` 复制旧项目当模板 | AI 从零生成，参考设计系统不复用代码 |
| 2 | 使用 `sed` 粗暴替换文案 | AI 理解主题后创作原创文案 |
| 3 | 硬编码特定领域内容（如"词根词缀"） | 所有文案从 `siteConfig` 和 `WordRoots` 动态读取 |
| 4 | innerHTML 直接插入未转义数据 | 优先 `textContent` / `createElement`，必要时 `escapeHtml()` |
| 5 | 忽略数据验证直接部署 | Step 5 强制验证后才能进 Step 6 |
| 6 | 多个项目共享同一 GitHub 仓库 | 部署前移除 `git remote`，独立 `vercel --prod --yes` |
| 7 | LocalStorage 操作无 try-catch | 所有 `getItem`/`setItem` 包裹错误处理 + 默认值 |
| 8 | DOM 操作前不检查元素存在 | 使用 `if (element)` 或 `?.` 可选链 |
| 9 | 跳过 Step 5 数据验证 | 数据不完整会导致页面渲染空白/崩溃 |
| 10 | 部署后不验证 URL 可访问 | 用 `curl` 检查 HTTP 200 + projectId 唯一性 |
| 11 | 忽略 🔴 CHECKPOINT 标记继续执行 | 每个 CHECKPOINT 的验证命令复制执行，🛑 出现立即停 |
| 12 | 失败表中写了修复方案但 AI 自己"脑补"别的 | 严格复制失败表中的一线修复命令，不自己发明方案 |
| 13 | 部署前忘记 `vercel whoami` 确认登录 | CHECKPOINT 2 第 3 步强制执行 |
| 14 | 没设 `HTTP_PROXY` 导致 Vercel `curl` 000 | 开始前在 CHECKPOINT 0 一起设置代理环境变量 |
| 15 | 生成 HTML 不使用 `templates/minimal.css` 的 class | 对照数据模板速查中的 31 个 CSS class 清单逐一检查 |
| 16 | 知识点数量 <10 或 >100 导致内容过少/加载慢 | 默认 20-30 个，简单主题 10-15 个，大主题上限 50 个 |
| 17 | Windows Git Bash 中文主机名导致 Vercel CLI 报错 | 不直接用 `vercel login`，改用 `export VERCEL_TOKEN` 环境变量 |
| 18 | 只验证 HTTP 200，不检查页面内容是否是当前主题 | 增加 stale-topic 检查：旧主题关键词不得出现在 HTML/manifest 中 |
| 19 | 用 bash heredoc 写含中文的 JS 数据 | heredoc 中文 JS 会损坏编码。用 `write_file` 工具或 Python `open().write()` 替代 |
| 20 | stale-topic 检查范围包含 siteConfig.js | siteConfig 里天然包含主题词，只检查 `*.html` 和 `manifest.json` |
| 21 | 不用 gen-html.py 生成 HTML，手动 sed 替换 | 运行 `python "$SKILL_DIR/scripts/gen-html.py" .` 从 siteConfig 动态生成，从源头消除语义残留 |
| 22 | gen-html.py 生成后不验证 SEO description | Step 5 阶段 4 强制检查 description 与 siteConfig 一致 |

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
cd $BASE_DIR/旧项目名称

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

> **历史事故复盘**见 `references/vercel-deployment-incident.md`（2026-02-25 共享 GitHub 仓库导致站点覆盖事故的完整记录）。gen-html.py 已从源头消除此问题的根因。

---

## 批量更新机制 🔄

当 skill 的设计系统有更新时，需要同步到所有已部署站点：

- **CSS 更新**：`bash scripts/update-css.sh --dry-run` 预览，`bash scripts/update-css.sh` 执行
- **HTML 重新生成**：对每个已部署项目运行 `python "$SKILL_DIR/scripts/gen-html.py" "$dir"` 后 `vercel --prod --yes`

完整文档见 `references/batch-update-mechanism.md`（含工作流程、安全特性、扩展性）。
