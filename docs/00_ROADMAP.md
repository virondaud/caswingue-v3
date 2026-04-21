# Roadmap Ça Swingue 3

## ✅ Features livrées

| # | Feature | Statut | Commits |
|---|---|---|---|
| ☑️ | Météo 7 jours + réservation (widget, messages WhatsApp) | 🟢 Live | `366fecc` → `d05b505` |
| ☑️ | Carnet de parcours (Vigneux) — notes par trou + présentation | 🟢 Live | `453c7bb` → `c490fd3` |
| ☑️ | Gradient couleur score (Stroke, Stableford, Scramble, Nico, 9pts) | 🟢 Live | `d05b505` → `3577cc2` |
| ☑️ | Icône v3 (badge rouge) + nom PWA « Ça Swingue 3 » | 🟢 Live | `bdf9178` / `26e1488` |
| ☑️ | 🎩 Caddy Pro MVP — profil, check-in, objectif, briefing, alerte | 🟢 Live | `9626ebf` → `7e79a61` |

---

## 🚧 En cours / À venir

| # | Feature | Spec | Dev | Test | Statut |
|---|---|---|---|---|---|
| 6 | 🛰️ GPS simple au drapeau | ☐ | ☐ | ☐ | À scoper |
| 7 | 📊 Stats cachées (FIR/GIR/putts) | ☐ | ☐ | ☐ | À scoper |
| 8 | 🎒 Usure du matériel | ☐ | ☐ | ☐ | À scoper |
| 9 | 🗺️ Carte satellite du trou | ☐ | ☐ | ☐ | À scoper (après GPS) |

---

## 🎩 Feature 5 — Caddy Pro (MVP v3) — ✅ livrée

Spec complète : [CADDY_V3_SCOPE.md](./CADDY_V3_SCOPE.md)

Scope v3 (compatible ça_swingue_4 Phase 4b) :

- [x] `PlayerProfile` — profil joueur durable (main dominante, tendances, forces, faiblesses, style)
- [x] `DailyCheckIn` — check-in forme 30s avant partie (optionnel)
- [x] `GameObjective` — objectif de la partie (Stableford, sub-90, etc.)
- [x] Moteur de règles basique (`runCaddyRules`, rule-based, offline-first)
- [x] **Skill S1 — Briefing pré-coup** dans le drawer du carnet
- [x] **Skill S2 — Alerte objectif** adaptative dans le drawer
- [x] Règles fondamentaux : grip / posture / alignement (trous 1, 7, 13 + mental distracted)
- [x] Règles chemin de club : draw / fade / anti-slice (gauchers + droitiers)

**À tester sur parcours réel** :
- [ ] Pertinence des briefings sur Vigneux
- [ ] Alerte objectif (Stableford) sur une partie complète
- [ ] Priorité des règles (est-ce que les bons messages remontent ?)

**Hors v3, reporté à ça_swingue_4 Phase 4b** :
- Coaching post-erreur (mental adaptatif)
- Bilan mi-parcours
- Mémoire vive (observations passives)
- Intégration stats Nantes
- Appels Claude API

---

Cocher au fur et à mesure. Chaque feature a son fichier `docs/0X_*.md` ou équivalent.
