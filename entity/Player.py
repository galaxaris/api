"""
API's Player utilities
"""
from api.items.Catalog import Pistol
from api.physics.Trajectory import Trajectory
from api.utils.Constants import MIN_SHOT_SPEED, MAX_SHOT_SPEED, DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY
from api.utils import Debug, State, Inputs, GlobalVariables

from api.entity.Entity import Entity
from api.utils.Inputs import get_inputs, get_once_inputs

import pygame as pg

class Player(Entity):
    """
    Player class, based on Entity class. Contains all the player's attributes and methods.
    """

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], direction = "right", max_velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
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
        self.force = force
        self.boost = False
        self.add_tag("player")
        self.set_direction(direction)
        self.equipped_weapon = Pistol(Trajectory(pg.Vector2(0,0), DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY, pg.Vector2(0,0)))
        self.set_physics_properties(max_velocity, acceleration, resistance)

        self.start_pos = pos



    def update(self):
        """
        Updates the player's position and velocity based on the inputs and the player's current state.

        :return:
        """
        inputs = get_inputs()
        boost_val = 1 if self.boost else 0

        was_falling = self.fall
        max_velocity = self.max_velocity
        self.equipped_weapon.update()

        if not Debug.is_enabled("freecam"):

            if inputs["aim"] and State.is_enabled("player_control"):

                max_velocity /= 2
                mouse_x, mouse_y = Inputs.get_mouse(Inputs.get_key_pressed("aim"))
                self.equipped_weapon.active_trajectory = Trajectory(self.pos + self.weapon_point, self.equipped_weapon.shot_speed,
                                                                    self.equipped_weapon.projectile_gravity, pg.Vector2(mouse_x, mouse_y))
                self.equipped_weapon.active_trajectory.build_trajectory_coordinates()


                if Inputs.MOUSE_SCROLL != 0:
                    self.equipped_weapon.shot_speed = max(MIN_SHOT_SPEED, min(self.equipped_weapon.shot_speed + Inputs.MOUSE_SCROLL, MAX_SHOT_SPEED))

                if self.equipped_weapon.active_trajectory.trajectory_coordinates:
                    last_trajectory_point = self.equipped_weapon.active_trajectory.trajectory_coordinates[-1] + GlobalVariables.get_variable("cam_pos")
                    self.set_direction("left" if last_trajectory_point.x < self.pos[0] else "right")

                if get_once_inputs()["shoot"] and State.is_enabled("player_control"):
                    print(pg.time.get_ticks())
                    new_projectile = self.equipped_weapon.shoot()
                    self.projectiles.append(new_projectile)
                    self.equipped_weapon.is_shooting = True

            else:
                self.equipped_weapon.active_trajectory = None
                self.equipped_weapon.shot_speed = DEFAULT_SHOT_SPEED

            if inputs["right"] and State.is_enabled("player_control"):
                self.is_controlled = True
                self.vel.x = max(0, min(self.vel.x + self.acceleration, max_velocity + boost_val))
                if not inputs["aim"]:
                    self.set_direction("right")


            if inputs["left"] and State.is_enabled("player_control"):
                self.is_controlled = True
                self.vel.x = max(-(max_velocity + boost_val), min(self.vel.x - self.acceleration, 0))
                if not inputs["aim"]:
                    self.set_direction("left")

            if inputs["jump"] and self.jump == False and State.is_enabled("player_control"):
                gravity = self.gravity if self.gravity else 1
                self.vel.y += -self.acceleration * max(1,gravity) * self.force
                self.jump = True

                #SFX
                if self.sfx_list:
                    if "jump" in self.sfx_list:
                        audio_manager = GlobalVariables.get_variable("audio_manager")
                        if audio_manager:
                            audio_manager.play_sfx("jump")


            self.boost = inputs["boost"] and State.is_enabled("player_control")
            self.interact = inputs["interact"] and State.is_enabled("player_control")

        if Debug.is_enabled("freecam"):
            self.vel = pg.Vector2(0, 0)
            self.update_sprite()
        else:
            # Updates whith Entity's update
            super().update()
            
            # Détection de l'atterrissage : le joueur tombait et n'est plus en train de tomber
            if was_falling and not self.fall:
                if self.sfx_list:
                    if "hit_ground" in self.sfx_list:
                        audio_manager = GlobalVariables.get_variable("audio_manager")
                        if audio_manager:
                            audio_manager.play_sfx("hit_ground")

    def kill(self):
        """
        Kills the player.

        Working: the player is respawned at the starting position (temporarily)

        :return:
        """
        self.vel = pg.Vector2(0, 0)
        self.set_position(self.start_pos)


    def draw(self, surface, offset = pg.Vector2(0, 0)):
        """
        Draws the player on the given surface.
        
        :param surface: Surface to draw on (usually the game's surface)
        :param offset: Offset to apply to the player's position (for moving camera)
        :return:
        """

        super().draw(surface, offset)

        if self.equipped_weapon.active_trajectory:
            self.equipped_weapon.active_trajectory.draw_trajectory(surface)

            if self.equipped_weapon.projectile:
                self.equipped_weapon.draw_projectile(surface)







