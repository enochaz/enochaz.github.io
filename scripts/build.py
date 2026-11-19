#!/usr/bin/env python3
"""Build the site with Python's standard library. Never touches coverage/."""
from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://enochaz.github.io'
GITHUB = 'https://github.com/enochaz'
EMAIL = 'enirox001@gmail.com'
BOOKS = json.loads((ROOT / 'content/books.json').read_text())
ARTICLES = json.loads((ROOT / 'content/articles.json').read_text())
PAGES = []
NAV = [('articles', '/articles/'), ('projects', '/projects/'), ('books', '/books/'), ('contact', '/contact/')]


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
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header><a class="name" href="/">enochaz</a><nav>{nav}</nav></header>
<main>
{body}
</main>
<footer>Enoch Azariah<a href="{GITHUB}">github</a><a href="https://x.com/eedee__">x</a><a href="mailto:{EMAIL}">email</a></footer>
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
    return '<ul class="list">' + ''.join(
        f'<li><span class="date">{e(a["date"])}</span> <a href="/articles/{e(a["slug"])}/">{e(a["title"])}</a></li>' for a in items) + '</ul>'


def book_line(b):
    return f'<li><a href="/books/{e(b["slug"])}/">{e(b["title"])}</a> <span class="muted">by {e(b["authors"])}</span></li>'


page('/', 'Enoch Azariah', 'Enoch Azariah (enochaz). I work on Bitcoin Core and sv2-tp.', f'''
<h1>Hi, I'm Enoch</h1>
<p>I'm a software engineer in Nigeria. I work on <a href="https://github.com/bitcoin/bitcoin">Bitcoin Core</a> and <a href="https://github.com/stratum-mining/sv2-tp">sv2-tp</a>, mostly around mining, multiprocess and IPC, and fuzzing.</p>
<p>A lot of my time goes into reading code, reviewing PRs and trying to figure out why things work the way they do.</p>
<p>Before Bitcoin I did web and mobile work, mostly Flutter, TypeScript and Python. In 2023 I interned at <a href="https://www.blockchaincommons.com/">Blockchain Commons</a> and worked on the Esplora GUI. These days I'm getting better at C++ by working on Bitcoin Core.</p>
<p>I write here sometimes, mostly about things I'm learning or working on.</p>
<h2>Writing</h2>
{article_list(ARTICLES[:5])}
<h2>Working on</h2>
<ul>
<li><a href="https://github.com/bitcoin/bitcoin">Bitcoin Core</a>, code, review and testing</li>
<li><a href="https://github.com/stratum-mining/sv2-tp">sv2-tp</a>, the Stratum v2 Template Provider</li>
<li><a href="https://github.com/bitcoin-core/libmultiprocess">libmultiprocess</a>, review and testing</li>
<li><a href="{GITHUB}/btc-ipc">btc-ipc</a>, a Python IPC client I use to try out Bitcoin Core's interfaces</li>
</ul>
''', '/')

page('/projects/', 'Projects', 'Things Enoch Azariah is working on or has worked on.', f'''
<h1>Projects</h1>
<p>Most of what I do is on <a href="{GITHUB}">GitHub</a>.</p>
<h2>Now</h2>
<p><a href="https://github.com/bitcoin/bitcoin">Bitcoin Core</a>. Writing code, reviewing PRs and testing changes, mostly around mining, multiprocess and IPC fuzzing. <a href="https://github.com/bitcoin/bitcoin/pulls?q=is%3Apr+author%3Aenochaz">My PRs</a>.</p>
<p><a href="https://github.com/stratum-mining/sv2-tp">sv2-tp</a>. The Stratum v2 Template Provider, and how it talks to Bitcoin Core.</p>
<p><a href="https://github.com/bitcoin-core/libmultiprocess">libmultiprocess</a>. Review and testing on the library behind Bitcoin Core's multiprocess setup.</p>
<p><a href="{GITHUB}/btc-ipc">btc-ipc</a>. A Python IPC client with a small indexer, benchmarks and tests. The indexer tracks blocks, transaction ids and which blocks are on the active chain, including reorgs. It's an experiment for seeing what the interfaces can do, so a method working there doesn't mean it's a stable API.</p>
<h2>Before</h2>
<p><a href="{GITHUB}/esplora">Esplora GUI</a>. Work on the block explorer frontend, from my Blockchain Commons internship.</p>
<p><a href="{GITHUB}?tab=repositories">Older stuff</a>. Web and mobile projects in Flutter, TypeScript and Python.</p>
''', '/projects/')

page('/articles/', 'Articles', 'Articles by Enoch Azariah, mostly about Bitcoin.', f'''
<h1>Articles</h1>
{article_list(ARTICLES)}
''', '/articles/')
for a in ARTICLES:
    body = (ROOT / 'content/articles' / (a['slug'] + '.html')).read_text()
    page('/articles/' + a['slug'] + '/', a['title'], a['description'],
         f'<h1>{e(a["title"])}</h1><p class="date">{e(a["date"])}</p>\n{body}\n<p><a href="/articles/">← all articles</a></p>', '/articles/')

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
<p><a href="/books/">← all books</a></p>
''', '/books/')

page('/contact/', 'Contact', 'How to reach Enoch Azariah.', f'''
<h1>Contact</h1>
<p>Email is the best way to reach me: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>I'm also <a href="{GITHUB}">enochaz</a> on GitHub and <a href="https://x.com/eedee__">@eedee__</a> on X.</p>
''', '/contact/')

page('/404.html', 'Not found', 'Page not found.', '<h1>Not found</h1><p>That page doesn\'t exist, or it moved. <a href="/">Go home</a>.</p>')

(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                  + ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in PAGES) + '</urlset>\n')
print(f'Built {len(PAGES) + 1} pages. coverage/ not touched.')
