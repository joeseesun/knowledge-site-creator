# Knowledge Site Creator

> 一句话生成任何领域的知识学习网站 - AI 理解主题，自动创作内容，生成页面，一键部署

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude-Code-7C3AED)](https://www.anthropic.com)

## ✨ 特性

- 🤖 **AI 全自动创作**：理解主题 → 生成数据 → 创作文案 → 部署上线
- 📚 **通用学习模式**：闪卡、渐进学习、测试、索引、进度追踪
- 🎨 **极简设计系统**：黄色主题、Inter 字体、响应式布局
- 📱 **PWA 支持**：自动生成图标、离线访问、可安装
- 🔍 **SEO 优化**：完整 meta 标签、sitemap、结构化数据
- ✅ **代码质量**：XSS 防护、错误处理、DOM 安全
- 🚀 **零模板依赖**：AI 参考设计系统从零生成页面

## 🎯 适用领域

适用于任何需要系统学习的知识领域：

- 📖 学科知识：进化心理学、量子力学、中医经络
- 💻 技术术语：大模型术语、编程概念、设计原则
- 🏛️ 历史文化：五代十国、唐诗宋词、世界历史
- 🔬 科学概念：化学元素、物理定律、生物分类
- 🎨 设计美学：CRAP 原则、配色理论、版式设计

## 🚀 快速开始

### 前置要求

- Claude Code CLI
- Node.js 18+
- Vercel CLI（可选，用于部署）

### 安装

#### 方法一：使用 npx skills（推荐）

```bash
# 自动安装到 Claude Code
npx skills add joeseesun/knowledge-site-creator
```

#### 方法二：手动安装

```bash
# 克隆仓库
git clone https://github.com/joeseesun/knowledge-site-creator.git

# 复制到 Claude Code skills 目录
cp -r knowledge-site-creator ~/.claude/skills/
```

#### 方法三：直接复制（如果已有本地副本）

```bash
cp -r /path/to/knowledge-site-creator ~/.claude/skills/
```

### 使用

在 Claude Code 中直接说：

```
生成一个进化心理学学习网站
```

或者：

```
创建量子力学基础概念网站
```

AI 会自动：
1. 分析主题特点和价值
2. 生成 20-30 个核心知识点数据
3. 创作首页文案、统计、介绍
4. 参考设计系统生成页面
5. 部署到 Vercel
6. 返回访问链接

## 📂 项目结构

```
knowledge-site-creator/
├── SKILL.md                    # 主 Skill 文件（AI 执行流程）
├── README.md                   # 本文件
├── references/                 # 设计规范和模式参考
│   ├── core-patterns.md       # 核心学习模式（闪卡、测试等）
│   ├── design-system.md       # 设计系统（配色、字体、间距）
│   ├── code-quality.md        # 代码质量标准
│   ├── pwa-setup.md           # PWA 配置指南
│   └── seo-best-practices.md  # SEO 优化最佳实践
└── scripts/                    # 辅助脚本
    └── update-css.sh          # CSS 更新脚本
```

## 🎨 设计系统

### 配色方案

- **主题色**：`#FBBF24`（黄色）
- **成功色**：`#10B981`（绿色）
- **错误色**：`#EF4444`（红色）
- **文字色**：`#1F2937`（深灰）
- **背景色**：`#FFFFFF`（白色）

### 核心学习模式

1. **闪卡（Flashcard）**：卡片翻转、键盘控制（←→空格）、进度显示
2. **学习（Learn）**：渐进式展示、上下翻页、自动保存进度
3. **测试（Quiz）**：4 选 1 测试题、Toast 反馈、答案解析
4. **索引（Index）**：搜索筛选、卡片网格、已掌握标记
5. **进度（Progress）**：学习统计、已掌握列表、进度条

## 📊 示例网站

- [五代十国历史工坊](https://five-dynasties-workshop.vercel.app) - 30 个历史知识点
- [大模型术语学习工坊](https://llm-terms-workshop.vercel.app) - 30 个 AI 术语（示例）

## 🛠️ 技术栈

- **前端**：原生 HTML/CSS/JavaScript（零依赖）
- **样式**：CSS 变量 + 8px 网格系统
- **存储**：LocalStorage（进度管理）
- **PWA**：manifest.json + Service Worker
- **部署**：Vercel（一键部署）
- **AI**：Claude Code（内容创作）

## 📝 核心原则

1. **设计系统优先**：复用设计语言，不复用具体页面代码
2. **AI 创作内容**：所有文案、统计、介绍都由 AI 根据主题创作
3. **零模板依赖**：AI 参考设计系统从零生成页面
4. **代码质量**：XSS 防护、错误处理、DOM 安全
5. **用户体验**：Toast 反馈、键盘快捷键、响应式设计

## 🔧 高级配置

### 自定义主题色

编辑生成的 `css/minimal.css`：

```css
:root {
  --color-primary: #FBBF24;  /* 改成你想要的颜色 */
}
```

### 修改知识点数量

在生成时明确告诉 AI：

```
生成一个进化心理学网站，包含 50 个核心概念
```

### 自定义数据结构

编辑生成的 `js/wordData.js`，按照固定格式添加知识点。

## 🤝 贡献

欢迎贡献代码、报告 Bug、提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 License

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**向阳乔木（Joe）**

- X (Twitter): [@vista8](https://x.com/vista8)
- 微信公众号：「向阳乔木推荐看」
- GitHub: [@joeseesun](https://github.com/joeseesun)

<p align="center">
  <img src="https://github.com/joeseesun/terminal-boost/raw/main/assets/wechat-qr.jpg?raw=true" alt="向阳乔木推荐看公众号二维码" width="200">
</p>

---

如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！
