#!/usr/bin/env python3
"""Génère un glossaire développement — les termes à comprendre quand on travaille avec une IA."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from datetime import datetime

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "Glossaire_Developpement.docx")

DARK_GREEN = RGBColor(0x00, 0x60, 0x39)
GREEN = RGBColor(0x16, 0xa3, 0x4a)
GREY = RGBColor(0x64, 0x74, 0x8b)
BLUE = RGBColor(0x08, 0x91, 0xb2)
PURPLE = RGBColor(0x7c, 0x3a, 0xed)
ORANGE = RGBColor(0xd9, 0x77, 0x06)

def h1(doc, text, page_break=True):
    if page_break:
        doc.add_page_break()
    tbl = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), 'E6F4EA')
    cell._tc.get_or_add_tcPr().append(shd)
    r = cell.paragraphs[0].add_run(text)
    r.bold = True; r.font.size = Pt(20); r.font.color.rgb = DARK_GREEN
    doc.add_paragraph()

def h2(doc, text, color=None):
    h = doc.add_heading(text, level=2)
    for r in h.runs:
        r.font.color.rgb = color or GREEN
        r.font.size = Pt(15)

def para(doc, text, bold=False, italic=False, size=11, color=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = color

def term_box(doc, emoji, term, english, definition, example, color='E6F4EA'):
    """Bloc définition pour un terme."""
    tbl = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shd)
    # Titre + anglais
    p1 = cell.paragraphs[0]
    r = p1.add_run(f"{emoji}  {term}")
    r.bold = True; r.font.size = Pt(16); r.font.color.rgb = DARK_GREEN
    if english:
        r2 = p1.add_run(f"   ({english})")
        r2.italic = True; r2.font.size = Pt(11); r2.font.color.rgb = GREY
    # Définition
    p2 = cell.add_paragraph()
    r = p2.add_run("En français : ")
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = BLUE
    r2 = p2.add_run(definition)
    r2.font.size = Pt(11)
    # Exemple
    p3 = cell.add_paragraph()
    r = p3.add_run("Dans ton projet : ")
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = GREEN
    r2 = p3.add_run(example)
    r2.italic = True; r2.font.size = Pt(10)
    doc.add_paragraph()

def main():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2); s.bottom_margin = Cm(2)
        s.left_margin = Cm(2); s.right_margin = Cm(2)

    # ═══════════════════════════════════════════════════
    # COUVERTURE
    # ═══════════════════════════════════════════════════
    hero = '/Users/mathieuvirondaud/claude/golf/ça_swingue/site/assets/images/swingue.jpg'
    if os.path.exists(hero):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(hero, width=Inches(6.0))

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("📖")
    r.font.size = Pt(50)

    t = doc.add_heading("Comprendre le développement", level=0)
    for r in t.runs: r.font.color.rgb = DARK_GREEN; r.font.size = Pt(28)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Glossaire des termes techniques\nque tu entendras quand on travaille ensemble")
    r.italic = True; r.font.size = Pt(12); r.font.color.rgb = GREY

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("━━━━━━━━━━━━━━━━━━━━")
    r.font.size = Pt(8); r.font.color.rgb = GREEN

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Chaque terme est expliqué simplement,\navec un exemple tiré de ton projet Ça Swingue.")
    r.font.size = Pt(11); r.font.color.rgb = GREY

    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{datetime.now().strftime('%d/%m/%Y')}  •  Virnaoned")
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = DARK_GREEN

    # ═══════════════════════════════════════════════════
    # 1. L'APPLICATION
    # ═══════════════════════════════════════════════════
    h1(doc, "1. Ce qui concerne l'application")
    para(doc, "Ces mots parlent de ce que ton app SAIT FAIRE pour l'utilisateur.", italic=True)

    term_box(doc, "🎯", "Feature", "fonctionnalité",
        "Une capacité précise que l'app fournit. Une chose qu'un utilisateur peut faire avec.",
        "« Partager sa partie en direct via Firebase » est une feature. « Club Advisor » est "
        "une autre feature. Tu peux ajouter des features une par une.")

    term_box(doc, "📱", "PWA", "Progressive Web App",
        "Une app web qui s'installe comme une vraie app (icône sur l'écran d'accueil, "
        "fonctionne offline, ressemble à une app native) mais sans passer par l'App Store.",
        "Ça Swingue Manager est une PWA. Tu l'as installée en tapant « Partager → Ajouter à "
        "l'écran d'accueil » depuis Safari.")

    term_box(doc, "💾", "localStorage",
        "stockage local (navigateur)",
        "Un espace mémoire de 5-10 Mo dans le navigateur où l'app range ses données "
        "(clé → valeur). Accessible uniquement sur ton appareil, perdu si tu vides les "
        "caches du navigateur.",
        "Tes scores, joueurs, parcours sont dans le localStorage. Les clés sont gm_c "
        "(courses), gm_p (players), gm_h (history), etc.")

    term_box(doc, "🗄", "IndexedDB",
        "base de données locale",
        "Version améliorée du localStorage : 50-250 Mo, structure en tables (stores), "
        "recherches par index. Utile quand on a beaucoup de données.",
        "On n'en utilise pas encore dans Ça Swingue v2. Dans v3, on la prévoyait pour stocker "
        "le cache des cartes satellite et les GPS de greens (qu'on a finalement retirés du "
        "pré-travail).")

    # ═══════════════════════════════════════════════════
    # 2. LE CODE ET LES OUTILS
    # ═══════════════════════════════════════════════════
    h1(doc, "2. Ce qui concerne le code")

    term_box(doc, "📄", "HTML", "HyperText Markup Language",
        "Le langage qui décrit la STRUCTURE d'une page web (titres, paragraphes, boutons).",
        "golf_manager.html est un fichier HTML. Il contient tout le texte et la structure "
        "de Ça Swingue.", color='FEF3C7')

    term_box(doc, "🎨", "CSS", "Cascading Style Sheets",
        "Le langage qui décrit l'APPARENCE (couleurs, tailles, positions).",
        "Les fonds verts, les cartes arrondies, les boutons de Ça Swingue — tout ça, c'est du CSS. "
        "Il est mélangé avec le HTML dans golf_manager.html.", color='FEF3C7')

    term_box(doc, "⚙️", "JavaScript (JS)",
        "langage de programmation navigateur",
        "Le langage qui fait AGIR la page : calculer les scores, envoyer sur Firebase, "
        "réagir aux clics. Tout ce qui n'est pas statique.",
        "Les 15 formats de jeu, le Club Advisor, le partage live — 100% JavaScript. "
        "Écrit dans golf_manager.html.", color='FEF3C7')

    term_box(doc, "🟦", "TypeScript (TS)",
        "JS avec types",
        "JavaScript avec des types en plus (nombres, textes, listes...) pour détecter les "
        "erreurs avant de tourner. Tout TS est compilé en JS avant d'être exécuté.",
        "On envisageait d'utiliser TypeScript pour ça_swingue 4 (le projet fusion) pour "
        "plus de fiabilité. Ça_swingue v2 et v3 restent en JavaScript pur.", color='FEF3C7')

    term_box(doc, "📦", "Module ES",
        "morceau de code réutilisable",
        "Un fichier JS qu'on peut importer dans un autre fichier JS. Au lieu d'avoir 10 000 "
        "lignes dans un seul fichier, on le découpe en modules logiques (un par responsabilité).",
        "On avait créé 6 modules (geo.js, idb-wrapper.js, etc.) pour v3 puis supprimés "
        "par YAGNI (pas encore utilisés).", color='FEF3C7')

    # ═══════════════════════════════════════════════════
    # 3. GIT ET GITHUB
    # ═══════════════════════════════════════════════════
    h1(doc, "3. Git et GitHub — le gestionnaire de versions")
    para(doc, "Git enregistre toutes les modifications du code dans un historique. "
              "GitHub héberge cet historique en ligne et le partage.", italic=True)

    term_box(doc, "📚", "Repo / Repository",
        "dépôt de code",
        "Le dossier complet d'un projet avec tout son historique. Existe en local (sur ton Mac) "
        "ET en ligne sur GitHub.",
        "Ton compte GitHub virondaud a 3 repos liés au golf : caswingue (v2 prod), "
        "caswingue-v3 (évolutions), caswinguetest (test).", color='DBEAFE')

    term_box(doc, "📸", "Commit",
        "instantané des modifications",
        "Une photo figée de ton code à un moment précis, avec un message qui décrit "
        "ce qui a changé.",
        "Chaque fois qu'on corrige un bug, on fait un commit. Ça_swingue v2 a plus de 50 "
        "commits d'historique depuis le démarrage.", color='DBEAFE')

    term_box(doc, "📤", "Push",
        "envoyer",
        "Envoyer tes commits locaux vers GitHub pour les publier en ligne.",
        "Quand tu cliques « Push origin » dans GitHub Desktop, tu pousses tes derniers "
        "commits sur caswingue-v3 (par exemple).", color='DBEAFE')

    term_box(doc, "📥", "Pull",
        "récupérer",
        "Télécharger les commits qui ont été ajoutés en ligne depuis ton dernier push. "
        "Utile si tu travailles depuis plusieurs Macs.",
        "Tu ne pulles pas souvent car tu es seul à pousser. Ça deviendra utile si quelqu'un "
        "d'autre contribue (par exemple sur le projet Birdie Club).", color='DBEAFE')

    term_box(doc, "🌿", "Branch",
        "branche",
        "Une ligne parallèle de développement. Permet de travailler sur une feature sans "
        "risquer de casser la version principale.",
        "On a la branche main (principale). On a brièvement créé « docs/18birdies-recovery-guide » "
        "pour un test de PR, puis supprimée.", color='DBEAFE')

    term_box(doc, "🔀", "PR / Pull Request",
        "demande de fusion",
        "Demande formelle de fusionner une branche dans une autre (typiquement une feature "
        "dans main). Permet de vérifier le code avant qu'il ne rejoigne le projet principal.",
        "On a essayé de créer une PR pour tester, mais c'est sur-dimensionné pour un projet solo. "
        "On pousse directement sur main.", color='DBEAFE')

    # ═══════════════════════════════════════════════════
    # 4. AUTOMATISATIONS
    # ═══════════════════════════════════════════════════
    h1(doc, "4. Automatisations et déploiement")

    term_box(doc, "⚙️", "Workflow",
        "flux de travail auto",
        "Une suite d'actions qui se déclenche automatiquement quand un événement se produit. "
        "Définie dans un fichier .yml sur GitHub.",
        "On a un workflow « deploy.yml » qui dit : à chaque push sur main, prends le "
        "dossier site/ et publie-le sur GitHub Pages.", color='F3E8FF')

    term_box(doc, "🤖", "CI (Continuous Integration)",
        "intégration continue",
        "Un ensemble de vérifications automatiques qui tournent à chaque modification du code "
        "(tests, qualité, compilation...). Évite de casser l'app sans s'en apercevoir.",
        "On avait un workflow CI (supprimé par YAGNI). Il lancera les tests quand on attaquera "
        "les vraies features.", color='F3E8FF')

    term_box(doc, "🚀", "Deploy / Déploiement",
        "mise en ligne",
        "L'action de publier l'app sur un serveur accessible au public.",
        "Quand le workflow deploy.yml se termine, l'app est accessible à "
        "https://virondaud.github.io/caswingue-v3/. Ça prend environ 30 secondes.",
        color='F3E8FF')

    term_box(doc, "📄", "GitHub Pages",
        "hébergement GitHub gratuit",
        "Un service gratuit de GitHub qui publie n'importe quel repo public comme un site web.",
        "Ton URL https://virondaud.github.io/caswingue/ est hébergée sur GitHub Pages.",
        color='F3E8FF')

    # ═══════════════════════════════════════════════════
    # 5. SÉCURITÉ
    # ═══════════════════════════════════════════════════
    h1(doc, "5. Sécurité")

    term_box(doc, "🔒", "CSP",
        "Content Security Policy",
        "Une liste de règles qui dit au navigateur : autorise ces sources, refuse les autres. "
        "Protège contre les scripts malveillants injectés.",
        "Dans golf_manager.html v3, il y a une balise meta CSP qui autorise Firebase, "
        "openmeteo, unpkg — et bloque tout le reste.", color='FEE2E2')

    term_box(doc, "🔑", "Hash SHA-256",
        "empreinte numérique",
        "Une \"signature\" unique de 64 caractères calculée à partir d'un fichier. Si le fichier "
        "change d'un seul octet, l'empreinte change complètement. Permet de vérifier qu'un "
        "fichier n'a pas été modifié.",
        "Dans DEV_STANDARDS on prévoyait de hasher le bundle pour s'assurer qu'un attaquant "
        "n'ait pas modifié le code entre le build et le déploiement.", color='FEE2E2')

    term_box(doc, "🔐", "Token / PAT",
        "jeton d'authentification",
        "Un mot de passe numérique à longue durée de vie qui prouve ton identité sur un service "
        "(GitHub, Firebase...). Plus pratique qu'un mot de passe mais à protéger soigneusement.",
        "Pour pousser les workflows GitHub, il fallait un PAT avec le scope « workflow ». Le "
        "terminal n'avait pas les bons droits donc on a poussé via GitHub Desktop.",
        color='FEE2E2')

    # ═══════════════════════════════════════════════════
    # 6. IA ET CLAUDE CODE
    # ═══════════════════════════════════════════════════
    h1(doc, "6. Ce qui concerne Claude / l'IA")

    term_box(doc, "🧠", "Skill",
        "compétence Claude Code",
        "Une commande préprogrammée qu'on tape dans Claude Code (précédée d'un /). L'IA suit un "
        "script précis au lieu d'improviser.",
        "Dans le projet golf-suivi, on a /onboarding, /planifier-seance, /analyser-parcours, "
        "/bilan-progression. Tu tapes la commande, Claude suit la checklist associée.",
        color='FEF3C7')

    term_box(doc, "🤝", "Claude Code",
        "app IA développeur",
        "L'application de bureau ou terminal d'Anthropic qui permet à Claude d'écrire et "
        "modifier du code directement dans tes dossiers.",
        "C'est avec Claude Code que tu travailles en ce moment. Je peux lire tes fichiers, "
        "exécuter des commandes bash, modifier du code.", color='FEF3C7')

    term_box(doc, "📝", "Prompt",
        "consigne donnée à l'IA",
        "Ce que tu tapes à Claude pour lui faire faire quelque chose. La qualité du prompt "
        "détermine la qualité de la réponse.",
        "« Fais-moi un Word explicatif avec des couleurs » est un prompt. Plus c'est précis, "
        "meilleur est le résultat.", color='FEF3C7')

    term_box(doc, "🎭", "YAGNI",
        "You Aren't Gonna Need It",
        "Principe de développement : « Tu n'en auras pas besoin ». Ne code pas par anticipation "
        "des besoins futurs — ajoute les choses quand elles sont vraiment nécessaires. "
        "Évite le code dormant.",
        "On a appliqué YAGNI à ça_swingue 3 : les modules prévus pour 4 futures features ont "
        "été supprimés. On les recréera seulement quand on décidera de coder ces features.",
        color='FEF3C7')

    # ═══════════════════════════════════════════════════
    # 7. PROJETS EN COURS
    # ═══════════════════════════════════════════════════
    h1(doc, "7. Comprendre la structure de tes projets")

    para(doc, "Tu as 4 projets golf en parallèle. Voici comment ils s'articulent :", bold=True)
    para(doc, "")

    tbl = doc.add_table(rows=5, cols=3)
    tbl.style = 'Light Grid Accent 1'
    hdr = tbl.rows[0].cells
    hdr[0].text = "Projet"; hdr[1].text = "Rôle"; hdr[2].text = "Statut"
    for c in hdr:
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True; r.font.color.rgb = DARK_GREEN
    rows_data = [
        ("ça_swingue/", "App v2 en production, stable, utilisée", "🟢 Ne pas toucher"),
        ("ça_swingue_3/", "Évolutions v2 (4 features prévues)", "🚧 Fondations posées"),
        ("ça_swingue_4/", "Fusion 3 outils (PWA + Nantes + golf-suivi)", "🎯 Plan écrit, pas démarré"),
        ("birdie_club/", "App indépendante championnats multi-user", "🆕 Plan écrit, pas démarré"),
    ]
    for i, (a,b,c) in enumerate(rows_data, 1):
        tbl.rows[i].cells[0].text = a
        tbl.rows[i].cells[1].text = b
        tbl.rows[i].cells[2].text = c

    doc.add_paragraph()
    para(doc, "Chaque projet a sa propre roadmap et sa propre arborescence.")
    para(doc, "Règle d'or : ne jamais modifier un projet depuis un autre (permissions strictes dans "
              "les settings.local.json).", italic=True)

    # ═══════════════════════════════════════════════════
    # 8. COMMANDES UTILES
    # ═══════════════════════════════════════════════════
    h1(doc, "8. Quelques commandes à connaître")

    para(doc, "Des commandes à taper dans GitHub Desktop ou que tu verras passer dans nos échanges :", italic=True)

    cmds = [
        ("📂 Pour lancer ton serveur local", "Double-clic sur Lancer_v3.command", "Ouvre un serveur Python sur le port 8093 pour tester v3 localement"),
        ("🔄 Pour voir tes commits", "GitHub Desktop → sidebar gauche → History", "Liste tous tes commits avec leurs messages"),
        ("📤 Pour publier des changements", "GitHub Desktop → Push origin", "Envoie tes commits locaux vers GitHub"),
        ("👁 Pour voir ton app en prod", "Ouvrir virondaud.github.io/<nom_repo>/", "L'URL publique après déploiement"),
        ("📊 Pour voir les workflows", "GitHub web → onglet Actions", "Statut des derniers runs (verts/rouges)"),
    ]

    for title, cmd, desc in cmds:
        para(doc, title, bold=True, size=12, color=DARK_GREEN)
        p = doc.add_paragraph()
        r = p.add_run("  " + cmd)
        r.font.name = 'Courier New'; r.font.size = Pt(10); r.font.color.rgb = BLUE
        para(doc, "  → " + desc, italic=True, size=10)
        para(doc, "")

    # ═══════════════════════════════════════════════════
    # 9. À RETENIR
    # ═══════════════════════════════════════════════════
    h1(doc, "9. À retenir")

    tbl = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), 'D1FAE5')
    cell._tc.get_or_add_tcPr().append(shd)

    items = [
        ("🎯 Feature", "pour TOI (l'utilisateur final)"),
        ("⚙️ Workflow", "pour l'APP (action automatique sur GitHub)"),
        ("🧠 Skill", "pour CLAUDE (commande IA)"),
        ("📦 Module", "pour le CODE (bloc réutilisable)"),
        ("🚀 Deploy", "pour le DÉPLOIEMENT (mise en ligne)"),
        ("🔒 CSP", "pour la SÉCURITÉ (règles du navigateur)"),
    ]
    for icon_term, role in items:
        p = cell.add_paragraph()
        r = p.add_run(f"▸ {icon_term}  ")
        r.bold = True; r.font.size = Pt(13); r.font.color.rgb = DARK_GREEN
        r2 = p.add_run(f"= {role}")
        r2.font.size = Pt(11)

    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Pas besoin de tout retenir.\nCe document reste ici, tu le consultes quand tu en as besoin.")
    r.italic = True; r.font.size = Pt(12); r.font.color.rgb = GREY

    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("⛳ Ça Swingue Manager — Guide du développeur occasionnel")
    r.bold = True; r.italic = True; r.font.size = Pt(11); r.font.color.rgb = GREEN

    doc.save(OUTPUT)
    print(f"✅ Document créé : {OUTPUT}")
    print(f"📄 Taille : {os.path.getsize(OUTPUT):,} octets")

if __name__ == "__main__":
    main()
