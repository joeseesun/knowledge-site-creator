# Python HTML Generator Pattern

## Problem

sed-replacing copied HTML templates only handles keyword-level matching. SEO descriptions from the previous topic persist semantically — e.g. "从任务收集、优先级判断、专注执行到每日复盘" appears in a negotiation psychology site because sed replaced "时间管理" but not the surrounding context.

## Solution

Write a Python script that reads `js/siteConfig.js` and generates all 6 HTML pages from the config data. Every meta description, OG title, and page content is derived from siteConfig — no sed, no template copy.

## Implementation

```python
"""Generate all 6 HTML pages from siteConfig.js data."""
import re, json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Parse siteConfig.js (JS object → Python dict)
with open('js/siteConfig.js', 'r', encoding='utf-8') as f:
    raw = f.read()
js_obj = re.sub(r'^const\s+siteConfig\s*=\s*', '', raw).rstrip().rstrip(';')
js_obj = js_obj.replace("'", '"')
js_obj = re.sub(r'(\{|,)\s*(\w+)\s*:', r'\1"\2":', js_obj)
sc = json.loads(js_obj)

# Extract config values
T = sc['topic']
SN = sc['siteName']
IN = sc['itemName']
DESC = sc['footer']['description']
TAG = sc['footer']['tagline']
HT = sc['hero']['title']
HS = sc['hero']['subtitle']
STATS = sc['stats']
CTA = sc['cta']
IC = sc['itemCount']

# Build reusable components
NAV = '<header class="nav">...'
SW = "<script>if('serviceWorker' in navigator){...}</script>"

def head(title, desc=DESC):
    # All meta tags use siteConfig data
    return '<head>...' + desc + '...' + title + '...</head>'

def page(body, title):
    return '<!DOCTYPE html><html lang="zh-CN">' + head(title) + '<body>' + NAV + body + '...' + SW + '</body></html>'

# Generate each page
pages = {
    'index.html': page(index_body, SN + ' - ' + str(IC) + IN + '系统学习'),
    'learn.html': page(learn_body, '渐进学习 - ' + SN),
    'flashcard.html': page(flash_body, '闪卡复习 - ' + SN),
    'roots.html': page(roots_body, IN + '索引 - ' + SN),
    'progress.html': page(progress_body, '学习进度 - ' + SN),
    'root-detail.html': page(detail_body, IN + '详情 - ' + SN),
}
for name, content in pages.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(content)

# Write manifest.json from siteConfig
manifest = {"name": SN, "short_name": T, "description": DESC, ...}
with open('manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
```

## Key advantages over sed-replacement

1. **SEO description is always correct** — derived from `siteConfig.footer.description`, not from a previous topic's HTML
2. **OG title is always correct** — derived from `siteConfig.siteName`
3. **No stale-topic risk** — HTML is generated fresh from config, not copied and modified
4. **Single source of truth** — siteConfig.js is the only input; change it and all pages update

## When to use this vs. AI from-scratch generation

- **Use this pattern** when you need reliable, repeatable HTML generation (testing, CI, batch generation)
- **Use AI from-scratch** when you want creative variation in page layout and content

## Pitfalls

1. **JS object → JSON conversion is fragile** — the regex `re.sub(r'(\{|,)\s*(\w+)\s*:', ...)` only handles simple unquoted keys. Nested objects with computed keys will fail.
2. **f-strings with embedded triple quotes** break Python — use string concatenation (`+`) instead of f-strings for HTML templates containing JS code with `'''`.
3. **`innerHTML` XSS warnings** — the generated HTML uses `innerHTML` for clearing containers (e.g., `grid.innerHTML=""`) which is safe (empty string), but lint tools flag it. Add a comment if needed.
