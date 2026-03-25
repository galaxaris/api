"""Button UI component with hover/click states."""

from api.UI.GameUI import UIElement
from api.assets.Texture import Texture
import pygame as pg

from api.utils import InputManager
from api.utils.Fonts import get_font


class Button(UIElement):
    """Interactive UI button supporting textures and callbacks."""

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], text: str = None, color_set: dict[str, tuple[int, int, int]] = ((0, 0, 0), (255, 255, 255), (188, 188, 188), (210, 210, 210)), font: str = "arial", border_radius: int = 7):
        """Initialize a button.

        :param pos: Top-left button position.
        :param size: Button size.
        :param text: Optional text drawn on fallback style.
        :param color_set: Tuple of four colors for the button (text, background, hover, focus) (default: black, white, gray, darker gray).
        :param font: Font used by `draw_text`.
        """
        super().__init__(pos, size)
        self.text = text
        self.text_color = color_set[0]
        self.bg_color = color_set[1]
        self.bg_color_hover = color_set[2]
        self.bg_color_focus = color_set[3]
        self.font = font
        self.default_texture = None
        self.hover_texture = None
        self.click_texture = None
        self.callback = None
        self.menu_offset = (0, 0)
        self.state = "default"
        self.border_radius = border_radius
        self.was_clicked_prev_frame = False
        self.add_tag("ui_button")

    ### PUBLIC METHODS ###
    def set_text(self, text: str):
        """
        Set button text for fallback rendering.

        :param text: Text to display on the button.
        :return:
        """
        self.text = text

    ### PRIVATE METHODS FOR STATE MANAGEMENT ###
    def define_texture(self, default: Texture, hover: Texture, click: Texture):
        """Define button textures for all visual states.

        :param default: Texture used when idle.
        :param hover: Texture used when hovered.
        :param click: Texture used when clicked.
        :return:
        """
        self.default_texture = default
        self.hover_texture = hover
        self.click_texture = click
        self.image = self.default_texture.image
        self.rect = self.image.get_rect(topleft=self.pos)

    def click(self, color: tuple[int, int, int] = (255, 0, 0)):
        """Apply clicked state visual style (mouse button held down).

        :param color: Fallback border/text color when click texture is missing.
        :return:
        """
        self.state = "click"
        if self.click_texture:
            self.image = self.click_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a red border if no click texture is defined
            pg.draw.rect(self.image, color, self.image.get_rect(), 2, border_radius=self.border_radius)
            self.draw_text(color, self.text_color)

    def idle(self, color: tuple[int, int, int] = (255, 255, 255)):
        """Apply idle state visual style.

        :param color: Fallback text color when no default texture exists.
        :return:
        """
        self.state = "default"
        if self.default_texture:
            self.image = self.default_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a white border if no default texture is defined
            self.draw_text(color, self.text_color)


    def hover(self, color: tuple[int, int, int] = (188, 188, 188)):
        """Apply hover state visual style.

        :param color: Fallback border/text color when hover texture is missing.
        :return:
        """
        self.state = "hover"

        if self.hover_texture:
            self.image = self.hover_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a red border if no hover texture is defined
            pg.draw.rect(self.image, color, self.image.get_rect(), 2, border_radius=self.border_radius)
            self.draw_text(color, self.text_color)

    def focus(self, color: tuple[int, int, int] = (161, 2, 131)):
        """Apply focused state visual style (when mouse clicks and holds the button).

        :param color: Fallback border/text color when hover texture is missing.
        :return:
        """
        self.state = "focus"
        if self.hover_texture:
            self.image = self.hover_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a darker gray border if no focus texture is defined
            pg.draw.rect(self.image, color, self.image.get_rect(), 2)
            self.draw_text(color, self.text_color)

    def draw_text(self, color, text_color=(0, 0, 0)):
        """Draw text on the internal button surface.

        :param color: Fill color for fallback rendering.
        :param text_color: Color of the text.
        :return:
        """

        self.image = pg.Surface((self.size.x, self.size.y), pg.SRCALPHA)
        button_rect = pg.Rect(0, 0, self.size.x, self.size.y)
        pg.draw.rect(self.image, color, button_rect, border_radius=self.border_radius)
        text = get_font(self.font, 20).render(self.text, False, text_color)
        text_rect = text.get_rect(center=(self.size.x // 2, self.size.y // 2))
        self.image.blit(text, text_rect)
        self.rect = self.image.get_rect(topleft=self.pos)


    def set_callback(self, callback):
        """Set callback triggered by `click`. ==> Same fonctionnality as for the Trigger component, but for mouse input (and not from collision).

        :param callback: Callable receiving this button instance.
        :return:
        """
        self.callback = callback

    def set_global_margin(self, margin):
        """Set menu offset used for mouse hit testing.

        :param margin: Global menu offset vector.
        :return:
        """
        self.menu_offset = margin

    def update(self, scene=None):
        """Update button state from current pointer/controller context.

        State machine:
        - idle: no interaction
        - hover: mouse over, not clicking
        - focus: mouse button pressed (held down)
        - Callback triggered on click release (mouse button up)

        :return:
        """
        super().update(scene)

        raw_mouse = pg.Vector2(InputManager.get_player_aim_vector(True)) - pg.Vector2(self.menu_offset)
        ratio = scene.scale_ratio
        mouse_pos = (raw_mouse[0] // ratio, raw_mouse[1] // ratio)
        self.rect.topleft = self.pos + pg.Vector2(self.menu_offset)//2

        #Track previous frame state for edge detection (click release)
        prev_was_clicked = getattr(self, 'was_clicked_prev_frame', False)
        is_currently_clicked = InputManager.is_mouse_clicked()

        if self.rect.collidepoint(mouse_pos):
            #Change cursor to pointer when hovering over the button
            #pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

            #Mouse is over the button
            if InputManager.is_mouse_clicked_once():
                #Just pressed on the button
                self.focus(self.bg_color_focus)
            elif is_currently_clicked:
                #Being held on the button
                self.click(self.bg_color_focus)
            elif prev_was_clicked and not is_currently_clicked:
                #Just released on the button => trigger callback
                if self.callback:
                    self.callback(self)
                self.idle(self.bg_color)
            else:
                #hovering  without clicking
                self.hover(self.bg_color_hover)
        else:

            #Not over the button
            if not InputManager.is_controller_connected():
                self.idle(self.bg_color)
            else:
                self.rect = self.image.get_rect(topleft=self.pos)

            #Reset cursor to default if not hovering over any button
            #pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        #Store current state for next frame
        self.was_clicked_prev_frame = is_currently_clicked

