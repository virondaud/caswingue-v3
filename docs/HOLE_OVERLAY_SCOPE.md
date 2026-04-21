# Carte du trou — Surcouche SVG (scope)

> Feature 9 de la roadmap. Superpose un SVG interactif sur l'image schéma du trou
> pour matérialiser tee, green, visée, dangers et arcs de distance à partir des coords GPS.

---

## 🎯 Objectif

Transformer l'image statique `assets/Parcours/Vigneux/vigneux_trou_X.png` en **carte intelligente** :

- Marqueurs positionnés aux vraies coords GPS
- Flèche de visée dérivée du landing zone + tendance du joueur
- Arcs de distance (100/150/200 m) centrés sur le tee
- Zone de lay-up optionnelle

**Pas** de tuiles satellites, pas de Leaflet, pas de licence commerciale. Juste du SVG vanilla sur image PNG.

---

## 🧭 Principe de projection

Pour projeter un point GPS sur l'image il faut **calibrer** deux ancres :

```
teePx   ↔  coordsTee   (pixel,  GPS)
greenPx ↔  coordsGreen (pixel,  GPS)
```

Ensuite, pour n'importe quel point GPS `P` :

1. Calcul du vecteur GPS tee→P en mètres (ΔN, ΔE) via haversine
2. Calcul de l'échelle pixel/mètre depuis la distance tee→green (GPS et pixel)
3. Calcul de la rotation : angle de l'axe tee→green dans l'image vs azimut GPS
4. Application de la transformation affine → `(x, y)` en pixels

Formule compacte :

```js
function gpsToPx(lat, lng, cal){
  const bGPS = gpsBearing(cal.teeLat, cal.teeLng, lat, lng);
  const dM   = gpsDistanceM(cal.teeLat, cal.teeLng, lat, lng);
  const bImg = cal.bearingImg; // angle axe tee→green dans l'image
  const bAxis= cal.bearingGPS; // azimut GPS tee→green
  const θ    = ((bGPS - bAxis) * Math.PI) / 180; // angle relatif à l'axe
  const pxPerM = cal.pxPerM;
  const dx = Math.sin(θ) * dM * pxPerM;
  const dy = -Math.cos(θ) * dM * pxPerM;
  // rotation pour tenir compte de l'axe image
  const α  = (bImg * Math.PI) / 180;
  return {
    x: cal.teePx.x + dx*Math.cos(α) - dy*Math.sin(α),
    y: cal.teePx.y + dx*Math.sin(α) + dy*Math.cos(α)
  };
}
```

Précision attendue : **±2-5 m** si la calibration tee/green est propre au pixel près. Largement suffisant pour de la stratégie de jeu, pas pour du GPS range finder au cm.

---

## 📦 Data model

Ajout dans `DB.courseNotebooks[courseId][holeIdx]` :

```ts
interface HoleCalibration {
  version: 1;
  imageSize: { w: number; h: number };  // dimensions image en pixels
  teePx:    { x: number; y: number };   // ancre tee dans l'image
  greenPx:  { x: number; y: number };   // ancre green dans l'image
}
```

Les coords GPS `coordsTee` et `coordsGreen` sont déjà dans le modèle actuel.

Les `dangers[].coords` sont déjà dans le modèle ; ils s'afficheront auto si calibration présente.

---

## 🛠 Flux de calibration (one-shot par trou)

Dans le modal plein écran (`openHoleMapFullscreen`) :

1. Bouton 🎯 **Calibrer** en haut → passe en mode calibration
2. Étape 1 : « Tape sur le départ blanc » → l'app enregistre (xTee, yTee)
3. Étape 2 : « Tape sur le centre du green » → l'app enregistre (xGreen, yGreen)
4. Sauvegarde `calibration` dans la note → sortie du mode calibration
5. Les marqueurs apparaissent immédiatement au bon endroit

Bouton 🔁 **Recalibrer** pour refaire l'opération.

---

## 🎨 Éléments rendus

Quand `calibration` existe, le SVG superpose :

| Élément | Condition | Style |
|---|---|---|
| 🚩 Marqueur tee | toujours | Cercle vert 12px + label « TEE » |
| ⛳ Marqueur green | toujours | Cercle jaune 14px + label « GREEN » |
| ➤ Flèche de visée | `teeShot.targetDistance` + `landingZone` | Ligne + pointe, orientée selon le landing (left/center/right) depuis le tee |
| 🔴 Cercle danger | `dangers[i].coords` | Rouge/orange selon type (bunker, water, trees) + label distance |
| 📏 Arcs distance | toujours | 100/150/200 m depuis le tee, pointillé gris |
| 🎯 Zone lay-up | `approach.targetBeforePin` > 0 | Zone pointillée avant green |

Les arcs 100/150/200 m aident à **lire les distances dangers sans ruban à mesurer**.

---

## 🖱 Interactions

- **Tap sur un marqueur danger** → popover avec `label` + distance depuis tee + distance jusqu'au green
- **Tap sur flèche de visée** → popover avec distance cible + club habituel + club advisor météo
- **Long-press sur l'image** → ajouter un nouveau danger à la position tapée (reverse project → GPS)
- **Pinch-zoom** (natif mobile) pour inspecter un secteur

---

## 📐 Rendu SVG responsive

```html
<div class="map-wrap" style="position:relative">
  <img src="..." style="display:block;width:100%">
  <svg style="position:absolute;inset:0;width:100%;height:100%" viewBox="0 0 IMG_W IMG_H" preserveAspectRatio="xMidYMid meet">
    <!-- markers -->
  </svg>
</div>
```

Le `viewBox` calé sur les dimensions natives de l'image garantit que les coordonnées SVG correspondent aux pixels de l'image quelle que soit la taille d'affichage.

---

## ✅ Scope strict v3

**Dans** :
- [ ] `HoleCalibration` dans le data model
- [ ] Mode calibration tap-tee-puis-green
- [ ] Projection GPS → pixel (`gpsToPx`)
- [ ] Marqueurs tee + green + dangers (depuis données existantes)
- [ ] Flèche de visée depuis `teeShot.targetDistance` + `landingZone`
- [ ] Arcs de distance 100/150/200 m
- [ ] Popover au tap sur marqueur danger
- [ ] Sauvegarde calibration dans la note

**Hors v3, reporté** :
- Long-press pour ajouter un danger (reverse projection)
- Zoom natif pinch (doit marcher via CSS si l'image est zoomable)
- Overlay en mode partie (intégration dans la vue `playing`) — à faire dans une itération ultérieure
- Animation flèche / trajectoire
- Intégration vent (flèche dérive)
- Multi-tees (jaune/bleu/rouge) — une seule calibration sur le tee par défaut

---

## 📅 Effort estimé

| Tâche | Heures |
|---|---|
| Helpers math `gpsToPx` + tests | 1h |
| Mode calibration (UI + save) | 2h |
| Rendu SVG marqueurs tee/green/dangers | 1.5h |
| Flèche de visée + arcs distance | 1.5h |
| Popover interactions | 1h |
| Polish + tests sur trou 1 Vigneux | 1h |

**Total : ~8h** (1 journée).

---

## 🔗 Dépendances

- Image locale dans `site/assets/Parcours/<Course>/<hole>.png` ✓ (trou 1 déjà là)
- `coordsTee` + `coordsGreen` saisis par trou ✓ (trou 1 déjà là)
- `dangers[].coords` saisis ✓ (trou 1 déjà là)
- Aucune librairie externe — SVG natif

---

## 🗂 Compatibilité v4

Le modèle `HoleCalibration` est pur JSON, portable sans migration vers IndexedDB.
L'image reste dans `assets/` du build v4, le chemin reste relatif.

---

_Créé le 2026-04-21 · scope de la feature 9 Carte satellite._
