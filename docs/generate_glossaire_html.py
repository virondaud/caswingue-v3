#!/usr/bin/env python3
"""Génère le glossaire développement au format HTML à partir de glossaire_data.json.

HTML features :
- Recherche instantanée (filtre les fiches en live)
- Sommaire cliquable (ancres)
- Responsive mobile
- Mode sombre automatique (prefers-color-scheme)
- Styles par section (même palette que le docx)
"""
import os, json, html
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "glossaire_data.json")
OUTPUT = "/Users/mathieuvirondaud/claude/Glossaire_Developpement.html"


def esc(text):
    if text is None:
        return ""
    return html.escape(text)


def term_html(t, section_color, section_hue):
    return f'''
    <article class="term" data-search="{esc(t['term'].lower())} {esc(t.get('english', '').lower())} {esc(t['definition'].lower())} {esc(t['example'].lower())}">
      <header>
        <span class="emoji">{t['emoji']}</span>
        <h3>{esc(t['term'])}</h3>
        {f'<span class="english">({esc(t["english"])})</span>' if t.get('english') else ''}
      </header>
      <p class="definition"><strong>En français :</strong> {esc(t['definition'])}</p>
      <p class="example"><strong>Dans ton projet :</strong> <em>{esc(t['example'])}</em></p>
    </article>
    '''


def section_html(section):
    terms_html = '\n'.join(term_html(t, section['color'], section['hue']) for t in section['terms'])
    intro_html = f'<p class="intro">{esc(section["intro"])}</p>' if section.get('intro') else ''
    return f'''
    <section id="section-{section['num']}" class="section hue-{section['hue']}">
      <h2>{section['num']}. {esc(section['title'])}</h2>
      {intro_html}
      <div class="terms">
        {terms_html}
      </div>
    </section>
    '''


def render(data):
    meta = data['meta']
    sections_html = '\n'.join(section_html(s) for s in data['sections'])

    # Section 7 — projets
    pt = data['projects_table']
    pt_rows = '\n'.join(f'<tr><td><code>{esc(r[0])}</code></td><td>{esc(r[1])}</td><td>{esc(r[2])}</td></tr>' for r in pt['rows'])
    projects_html = f'''
    <section id="section-{pt['num']}" class="section hue-green">
      <h2>{pt['num']}. {esc(pt['title'])}</h2>
      <p class="intro"><strong>{esc(pt['intro'])}</strong></p>
      <table class="projects-table">
        <thead><tr><th>Projet</th><th>Rôle</th><th>Statut</th></tr></thead>
        <tbody>{pt_rows}</tbody>
      </table>
      <p class="note"><em>{esc(pt['note'])}</em></p>
    </section>
    '''

    # Section 8 — commandes
    cm = data['commands']
    cmd_blocks = '\n'.join(
        f'''<div class="cmd-block">
          <h4>{esc(title)}</h4>
          <code class="cmd">{esc(cmd)}</code>
          <p class="cmd-desc">→ {esc(desc)}</p>
        </div>''' for title, cmd, desc in cm['items']
    )
    commands_html = f'''
    <section id="section-{cm['num']}" class="section hue-green">
      <h2>{cm['num']}. {esc(cm['title'])}</h2>
      <p class="intro">{esc(cm['intro'])}</p>
      {cmd_blocks}
    </section>
    '''

    # Section 9 — à retenir
    rc = data['recap']
    recap_items = '\n'.join(f'<li><strong>{esc(icon)}</strong> = {esc(role)}</li>' for icon, role in rc['items'])
    recap_html = f'''
    <section id="section-{rc['num']}" class="section hue-green recap">
      <h2>{rc['num']}. {esc(rc['title'])}</h2>
      <ul class="recap-list">{recap_items}</ul>
      <p class="note text-center"><em>Pas besoin de tout retenir. Ce document reste ici, tu le consultes quand tu en as besoin.</em></p>
    </section>
    '''

    # Sommaire
    toc_items = []
    for s in data['sections']:
        toc_items.append((s['num'], s['title']))
    toc_items.append((pt['num'], pt['title']))
    toc_items.append((cm['num'], cm['title']))
    toc_items.append((rc['num'], rc['title']))
    toc_items.sort(key=lambda x: x[0])
    toc_html = '\n'.join(f'<li><a href="#section-{num}">{num}. {esc(title)}</a></li>' for num, title in toc_items)

    today = datetime.now().strftime('%d/%m/%Y')

    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(meta['title'])} — Glossaire</title>
<style>
:root {{
  --bg: #f7f5f2;
  --bg-card: #ffffff;
  --ink: #2c2620;
  --ink-soft: #6b6258;
  --ink-mute: #a59c90;
  --brand: #00603b;
  --brand-soft: #16a34a;
  --accent-blue: #0891b2;
  --accent-green: #16a34a;
  --line: #e5ddd0;
  --hue-green: #E6F4EA;
  --hue-yellow: #FEF3C7;
  --hue-blue: #DBEAFE;
  --hue-purple: #F3E8FF;
  --hue-red: #FEE2E2;
  --shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #1a1614;
    --bg-card: #2a2320;
    --ink: #f0ece6;
    --ink-soft: #c8bfb3;
    --ink-mute: #8b8074;
    --line: #3d332c;
    --hue-green: #0f3b22;
    --hue-yellow: #3d3410;
    --hue-blue: #0d2e4a;
    --hue-purple: #2e1a3d;
    --hue-red: #3d1a1a;
    --shadow: 0 1px 3px rgba(0,0,0,0.3), 0 4px 12px rgba(0,0,0,0.2);
  }}
}}

* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}}

.app-header {{
  position: sticky;
  top: 0;
  background: var(--bg);
  z-index: 100;
  border-bottom: 1px solid var(--line);
  padding: 16px 20px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}}
.app-header h1 {{
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 700;
  color: var(--brand);
}}
.app-header .meta {{
  color: var(--ink-mute);
  font-size: 13px;
  margin-bottom: 12px;
}}
.search-wrap {{
  position: relative;
}}
#search {{
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 1px solid var(--line);
  border-radius: 10px;
  font-size: 15px;
  background: var(--bg-card);
  color: var(--ink);
  font-family: inherit;
}}
#search:focus {{
  outline: none;
  border-color: var(--brand-soft);
  box-shadow: 0 0 0 3px rgba(22,163,74,0.12);
}}
.search-wrap::before {{
  content: '🔍';
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 15px;
}}

main {{
  max-width: 820px;
  margin: 0 auto;
  padding: 20px;
}}

.toc {{
  background: var(--bg-card);
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 28px;
  box-shadow: var(--shadow);
}}
.toc h2 {{
  margin: 0 0 10px;
  font-size: 14px;
  color: var(--ink-mute);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  font-weight: 600;
}}
.toc ul {{
  list-style: none;
  padding: 0;
  margin: 0;
  columns: 2;
  column-gap: 20px;
}}
.toc li {{
  margin: 4px 0;
  break-inside: avoid;
}}
.toc a {{
  color: var(--ink);
  text-decoration: none;
  font-size: 14px;
  padding: 3px 0;
  display: inline-block;
}}
.toc a:hover {{ color: var(--brand); text-decoration: underline; }}

.section {{
  margin: 40px 0;
  scroll-margin-top: 130px;
}}
.section h2 {{
  font-size: 22px;
  color: var(--brand);
  border-bottom: 2px solid var(--brand);
  padding-bottom: 8px;
  margin-bottom: 14px;
}}
.section .intro {{
  color: var(--ink-soft);
  font-style: italic;
  margin-bottom: 20px;
  font-size: 14px;
}}

.terms {{
  display: flex;
  flex-direction: column;
  gap: 14px;
}}

.term {{
  background: var(--hue-green);
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: var(--shadow);
}}
.hue-yellow .term {{ background: var(--hue-yellow); }}
.hue-blue .term {{ background: var(--hue-blue); }}
.hue-purple .term {{ background: var(--hue-purple); }}
.hue-red .term {{ background: var(--hue-red); }}

.term header {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}}
.term .emoji {{
  font-size: 22px;
  line-height: 1;
}}
.term h3 {{
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--brand);
}}
.term .english {{
  font-size: 13px;
  color: var(--ink-mute);
  font-style: italic;
}}
.term p {{
  margin: 6px 0;
  font-size: 14px;
  color: var(--ink);
}}
.term .definition strong {{ color: var(--accent-blue); }}
.term .example strong {{ color: var(--accent-green); }}
.term .example em {{
  font-size: 13px;
  color: var(--ink-soft);
}}

.term.hidden {{ display: none; }}

.section.empty h2 + .terms::after {{
  content: 'Aucun résultat dans cette section';
  color: var(--ink-mute);
  font-style: italic;
  padding: 12px;
  display: block;
}}

.projects-table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-card);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: var(--shadow);
  margin: 10px 0;
  font-size: 14px;
}}
.projects-table th {{
  background: var(--hue-green);
  padding: 10px 12px;
  text-align: left;
  color: var(--brand);
  font-weight: 600;
}}
.projects-table td {{
  padding: 10px 12px;
  border-top: 1px solid var(--line);
}}
.projects-table code {{
  background: var(--hue-yellow);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}}

.cmd-block {{
  background: var(--bg-card);
  padding: 14px 18px;
  border-radius: 10px;
  margin: 10px 0;
  box-shadow: var(--shadow);
  border-left: 3px solid var(--brand-soft);
}}
.cmd-block h4 {{
  margin: 0 0 6px;
  font-size: 14px;
  color: var(--brand);
}}
.cmd-block .cmd {{
  display: block;
  background: var(--bg);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  color: var(--accent-blue);
  margin: 6px 0;
}}
.cmd-block .cmd-desc {{
  font-size: 13px;
  color: var(--ink-soft);
  font-style: italic;
  margin: 4px 0 0;
}}

.recap {{ background: var(--hue-green); border-radius: 12px; padding: 20px 24px; }}
.recap-list {{
  list-style: none;
  padding: 0;
  margin: 10px 0;
}}
.recap-list li {{
  padding: 8px 0;
  border-bottom: 1px solid var(--line);
  font-size: 15px;
}}
.recap-list li:last-child {{ border: none; }}

.note {{ color: var(--ink-mute); font-size: 13px; }}
.text-center {{ text-align: center; }}

footer.page-footer {{
  margin: 40px 0 20px;
  padding: 20px;
  text-align: center;
  color: var(--ink-mute);
  font-size: 13px;
  border-top: 1px solid var(--line);
}}
footer.page-footer a {{ color: var(--brand); text-decoration: none; }}
footer.page-footer a:hover {{ text-decoration: underline; }}

@media (max-width: 600px) {{
  .toc ul {{ columns: 1; }}
  .app-header h1 {{ font-size: 17px; }}
}}
</style>
</head>
<body>

<header class="app-header">
  <h1>📖 {esc(meta['title'])}</h1>
  <div class="meta">{esc(meta['subtitle'])} · {today} · <a href="Glossaire_Developpement.docx" style="color:var(--brand);text-decoration:none">📄 Version Word</a></div>
  <div class="search-wrap">
    <input id="search" type="search" placeholder="Rechercher un terme, une définition…" autocomplete="off">
  </div>
</header>

<main>
  <nav class="toc" aria-label="Sommaire">
    <h2>Sommaire</h2>
    <ul>{toc_html}</ul>
  </nav>

  {sections_html}
  {projects_html}
  {commands_html}
  {recap_html}

  <footer class="page-footer">
    ⛳ Guide du développeur occasionnel — {esc(meta['author'])}<br>
    Source : <code>glossaire_data.json</code> · Régénérable via <code>/glossaire &lt;terme&gt;</code> dans Claude Code
  </footer>
</main>

<script>
const input = document.getElementById('search');
const terms = document.querySelectorAll('.term');
const sections = document.querySelectorAll('.section');

function filter() {{
  const q = input.value.trim().toLowerCase();
  terms.forEach(t => {{
    const hay = t.dataset.search;
    t.classList.toggle('hidden', q && !hay.includes(q));
  }});
  sections.forEach(s => {{
    const visible = [...s.querySelectorAll('.term')].some(t => !t.classList.contains('hidden'));
    const hasTerms = s.querySelector('.term');
    if (hasTerms) s.style.display = visible ? '' : 'none';
  }});
}}

input.addEventListener('input', filter);
input.addEventListener('keydown', e => {{ if (e.key === 'Escape') {{ input.value = ''; filter(); }} }});
</script>

</body>
</html>
'''


def main():
    with open(DATA, encoding='utf-8') as f:
        data = json.load(f)
    out = render(data)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f"✅ HTML créé : {OUTPUT}")
    print(f"📄 Taille : {os.path.getsize(OUTPUT):,} octets")


if __name__ == "__main__":
    main()
