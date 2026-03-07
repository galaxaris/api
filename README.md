# 📘 Documentation Technique : API Omicronde (vBeta)

L'API Omicronde est un moteur de jeu orienté objet (similaire à Unity) agissant comme une surcouche de PyGame 2.6.0+ (Python 3.10+).

## 1. Architecture Globale

L'API est divisée en plusieurs sous-modules spécialisés :

* **assets** : Gestion des textures, animations et de l'audio.
* **engine** : Cœur du rendu, gestion des scènes et de la caméra.
* **entity** : Entités mobiles soumises à la physique et aux entrées.
* **environment** : Décors, environnements solides, parallaxe et déclencheurs (triggers).
* **items** : Objets en jeu (inventaire, armes).
* **physics** : Collisions prédictives et calculs de trajectoire.
* **UI** : Éléments d'interface utilisateur (boutons, boîtes de dialogue, menus).
* **utils** : Gestionnaires globaux, entrées (inputs), polices et outils de débogage.

---

## 2. Le Moteur (Engine)

### 2.1. La classe `Game` (`Game.py`)

La classe `Game` centralise l'initialisation de Pygame (fenêtre, événements, polices, sons) et gère la boucle principale.

* **Initialisation** : Prend en charge une taille de fenêtre (`size`), une résolution de rendu interne (`render_size` pour le pixel art), et le framerate maximum (`fps`).
* **Boucle Principale (`run`)** : Gère la boucle de jeu, la vérification des événements Pygame, le rafraîchissement des inputs, et le redimensionnement de la surface de rendu (Scale).
* **Outils Intégrés** : Raccourcis natifs pour le plein écran (F11), le déblocage des FPS (F10), le mode débogage (F12) et la caméra libre (F8).
* **Liaison d'événements (`bind`)** : Permet d'associer des événements Pygame spécifiques à des fonctions de rappel (callbacks).

### 2.2. La classe `Scene` (`Scene.py`)

Hérite de `pg.Surface` et orchestre tous les éléments à afficher.

* **Système de Calques (Layers)** : Les objets sont triés dans des listes via un dictionnaire `layers` et un ordre de rendu `layer_order` (équivalent z-index).
* **Préfixes de Calques** :
* Les calques standards affichent les objets de manière statique par rapport à la fenêtre (comme le HUD).
* Les calques contenant `#` (ex: `World#1`) sont soumis au décalage de la caméra.
* Les calques avec `_` (ex: `_background`, `_UI`) sont des surfaces internes réservées par le moteur.


* **Rendu** : La méthode `draw` gère l'ordre d'affichage depuis le fond jusqu'à l'UI, en gérant le culling (ne dessine pas les objets hors écran).

### 2.3. La Caméra (`GameCamera.py`)

* **Suivi de cible** : La méthode `focus(game_object)` centre la caméra sur une entité (ex: le joueur).
* **Limites** : `set_limits(topleft, bottomright)` empêche la caméra de sortir d'une zone définie.
* **Mode Freecam** : Permet de détacher la caméra et de naviguer librement avec des touches directionnelles lors du débogage.

---

## 3. Entités et Objets du Jeu

### 3.1. `GameObject` (`GameObject.py`)

Il s'agit de la brique fondamentale de l'API (basée sur l'approche de Unity).

* **Propriétés** : Possède une position vectorielle (`pos`), une taille (`size`), une image/surface (`image`), un rectangle de collision (`rect`), et une direction (`"left"` ou `"right"`).
* **Système de Tags** : Utilise un `set()` pour classer les objets (`add_tag()`, `remove_tag()`) facilitant les interactions (ex: `"solid"`, `"player"`).
* **Cycle de vie** : `update()` actualise l'animation si elle existe, et `draw()` dessine l'objet sur une surface en appliquant l'offset de la caméra.

### 3.2. `Entity` (`Entity.py`)

Étend `GameObject` avec des propriétés physiques et d'états (similaire à un Rigidbody2D).

* **Physique** : Intègre des vecteurs de vélocité (`vel`), un paramètre de gravité (`gravity`), et des états booléens (`jump`, `fall`, `is_hitting_ground`).
* **Collisions** : `update()` calcule les collisions avec d'autres `GameObject` possédant le tag `"solid"` et modifie la position pour empêcher l'entité de traverser les murs, le sol ou les plafonds.
* **Animations d'état** : `update_sprite()` bascule automatiquement entre les animations "idle", "run", "jump" ou "fall" selon la vélocité.

### 3.3. `Player` (`Player.py`)

La classe `Player` hérite de `Entity` et inclut la gestion complète des contrôles du joueur.

* **Mouvements** : Gère l'accélération, la résistance, la vitesse maximale, le sprint (boost), et le saut avec les entrées clavier/manette de `Inputs.py`.
* **Visée** : Si l'entrée "aim" est activée, génère et affiche une ligne de trajectoire balistique prédictive (`Trajectory`) vers la position de la souris.

---

## 4. Environnement et Interactions

* **`Solid`** : Objet statique basique portant le tag `"solid"` pour faire office de plateforme ou de mur.
* **`ParallaxBackground`** : Génère un effet de profondeur en déplaçant plusieurs calques d'images (`ParallaxLayer`) à des vitesses différentes (`speed`) selon le mouvement de la caméra.
* **Triggers** (`Trigger.py`) : Zones invisibles basées sur `GameObject` qui déclenchent des `callbacks` lorsqu'une entité (définie par `target_tags`) y pénètre.
* **`TriggerKillBox`** : Appelle automatiquement la méthode `kill()` de l'entité entrante (pratique pour le vide ou la lave).
* **`TriggerInteract`** : Affiche une touche d'interaction visuelle ("E") et attend que le joueur valide pour exécuter un événement.



---

## 5. Gestion des Médias (Assets)

### 5.1. `AudioManager` (`AudioManager.py`)

Système audio centralisé gérant 16 canaux simultanés par défaut.

* **SFX (Effets sonores)** : `load_sfx` stocke un objet `pg.mixer.Sound` en mémoire. `play_sfx` vérifie qu'un canal est libre pour éviter le spam audio.
* **Musique** : Gérée via chemin de fichier (streaming). Gère le bouclage automatique, la pause et la reprise.

### 5.2. `Animation` (`Animation.py`)

Prend une `Texture` (feuille de sprites horizontale) et la découpe automatiquement en fonction du nombre de frames (images) donné.

* **Exécution** : Change d'image en fonction d'un intervalle de temps donné (`delay` en ms).
* **Direction** : Génère automatiquement une version miroir des images pour gérer les directions ("left" / "right").

---

## 6. Interface Utilisateur (UI)

La gestion de l'interface repose sur la classe `GameUI` qui agit comme un chef d'orchestre sur une surface transparente.

* **Moteur UI (`GameUI.py`)** : Gère l'affichage, bloque le contrôle du joueur via `State.toggle("player_control", False)` si un menu est ouvert, et assombrit l'écran derrière une fenêtre modale.
* **`Button` (`Button.py`)** : Bouton cliquable qui gère les états visuels "idle", "hover", et "click" avec support optionnel de textures. Prend en charge les offsets de menu pour la détection du curseur.
* **`TextBox` & `Dialog` (`TextBox.py`, `Dialog.py`)** :
* `TextBox` affiche un titre, une zone de texte retournée à la ligne automatiquement (`process_text()`), un portrait optionnel ("left" ou "right"), et un indice pour la touche "continuer/fermer".
* `Dialog` agit comme un conteneur enchaînant plusieurs `TextBox` et gère le passage à la réplique suivante lors de l'interaction du joueur.


* **`Modal` (`Modal.py`)** : Conteneur bloquant supportant l'ajout d'éléments en grilles (tableau 2D de boutons) afin de permettre la navigation intégrale à la manette.

---

## 7. Outils Utilitaires (Utils)

* **`Inputs.py`** : Système unifié qui fusionne les entrées du clavier, de la souris et de la manette (Xbox & PlayStation).
* `get_inputs()` : Retourne les actions maintenues.
* `get_once_inputs()` : Retourne les actions enfoncées lors de la frame courante uniquement.


* **`GlobalVariables.py`** : Magasin clé/valeur (ex: `cam_pos`, `scale_ratio`, `audio_manager`) évitant de passer ces constantes en paramètre de chaque classe.
* **`State.py`** : Gère des drapeaux d'états de jeu globaux via `toggle()` (ex: bloquer les inputs via `"player_control"`, activer le menu via `"in_menu"`).
* **`Collision.py`** : Fonctions de prédiction de collision (`get_collided_objects`). Détermine par quel côté (`"top"`, `"bottom"`, `"left"`, `"right"`) se produirait le contact pour ajuster précisément la physique du jeu.

# Examples :

Voici des exemples concrets et pratiques pour illustrer l'utilisation de l'API Omicronde, basés sur son architecture et ses modules.

### 1. Initialisation du Jeu et de la Boucle Principale

La classe `Game` gère la fenêtre et la boucle d'événements. Il faut lui passer une fonction qui sera exécutée à chaque frame pour mettre à jour la logique du jeu.

```python
import pygame as pg
from api.Game import Game

# 1. Création de l'instance du jeu (rendu interne de 640x360, mis à l'échelle en 1280x720)
my_game = Game(
    size=(1280, 720), 
    render_size=(640, 360), 
    name="Projet Omicronde", 
    flags=pg.RESIZABLE, 
    fps=60
)

# 2. Définition de la logique de mise à jour (exécutée à chaque frame)
def game_loop():
    # Mettre à jour les entités, la physique, etc.
    pass 

# 3. Lancement du jeu
my_game.run(game_loop)

```

### 2. Création et Animation d'une Entité (Entity)

Pour créer un personnage ou un ennemi, on utilise la classe `Entity` qui gère la physique basique et les animations. On utilise `Texture` et `Animation` pour lui donner vie.

```python
from api.entity.Entity import Entity
from api.assets.Animation import Animation
from api.assets.Texture import Texture
from api.assets.Resource import Resource, ResourceType

# Configuration des ressources
resource_manager = Resource(ResourceType.GLOBAL, "chemin/vers/assets")

# 1. Création d'une entité (ex: un ennemi) aux coordonnées (100, 200) de taille 32x32
enemy = Entity(pos=(100, 200), size=(32, 32))
enemy.set_gravity(0.5) # Applique la gravité
enemy.add_tag("enemy") # Utile pour les collisions et les triggers

# 2. Ajout d'une animation à partir d'une feuille de sprites
tex_run = Texture("enemy_run_sheet.png", resource_manager)
# Découpe la texture en 4 frames, avec un délai de 150ms entre chaque frame
anim_run = Animation(texture=tex_run, frame_count=4, delay=150)

# 3. Assignation de l'animation à l'entité
enemy.add_animation("run", anim_run)
enemy.set_sprite("run")

# 4. Ajout de l'entité à la scène principale
my_game.scene.add(enemy, layer="World#1")

```

### 3. Utilisation des Déclencheurs (Triggers)

Les Triggers permettent d'exécuter des actions d'interaction ou de zone. Voici comment créer une "KillBox" (zone mortelle, comme de la lave ou un vide) qui ciblera le joueur.

```python
from api.environment.Trigger import TriggerKillBox

# 1. Création d'une zone mortelle de 500x50 pixels en bas du niveau
# L'entité qui entre dedans (ici, taggée "player") verra sa méthode kill() appelée
lava_pit = TriggerKillBox(
    pos=(0, 600), 
    size=(500, 50), 
    target_tags=["player"], 
    sfx="burn_sound" # Jouera ce son si l'AudioManager est configuré
)

# 2. Ajout du trigger à la scène
my_game.scene.add(lava_pit)

```

### 4. Interface Utilisateur : Création d'un Bouton

L'interface utilisateur (`GameUI`) fonctionne de manière asynchrone par-dessus la scène. Voici comment ajouter un bouton cliquable.

```python
from api.UI.Button import Button

# 1. Création d'un bouton au centre de l'écran (avec une couleur au survol)
start_button = Button(
    pos=(220, 150), 
    size=(200, 50), 
    text="Jouer", 
    bg_color=(255, 255, 255), 
    bg_color_hover=(188, 188, 188),
    font="arial"
)

# 2. Création d'une fonction de rappel (callback) appelée lors du clic
def on_start_click(btn):
    print("Démarrage du niveau !")
    my_game.scene.UI.hide("menu_start") # Cache le bouton après le clic

start_button.set_callback(on_start_click)

# 3. Ajout du bouton à l'UI de la scène et affichage
my_game.scene.UI.add("menu_start", start_button)
my_game.scene.UI.show("menu_start")

```

### 5. Gestion de l'Audio (Sons et Musique)

L'outil `AudioManager` charge les sons en mémoire, définit les canaux et rend le tout accessible globalement.

```python
from api.assets.AudioManager import AudioManager

# 1. Initialisation du gestionnaire audio (se place automatiquement dans les variables globales)
audio = AudioManager(sfx_volume=0.8, music_volume=0.5, channels=16)

# 2. Chargement des médias
audio.load_music("theme_principal", "assets/music/main_theme.ogg")
audio.load_sfx("jump", "assets/sfx/jump.wav")

# 3. Lecture
audio.play_music("theme_principal", loops=-1) # -1 = boucle infinie
audio.play_sfx("jump") # Joue le son de saut

# Optionnel: Arrêter une musique ou un son
# audio.stop_music()

```

### 6. Configuration d'une Caméra Suivant le Joueur

La `GameCamera` permet de naviguer dans le niveau. On peut la lier à un objet (comme le joueur) pour qu'elle le suive en permanence.

```python
# En supposant que 'my_player' est une instance de Player ou Entity
# 1. Cibler le joueur
my_game.scene.camera.focus(my_player)

# 2. Ajouter un décalage (offset) pour que le joueur soit centré à l'écran (ex: milieu d'un écran 640x360)
my_game.scene.camera.set_offset((320, 180))

# 3. (Optionnel) Définir les limites de la caméra pour ne pas sortir de la carte
my_game.scene.camera.set_limits(topleft=(0, 0), bottomright=(2000, 1000))

```