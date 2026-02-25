# SEO 最佳实践 - 知识网站优化指南

> 让知识网站被搜索引擎收录，提升自然流量

## 核心原则

1. **语义化 HTML** - 正确使用标签（h1, h2, article, section）
2. **元数据完整** - Title, Description, Keywords, OG标签
3. **结构化数据** - Schema.org 标记（JSON-LD）
4. **内容优化** - 清晰的标题层级，关键词密度
5. **性能优化** - 快速加载（已有PWA缓存）
6. **移动友好** - 响应式设计（已有）

---

## 1. 基础元数据（所有页面）

### 1.1 通用 Meta 标签

```html
<head>
  <!-- 基础 SEO -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${pageTitle} - ${siteConfig.siteName}</title>
  <meta name="description" content="${pageDescription}">
  <meta name="keywords" content="${siteConfig.topic}, 学习, 教育, ${siteConfig.itemName}">
  <meta name="author" content="${siteConfig.author || '向阳乔木'}">

  <!-- 语言和地区 -->
  <meta name="language" content="zh-CN">
  <link rel="canonical" href="${currentPageUrl}">

  <!-- 搜索引擎指令 -->
  <meta name="robots" content="index, follow">
  <meta name="googlebot" content="index, follow">
  <meta name="bingbot" content="index, follow">
</head>
```

### 1.2 Open Graph（社交媒体分享）

```html
<!-- Open Graph (Facebook, LinkedIn) -->
<meta property="og:type" content="website">
<meta property="og:url" content="${currentPageUrl}">
<meta property="og:title" content="${pageTitle} - ${siteConfig.siteName}">
<meta property="og:description" content="${pageDescription}">
<meta property="og:image" content="${siteConfig.ogImage || '/icon-512.png'}">
<meta property="og:locale" content="zh_CN">
<meta property="og:site_name" content="${siteConfig.siteName}">
```

### 1.3 Twitter Card

```html
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="${siteConfig.twitterHandle || '@vista8'}">
<meta name="twitter:creator" content="${siteConfig.twitterHandle || '@vista8'}">
<meta name="twitter:title" content="${pageTitle} - ${siteConfig.siteName}">
<meta name="twitter:description" content="${pageDescription}">
<meta name="twitter:image" content="${siteConfig.twitterImage || '/icon-512.png'}">
```

---

## 2. 结构化数据（Schema.org）

### 2.1 网站信息（首页 - index.html）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "${siteConfig.siteName}",
  "description": "${siteConfig.footer.description}",
  "url": "${siteBaseUrl}",
  "author": {
    "@type": "Person",
    "name": "${siteConfig.author || '向阳乔木'}",
    "url": "https://x.com/vista8"
  },
  "inLanguage": "zh-CN",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "${siteBaseUrl}/roots.html?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
```

### 2.2 教育课程（首页 - index.html）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "${siteConfig.siteName}",
  "description": "${siteConfig.footer.description}",
  "provider": {
    "@type": "Organization",
    "name": "${siteConfig.author || '向阳乔木'}",
    "url": "https://x.com/vista8"
  },
  "educationalLevel": "Beginner",
  "inLanguage": "zh-CN",
  "numberOfLessons": ${siteConfig.itemCount},
  "coursePrerequisites": "无",
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseWorkload": "PT15M"
  }
}
</script>
```

### 2.3 知识点详情（root-detail.html）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${root.root}",
  "description": "${root.meaning}",
  "articleBody": "${root.description}",
  "author": {
    "@type": "Person",
    "name": "${siteConfig.author || '向阳乔木'}"
  },
  "datePublished": "${siteConfig.publishDate || new Date().toISOString()}",
  "dateModified": "${new Date().toISOString()}",
  "inLanguage": "zh-CN",
  "educationalUse": "学习",
  "typicalAgeRange": "16-"
}
</script>
```

### 2.4 面包屑导航（适用于详情页）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "${siteBaseUrl}"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "${siteConfig.itemName}索引",
      "item": "${siteBaseUrl}/roots.html"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "${root.root}",
      "item": "${siteBaseUrl}/root-detail.html?id=${root.id}"
    }
  ]
}
</script>
```

---

## 3. 语义化 HTML 结构

### 3.1 首页结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <!-- Meta 标签 -->
</head>
<body>
  <!-- Header -->
  <header role="banner">
    <nav role="navigation" aria-label="主导航">
      <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/learn.html">学习</a></li>
        <li><a href="/roots.html">索引</a></li>
      </ul>
    </nav>
  </header>

  <!-- Hero 区域 -->
  <main role="main">
    <section class="hero" aria-label="网站介绍">
      <h1>${siteConfig.hero.title.join(' ')}</h1>
      <p class="subtitle">${siteConfig.hero.subtitle}</p>
    </section>

    <!-- 统计卡片 -->
    <section class="stats" aria-label="网站统计">
      <div class="stat-card">
        <h2 class="stat-value">${stats[0].value}</h2>
        <p class="stat-label">${stats[0].label}</p>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer role="contentinfo">
    <p>${siteConfig.footer.tagline}</p>
    <p>${siteConfig.footer.description}</p>
  </footer>
</body>
</html>
```

### 3.2 详情页结构

```html
<main role="main">
  <article itemscope itemtype="https://schema.org/Article">
    <header>
      <h1 itemprop="headline">${root.root}</h1>
      <p itemprop="description">${root.meaning}</p>
    </header>

    <section itemprop="articleBody">
      <h2>详细说明</h2>
      <p>${root.description}</p>
    </section>

    <section>
      <h2>应用例子</h2>
      <ul>
        ${root.examples.map(ex => `<li>${ex.word}: ${ex.meaning}</li>`).join('')}
      </ul>
    </section>

    <section>
      <h2>小测验</h2>
      <div role="group" aria-label="选择题">
        <p>${root.quiz.question}</p>
        <!-- 选项 -->
      </div>
    </section>
  </article>
</main>
```

---

## 4. sitemap.xml（动态生成）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- 首页 -->
  <url>
    <loc>${siteBaseUrl}/</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- 功能页面 -->
  <url>
    <loc>${siteBaseUrl}/learn.html</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <url>
    <loc>${siteBaseUrl}/flashcard.html</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <url>
    <loc>${siteBaseUrl}/roots.html</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>

  <url>
    <loc>${siteBaseUrl}/progress.html</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>

  <!-- 所有知识点详情页 -->
  ${WordRoots.map(root => `
  <url>
    <loc>${siteBaseUrl}/root-detail.html?id=${root.id}</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  `).join('')}
</urlset>
```

### 生成 sitemap.xml 的脚本

```javascript
// js/generate-sitemap.js
const fs = require('fs');

// 从 wordData.js 导入数据（如果在 Node.js 环境）
const WordRoots = [...]; // 或者 require('./wordData.js')
const siteConfig = require('./siteConfig.js');

const siteBaseUrl = 'https://your-site.vercel.app'; // 实际部署后的 URL

const staticPages = [
  { url: '/', priority: '1.0', changefreq: 'daily' },
  { url: '/learn.html', priority: '0.8', changefreq: 'weekly' },
  { url: '/flashcard.html', priority: '0.8', changefreq: 'weekly' },
  { url: '/roots.html', priority: '0.9', changefreq: 'daily' },
  { url: '/progress.html', priority: '0.7', changefreq: 'weekly' },
];

const dynamicPages = WordRoots.map(root => ({
  url: `/root-detail.html?id=${root.id}`,
  priority: '0.6',
  changefreq: 'monthly'
}));

const allPages = [...staticPages, ...dynamicPages];
const lastmod = new Date().toISOString().split('T')[0];

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages.map(page => `  <url>
    <loc>${siteBaseUrl}${page.url}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

fs.writeFileSync('sitemap.xml', sitemap);
console.log('✓ sitemap.xml generated');
```

---

## 5. robots.txt

```txt
# robots.txt
User-agent: *
Allow: /

# Sitemap 位置
Sitemap: ${siteBaseUrl}/sitemap.xml

# 禁止抓取（可选）
Disallow: /js/
Disallow: /css/

# 爬虫速率限制（可选）
Crawl-delay: 1
```

---

## 6. 页面特定优化

### 6.1 首页（index.html）

**Title**: `${siteConfig.siteName} - ${siteConfig.itemCount}个核心${siteConfig.itemName}系统学习`

**Description**: `${siteConfig.footer.description}（140-160字符）`

**H1**: `${siteConfig.hero.title.join(' ')}`（只用一次）

**关键词密度**:
- 主关键词（${siteConfig.topic}）出现 3-5 次
- 次关键词（学习、${siteConfig.itemName}）出现 2-3 次

### 6.2 学习页（learn.html）

**Title**: `渐进学习 - ${siteConfig.siteName}`

**Description**: `系统学习${siteConfig.itemCount}个${siteConfig.itemName}，从基础到进阶，一次一个概念，轻松掌握${siteConfig.topic}核心知识。`

### 6.3 索引页（roots.html）

**Title**: `${siteConfig.itemName}索引 - ${siteConfig.siteName}`

**Description**: `浏览所有${siteConfig.itemCount}个${siteConfig.itemName}，支持搜索和分类筛选，快速找到你需要的${siteConfig.topic}知识点。`

### 6.4 详情页（root-detail.html）

**Title**: `${root.root} - ${root.meaning} | ${siteConfig.siteName}`

**Description**: `深入学习${root.root}：${root.description.substring(0, 120)}...`

**H1**: `${root.root}`

**内容优化**:
- 使用 `<h2>` 分段（详细说明、应用例子、小测验）
- 关键词密度 2-3%
- 内容长度 500+ 字

---

## 7. 性能优化（SEO 相关）

### 7.1 图片优化

```html
<!-- 使用现代图片格式 + 懒加载 -->
<img
  src="/images/example.webp"
  alt="描述性文字（包含关键词）"
  loading="lazy"
  width="800"
  height="600"
>
```

### 7.2 关键资源预加载

```html
<head>
  <!-- 预加载关键资源 -->
  <link rel="preload" href="/css/minimal.css" as="style">
  <link rel="preload" href="/js/wordData.js" as="script">

  <!-- DNS 预解析（如果有外部资源）-->
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
</head>
```

### 7.3 Service Worker 缓存策略

已在 `pwa-setup.md` 中实现：
- 静态资源缓存优先
- 首次加载 < 3 秒
- Lighthouse Performance > 90

---

## 8. 提交到搜索引擎

### 8.1 Google Search Console

1. 访问 https://search.google.com/search-console
2. 添加资源（域名或 URL 前缀）
3. 验证所有权（DNS 或 HTML 文件）
4. 提交 sitemap.xml
5. 请求索引（首次）

### 8.2 Bing Webmaster Tools

1. 访问 https://www.bing.com/webmasters
2. 添加站点
3. 验证所有权
4. 提交 sitemap.xml

### 8.3 百度站长平台

1. 访问 https://ziyuan.baidu.com
2. 添加网站
3. 验证网站
4. 提交 sitemap
5. 主动推送（可选）

---

## 9. SEO 检查清单 ✅

部署后检查：

### 基础 SEO
- [ ] 每个页面有唯一的 `<title>`（50-60字符）
- [ ] 每个页面有 `<meta name="description">`（140-160字符）
- [ ] H1 标签只用一次，包含主关键词
- [ ] 语义化 HTML（header, main, footer, article, section）
- [ ] 所有图片有 alt 属性
- [ ] 内部链接正确（相对路径）

### 技术 SEO
- [ ] robots.txt 存在且正确
- [ ] sitemap.xml 存在且包含所有页面
- [ ] 所有页面响应式（移动友好）
- [ ] HTTPS 启用（Vercel 自动）
- [ ] 页面加载速度 < 3 秒
- [ ] 没有 404 错误

### 结构化数据
- [ ] 首页有 WebSite schema
- [ ] 首页有 Course schema
- [ ] 详情页有 Article schema
- [ ] 详情页有 BreadcrumbList schema

### 社交媒体
- [ ] Open Graph 标签完整
- [ ] Twitter Card 标签完整
- [ ] 分享图片（og:image）存在且美观

### 提交
- [ ] 提交到 Google Search Console
- [ ] 提交到 Bing Webmaster Tools
- [ ] 提交到百度站长平台（可选）

---

## 10. 常见问题

### Q1: 页面不被索引？

**检查清单**：
1. `robots.txt` 是否允许抓取
2. sitemap.xml 是否提交
3. 是否有 `<meta name="robots" content="noindex">`（移除）
4. 内容是否原创且有价值（避免重复内容）

### Q2: 排名不高？

**优化方向**：
1. **内容质量**：增加深度、原创性、实用性
2. **关键词优化**：标题、描述、H1/H2 包含目标关键词
3. **外部链接**：在其他网站（如公众号文章）添加链接
4. **用户体验**：降低跳出率，增加停留时间

### Q3: 如何提升 Lighthouse SEO 分数？

**关键因素**：
- ✅ 文档有 `<title>`
- ✅ 文档有 `<meta name="description">`
- ✅ 链接有可访问的名称（text 或 aria-label）
- ✅ 图片有 alt 属性
- ✅ 文档有 `<meta name="viewport">`
- ✅ 移动端字体大小 >= 12px

---

## Linus 视角：SEO 的工程化

> "SEO 不是魔法，而是工程。好的 SEO 来自于好的网站架构、清晰的内容结构、快速的加载速度。那些试图'欺骗'搜索引擎的做法都是垃圾。"

**核心原则**：
- ✅ **内容为王**：高质量内容自然排名高
- ✅ **技术基础**：快速、安全、可访问
- ✅ **语义化**：让搜索引擎理解你的内容
- ❌ **不要耍小聪明**：关键词堆砌、隐藏文本、购买链接

**SEO = 用户体验**：
- 用户喜欢的，搜索引擎也喜欢
- 快速加载、清晰导航、移动友好
- 好内容会自然获得外部链接
