#!/usr/bin/env python3
"""Generate the Pandoc markdown source for one language from shared JSON content.

Content lives in site/content/<lang>.json (the single source of truth, also read by
the website). Styling lives in templates/styling.tex (the LaTeX preamble, separated out
of the old resume.md). This script stitches them into the exact markdown shape the
existing Pandoc + XeLaTeX pipeline already turns into a PDF, so the markdown -> PDF path
is unchanged. For English the output is byte-identical to the original resume.md, which
lets us prove PDF parity with a plain diff (no rendering needed).

Usage:  python3 build_resume.py <lang>   # prints the markdown to stdout
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def latex_header_includes(styling, data):
    """Footer text is localized via @@TOKENS@@; everything else is verbatim styling."""
    contact = data["contact"]
    styling = (styling
               .replace("@@NAME@@", data["name"])
               .replace("@@FOOTER_TITLE@@", data["footer_title"])
               .replace("@@CONTACT_URL@@", contact["url"])
               .replace("@@CONTACT_LABEL@@", contact["label"]))
    out = ["---", "header-includes: |", "  ```{=latex}"]
    for line in styling.split("\n"):
        out.append("  " + line if line else "")
    out += ["  ```", "---", ""]
    return out


def body(data):
    c = data["contact"]
    s = data["sections"]
    L = []
    # name / contact banner
    L += ["```{=latex}",
          "\\resumeheader",
          "  {" + data["name"] + "}",
          "  {" + data["tagline"] + "}",
          "  {\\href{" + c["url"] + "}{" + c["label"] + "}}",
          "```",
          ""]
    # intro paragraph (first-line indented)
    L += ["```{=latex}",
          "{\\setlength{\\parindent}{1.5em}%",
          data["summary"] + "\\par}",
          "```",
          ""]
    # experience
    L += ["## " + s["experience"], ""]
    for e in data["experience"]:
        if e.get("page_break_before"):
            L += ["```{=latex}", "\\needspace{9\\baselineskip}", "```", ""]
        L += ["### " + e["company"] + " - " + e["title"]
              + " \\hfill \\datestamp{" + e["date"] + "}",
              "*" + e["location"] + "*",
              ""]
        L += ["- " + b for b in e["bullets"]]
        L += [""]
    # education
    L += ["## " + s["education"], ""]
    for ed in data["education"]:
        L += ["### " + ed["institution"] + " \\hfill \\datestamp{" + ed["date"] + "}",
              ed["detail"],
              ""]
    # skills
    L += ["## " + s["skills"], ""]
    L += ["- " + skill for skill in data["skills"]]
    L += [""]
    # languages
    L += ["## " + s["languages"], ""]
    L += ["- " + lang for lang in data["spoken_languages"]]
    return L


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 build_resume.py <lang>")
    lang = sys.argv[1]
    with open(os.path.join(ROOT, "site", "content", lang + ".json"), encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(ROOT, "templates", "styling.tex"), encoding="utf-8") as f:
        styling = f.read().rstrip("\n")
    lines = latex_header_includes(styling, data) + body(data)
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
