# Omicronde API Documentation

Omicronde API is a collection of class for developping the game and editor tool.
It will be used by both the game and the editor to ensure consistency and reusability of code.
Made to be used with Python 3.10+ and PyGame 2.6.0

# API Overview

## GameScene

* Description : The `GameScene` class is responsible for managing the game scene, including loading assets, updating game state, and rendering graphics.
* Attributes : 
  * `width` (int) : The width of the game scene in pixels.
  * `height` (int) : The height of the game scene in pixels.
  * `name` (str) : The name of the game scene."
  * `clock` (pygame.time.Clock) : The clock object to manage the frame rate.
  * `screen` (pygame.Surface) : The surface where the game scene is rendered.
  * `running` (bool) : A flag indicating whether the game loop is running.
* Methods : 
  * `run()` : Starts the game loop for the scene.
    * `@return` : None
  
## GameObject `(pygame.sprite.Sprite)`

## Solid `(GameObject)`

