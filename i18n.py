#!/usr/bin/env python3
"""Translation tooling: turn the structured English content into translator-friendly
gettext catalogs and back.

English (`site/content/en.json`) is the single source of truth: structure + English text +
non-translatable data (names, companies, locations, dates*, URLs). Translators only ever
edit `locale/<lang>.po` in Poedit. This script bridges the two:

  python3 i18n.py extract        # en.json -> locale/resume.pot, merged into each <lang>.po
  python3 i18n.py compile [lang] # en.json + <lang>.po -> site/content/<lang>.json
  python3 i18n.py seed           # one-time: pre-fill the .po from the existing JSON

Each translatable string is one PO entry: msgctxt = a stable key (the JSON path), msgid =
the English source text, msgstr = the translation. compile uses a translation only if it is
present and not fuzzy; otherwise it falls back to English.

Requires: polib (pure-Python; `pip install polib`). Only this dev/CI step needs it — the
website and build_resume.py stay dependency-free.
"""
import json
import os
import sys

import polib

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "site", "content")
LOCALE = os.path.join(ROOT, "locale")

# Target languages (en is the source, not a target).
LANGS = ["fr", "zh-TW"]

# The PDF-button label historically lived in app.js; seed it from there so the migration
# loses nothing. After seeding it is a normal translatable string in the .po.
SEED_PDF_LABELS = {"fr": "Télécharger le PDF", "zh-TW": "下載 PDF"}


def load_en():
    with open(os.path.join(CONTENT, "en.json"), encoding="utf-8") as f:
        return json.load(f)


def translatable_entries(en):
    """Ordered list of (msgctxt, english_source) for every translatable string."""
    out = [
        ("tagline", en["tagline"]),
        ("summary", en["summary"]),
        ("footer_title", en["footer_title"]),
    ]
    for k in ("experience", "education", "skills", "languages"):
        out.append((f"section.{k}", en["sections"][k]))
    out.append(("ui.download_pdf", en["ui"]["download_pdf"]))
    for e in en["experience"]:
        eid = e["id"]
        out.append((f"experience.{eid}.title", e["title"]))
        out.append((f"experience.{eid}.date", e["date"]))
        for i, b in enumerate(e["bullets"], 1):
            out.append((f"experience.{eid}.bullet.{i}", b))
    for ed in en["education"]:
        eid = ed["id"]
        out.append((f"education.{eid}.institution", ed["institution"]))
        out.append((f"education.{eid}.date", ed["date"]))
        out.append((f"education.{eid}.detail", ed["detail"]))
    for i, s in enumerate(en["skills"], 1):
        out.append((f"skill.{i}", s))
    for i, lng in enumerate(en["spoken_languages"], 1):
        out.append((f"language.{i}", lng))
    return out


def _metadata(lang=""):
    return {
        "Project-Id-Version": "resume",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
        "Language": lang,
    }


def cmd_extract():
    en = load_en()
    entries = translatable_entries(en)
    os.makedirs(LOCALE, exist_ok=True)

    pot = polib.POFile()
    pot.metadata = _metadata()
    for ctx, src in entries:
        pot.append(polib.POEntry(msgctxt=ctx, msgid=src, msgstr=""))
    pot.save(os.path.join(LOCALE, "resume.pot"))
    print(f"wrote locale/resume.pot ({len(entries)} strings)")

    for lang in LANGS:
        path = os.path.join(LOCALE, f"{lang}.po")
        old = {}
        if os.path.exists(path):
            for e in polib.pofile(path):
                old[e.msgctxt] = e
        cat = polib.POFile()
        cat.metadata = _metadata(lang)
        new_count = fuzzy_count = 0
        for ctx, src in entries:
            entry = polib.POEntry(msgctxt=ctx, msgid=src, msgstr="")
            prev = old.get(ctx)
            if prev is not None and prev.msgstr:
                entry.msgstr = prev.msgstr
                if prev.msgid != src:        # English changed -> needs re-check
                    entry.flags.append("fuzzy")
                    fuzzy_count += 1
            else:
                new_count += 1
            cat.append(entry)
        cat.save(path)
        print(f"updated locale/{lang}.po ({new_count} new, {fuzzy_count} fuzzy)")


def _translations(lang):
    """ctx -> usable translation (non-empty, not fuzzy) from locale/<lang>.po."""
    path = os.path.join(LOCALE, f"{lang}.po")
    tr = {}
    for e in polib.pofile(path):
        if e.msgstr and not e.obsolete and "fuzzy" not in e.flags:
            tr[e.msgctxt] = e.msgstr
    return tr


def compile_lang(en, lang):
    tr = _translations(lang)
    missing = []

    def t(ctx, en_value):
        if ctx in tr:
            return tr[ctx]
        missing.append(ctx)
        return en_value

    out = {
        "lang": lang,
        "name": en["name"],
        "tagline": t("tagline", en["tagline"]),
        "contact": dict(en["contact"]),
        "summary": t("summary", en["summary"]),
        "footer_title": t("footer_title", en["footer_title"]),
        "sections": {k: t(f"section.{k}", v) for k, v in en["sections"].items()},
        "ui": {"download_pdf": t("ui.download_pdf", en["ui"]["download_pdf"])},
        "experience": [],
        "education": [],
        "skills": [],
        "spoken_languages": [],
    }
    for e in en["experience"]:
        eid = e["id"]
        entry = {
            "id": eid,
            "company": e["company"],
            "title": t(f"experience.{eid}.title", e["title"]),
            "date": t(f"experience.{eid}.date", e["date"]),
            "location": e["location"],
            "bullets": [t(f"experience.{eid}.bullet.{i}", b)
                        for i, b in enumerate(e["bullets"], 1)],
        }
        if e.get("page_break_before"):
            entry["page_break_before"] = True
        out["experience"].append(entry)
    for ed in en["education"]:
        eid = ed["id"]
        out["education"].append({
            "id": eid,
            "institution": t(f"education.{eid}.institution", ed["institution"]),
            "date": t(f"education.{eid}.date", ed["date"]),
            "detail": t(f"education.{eid}.detail", ed["detail"]),
        })
    out["skills"] = [t(f"skill.{i}", s) for i, s in enumerate(en["skills"], 1)]
    out["spoken_languages"] = [t(f"language.{i}", lng)
                               for i, lng in enumerate(en["spoken_languages"], 1)]
    return out, missing


def cmd_compile(only=None):
    en = load_en()
    langs = [only] if only else LANGS
    for lang in langs:
        out, missing = compile_lang(en, lang)
        path = os.path.join(CONTENT, f"{lang}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
        note = f"{len(missing)} untranslated (fell back to English)" if missing else "fully translated"
        print(f"wrote site/content/{lang}.json ({note})")


def cmd_seed():
    """One-time migration: pre-fill locale/<lang>.po from the existing site/content/<lang>.json."""
    en = load_en()
    entries = translatable_entries(en)
    os.makedirs(LOCALE, exist_ok=True)
    for lang in LANGS:
        with open(os.path.join(CONTENT, f"{lang}.json"), encoding="utf-8") as f:
            tgt = json.load(f)
        vals = _seed_values(en, tgt)
        vals["ui.download_pdf"] = SEED_PDF_LABELS.get(lang, en["ui"]["download_pdf"])
        cat = polib.POFile()
        cat.metadata = _metadata(lang)
        filled = 0
        for ctx, src in entries:
            msgstr = vals.get(ctx, "")
            if msgstr:
                filled += 1
            cat.append(polib.POEntry(msgctxt=ctx, msgid=src, msgstr=msgstr))
        cat.save(os.path.join(LOCALE, f"{lang}.po"))
        print(f"seeded locale/{lang}.po ({filled}/{len(entries)} from existing JSON)")


def _seed_values(en, tgt):
    """Pair en (has ids) with the existing target JSON (same order, no ids) by position."""
    v = {
        "tagline": tgt["tagline"],
        "summary": tgt["summary"],
        "footer_title": tgt["footer_title"],
    }
    for k in ("experience", "education", "skills", "languages"):
        v[f"section.{k}"] = tgt["sections"][k]
    for e_en, e_t in zip(en["experience"], tgt["experience"]):
        eid = e_en["id"]
        v[f"experience.{eid}.title"] = e_t["title"]
        v[f"experience.{eid}.date"] = e_t["date"]
        for i, b_t in enumerate(e_t["bullets"], 1):
            v[f"experience.{eid}.bullet.{i}"] = b_t
    for ed_en, ed_t in zip(en["education"], tgt["education"]):
        eid = ed_en["id"]
        v[f"education.{eid}.institution"] = ed_t["institution"]
        v[f"education.{eid}.date"] = ed_t["date"]
        v[f"education.{eid}.detail"] = ed_t["detail"]
    for i, s in enumerate(tgt["skills"], 1):
        v[f"skill.{i}"] = s
    for i, lng in enumerate(tgt["spoken_languages"], 1):
        v[f"language.{i}"] = lng
    return v


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("extract", "compile", "seed"):
        sys.exit("usage: python3 i18n.py {extract|compile [lang]|seed}")
    cmd = sys.argv[1]
    if cmd == "extract":
        cmd_extract()
    elif cmd == "seed":
        cmd_seed()
    else:
        cmd_compile(sys.argv[2] if len(sys.argv) > 2 else None)


if __name__ == "__main__":
    main()
