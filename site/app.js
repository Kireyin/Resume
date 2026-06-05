"use strict";

// Supported languages: code -> label shown in the switcher.
const LANGS = { "en": "English", "fr": "Français", "zh-TW": "中文" };

// PDF filename per language (config, not translation; English keeps resume.pdf).
// The button *label* is a translatable string and comes from the content JSON.
const PDF_FILE = {
  "en": "resume.pdf",
  "fr": "resume.fr.pdf",
  "zh-TW": "resume.zh-tw.pdf",
};

const $ = (id) => document.getElementById(id);

function el(tag, opts = {}) {
  const node = document.createElement(tag);
  if (opts.class) node.className = opts.class;
  if (opts.text != null) node.textContent = opts.text;
  if (opts.href != null) node.href = opts.href;
  return node;
}

// Decide the active language: ?lang= > saved choice > browser > English.
function pickLang() {
  const params = new URLSearchParams(location.search);
  const fromUrl = params.get("lang");
  if (fromUrl && LANGS[fromUrl]) return fromUrl;
  const saved = localStorage.getItem("lang");
  if (saved && LANGS[saved]) return saved;
  const nav = (navigator.language || "").toLowerCase();
  if (nav.startsWith("fr")) return "fr";
  if (nav.startsWith("zh")) return "zh-TW";
  return "en";
}

function buildSwitcher(active) {
  const nav = $("lang-switcher");
  nav.replaceChildren();
  Object.keys(LANGS).forEach((code) => {
    const btn = el("button", { text: LANGS[code] });
    btn.type = "button";
    btn.className = code === active ? "active" : "";
    btn.setAttribute("aria-pressed", String(code === active));
    btn.addEventListener("click", () => setLang(code));
    nav.appendChild(btn);
  });
}

function renderExperience(items) {
  const root = $("experience");
  root.replaceChildren();
  items.forEach((e) => {
    const entry = el("div", { class: "entry" });
    const h = el("h3");
    h.append(el("span", { class: "entry-title", text: `${e.company} - ${e.title}` }));
    h.append(el("span", { class: "date", text: e.date }));
    entry.append(h);
    if (e.location) entry.append(el("p", { class: "location", text: e.location }));
    const ul = el("ul");
    (e.bullets || []).forEach((b) => ul.append(el("li", { text: b })));
    entry.append(ul);
    root.append(entry);
  });
}

function renderEducation(items) {
  const root = $("education");
  root.replaceChildren();
  items.forEach((ed) => {
    const entry = el("div", { class: "entry" });
    const h = el("h3");
    h.append(el("span", { class: "entry-title", text: ed.institution }));
    h.append(el("span", { class: "date", text: ed.date }));
    entry.append(h);
    if (ed.detail) entry.append(el("p", { class: "detail", text: ed.detail }));
    root.append(entry);
  });
}

function renderList(id, items) {
  const ul = $(id);
  ul.replaceChildren();
  (items || []).forEach((s) => ul.append(el("li", { text: s })));
}

function render(d, lang) {
  document.documentElement.lang = lang;
  document.body.classList.toggle("lang-cjk", lang === "zh-TW");
  document.title = `${d.name} — ${d.footer_title || d.tagline}`;

  $("name").textContent = d.name;
  $("tagline").textContent = d.tagline;

  const contact = $("contact");
  contact.textContent = d.contact.label;
  contact.href = d.contact.url;

  const pdf = $("pdf-link");
  pdf.textContent = d.ui.download_pdf;
  pdf.href = PDF_FILE[lang];

  $("summary").textContent = d.summary;

  $("h-experience").textContent = d.sections.experience;
  $("h-education").textContent = d.sections.education;
  $("h-skills").textContent = d.sections.skills;
  $("h-languages").textContent = d.sections.languages;

  renderExperience(d.experience);
  renderEducation(d.education);
  renderList("skills", d.skills);
  renderList("languages", d.spoken_languages);
}

async function setLang(lang) {
  try {
    const res = await fetch(`content/${lang}.json`, { cache: "no-cache" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    localStorage.setItem("lang", lang);
    const params = new URLSearchParams(location.search);
    params.set("lang", lang);
    history.replaceState(null, "", `?${params.toString()}`);
    buildSwitcher(lang);
    render(data, lang);
  } catch (err) {
    console.error("Failed to load language:", lang, err);
    $("resume").insertAdjacentHTML(
      "afterbegin",
      `<p class="load-error">Could not load content for "${lang}". Serve this folder over HTTP (e.g. <code>python3 -m http.server</code>).</p>`
    );
  }
}

setLang(pickLang());
