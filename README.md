# 📘 Documentation Technique : API Omicronde (v1.0)

L'API Omicronde est une surcouche de **PyGame 2.6.0+** (Python 3.10+) conçue pour faciliter la gestion des scènes, des calques (layers), de la caméra et des animations.

## 1. Architecture Globale

Le moteur repose sur une structure hiérarchique :

1. **Game** : Gère la fenêtre, la boucle principale et les événements.
2. **Scene** : Gère le monde, les calques et la caméra.
3. **GameObject** : L'unité de base pour tout élément affiché à l'écran.

---

## 2. Initialisation de la Fenêtre (`Game.py`)

La classe `Game` centralise la configuration de l'affichage. Elle gère la mise à l'échelle (scaling) automatique entre la résolution de rendu interne et la taille de la fenêtre.

### Exemple d'initialisation :

```python
from api.Game import Game
import pygame as pg

# Initialise un jeu avec un rendu interne de 640x360 mis à l'échelle dans une fenêtre 1280x720
my_game = Game(
    size=(1280, 720), 
    render_size=(640, 360), 
    name="Mon Jeu Galaxaris", 
    flags=pg.RESIZABLE, 
    fps=60
)

# Lancer la boucle de jeu
my_game.run(mon_code_de_logique)

```

* **Gestion des entrées** : Utilisez `my_game.bind(event_type, callback)` pour lier des fonctions aux événements PyGame.

---

## 3. Gestion du Monde et de la Caméra (`Scene.py` & `GameCamera.py`)

La `Scene` hérite de `pg.Surface`. Elle utilise un système de **layers** pour gérer l'ordre d'affichage.

### Les Calques (Layers)

Le nom du calque définit son comportement :

* **Calque standard** : S'affiche statiquement (UI, HUD).
* **Calque avec `#**` (ex: `"World#1"`) : Les objets sur ce calque sont affectés par le déplacement de la **Caméra**.
* **Calque avec `_**` (ex: `"_background"`) : Calque interne réservé au rendu automatique du fond.

### La Caméra

La caméra permet de suivre un objet ou de se déplacer librement dans le monde.

```python
# Faire en sorte que la caméra suive le joueur
my_game.screen.camera.focus(player_object)
my_game.screen.camera.set_offset((320, 180)) # Centre la caméra

```

---

## 4. Objets de Jeu (`GameObject.py`)

Tout objet (joueur, ennemi, décor) doit hériter ou utiliser `GameObject`. Contrairement au `Sprite` standard, il intègre nativement une position `Vector2` et une gestion de direction.

### Propriétés clés :

* `pos` : Vecteur position `(x, y)`.
* `direction` : `"left"` ou `"right"`.
* `draw(surface, offset)` : Dessine l'objet en appliquant le décalage de caméra si nécessaire.

---

## 5. Systèmes Visuels (`assets/` & `environment/`)

### Animations (`Animation.py`)

Le système d'animation découpe automatiquement une feuille de sprites (sprite sheet) horizontale.

```python
from api.assets.Animation import Animation
from api.assets.Texture import Texture

tex = Texture("player_sheet.png", resource_manager)
anim = Animation(tex, frame_count=8, delay=120)
player.set_animation(anim)

```

### Arrière-plans Parallaxe (`Parallax.py`)

Permet de créer de la profondeur. Plus la `speed` est proche de 1.0, plus l'image suit la caméra. Proche de 0.0, elle reste quasi statique.

```python
from api.environment.Parallax import ParallaxBackground, ParallaxImage

parallax_bg = ParallaxBackground(render_size=(640, 360))
img = ParallaxImage(speed=(0.2, 0.1), texture=sky_texture)
parallax_bg.add(img)

my_scene.set_background(parallax_bg)

```

---