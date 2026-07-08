#!/usr/bin/env python3
"""Generate all 6 HTML pages + manifest.json from siteConfig.js data.

Usage:
  python scripts/gen-html.py          # reads from current directory
  python scripts/gen-html.py /path/to/project

This script eliminates stale-topic bugs by generating every HTML page's
meta description, OG title, and page content directly from siteConfig.js.
No sed replacement, no template copying.

Requirements: Python 3.7+, no external dependencies.
"""
import re, json, os, sys

def parse_site_config(path):
    """Parse siteConfig.js (JS object literal) into a Python dict."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    # Strip 'const siteConfig =' prefix and trailing ';'
    js_obj = re.sub(r'^const\s+siteConfig\s*=\s*', '', raw).rstrip().rstrip(';')
    # Convert JS object literal to JSON
    js_obj = js_obj.replace("'", '"')  # single quotes → double quotes
    js_obj = re.sub(r'(\{|,)\s*(\w+)\s*:', r'\1"\2":', js_obj)  # unquoted keys
    return json.loads(js_obj)

def generate_head(title, desc, topic, item_name):
    """Generate <head> with correct SEO meta from siteConfig."""
    return (
        '<head>'
        '<meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
        '<title>' + title + '</title>'
        '<meta name="description" content="' + desc + '">'
        '<meta name="keywords" content="' + topic + ',学习,' + item_name + '">'
        '<meta property="og:title" content="' + title + '">'
        '<meta property="og:description" content="' + desc + '">'
        '<meta property="og:type" content="website">'
        '<meta property="og:image" content="/icon-512.png">'
        '<meta name="theme-color" content="#FBBF24">'
        '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' '
        'viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>📊</text></svg>">'
        '<link rel="manifest" href="/manifest.json">'
        '<link rel="apple-touch-icon" href="/icon-192.png">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="css/minimal.css">'
        '</head>'
    )

def generate_nav(site_name):
    """Generate <header> nav bar."""
    return (
        '<header class="nav"><nav class="nav-container">'
        '<a class="nav-brand" href="/">' + site_name + '</a>'
        '<div class="nav-links">'
        '<a class="nav-link" href="/learn.html">学习</a>'
        '<a class="nav-link" href="/flashcard.html">闪卡</a>'
        '<a class="nav-link" href="/roots.html">索引</a>'
        '<a class="nav-link" href="/progress.html">进度</a>'
        '</div></nav></header>'
    )

def generate_page(body, title, desc, topic, item_name, site_name):
    """Wrap body in a complete HTML page with correct metadata."""
    sw = "<script>if('serviceWorker' in navigator){window.addEventListener('load',()=>navigator.serviceWorker.register('/sw.js'));}</script>"
    return (
        '<!DOCTYPE html><html lang="zh-CN">'
        + generate_head(title, desc, topic, item_name)
        + '<body>'
        + generate_nav(site_name)
        + body
        + '<script src="js/siteConfig.js"></script>'
        + '<script src="js/wordData.js"></script>'
        + '<script src="js/storage.js"></script>'
        + sw
        + '</body></html>'
    )

def build_pages(sc):
    """Build all 6 page bodies from siteConfig data."""
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

    sc_html = ''.join(
        '<div class="stat-card"><div class="stat-value">' + s['value'] +
        '</div><div class="stat-label">' + s['label'] + '</div></div>'
        for s in STATS
    )

    index_body = (
        '<main class="hero"><div class="container">'
        '<h1 class="hero-title"><span>' + HT[0] + '</span><span>' + HT[1] + '</span><span>' + HT[2] + '</span></h1>'
        '<p class="hero-subtitle">' + HS + '</p>'
        '<div class="stat-grid">' + sc_html + '</div>'
        '<div style="display:flex;gap:var(--spacing-md);justify-content:center;margin-top:var(--spacing-xl)">'
        '<a class="btn btn-primary btn-large" href="/learn.html">' + CTA['primary'] + '</a>'
        '<a class="btn btn-large" href="/flashcard.html">' + CTA['secondary'] + '</a></div>'
        '<section class="card" style="margin-top:var(--spacing-2xl)">'
        '<h2 class="footer-tagline">' + TAG + '</h2><p>' + DESC + '</p>'
        '<div id="demos" class="roots-grid" style="margin-top:var(--spacing-lg)"></div>'
        '</section></div></main>'
        '<script>window.addEventListener("DOMContentLoaded",()=>{'
        'let d=document.getElementById("demos");'
        'WordRoots.slice(0,5).forEach(r=>{'
        'let c=document.createElement("div");c.className="card root-card";'
        'let n=document.createElement("div");n.className="root-name";n.textContent=r.root;'
        'let m=document.createElement("div");m.className="root-meaning";m.textContent=r.meaning;'
        'c.append(n,m);d.appendChild(c);});});</script>'
    )

    learn_body = (
        '<main class="learn-container"><h1>渐进学习</h1>'
        '<div class="card"><span class="tag" id="origin"></span><h2 id="rootName"></h2>'
        '<p id="meaning" class="root-meaning"></p><p id="description"></p><div id="examples"></div></div>'
        '<div class="card"><h3>小测验</h3><p id="question"></p><div id="options"></div><p id="feedback" class="feedback-toast"></p></div>'
        '<div class="learn-nav"><button class="btn" id="prev">← 上一个</button><span id="counter"></span>'
        '<button class="btn btn-primary" id="master">✓ 已掌握</button><button class="btn" id="next">下一个 →</button></div>'
        '<div class="progress-bar-bg"><div id="bar" class="progress-bar-fill"></div></div></main>'
        '<script>let idx=0;function show(){let r=WordRoots[idx];origin.textContent=r.origin;rootName.textContent=r.root;'
        'meaning.textContent=r.meaning;description.textContent=r.description;examples.innerHTML="";'
        'r.examples.forEach(e=>{let d=document.createElement("div");d.className="card";'
        'let b=document.createElement("strong");b.textContent=e.word;'
        'let p=document.createElement("p");p.textContent=e.meaning+" — "+e.explanation;'
        'd.append(b,p);examples.appendChild(d)});'
        'question.textContent=r.quiz.question;options.innerHTML="";feedback.textContent="";'
        'r.quiz.options.forEach((o,i)=>{let btn=document.createElement("button");'
        'btn.className="quiz-option";btn.textContent=o;'
        'btn.onclick=()=>feedback.textContent=i===r.quiz.correctAnswer?"✓ 回答正确":"✗ 正确答案："+r.quiz.options[r.quiz.correctAnswer];'
        'options.appendChild(btn)});'
        'counter.textContent=(idx+1)+" / "+WordRoots.length;'
        'bar.style.width=((idx+1)/WordRoots.length*100)+"%"}'
        'prev.onclick=()=>{idx=(idx+WordRoots.length-1)%WordRoots.length;show()};'
        'next.onclick=()=>{idx=(idx+1)%WordRoots.length;show()};'
        'master.onclick=()=>{StorageManager.markRootAsMastered(WordRoots[idx].id);feedback.textContent="✓ 已标记掌握"};'
        'show()</script>'
    )

    flash_body = (
        '<main class="container" style="padding:var(--spacing-2xl) 0"><h1>闪卡复习</h1>'
        '<div class="flashcard" id="card"><div class="flashcard-inner">'
        '<div class="flashcard-front"><div id="front" class="flashcard-root"></div>'
        '<div id="frontMeaning" class="flashcard-meaning"></div></div>'
        '<div class="flashcard-back"><div id="back" class="flashcard-description"></div></div></div></div>'
        '<div class="flashcard-controls"><button class="btn" id="prevCard">←</button>'
        '<button class="btn btn-primary" id="flip">翻转</button><button class="btn" id="nextCard">→</button></div>'
        '<div id="cardCount" class="flashcard-progress"></div></main>'
        '<script>let i=0;function show(){let r=WordRoots[i];front.textContent=r.root;'
        'frontMeaning.textContent=r.meaning;back.textContent=r.description;'
        'cardCount.textContent=(i+1)+" / "+WordRoots.length;card.classList.remove("flipped")}'
        'flip.onclick=()=>card.classList.toggle("flipped");'
        'card.onclick=()=>card.classList.toggle("flipped");'
        'prevCard.onclick=()=>{i=(i+WordRoots.length-1)%WordRoots.length;show()};'
        'nextCard.onclick=()=>{i=(i+1)%WordRoots.length;show()};show()</script>'
    )

    roots_body = (
        '<main class="container" style="padding:var(--spacing-2xl) 0"><h1>' + IN + '索引</h1>'
        '<input id="search" class="search-bar" placeholder="搜索' + T + '...">'
        '<div id="grid" class="roots-grid"></div></main>'
        '<script>function draw(list){grid.innerHTML="";list.forEach(r=>{'
        'let a=document.createElement("a");a.className="card root-card";a.href="root-detail.html?id="+r.id;'
        'let n=document.createElement("div");n.className="root-name";n.textContent=r.root;'
        'let m=document.createElement("div");m.className="root-meaning";m.textContent=r.meaning;'
        'let o=document.createElement("span");o.className="root-origin tag";o.textContent=r.origin;'
        'a.append(n,m,o);grid.appendChild(a)})}'
        'draw(WordRoots);search.oninput=()=>{let q=search.value.trim();'
        'draw(WordRoots.filter(r=>!q||r.root.includes(q)||r.meaning.includes(q)||r.origin.includes(q)))}</script>'
    )

    progress_body = (
        '<main class="container" style="padding:var(--spacing-2xl) 0"><h1>学习进度</h1>'
        '<div class="stat-grid">'
        '<div class="stat-card"><div id="done" class="stat-value">0</div><div class="stat-label">已掌握</div></div>'
        '<div class="stat-card"><div class="stat-value">' + str(IC) + '</div><div class="stat-label">总' + IN + '</div></div>'
        '<div class="stat-card"><div id="pct" class="stat-value">0%</div><div class="stat-label">完成率</div></div></div>'
        '<div class="progress-bar-bg"><div id="pbar" class="progress-bar-fill"></div></div>'
        '<div id="plist" class="roots-grid" style="margin-top:var(--spacing-xl)"></div></main>'
        '<script>let p=StorageManager.getProgress();let ids=p.masteredRoots||[];'
        'done.textContent=ids.length;'
        'pct.textContent=Math.round(ids.length/WordRoots.length*100)+"%";'
        'pbar.style.width=(ids.length/WordRoots.length*100)+"%";'
        'WordRoots.filter(r=>ids.includes(r.id)).forEach(r=>{'
        'let c=document.createElement("div");c.className="card";c.textContent=r.root;plist.appendChild(c)})</script>'
    )

    detail_body = (
        '<main class="container" style="padding:var(--spacing-2xl) 0"><article class="card">'
        '<span id="dorigin" class="tag"></span><h1 id="droot"></h1>'
        '<p id="dmeaning" class="root-meaning"></p><p id="ddesc"></p>'
        '<h2>实战例子</h2><div id="dex"></div>'
        '<h2>小测验</h2><p id="dq"></p><div id="dop"></div><p id="dfb" class="feedback-toast"></p></article></main>'
        '<script>let id=Number(new URLSearchParams(location.search).get("id")||1);'
        'let r=WordRoots.find(x=>x.id===id)||WordRoots[0];'
        'document.title=r.root+" - ' + SN + '";'
        'dorigin.textContent=r.origin;droot.textContent=r.root;dmeaning.textContent=r.meaning;ddesc.textContent=r.description;'
        'r.examples.forEach(e=>{let c=document.createElement("div");c.className="card";'
        'c.textContent=e.word+"："+e.meaning+" — "+e.explanation;dex.appendChild(c)});'
        'dq.textContent=r.quiz.question;'
        'r.quiz.options.forEach((o,i)=>{let b=document.createElement("button");'
        'b.className="quiz-option";b.textContent=o;'
        'b.onclick=()=>dfb.textContent=i===r.quiz.correctAnswer?"✓ 回答正确":"✗ 正确答案："+r.quiz.options[r.quiz.correctAnswer];'
        'dop.appendChild(b)})</script>'
    )

    pages = {
        'index.html': (index_body, SN + ' - ' + str(IC) + '个' + IN + '系统学习'),
        'learn.html': (learn_body, '渐进学习 - ' + SN),
        'flashcard.html': (flash_body, '闪卡复习 - ' + SN),
        'roots.html': (roots_body, IN + '索引 - ' + SN),
        'progress.html': (progress_body, '学习进度 - ' + SN),
        'root-detail.html': (detail_body, IN + '详情 - ' + SN),
    }
    return pages

def main():
    project_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    os.chdir(project_dir)

    # Parse siteConfig
    sc = parse_site_config('js/siteConfig.js')
    T = sc['topic']
    SN = sc['siteName']
    IN = sc['itemName']
    DESC = sc['footer']['description']

    # Generate pages
    pages = build_pages(sc)
    for name, (body, title) in pages.items():
        content = generate_page(body, title, DESC, T, IN, SN)
        with open(name, 'w', encoding='utf-8') as f:
            f.write(content)

    # Generate manifest.json
    manifest = {
        "name": SN,
        "short_name": T,
        "description": DESC,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "theme_color": "#FBBF24",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
        ],
        "categories": ["education", "productivity"],
        "lang": "zh-CN"
    }
    with open('manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print('Generated', len(pages), 'HTML + manifest')
    print('topic:', T)
    print('siteName:', SN)
    print('desc:', DESC[:80])

if __name__ == '__main__':
    main()
