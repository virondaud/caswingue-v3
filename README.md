# Ça Swingue Manager — v3 (évolutions)

> Projet parallèle à `ça_swingue/` pour développer les nouvelles fonctionnalités
> sans risquer la version stable en production.

**Statut** : 🚧 Chantier · Base = copie de Ça Swingue v2.0 au 20/04/2026

---

## 🎯 Objectif

Ajouter 4 fonctionnalités majeures à la PWA, validées une par une, puis
décider si on les re-merge dans `ça_swingue/` ou si `ça_swingue_3` devient
la nouvelle branche principale.

---

## 📋 Features à implémenter (à valider avant de coder)

### 1. 🛰️ GPS simple au drapeau

**Problème** : en partie, il faut ouvrir 18Birdies pour connaître la distance au green, ce qui casse le flow.

**Solution** : bouton compact sur la vue Playing qui utilise `navigator.geolocation` et retourne la distance vers le centre, l'avant et l'arrière du green du trou en cours.

**Scope** :
- Coordonnées GPS par trou (centre green) stockées dans Course
- `navigator.geolocation.getCurrentPosition()` + haversine
- Affichage dans le header du trou : `🏴 138m • ⏩ 132m • ⏪ 145m`
- Fallback gracieux si permissions refusées / offline
- Collecte : 1 fois, au trou, l'utilisateur "marque le drapeau" et les coords sont enregistrées pour ce parcours (crowd-sourcing implicite)

**Estimation** : 1 semaine

---

### 2. 📊 Stats cachées par trou (FIR / GIR / Putts)

**Problème** : ça_swingue stocke le score brut mais pas les stats clés qui expliquent le score.

**Solution** : saisie ultra-légère après chaque trou, 3 toggles + 1 compteur.

**Scope** :
- Pour chaque trou : FIR (fairway touché oui/non/NA sur par 3), GIR (green in regulation), putts (nombre)
- Saisie inline dans la scoreRow (pas de modal)
- Agrégation automatique : % FIR, % GIR, moyenne putts
- Stats globales par joueur dans la vue Stats
- Détection auto du GIR (si score <= par - 2, GIR obligatoire)

**Estimation** : 1 semaine

---

### 3. 🎒 Usure du matériel

**Problème** : on ne sait pas quand changer ses gants, ses balles, ses grips.

**Solution** : compteur passif par partie, alertes au seuil.

**Scope** :
- Par joueur, enregistrement du matériel courant (date d'achat, état)
- À chaque partie terminée, incrémenter compteurs (parties, trous)
- Seuils d'alerte configurables (par défaut : gants 20 parties, balles 3, grips 150)
- Badge "À renouveler" sur les items concernés
- Historique des changements (pour voir la durée de vie réelle)

**Estimation** : 3-4 jours

---

### 4. 🗺️ Carte satellite du trou

**Problème** : voir un trou avant de jouer aide à visualiser la stratégie.

**Solution** : image statique Google Maps / OpenStreetMap centrée sur le trou.

**Scope** :
- Si coordonnées GPS disponibles (voir feature 1), afficher une image statique
- OSM tiles ou Mapbox static image API (gratuit < 50k req/mois)
- Zoom adapté à la longueur du trou
- Overlay optionnel : position du tee, du green, distances
- Cache local du bitmap pour usage offline

**Estimation** : 1 semaine

---

## 📅 Roadmap

| Phase | Features | Durée estimée |
|---|---|---|
| **P1** | GPS + Stats cachées | 2 semaines |
| **P2** | Usure matériel | 3-4 jours |
| **P3** | Carte satellite | 1 semaine |
| **Total** | | **~4 semaines** |

---

## 🔀 Stratégie de déploiement

- **Branche séparée** : `v3-dev` sur le repo GitHub, sous-chemin `/v3/` si déployé en prod
- **Pas de sync avec `ça_swingue/`** pendant le dev (éviter les régressions)
- **Tests intensifs** sur appareil réel avant de proposer la fusion
- **Rollback facile** : les données utilisateur restent compatibles v2 (structures étendues, pas modifiées)

---

## 📦 Structure

```
ça_swingue_3/
├── site/                   # Copie de l'app v2.0 au départ
│   └── golf_manager.html   # Tout le code
├── docs/                   # Spécifications des features
│   └── 01_gps.md
│   └── 02_stats_cachees.md
│   └── ...
├── .claude/
│   ├── CLAUDE.md           # Brief Claude
│   └── settings.local.json
└── README.md               # Ce fichier
```

---

## 🤝 Validation

Chaque feature doit être **validée par l'utilisateur** (scope, UI, data model)
avant d'être codée. L'IA produit des maquettes textuelles avant d'attaquer.
