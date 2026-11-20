# enochaz.github.io

A small, static GitHub Pages site. Live at https://enochaz.github.io/.

## Editing

The source for page content and the shared layout is `scripts/build.py`. The
bookshelf is maintained in `content/books.json`. Styling lives in `assets/style.css`. No packages, framework, or Jekyll installation are required.

After editing, use Python 3.12 or newer:

```sh
python3 scripts/build.py
```

Commit the changed sources **and generated HTML**. GitHub Pages serves the root
of `main`; the existing `.nojekyll` file keeps this a plain static site.
The build script never deletes files or writes under `coverage/`.

To preview locally:

```sh
python3 -m http.server 8000
```

Visit http://localhost:8000/.

## Books

Books live in `content/books.json` (slug, title, authors, status `Reading` or `Finished`, optional note, url).

## Publishing your own articles

Add an entry to `content/articles.json` with `slug`, `title`, `date`
(`YYYY-MM-DD`), and `description`. Put the article body in
`content/articles/<slug>.html`, using ordinary HTML paragraphs and headings.
Run `python3 scripts/build.py` and commit the source and generated pages.
Keep the list in newest-first order. The homepage is the article list.
The list starts empty until you publish your own writing.
