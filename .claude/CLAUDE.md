# Ça Swingue Manager v3 — Brief Claude

## 🎯 Mission

Tu interviens sur **Ça Swingue 3**, une branche d'évolution de la PWA golf
`ça_swingue/` (v2.0 stable). Ton rôle : développer 4 nouvelles features
sans casser la compatibilité avec les données existantes.

## 📏 Standards à respecter

Ce projet est soumis aux **Dev Standards** communs : `/Users/mathieuvirondaud/claude/golf/DEV_STANDARDS.md`.

Pour ça_swingue_3 spécifiquement (partie "évolutions" sur base v2.0) :
- 🟡 **Pas de refactor complet** — on garde l'architecture monolithique de v2.0 pour ne pas casser
- ✅ **Ajout obligatoire** : hash SHA-256 du fichier principal + CSP strict dans le HTML
- ✅ **IndexedDB progressif** : les nouvelles features (GPS coords, stats FIR/GIR/putts) stockent en IndexedDB parallèle à localStorage
- ⚠️ **Tests recommandés** : au moins pour les nouvelles fonctions (calcul haversine GPS, agrégation FIR/GIR)
- ✅ **Chiffrement recommandé** pour les coordonnées GPS des greens (données potentiellement sensibles si user très identifiable)

Voir la matrice complète dans DEV_STANDARDS.md section 9.

## 📍 Contexte projet

- **Base de code** : `site/golf_manager.html` est une copie exacte de
  `ça_swingue/site/golf_manager.html` au 20/04/2026 (commit `86f27e9`).
- **Version parent** : Ça Swingue v2.0 (version déployée à
  `https://virondaud.github.io/caswingue/`).
- **Ne jamais toucher** au dossier `ça_swingue/` depuis ce projet.
- **Ne jamais déployer** à la même URL que la v2.0 tant que la validation n'est
  pas complète.

## 📋 Features prioritaires

1. **GPS simple au drapeau** — distance centre/avant/arrière green via
   `navigator.geolocation`. Crowd-sourcing des coordonnées greens au fil des parties.
2. **Stats cachées** — FIR / GIR / putts saisis inline à chaque trou.
3. **Usure du matériel** — compteurs passifs + alertes de renouvellement.
4. **Carte satellite du trou** — image statique OSM/Mapbox centrée.

Voir `README.md` pour les spécifications détaillées.

## 🔒 Règles immuables

- **Proposer avant de coder** : toute feature doit faire l'objet d'une
  spécification textuelle validée (data model, UI, edge cases).
- **Compatibilité données v2.0** : les nouvelles structures étendent les
  anciennes, jamais de breaking change. Un utilisateur qui fait un export v2
  puis un import v3 doit retrouver ses données.
- **Saisies minimales** : chaque nouvelle saisie coûte en friction utilisateur.
  Viser ≤ 2 taps par trou pour toute nouvelle donnée.
- **Offline-first** : toute feature doit fonctionner sans réseau, les synchros
  Firebase sont secondaires.

## 🧭 Workflow

1. Lire `README.md` pour le scope
2. Lire `docs/0X_<feature>.md` pour la spec (si elle existe)
3. Sinon, proposer la spec avant tout code
4. Coder dans `site/golf_manager.html`
5. Tester localement avec serveur Python (`site/` servi sur port 8093)
6. Commit avec message descriptif (pas de push auto vers le repo v2)

## 📦 Données existantes v2.0

Les structures importantes sont décrites dans le brief v2.0 du projet parent.
Les plus utilisées :

- `DB.courses[]` : parcours avec `holes[{par, handicap, distBlanc, distJaune}]`
- `DB.players[]` : joueurs avec `clubs[]`, `puttCal`, `globalCode`
- `DB.game` et `DB.history[]` : parties
- `DB.practice[]` : sessions d'entraînement (inclut linkedGameId auto)

## 📝 Proposer une feature — checklist

Avant d'attaquer le code :

- [ ] Data model (quels nouveaux champs, dans quelle structure)
- [ ] UI (sketchs textuels, taps nécessaires)
- [ ] Edge cases (offline, permissions refusées, données manquantes)
- [ ] Compatibilité v2 (migration automatique si besoin)
- [ ] Estimation (jours de dev)

Valider tout ça avec l'utilisateur avant de toucher `golf_manager.html`.

---

_Maintenu par Virnaoned · v3 démarré le 2026-04-20_
