# Alexandre Brispot [![Open to offers](https://img.shields.io/badge/Open%20to%20offers-Yes-1abc9c.svg)](#)

[![PDF - English](https://img.shields.io/badge/PDF-English-A09BE7.svg)](https://github.com/Kireyin/Resume/raw/main/resume.pdf)
[![PDF - Français](https://img.shields.io/badge/PDF-Fran%C3%A7ais-A09BE7.svg)](https://github.com/Kireyin/Resume/raw/main/resume.fr.pdf)
[![PDF - 繁體中文](https://img.shields.io/badge/PDF-%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87-A09BE7.svg)](https://github.com/Kireyin/Resume/raw/main/resume.zh-tw.pdf)

If you are looking for an iOS dev, a Mobile dev lead/manager, in Paris (FR) or remotely, you are on the good repo ;)</br>
Click a badge above to download my resume (English, French, or Traditional Chinese).

## How this repo is built

English content lives in [`site/content/en.json`](site/content/en.json) — the single source
of truth. Translations are authored as gettext catalogs in [`locale/`](locale) and compiled
into `site/content/fr.json` / `zh-TW.json`. Two independent tracks render the content:

- **PDF** — `build_resume.py` merges the content with the LaTeX styling in
  [`templates/styling.tex`](templates/styling.tex) and Pandoc + XeLaTeX produces
  `resume.pdf` / `resume.fr.pdf` / `resume.zh-tw.pdf` in CI.
- **Website** — a static, no-build site in [`site/`](site) (`index.html` + `style.css` +
  `app.js`) that fetches the same JSON and renders it, with a language switcher. Deployable
  to any static host.

### Translating

Translators never touch JSON. Open [`locale/fr.po`](locale/fr.po) or
[`locale/zh-TW.po`](locale/zh-TW.po) in [Poedit](https://poedit.net) (free, Win/Mac/Linux) —
each entry shows the English source with a box for the translation. Translate, save, then run
`python3 i18n.py compile` (after `pip install polib`) to regenerate the JSON the site and
PDFs consume. CI recompiles on every push, so the JSON can't drift from the catalogs.

See [`CLAUDE.md`](CLAUDE.md) for the full build details.
