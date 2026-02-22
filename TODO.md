# TODO for API

- Collision : 
  - Empecher les clips entre les objets
- UI 
  - TextBox
  - Menu
  - Dialogue
  - HUD

Entity :
  - Player improvements  
  - Enemy improvements

Objects :
  - GraplingHook
  - WaterGun

Environment :
  - Physics
  - Solid
  - InOut
  - Trap

# Plan


## Engine

- Level.py :
  - Loader un niveau à partir d'un .level (zip caché contenant un .json et les assets)
  - Sauvegarder un niveau dans un .level

## Environment

- Solid.py (GameObject) :
  - Ajouter des propriétés physiques 
  - Gérer les interactions avec d'autres objets

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

- Button.py :
  - Ajouter des animations pour les états (hover, click)
  - Permettre la personnalisation des styles (couleurs, polices, etc.)
  
- TextBox.py :
  - Ajouter la possibilité d'afficher du texte multi-ligne
  - Fond personnalisable (couleur, image, etc.)
  - Permettre la personnalisation des styles (couleurs, polices, etc.)
  
- Dialog.py :
  - Générer des dialogues à partir de fichiers de script (ex: .json, .yaml)
  - Ajouter des options de dialogue pour les choix du joueur
  - Générer une multitude de TextBox pour les dialogues

- HUD.py :
  - Ajouter des éléments de HUD (barres de santé, énergie, etc.)
  - Permettre la personnalisation du HUD (position, style, etc.)

- Menu.py :
  - Ajouter des animations pour les transitions de menu
  - Permettre la personnalisation du style du menu (couleurs, polices, etc.)



## Entity

- Character.py :
  - Ajouter des animations pour les différentes actions (marcher, sauter, attaquer, etc.)
  - Gérer les états du personnage (santé, énergie, etc.)
  - Implémenter un système de compétences ou d'actions spéciales

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

- Add Information of DebugMode (ex: FPS, position du joueur, etc.)
