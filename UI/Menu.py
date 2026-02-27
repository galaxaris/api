class Menu:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def display(self):
        print(f"Menu: {self.name}")
        for item in self.items:
            print(f"- {item}")