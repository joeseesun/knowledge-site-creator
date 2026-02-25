# PWA（Progressive Web App）配置指南

> 让知识学习网站支持离线访问和安装到主屏幕

## PWA 核心特性

1. **Service Worker**：缓存静态资源，支持离线访问
2. **Web App Manifest**：定义 app 元数据（图标、名称、颜色）
3. **HTTPS**：PWA 必需（Vercel 自动提供）
4. **响应式设计**：已有（viewport meta）

---

## 1. Web App Manifest

### manifest.json

放置在项目根目录：

```json
{
  "name": "${siteConfig.siteName}",
  "short_name": "${siteConfig.itemName}学习",
  "description": "${siteConfig.footer.description}",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FFFFFF",
  "theme_color": "#FBBF24",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["education", "productivity"],
  "lang": "zh-CN"
}
```

### 字段说明

| 字段 | 说明 | 值 |
|------|------|-----|
| `name` | 完整名称 | `${siteConfig.siteName}` |
| `short_name` | 主屏幕显示的短名称 | `${siteConfig.itemName}学习` |
| `start_url` | 启动 URL | `/` |
| `display` | 显示模式 | `standalone`（全屏，无浏览器 UI）|
| `background_color` | 启动画面背景色 | `#FFFFFF` |
| `theme_color` | 主题色（地址栏） | `#FBBF24`（黄色）|

---

## 2. Service Worker

### sw.js

放置在项目根目录：

```javascript
// Service Worker 版本（每次修改内容时更新）
const CACHE_VERSION = 'v1';
const CACHE_NAME = `${siteConfig.topic}-${CACHE_VERSION}`;

// 需要缓存的静态资源
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/learn.html',
  '/flashcard.html',
  '/roots.html',
  '/progress.html',
  '/root-detail.html',
  '/css/minimal.css',
  '/js/wordData.js',
  '/js/siteConfig.js',
  '/js/storage.js',
  '/manifest.json'
];

// 安装事件：缓存静态资源
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Service Worker...');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        // 强制激活新的 Service Worker
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Cache failed:', error);
      })
  );
});

// 激活事件：清理旧缓存
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        // 立即接管所有页面
        return self.clients.claim();
      })
  );
});

// 拦截请求：缓存优先策略
self.addEventListener('fetch', (event) => {
  // 只处理 GET 请求
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // 如果缓存存在，直接返回
        if (cachedResponse) {
          console.log('[SW] Serving from cache:', event.request.url);
          return cachedResponse;
        }

        // 缓存不存在，发起网络请求
        console.log('[SW] Fetching from network:', event.request.url);
        return fetch(event.request)
          .then((networkResponse) => {
            // 如果是静态资源，缓存一份
            if (event.request.url.includes(self.location.origin)) {
              const responseClone = networkResponse.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(event.request, responseClone);
                });
            }
            return networkResponse;
          })
          .catch((error) => {
            console.error('[SW] Fetch failed:', error);
            // 返回离线页面（可选）
            return new Response('Offline - Please check your connection', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
      })
  );
});

// 消息事件：支持手动更新缓存
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});
```

### 缓存策略说明

**Cache First（缓存优先）**：
1. 先查缓存
2. 有缓存 → 直接返回（快！）
3. 无缓存 → 网络请求 → 缓存一份 → 返回

**适用场景**：静态资源（HTML、CSS、JS、图片）

---

## 3. 注册 Service Worker

### 在所有 HTML 页面的 `<head>` 中添加

```html
<!-- PWA Manifest -->
<link rel="manifest" href="/manifest.json">

<!-- iOS Safari 支持 -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="${siteConfig.short_name}">
<link rel="apple-touch-icon" href="/icon-192.png">

<!-- 主题色 -->
<meta name="theme-color" content="#FBBF24">
```

### 在所有 HTML 页面的 `</body>` 前添加

```html
<script>
  // 注册 Service Worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('SW registered:', registration.scope);

          // 监听更新
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // 有新版本，提示用户刷新
                console.log('New version available! Refresh to update.');
                // 可选：显示更新提示
                showUpdateNotification();
              }
            });
          });
        })
        .catch((error) => {
          console.error('SW registration failed:', error);
        });
    });
  }

  // 显示更新提示（可选）
  function showUpdateNotification() {
    const banner = document.createElement('div');
    banner.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #FBBF24;
      color: #000;
      padding: 12px 24px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      z-index: 9999;
      font-size: 14px;
      cursor: pointer;
    `;
    banner.textContent = '发现新版本，点击更新';
    banner.onclick = () => {
      window.location.reload();
    };
    document.body.appendChild(banner);

    // 10秒后自动隐藏
    setTimeout(() => {
      banner.remove();
    }, 10000);
  }
</script>
```

---

## 4. 生成图标

### 图标规格

PWA 需要两个尺寸的图标：
- `icon-192.png`（192x192）
- `icon-512.png`（512x512）

### 简单方案：使用 Emoji 作为图标

```bash
# 创建 icon 生成脚本
cat > generate-icons.sh << 'EOF'
#!/bin/bash

# 使用 ImageMagick 从 emoji 生成图标
convert -background "#FBBF24" -fill white -font "Arial-Unicode-MS" \
  -size 192x192 -gravity center label:"📚" icon-192.png

convert -background "#FBBF24" -fill white -font "Arial-Unicode-MS" \
  -size 512x512 -gravity center label:"📚" icon-512.png

echo "✓ Icons generated"
EOF

chmod +x generate-icons.sh
./generate-icons.sh
```

### 或使用在线工具

- **PWA Asset Generator**: https://www.pwabuilder.com/imageGenerator
- 上传一张正方形图片（至少 512x512）
- 自动生成所有需要的尺寸

---

## 5. 测试 PWA

### Chrome DevTools

1. 打开 Chrome DevTools（F12）
2. 切换到 **Application** 标签
3. 检查：
   - **Manifest**：查看 manifest.json 是否正确加载
   - **Service Workers**：查看 SW 是否注册成功
   - **Cache Storage**：查看缓存的资源

### Lighthouse

1. DevTools → **Lighthouse** 标签
2. 选择 **Progressive Web App** 类别
3. 点击 **Generate report**
4. 目标分数：**90+ / 100**

### 手机测试

**Android Chrome**：
1. 访问网站
2. 点击右上角菜单 → "安装应用"
3. 安装到主屏幕

**iOS Safari**：
1. 访问网站
2. 点击分享按钮 → "添加到主屏幕"
3. 图标会出现在主屏幕

---

## 6. 常见问题

### Q1: Service Worker 不更新？

**解决方案**：
```javascript
// 强制更新 Service Worker
navigator.serviceWorker.getRegistration().then((registration) => {
  registration.update();
});

// 或者直接跳过等待
navigator.serviceWorker.addEventListener('controllerchange', () => {
  window.location.reload();
});
```

### Q2: iOS 不显示"添加到主屏幕"？

**检查清单**：
- ✅ 必须使用 HTTPS（Vercel 自动提供）
- ✅ 必须有 `apple-touch-icon`
- ✅ 必须有 `<meta name="apple-mobile-web-app-capable">`
- ✅ 网站必须被用户访问至少 30 秒

### Q3: 缓存太多，如何清理？

**用户端清理**：
1. Chrome：设置 → 隐私和安全 → 清除浏览数据 → 缓存
2. Safari：设置 → Safari → 清除历史记录和网站数据

**开发者清理**：
```javascript
// 清除所有缓存
caches.keys().then((cacheNames) => {
  return Promise.all(
    cacheNames.map((cacheName) => caches.delete(cacheName))
  );
});
```

---

## 7. PWA 最佳实践

### ✅ 必须做

1. **HTTPS**：PWA 强制要求（Vercel 自动提供）
2. **响应式设计**：适配所有设备（已有）
3. **快速加载**：首屏加载 < 3 秒（Service Worker 缓存）
4. **离线可用**：至少首页可离线访问

### ⚠️ 建议做

1. **更新提示**：检测到新版本时提示用户刷新
2. **骨架屏**：加载时显示内容骨架（而不是空白）
3. **懒加载**：图片和非首屏内容懒加载

### ❌ 不要做

1. **不要缓存用户数据**：LocalStorage 中的进度数据不应通过 SW 缓存
2. **不要缓存 API 请求**：动态数据应该实时获取
3. **不要忘记更新版本号**：修改内容后必须更新 `CACHE_VERSION`

---

## 8. Vercel 部署配置

### vercel.json 添加 PWA 支持

```json
{
  "headers": [
    {
      "source": "/sw.js",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        },
        {
          "key": "Service-Worker-Allowed",
          "value": "/"
        }
      ]
    },
    {
      "source": "/manifest.json",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/manifest+json"
        }
      ]
    }
  ]
}
```

**重要**：Service Worker 文件（sw.js）必须设置 `Cache-Control: no-cache`，确保浏览器每次都检查是否有新版本。

---

## 快速检查清单 ✅

部署 PWA 后，检查：

- [ ] manifest.json 可访问（浏览器打开 `/manifest.json`）
- [ ] sw.js 可访问（浏览器打开 `/sw.js`）
- [ ] 图标已生成（icon-192.png, icon-512.png）
- [ ] Chrome DevTools → Application → Manifest 显示正确
- [ ] Service Worker 注册成功（Console 有 "SW registered" 日志）
- [ ] Lighthouse PWA 分数 > 90
- [ ] 手机上可以"安装到主屏幕"
- [ ] 断网后首页仍可访问（离线测试）

---

## Linus 视角：PWA 的价值

> "好的 PWA 应该是不可见的。用户不应该感觉到它是网页还是原生 app。如果你的 PWA 需要向用户解释什么是 Service Worker，那你就失败了。它应该就是'能用'，而且'很快'。"

**核心原则**：
- ✅ 透明：用户无感知，自动生效
- ✅ 快速：缓存让加载接近瞬时
- ✅ 可靠：离线也能基本可用
- ❌ 不要过度工程化：不需要复杂的缓存策略
