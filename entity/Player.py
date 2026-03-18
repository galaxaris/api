"""
API's Player utilities
"""
from api.entity.Character import Character
from api.physics.Collision import get_collided_objects
from api.utils.Constants import MIN_SHOT_SPEED, MAX_SHOT_SPEED, DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY
from api.utils import Debug, Inputs

from api.utils.Inputs import get_inputs, get_once_inputs

import pygame as pg
import math

class Player(Character):
    """
    Player class, based on Entity class. Contains all the player's attributes and methods.
    """

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], direction: str = "right"):
        """
        Initializes the player with the given attributes.

        :param pos: Player position
        :param size: Player size
        :param direction: Player direction
        :param max_velocity: Player max velocity
        :param acceleration: Player acceleration
        :param resistance: Player resistance
        :param force: Player force
        :param sfx_list: List of sound effects. (key: name)
        """
        super().__init__(pos, size)
        self.add_tag("player")
        self.set_direction(direction)


    def update(self, scene=None):
        """
        Updates the player's position and velocity based on the inputs and the player's current state.

        :return:
        """

        inputs = get_inputs()

        was_falling = self.fall
        Time = scene.Time if scene and scene.Time else None


        if not Debug.is_enabled("freecam"):
            if inputs["aim"] and scene.global_state["player_control"]:
                self.speed_malus = self.max_velocity//2
                mouse = pg.Vector2(Inputs.get_mouse(Inputs.get_key_pressed("aim")))
                cam_pos = scene.camera.position
                player_screen_pos = self.pos - cam_pos + self.size/2
                angle_with_player = mouse / scene.scale_ratio - player_screen_pos

                self.equipped_weapon.trajectory.angle_radians = math.atan2(-angle_with_player.y, angle_with_player.x)

                if Inputs.MOUSE_SCROLL != 0:
                    self.equipped_weapon.trajectory.ini_speed = max(MIN_SHOT_SPEED, min(self.equipped_weapon.trajectory.ini_speed + Inputs.MOUSE_SCROLL, MAX_SHOT_SPEED))

                if Inputs.is_controller_connected() and (mouse == (0, -1000) or mouse == (0,0)):
                    self.equipped_weapon.trajectory.angle_radians = 0.56
                    if get_once_inputs()["aim_up"] and self.equipped_weapon.trajectory.ini_speed < MAX_SHOT_SPEED:
                        self.equipped_weapon.trajectory.ini_speed += 1
                    elif get_once_inputs()["aim_down"] and self.equipped_weapon.trajectory.ini_speed > MIN_SHOT_SPEED:
                        self.equipped_weapon.trajectory.ini_speed -= 1

                if get_once_inputs()["shoot"] and scene.global_state["player_control"]:
                    haveShooted = self.equipped_weapon.shoot(self.pos + self.size//2)
                    #self.equipped_weapon.is_aiming = False
                    #SFX
                    if self.sfx_list and haveShooted:
                        if "fire" in self.sfx_list:
                            audio_manager = scene.audio_manager
                            if audio_manager:
                                audio_manager.play_sfx("fire")

                else:
                    self.equipped_weapon.is_aiming = True


            else:
                self.speed_malus = 0
                self.equipped_weapon.trajectory.ini_speed = DEFAULT_SHOT_SPEED
                self.equipped_weapon.is_aiming = False


            if inputs["right"] and scene.global_state["player_control"]:
                self.is_controlled = True
                self.do_right(Time)
                if not inputs["aim"]:
                    self.set_direction("right")


            if inputs["left"] and scene.global_state["player_control"]:
                self.is_controlled = True
                self.do_left(Time)
                if not inputs["aim"]:
                    self.set_direction("left")

            if inputs["jump"] and scene.global_state["player_control"] and (not self.in_trigger_interact or not Inputs.is_controller_connected()) :
                self.do_jump()


            self.boost = inputs["boost"] and scene.global_state["player_control"] and not inputs["aim"]
            self.interact = inputs["interact"] and scene.global_state["player_control"]

        if Debug.is_enabled("freecam"):
            self.vel = pg.Vector2(0, 0)
            self.update_sprite()
        else:
            # Updates whith Entity's update
            super().update(scene)

            enemies_collisions = get_collided_objects(self,"enemy", scene.game_objects, self.vel.x, self.vel.y)
            if enemies_collisions:
                if not self.invincible:
                    for obj in enemies_collisions:
                        self.take_damage(obj[0].damage_force)

            # Détection de l'atterrissage : le joueur tombait et n'est plus en train de tomber
            if was_falling and not self.fall:
                if self.sfx_list:
                    if "hit_ground" in self.sfx_list:
                        audio_manager = scene.audio_manager
                        if audio_manager:
                            audio_manager.play_sfx("hit_ground")



    def draw(self, surface: pg.Surface, scene=None):
        super().draw(surface, scene)
        inputs = get_inputs()
        if inputs["show_inventory"] and scene.global_state["player_control"]:
            self.inventory.player_pos = self.pos
            self.inventory.player_size = self.size


            self.inventory.update(scene)
            self.inventory.player_rect = self.rect
            self.inventory.draw(surface, scene)





