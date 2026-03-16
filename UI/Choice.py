from api.UI.GameUI import UIElement


class Choice(UIElement):
    """Textbox with buttons for branching dialog or menu options."""

    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        """Initialize a choice container.

        :param pos: Top-left position of the choice box.
        :param size: Size of the choice box.
        """
        super().__init__(pos, size)
        self.buttons: dict[UIElement, str] = {}
        self.add_tag("ui_choice")

    def add_choice(self, button: UIElement, goal: str = None):
        """Add a button to the choice container.

        :param button: Button element representing a choice.
        :return:
        """
        self.buttons.append(button)