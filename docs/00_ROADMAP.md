# Roadmap Ça Swingue 3

## ✅ Features livrées

| # | Feature | Statut | Commits |
|---|---|---|---|
| ☑️ | Météo 7 jours + réservation (widget, messages WhatsApp) | 🟢 Live | `366fecc` → `d05b505` |
| ☑️ | Carnet de parcours (Vigneux) — notes par trou + présentation | 🟢 Live | `453c7bb` → `c490fd3` |
| ☑️ | Gradient couleur score (Stroke, Stableford, Scramble, Nico, 9pts) | 🟢 Live | `d05b505` → `3577cc2` |
| ☑️ | Icône v3 (badge rouge) + nom PWA « Ça Swingue 3 » | 🟢 Live | `bdf9178` / `26e1488` |

---

## 🚧 En cours / À venir

| # | Feature | Spec | Dev | Test | Statut |
|---|---|---|---|---|---|
| 5 | 🎩 **Caddy Pro (MVP)** — profil + forme + objectif + briefing + alerte | [✅](./CADDY_V3_SCOPE.md) | ☐ | ☐ | Spec validée, à coder |
| 6 | 🛰️ GPS simple au drapeau | ☐ | ☐ | ☐ | À scoper |
| 7 | 📊 Stats cachées (FIR/GIR/putts) | ☐ | ☐ | ☐ | À scoper |
| 8 | 🎒 Usure du matériel | ☐ | ☐ | ☐ | À scoper |
| 9 | 🗺️ Carte satellite du trou | ☐ | ☐ | ☐ | À scoper (après GPS) |

---

## 🎩 Feature 5 — Caddy Pro (MVP v3)

Spec complète : [CADDY_V3_SCOPE.md](./CADDY_V3_SCOPE.md)

Scope v3 (compatible ça_swingue_4 Phase 4b) :

- [ ] `PlayerProfile` — profil joueur durable (tendances, forces, faiblesses)
- [ ] `DailyCheckIn` — check-in forme 30s avant partie (optionnel)
- [ ] `GameObjective` — objectif de la partie (Stableford, sub-90, etc.)
- [ ] Moteur de règles basique (rule-based, offline-first)
- [ ] **Skill S1 — Briefing pré-coup** dans le drawer existant
- [ ] **Skill S2 — Alerte objectif** adaptative dans le drawer

**Hors v3, reporté à ça_swingue_4 Phase 4b** :
- Coaching post-erreur (mental adaptatif)
- Bilan mi-parcours
- Mémoire vive (observations passives)
- Intégration stats Nantes
- Appels Claude API

---

Cocher au fur et à mesure. Chaque feature a son fichier `docs/0X_*.md` ou équivalent.
