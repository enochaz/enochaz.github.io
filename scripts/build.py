#!/usr/bin/env python3
"""Build the site with Python's standard library. Never touches coverage/."""
from pathlib import Path
from html import escape as e
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://enochaz.github.io'
GITHUB = 'https://github.com/enochaz'
EMAIL = 'enirox001@gmail.com'
BOOKS = json.loads((ROOT / 'content/books.json').read_text())
ARTICLES = json.loads((ROOT / 'content/articles.json').read_text())
PAGES = []
CSS_V = hashlib.sha256((ROOT / 'assets/style.css').read_bytes()).hexdigest()[:8]
NAV = [('projects', '/projects/'), ('books', '/books/'), ('contact', '/contact/')]


def page(path, title, description, body, active=''):
    nav = ''.join(f'<a href="{url}"' + (' aria-current="page"' if active == url else '') + f'>{name}</a>' for name, url in NAV)
    full_title = 'enochaz' if path == '/' else f'{title} · enochaz'
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(description, quote=True)}">
  <meta name="author" content="Enoch Azariah">
  <meta name="color-scheme" content="light dark">
  <meta property="og:title" content="{e(full_title, quote=True)}">
  <meta property="og:description" content="{e(description, quote=True)}">
  <meta property="og:url" content="{SITE}{path}">
  <link rel="canonical" href="{SITE}{path}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css?v={CSS_V}">
</head>
<body>
<div class="wrap">
<header class="site"><a class="name" href="/">enochaz</a><nav>{nav}</nav></header>
<main>
{body}
</main>
<footer class="site"><span>© 2026 Enoch Azariah</span><nav><a href="{GITHUB}">github</a><a href="https://x.com/eedee__">x</a><a href="mailto:{EMAIL}">email</a></nav></footer>
</div>
</body>
</html>
'''
    dest = ROOT / ('index.html' if path == '/' else path.strip('/') + '/index.html' if path.endswith('/') else path.lstrip('/'))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    if path != '/404.html':
        PAGES.append(path)


def article_list(items):
    if not items:
        return '<p class="muted">Nothing here yet.</p>'
    return '<ul class="rows">' + ''.join(
        f'<li><div class="top"><a href="/articles/{e(a["slug"])}/">{e(a["title"])}</a><span class="date">{e(a["date"])}</span></div><span class="desc">{e(a["description"])}</span></li>' for a in items) + '</ul>'


def book_line(b):
    return f'<li><a href="/books/{e(b["slug"])}/">{e(b["title"])}</a> <span class="muted">by {e(b["authors"])}</span></li>'


page('/', 'Articles', 'Articles by Enoch Azariah (enochaz), mostly about Bitcoin.', f'''
{article_list(ARTICLES)}
''', '/')

page('/projects/', 'Projects', 'Things Enoch Azariah works on.', f'''
<h1>Projects</h1>
<h2>Now</h2>
<ul>
<li><a href="https://github.com/bitcoin/bitcoin">Bitcoin Core</a> <span class="muted">· mining, multiprocess, IPC fuzzing (<a href="https://github.com/bitcoin/bitcoin/pulls?q=is%3Apr+author%3Aenochaz">my PRs</a>)</span></li>
<li><a href="https://github.com/stratum-mining/sv2-tp">sv2-tp</a> <span class="muted">· Stratum v2 Template Provider</span></li>
<li><a href="https://github.com/bitcoin-core/libmultiprocess">libmultiprocess</a> <span class="muted">· review and testing</span></li>
<li><a href="{GITHUB}/btc-ipc">btc-ipc</a> <span class="muted">· Python IPC client for trying out Bitcoin Core's interfaces</span></li>
</ul>
<h2>Before</h2>
<ul>
<li><a href="{GITHUB}/esplora">Esplora GUI</a> <span class="muted">· Blockchain Commons internship, 2023</span></li>
<li><a href="{GITHUB}?tab=repositories">Older projects</a> <span class="muted">· web and mobile, Flutter, TypeScript, Python</span></li>
</ul>
''', '/projects/')

# /articles/ used to be the list; send old links to the homepage.
(ROOT / 'articles/index.html').write_text('<!doctype html><meta charset="utf-8"><title>enochaz</title><link rel="canonical" href="' + SITE + '/"><meta http-equiv="refresh" content="0; url=/"><a href="/">Articles</a>\n')
for a in ARTICLES:
    body = (ROOT / 'content/articles' / (a['slug'] + '.html')).read_text()
    page('/articles/' + a['slug'] + '/', a['title'], a['description'],
         f'<article><h1>{e(a["title"])}</h1><p class="date">{e(a["date"])}</p>\n{body}\n</article><a class="back" href="/">← all articles</a>', '/')

reading = [b for b in BOOKS if b['status'] == 'Reading']
finished = [b for b in BOOKS if b['status'] == 'Finished']
page('/books/', 'Books', 'Books Enoch Azariah is reading or has read.', f'''
<h1>Books</h1>
<h2>Reading</h2>
<ul>{''.join(book_line(b) for b in reading)}</ul>
<h2>Read</h2>
<ul>{''.join(book_line(b) for b in finished)}</ul>
''', '/books/')
for b in BOOKS:
    note = f'<p>{e(b["note"])}</p>' if b.get('note') else ''
    page(f'/books/{b["slug"]}/', b['title'], b.get('note') or f'{b["title"]} by {b["authors"]}.', f'''
<h1>{e(b["title"])}</h1>
<p class="muted">by {e(b["authors"])} · {e(b["status"].lower())}</p>
{note}
<p><a href="{e(b["url"], quote=True)}">About the book</a></p>
<a class="back" href="/books/">← all books</a>
''', '/books/')

page('/contact/', 'Contact', 'How to reach Enoch Azariah.', f'''
<h1>Contact</h1>
<p>Email is the best way to reach me: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>I'm also <a href="{GITHUB}">enochaz</a> on GitHub and <a href="https://x.com/eedee__">@eedee__</a> on X.</p>
''', '/contact/')

page('/404.html', 'Not found', 'Page not found.', '<h1>Not found</h1><p>That page doesn\'t exist, or it moved. <a href="/">Back to the articles</a>.</p>')

(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                  + ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in PAGES) + '</urlset>\n')
print(f'Built {len(PAGES) + 1} pages. coverage/ not touched.')
