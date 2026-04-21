# Caddy v3 — Scope et data model

> Version minimale du « caddy professionnel » à implémenter dans ça_swingue_3.
> Structure portable vers ça_swingue_4 Phase 4b sans migration complexe.

---

## 🎯 Scope strict v3

**Dans** (5 briques) :
1. `PlayerProfile` — profil joueur durable (tendances, forces, faiblesses)
2. `DailyCheckIn` — check-in forme en 30 s avant la partie
3. `GameObjective` — objectif de partie (Stableford, sub-90, etc.)
4. **Briefing pré-coup** dans le drawer existant du carnet (enrichi avec profil + forme + objectif + conditions)
5. **Alerte objectif** simple (« tu es dans les clous », « mode attaque », « profite »)

**Hors v3, à faire en v4 Phase 4b** :
- Coaching post-erreur (mental adaptatif)
- Bilan mi-parcours détaillé
- Mémoire vive (observations passives → profil)
- Appels Claude API
- Enrichissement par stats Nantes (% GIR, tendances historiques)

---

## 📦 Data model

### PlayerProfile
Un profil par joueur — stocké dans `DB.players[i].profile`.

```ts
interface PlayerProfile {
  version: 1;
  tendencies: {
    drive: 'fade' | 'draw' | 'straight' | 'unknown';
    irons: 'push' | 'pull' | 'straight' | 'unknown';
    putting: 'short' | 'long' | 'accurate' | 'unknown';
  };
  strengths: string[]; // tags : 'putting', 'wedges', 'driver', 'irons', 'mental', 'short_game'
  weaknesses: string[]; // tags : 'bunker', 'short_putts', 'rough', 'driver_pressure', 'long_irons', 'mental_recovery'
  style: 'aggressive' | 'balanced' | 'conservative';
  notes?: string; // texte libre perso
}
```

**Stockage** : localStorage (v3) → IndexedDB `players` store (v4).
**Sync .md** : exportable au format `01_profil.md` de golf-suivi (compatible v4).

### DailyCheckIn
Par partie — stocké dans `DB.game.checkIn` puis persisté dans l'historique.

```ts
interface DailyCheckIn {
  sleep: 'good' | 'fair' | 'poor';
  physical: 1 | 2 | 3 | 4 | 5; // étoiles
  mental: 'sharp' | 'normal' | 'distracted';
  warmedUp: boolean;
  completedAt: number; // timestamp
}
```

**UI** : bouton optionnel en début de partie. Si sauté, le caddy fonctionne en mode « valeurs neutres ».

### GameObjective
Par partie — stocké dans `DB.game.objective`.

```ts
interface GameObjective {
  type: 'stableford' | 'netVsPar' | 'grossVsPar' | 'brutAbs' | 'personalBest' | 'none';
  target?: number; // 32 (stableford), -5 (net), 90 (brut), etc.
  priority: 'result' | 'learning' | 'fun';
}
```

### CaddyRule
Bibliothèque de règles — chargée au runtime, pas stockée.

```ts
interface CaddyRule {
  id: string;
  skill: 'prebrief' | 'objective_alert';
  when: RuleCondition; // prédicat évalué contre le contexte courant
  say: string | ((ctx: CaddyContext) => string);
  priority: number; // 1-10, plus haut = plus important
  enabled: boolean;
}

interface CaddyContext {
  profile: PlayerProfile;
  checkIn: DailyCheckIn | null;
  objective: GameObjective;
  currentHole: HoleInfo;
  courseNote: HoleNote | null; // note du carnet pour ce trou
  weather: WeatherSnapshot | null;
  roundStats: { played: number, brut: number, net: number, pts: number };
}
```

---

## 🔧 Skills concrets v3

### S1 — Briefing pré-coup (skill `prebrief`)

Injecté dans le drawer du carnet, **si** des notes ou des règles matchent.

Exemple :
```
Trou 4 — Par 4, 346m
🚩 Ta cible : 230m centre-gauche (Bois 5 habituel)
⚠️ Bunker droit à 220m
🎯 Attaque front du green
💨 Vent de face aujourd'hui — prends 1 club de plus au 2e coup
🧠 Tu tends à tirer à droite avec driver (profil) → Bois 5 idéal ici
```

**Sources** :
- Carnet du trou : distances, dangers, stratégie
- Conditions : météo live (déjà en place)
- Profil joueur : tendances qui match ce trou (ex. dog-leg gauche + joueur qui fade)
- Forme : adapte le ton (si épuisé, « simplifie, vise le centre du fairway »)

### S1.b — Règles du caddy pro (depuis 2026-04-21)

Le caddy respecte ces principes **systématiquement** :

1. **Distances contextualisées** — jamais afficher une distance depuis le tee pour un élément qui concerne le 2ᵉ coup.
   - Bunker fairway au tee shot : distance **depuis le tee** (ex. « bunker droit 211m »)
   - Même bunker vu depuis le green (2ᵉ coup) : distance **depuis le centre du green** (ex. « bunker 44m avant green »)
   - Bunker greenside : distance **depuis le centre du green** (ex. « bunker arrière 10m »)

2. **Taille du green** dérivée des 4 bords (green_front/back/left/right) :
   - Longueur (front→back) × Largeur (left→right)
   - Affichée comme « Green ≈ 20m × 12m » dans la présentation du trou

3. **Visée idéale = repère visuel sur le terrain**, jamais une distance brute.
   - Le label doit décrire un point repérable : « angle du fairway avec la forêt droite », « grand pin à gauche », « coin du bunker »
   - Le marker SVG est une flèche tee→visée (sans distance numérique)

4. **Recommandation de club** basée sur les distances réelles du joueur :
   - Match de `teeShot.targetDistance` vs plein coup du joueur (tolérance ±8m)
   - Privilégie un club qui atteint ou dépasse légèrement la cible
   - Règle `club_rec_teeshot` dans `CADDY_RULES`

5. **Stratégie par longueur de trou** :
   - Par 4 long (> 320m) : anticiper le 2ᵉ coup (wedge, fer 9)
   - Par 4 court (< 280m) : privilégier le placement sur la longueur
   - Règles `strategy_long_par4` / `strategy_short_par4`

### S2 — Alerte objectif (skill `objective_alert`)

Bandeau discret dans le drawer, adaptatif selon l'avancée :

| Contexte | Message |
|---|---|
| Après 3 trous, en avance sur objectif | « Tu tiens la cadence, reste sur ton plan » |
| Après 6 trous, retard de 5 pts | « Encore jouable, priorité fairway, pas de risque » |
| Après 12 trous, hors d'atteinte | « Objectif derrière, profite et travaille le rythme » |
| Après 12 trous, pile sur objectif | « Tenir les 6 derniers comme les 12 premiers » |

---

## 🗂 Compatibilité v4

- `PlayerProfile` → exporté en `.md` golf-suivi (sync bidirectionnelle)
- `DailyCheckIn` et `GameObjective` → stockés dans la partie, historisés
- Règles de `CaddyRule` → enrichies en v4 par les stats Nantes et la conversation Claude

**Pas de migration** en passant de v3 à v4 : les mêmes structures JSON sont lisibles.

---

## 📅 Ordre d'implémentation proposé

1. **Profil joueur** (édition dans Joueurs / profil perso) — 2h
2. **Check-in forme** (modal pré-partie, skippable) — 1h
3. **Objectif de partie** (modal après check-in ou setup) — 1h
4. **Moteur de règles** (rule engine basique) — 2h
5. **Briefing pré-coup** dans drawer (intégration) — 2h
6. **Alerte objectif** dans drawer — 1h

**Total estimé : ~1 semaine** pour le MVP Caddy v3.

---

_Créé par Virnaoned · v3 scope validé le 2026-04-21_
