"""Textbox UI utilities and component."""

from typing import Optional
import pygame as pg
from pygame.surface import Surface

from api.UI.GameUI import UIElement
from api.assets.Texture import Texture
from api.utils.Fonts import get_font
from api.utils import Inputs


def process_text(font_name: str, text: str, max_width: int) -> list[Surface]:
    """
    Split text into wrapped lines that fit a maximum width.

    Manual line breaks (`\n`) are preserved by processing each paragraph
    independently.

    :param font_name: Font used for width measurements.
    :param text: Raw text content.
    :param max_width: Maximum width allowed for each rendered line.
    :return: List of rendered text line surfaces.
    """
    text_content = []
    font = get_font(font_name, 16)
    space_width = font.size(' ')[0]

    # On sépare d'abord par les paragraphes manuels
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        words = paragraph.split(' ')
        current_line_words = []
        current_line_width = 0

        for word in words:
            # Calcul de la largeur du mot
            word_width = font.size(word)[0]

            # Si le mot dépasse la largeur max, on valide la ligne actuelle et on recommence
            if current_line_width + word_width > max_width:
                if current_line_words:
                    line_text = " ".join(current_line_words)
                    text_content.append(font.render(line_text, False, (255, 255, 255)))

                current_line_words = [word]
                current_line_width = word_width + space_width
            else:
                current_line_words.append(word)
                current_line_width += word_width + space_width

        # On ajoute la dernière ligne du paragraphe
        if current_line_words:
            line_text = " ".join(current_line_words)
            text_content.append(font.render(line_text, False, (255, 255, 255)))

    return text_content


def process_title(title: str, font: str) -> Surface:
    """Render a textbox title with the large title style.

    :param title: Title text.
    :param font: Font name/path marker.
    :return: Rendered title surface.
    """
    return get_font(font, 32).render(title, False, (255, 255, 255))


class TextBox(UIElement):
    """Dialog-style textbox with optional portrait and interaction hint."""

    title_surface: Surface
    text_surfaces: list[Surface]
    image: Optional[Surface]
    image_side: str
    closable: bool
    font: str
    raw_text: str
    goal: str

    def __init__(self, title: str, text: str = "", font: str = "aptos", image_side: str = "left",
                 texture: Texture = None, closable: bool = True, goal="fermer", border_radius: int = 10):
        """Initialize a textbox.

        :param title: Displayed title, usually speaker name.
        :param text: Dialog/message text.
        :param font: Base font used for title and content.
        :param image_side: Portrait side when an image is provided.
        :param texture: Optional portrait texture.
        :param closable: Whether interaction can close this textbox.
        :param goal: Semantic goal marker used by UI flow.
        """
        super().__init__((0, 0), (0, 0))
        self.raw_text = text
        self.font = font
        self.title_surface = process_title(title, font)
        self.image_side = image_side
        self.closable = closable
        self.goal = goal
        self.image = None
        self.text_surfaces = []  # Sera généré au premier draw selon la largeur disponible
        self.color = (30, 30, 30, 220)
        self.border_radius = border_radius

        if texture:
            self.set_image(texture, image_side)

        self.add_tag("ui_textbox")
        self.add_tag("ui_block")
        self.add_tag("ui_closable")
        self.add_tag("ui_bypassdebug")

    def set_text(self, text: str, font: str = None):
        """Set textbox content and invalidate cached line rendering.

        :param text: New body text.
        :param font: Optional font override.
        :return:
        """
        if font: self.font = font
        self.raw_text = text
        self.text_surfaces = []  # Reset pour forcer le recalcul au prochain draw

    def set_image(self, texture: Texture, image_side: str = "left"):
        """Set or clear the portrait image.

        :param texture: Portrait texture, or `None` to clear.
        :param image_side: Portrait side (`"left"` or `"right"`).
        :return:
        """
        if texture:
            self.image = texture.image
            self.image_side = image_side
        else:
            self.image = None
        self.text_surfaces = []  # Reset car l'espace disponible pour le texte change

    def set_title(self, title: str, font: str):
        """Update textbox title rendering.

        :param title: New title text.
        :param font: Font used for title rendering.
        :return:
        """
        self.title_surface = process_title(title, font)

    def draw(self, surface: pg.Surface, scene=None):
        """Render textbox content at the bottom of the destination surface.

        Layout is computed dynamically from the destination size and optional
        portrait image, then text is wrapped to fit the remaining content area.

        :param scene:
        :param surface: Destination surface.
        :return:
        """
        margin = 15
        width = surface.get_width() - margin * 2
        height = surface.get_height() // 3


        image_size_px = height - margin * 2
        image_area_width = image_size_px + margin if self.image else 0


        max_text_width = width - image_area_width - margin * 2

        if not self.text_surfaces:
            self.text_surfaces = process_text(self.font, self.raw_text, max_text_width)

        text_box_rect = pg.Rect(0, 0, width, height)
        text_box_bg = pg.Surface((width, height), pg.SRCALPHA, 32).convert_alpha()
        pg.draw.rect(text_box_bg, self.color, text_box_rect, border_radius=self.border_radius)

        content_surface = pg.Surface((max_text_width, height - margin * 2), pg.SRCALPHA, 32).convert_alpha()

        content_surface.blit(self.title_surface, (0, 0))
        line_y = self.title_surface.get_height() + 4

        for line in self.text_surfaces:
            content_surface.blit(line, (0, line_y))
            line_y += line.get_height() + 4

        if self.closable:
            hint_text = Inputs.get_hint_input("interact")
            hint_surface = get_font(self.font, 16).render(hint_text, False, (180, 180, 180))
            content_surface.blit(hint_surface, (content_surface.get_width() - hint_surface.get_width(), content_surface.get_height() - hint_surface.get_height()))

        # 6. Assemblage final (Image + Contenu)
        if self.image:
            # Redimensionnement de l'image si nécessaire
            if self.image.get_size() != (image_size_px, image_size_px):
                self.image = pg.transform.scale(self.image, (image_size_px, image_size_px))

            if self.image_side == "left":
                text_box_bg.blit(self.image, (margin, margin))
                text_box_bg.blit(content_surface, (image_area_width + margin, margin))
            else:
                text_box_bg.blit(content_surface, (margin, margin))
                text_box_bg.blit(self.image, (width - image_size_px - margin, margin))
        else:
            text_box_bg.blit(content_surface, (margin, margin))

        # 7. Affichage sur l'écran principal (en bas)
        surface.blit(text_box_bg, (margin, surface.get_height() - height - margin))