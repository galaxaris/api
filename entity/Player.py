"""
API's Player utilities
"""
from api.entity.Character import Character
from api.physics.Collision import get_collided_objects
from api.utils.Console import print_info, print_warning, print_error
from api.utils.Constants import MIN_SHOT_SPEED, MAX_SHOT_SPEED, DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY, \
    DEFAULT_GRAPPLING_SPEED
from api.utils import Debug, InputManager

from api.utils.InputManager import get_inputs, get_once_inputs, onKeyDown, onKeyPress, onKeyPress, onKeyUp


import pygame as pg
import math

class Player(Character):
    """
    Player class, based on Entity class. Contains all the player's attributes and methods.
    """

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int], direction: str = "right", 
                 health: int=100, damage_resistance: int=0, damage_force: int=10, max_velocity: float|int = 2, acceleration: float|int = 0.5, resistance:float|int = 0.2, 
                 force:float|int = 20):
        """
        Initializes the player with the given attributes.
        => Full param are inherited from Character & Entity

        :param pos: Player position
        :param size: Player size
        :param direction: Player direction
        :param max_velocity: Player max velocity
        :param acceleration: Player acceleration
        :param resistance: Player resistance
        :param force: Player force
        :param sfx_list: List of sound effects. (key: name)
        """
        super().__init__(pos, size, health=health, damage_resistance=damage_resistance, 
                         damage_force=damage_force, max_velocity=max_velocity, acceleration=acceleration, resistance=resistance, force=force)
        self.add_tag("player")
        self.set_direction(direction)


    def update(self, scene=None):
        """
        Updates the player's position and velocity based on the inputs and the player's current state.

        :return:
        """

        #inputs = get_inputs()

        was_falling = self.fall
        Time = scene.Time if scene and scene.Time else None


        if not Debug.is_enabled("freecam"):
            if onKeyPress("aim") and scene.global_state["player_control"]:
                self.speed_malus = self.max_velocity//2
                mouse = pg.Vector2(InputManager.get_player_aim_vector(onKeyDown("aim")))
                cam_pos = scene.camera.position
                player_screen_pos = self.pos - cam_pos + self.size/2
                angle_with_player = mouse / scene.scale_ratio - player_screen_pos

                self.equipped_weapon.trajectory.angle_radians = math.atan2(-angle_with_player.y, angle_with_player.x)

                if InputManager.MOUSE_SCROLL != 0 and self.equipped_weapon.name != "grappling gun":
                    self.equipped_weapon.trajectory.ini_speed = max(MIN_SHOT_SPEED, min(self.equipped_weapon.trajectory.ini_speed + InputManager.MOUSE_SCROLL, MAX_SHOT_SPEED))

                if InputManager.is_controller_connected() and (mouse == (0, -1000) or mouse == (0,0)):
                    self.equipped_weapon.trajectory.angle_radians = 0.56
                    if onKeyPress("aim_up") and self.equipped_weapon.trajectory.ini_speed < MAX_SHOT_SPEED:
                        self.equipped_weapon.trajectory.ini_speed += 1
                    elif onKeyPress("aim_down") and self.equipped_weapon.trajectory.ini_speed > MIN_SHOT_SPEED:
                        self.equipped_weapon.trajectory.ini_speed -= 1

                if onKeyDown("shoot"):
                    if self.ammo <= 0:
                        return
                    if( self.equipped_weapon.name!= "grappling gun"):
                        self.ammo -= 1

                if onKeyPress("shoot") and scene.global_state["player_control"]:
                    if self.ammo <= 0 and self.equipped_weapon.name!= "grappling gun":
                        audio_manager = scene.audio_manager
                        if audio_manager:
                            audio_manager.play_sfx("empty_weapon")
                        return
                    is_shot = self.equipped_weapon.shoot(self.pos + self.size//2)

                    #self.equipped_weapon.is_aiming = False
                    #SFX
                    if self.sfx_list and is_shot:
                        if "fire" in self.sfx_list:
                            audio_manager = scene.audio_manager
                            if audio_manager:
                                audio_manager.play_sfx("fire")

                else:
                    self.equipped_weapon.is_aiming = True



            else:
                self.is_aiming = False
                self.speed_malus = 0
                if self.equipped_weapon.name != "grappling gun":
                    self.equipped_weapon.trajectory.ini_speed = DEFAULT_SHOT_SPEED
                else:
                    self.equipped_weapon.trajectory.ini_speed = DEFAULT_GRAPPLING_SPEED

                self.equipped_weapon.is_aiming = False

            if self.equipped_weapon.name == "grappling gun":

                projectile = self.equipped_weapon.projectile

                if projectile :

                    scene.global_state["player_control"] = False

                    player_center = self.pos + self.size / 2
                    grapple_pos = projectile.pos + projectile.size / 2

                    direction = grapple_pos - player_center
                    distance = int(direction.length())

                    if "anchored" in projectile.tags and not projectile.to_kill:

                        if distance < 40:
                            self.vel = pg.Vector2(0, 0)
                            projectile.to_kill = True

                        else:

                            grappling_speed = self.equipped_weapon.current_trajectory_ini_speed * 0.7
                            normalized = direction.normalize()
                            self.vel = normalized * grappling_speed

                    if distance > self.equipped_weapon.range:

                        grappling_speed = self.equipped_weapon.current_trajectory_ini_speed * 0.7
                        normalized = direction.normalize()
                        self.equipped_weapon.projectile.vel = - normalized * grappling_speed

                        self.equipped_weapon.range_reached = True

                    if distance < 40 and self.equipped_weapon.range_reached :
                        self.equipped_weapon.projectile.on_impact()



            if onKeyPress("right") and scene.global_state["player_control"]:
                self.is_controlled = True
                self.do_right(Time)
                if not onKeyPress("aim"):
                    self.set_direction("right")


            if onKeyPress("left") and scene.global_state["player_control"]:
                self.is_controlled = True
                self.do_left(Time)
                if not onKeyPress("aim"):
                    self.set_direction("left")

            if onKeyPress("jump") and scene.global_state["player_control"] and (not self.in_trigger_interact or not InputManager.is_controller_connected()) :
                self.do_jump()


            self.boost = onKeyPress("boost") and scene.global_state["player_control"] and not onKeyPress("aim")
            self.interact = onKeyUp("interact") and scene.global_state["player_control"]

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
        if onKeyPress("show_inventory") and scene.global_state["player_control"]:
            self.inventory.player_pos = self.pos
            self.inventory.player_size = self.size

            self.inventory.update(scene)
            self.inventory.player_rect = self.rect
            self.inventory.draw(surface, scene)


            if onKeyUp("select_weapon") and scene.global_state["player_control"]:
                self.inventory.switch_weapon()
                self.equipped_weapon = self.inventory.weapons[self.inventory.active_index]

        if self.equipped_weapon.name == "grappling gun":
            projectile = self.equipped_weapon.projectile
            if projectile and not projectile.to_kill:
                cam_pos = scene.camera.position
                player_center = self.pos + self.size / 2 - cam_pos
                projectile_center = projectile.pos + projectile.size / 2 - cam_pos
                pg.draw.line(surface, (100, 100, 100), player_center, projectile_center, 3)





