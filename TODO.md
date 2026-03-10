# TODO for API

Entity :
  - Player improvements  

  - Enemy (IA)
  - Boss

Environment :
  - InOut (Doors, Teleporters)
  - Trap
  - Handle Collisions correctly

Objects :
  - GraplingHook
  - WaterGun

# Plan


## Engine

- Level.py :
  - Loader un niveau à partir d'un .level (zip caché contenant un .json et les assets)
  - Sauvegarder un niveau dans un .level

## Environment

- InOut.py (GameObject) :
  - Ajouter des propriétés d'entrée/sortie (ex: portes, téléporteurs, etc.)
  - Gérer les interactions avec le joueur et les ennemis
  
- Trap.py (GameObject) :
  - Ajouter des propriétés de piège (ex: dégâts, activation, etc.)
  - Gérer les interactions avec le joueur et les ennemis

   
## Assets

- SFX 
    - Ajouter un système de gestion des sons (chargement, lecture, volume, etc.)
    - Intégrer une bibliothèque de sons libres de droits pour les tests

## UI 
- HealthBar.py (UIElement) :
  - Ajouter une barre de santé pour le joueur et les ennemis
  - Gérer les mises à jour de la barre de santé en fonction des dégâts subis

## Entity

- Player.py (Character) :
  - Ajouter la gestion des entrées pour contrôler le personnage
  - Implémenter un système de progression (niveaux, compétences, etc.)

- Enemy.py (Character) :
  - Ajouter des comportements d'IA pour les ennemis (patrouille, poursuite, attaque, etc.)
  - Gérer les interactions avec le joueur (dégâts, collisions, etc.)

## Interaction

- GraplingHook.py (GameObject) :
  - Ajouter la possibilité de se balancer ou de se propulser vers des points d'accroche
  - Gérer les interactions avec les objets et les ennemis pendant l'utilisation du grappin

- WaterGun.py (GameObject) :
  - Ajouter la possibilité de tirer de l'eau pour interagir avec l'environnement (éteindre des incendies, activer des mécanismes, etc.)
  - Gérer les interactions avec les ennemis (ralentir, étourdir, etc.)

# Debug Tools
