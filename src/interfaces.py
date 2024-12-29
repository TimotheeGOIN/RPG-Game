import pygame
from item import Item


# classe gérant l'affichage des boutons
class Button:

    def __init__(self, button_function: str, position: tuple[int, int], text: str="", base_text_color: str | tuple[int, int, int]="gray", lighting_color: str | tuple[int, int, int]="white") -> None:

        self.font = pygame.font.Font("./assets/fonts/pixelon.otf", 32)
        # charger l'illumination des contours des boutons
        self.button_illumination = pygame.image.load("./assets/menus/illumination.png")
        self.button_function = button_function
        self.base_text_color = base_text_color
        self.text_input = text
        self.text_color = self.base_text_color
        self.lighting_color = lighting_color

        self.image = pygame.image.load("./assets/menus/button.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.x = position[0]
        self.image_rect.y = position[1]

        self.text = self.font.render(self.text_input, 0, base_text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.x = round(self.image_rect.x + (self.image.get_width() - self.text.get_width()) / 2)
        self.text_rect.y = round(self.image_rect.y + (self.image.get_height() - self.text.get_height()) / 2) + 2 # - 2 corrige le padding dû à cette police

    def display(self, surface: pygame.Surface) -> None:

        # afficher le bouton puis le texte
        surface.blit(self.image, self.image_rect)
        surface.blit(self.text, self.text_rect)
        # illuminer le bouton si la souris passe dessus
        self.light_up(surface)

    def light_up(self, surface: pygame.Surface) -> None:
        """Lights up edges of the button by displaying a white sprite on the button's edges.
        :param surface: Surface on what will the highlighting sprite be displayed. Usually same as the button.
        """
        # check si la pos de la souris touche le rect du bouton
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):
            # fais apparaitre le contour blanc pour illuminer et modifie la couleur du texte en blanc
            surface.blit(self.button_illumination, (self.image_rect.x, self.image_rect.y))
            self.modify_text_color("white")
        else: # remet la couleur du texte en gris
            self.modify_text_color("gray")

    def modify_text_color(self, text_color: str | tuple[int, int, int]) -> None:
        # générer le nouveau texte
        self.text = self.font.render(self.text_input, 0, text_color)

    # générer / modifier le texte du bouton
    def modify_text(self, text_input: str, text_color="gray") -> None:
        # générer le nouveau texte
        self.text_input = text_input
        self.text = self.font.render(text_input, 0, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.x = round(self.image_rect.x + (self.image.get_width() - self.text.get_width()) / 2)
        self.text_rect.y = round(self.image_rect.y + (self.image.get_height() - self.text.get_height()) / 2) + 2  # - 2 corrige le padding dû à cette police


# classe gérant l'affichage de l'inventaire
class Inventory:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        # charger l'illumination des contours des items
        self.item_illumination = pygame.image.load("./assets/menus/item_illumination.png")
        # charger les images qui assombrissent l'arrière de la quantité des items
        self.darken_items = pygame.image.load("./assets/menus/darken_itemss.png")
        self.darken_items = pygame.transform.scale(self.darken_items, (20, 20))
        # polices d'écritures
        self.font = pygame.font.Font("./assets/fonts/items_font.ttf", 16)
        self.invfont = pygame.font.Font("./assets/fonts/Test2.ttf", 40)
        self.title = self.invfont.render("Inventaire", 1, "black")

        # charger les assets de la fenêtre de l'inventaire
        self.window = pygame.image.load("./assets/menus/inventory_window.bmp")
        self.window = pygame.transform.scale(self.window, (260, 310))

        self.slot_img = pygame.image.load("./assets/menus/slot_test.png")
        self.slot_img = pygame.transform.scale(self.slot_img, (40, 40))

        # position de la fenêtre d'inventaire
        self.window_rect = self.window.get_rect()
        self.window_rect.x = self.screen.get_width() - self.window_rect.width - 10
        self.window_rect.y = self.screen.get_height() / 2 - self.window_rect.height / 2
        self.window_rect.bottom = self.screen.get_height() - round(self.screen.get_height() * 1.618 / 10)
        # self.window_rect.center = self.screen.get_rect().center

    def light_up_slot(self, item: Item) -> None:
        # check si la pos de la souris touche le rect de l'item
        if item.image_rect.collidepoint(InterfaceManager.sub_pos(pygame.mouse.get_pos(), self.window_rect.topleft)):
            # fais apparaitre le contour blanc pour illuminer et modifie la couleur du texte en blanc
            self.window.blit(self.item_illumination, (item.image_rect.x, item.image_rect.y))

# classe gérant l'affichage des infos des items dans l'inventaire
class ItemInfosWindow:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font("./assets/fonts/pixelon.otf", 24)
        self.text_antialiasing = False
        self.text_padding = self.font.get_height()

        # charger les assets concernant l'affichage des infos des items
        self.window = pygame.image.load("./assets/menus/infos_window.png")
        self.window = pygame.transform.scale(self.window, (260, 180))
        self.window_rect = self.window.get_rect()
        self.window_rect.bottom = self.screen.get_height() - round(self.screen.get_height() * 1.618 / 10)
        self.window_rect.x = 10
        self.window_rect.y = self.window_rect.bottom - self.window_rect.height

        # caractéristiques de l'item sous forme de textes
        self.item_name = self.font.render("Rien", self.text_antialiasing, "gray")
        self.item_name_rect = self.item_name.get_rect()
        self.item_name_rect.x = 10
        self.item_name_rect.y = 10
        self.item_name_rect.topleft = self.item_name_rect.x, self.item_name_rect.y

        self.item_quantity = self.font.render("Rien", self.text_antialiasing, "gray")
        self.item_quantity_rect = self.item_quantity.get_rect()
        self.item_quantity_rect.x = 10
        self.item_quantity_rect.y = 10 + self.text_padding
        self.item_quantity_rect.topleft = self.item_quantity_rect.x, self.item_quantity_rect.y

        self.item_desc = self.font.render("Rien", self.text_antialiasing, "gray")
        self.desc_texts = []
        self.item_desc_rect = self.item_desc.get_rect()
        self.item_desc_rect.x = 10
        self.item_desc_rect.y = 10 + self.text_padding * 2
        self.item_desc_rect.topleft = self.item_desc_rect.x, self.item_desc_rect.y

    def actualize_item_infos(self, item: Item) -> None:
        """Actualize the item infos window with the given item infos."""
        self.item_name = self.font.render(item.name, self.text_antialiasing, "gray")
        self.item_quantity = self.font.render(f"x{item.quantity}", self.text_antialiasing, "gray")
        if item.description is not None:
            self.item_desc = self.font.render(item.description, self.text_antialiasing, "gray")
            self.desc_texts = InterfaceManager.separate_text(item.description, 16, self.font, "gray", self.text_antialiasing, True)


# classe gérant le chargement des images de toutes les interfaces
class InterfaceManager:

    def __init__(self, screen: pygame.Surface) -> None:

        # récupérer le screen
        self.screen = screen
        # récupérer une instance de Button
        self.button = Button("button_instance", (0, 0))
        # définir les niveaux d'intensité d'assombrissement du fond des menus
        self.darken_filter = pygame.image.load("./assets/menus/darken.png")
        self.darken: bool = True
        self.dark_strenght_lvls: dict[str, int] = {"high": 5, "mid": 3, "low": 1}
        self.dark_strenght: str = "mid"
        # générer le curseur de la souris avec une image personnalisée
        self.cursor_image = pygame.image.load("./assets/menus/cursor.png")
        self.cursor_image = pygame.transform.scale(self.cursor_image, (24, 24))
        self.cursor = pygame.cursors.Cursor((0, 0), self.cursor_image)
        pygame.mouse.set_cursor(self.cursor)

        self.main_menu_button_list: list[Button] = [
            Button("play", (self.center_btn_on_x(), 230), "Jouer", "gray", "white"),
            Button("settings", (self.center_btn_on_x(), 280), "Options", "gray", "white"),
            Button("quit", (self.center_btn_on_x(), 370), "Quitter", "gray", "white")
        ]

        self.pause_button_list: list[Button] = [
            Button("settings", (self.center_btn_on_x(), 230), "Options", "gray", "white"),
            Button("resume", (self.center_btn_on_x(), 280), "Reprendre", "gray", "white"),
            Button("quit", (self.center_btn_on_x(), 370), "Quitter", "gray", "white")
        ]

        self.settings_button_list: list[Button] = [
            Button("fullscreen", (self.center_btn_on_x(), 120), "Plein écran", "gray", "white"),
            Button("luminosity", (self.center_btn_on_x(), 280), "Luminosité : Moyenne", "gray", "white"),
            Button("back",  (self.center_btn_on_x(), 370), "Retour", "gray", "white")
        ]

    def center_btn_on_x(self) -> int:
        return round(self.screen.get_width() / 2 - self.button.image.get_width() / 2)

    def darken_back(self) -> None:
        if self.darken: # assombrir le jeu lors de l'ouverture du menu pause

            for i in range(0, self.dark_strenght_lvls[self.dark_strenght] + 1):
                self.screen.blit(self.darken_filter, (-60, -60))
            self.darken = False

    @staticmethod
    def set_fullscreen() -> None:
        pygame.display.toggle_fullscreen()

    @staticmethod
    def separate_text(text: str, limit: int, font: pygame.font.Font, color: str | tuple[int, int, int] = "black",
                      antialiasing: bool = True, to_surface: bool = False) -> list[str | pygame.Surface] | None:
        # vérifie que le texte a bien besoin d'être divisé
        if not len(text) > limit:
            # sinon le retourne en texte ou en surface
            if to_surface:
                return [font.render(text, antialiasing, color)]
            else:
                return [text]

        # initialiser les listes
        texts_list = [] # liste des textes "finaux" (str ou Surface) qui vont être retournés
        words_list = [] # liste "mémoire" de mots pour 1 seule "phrase" (on pourrait dire que 'texts_list' contient plusieurs 'words_list')
        all_words = text.split() # tous les mots (qui étaient contenus dans le paramètre 'text')

        for word in all_words:
            # actualise la longueur des mots qui sont actuellement dans la "mémoire" de la boucle
            string_lenght = sum([len(wd) for wd in words_list])

            # si on ne peut pas ajouter le mot à la "mémoire" sans dépasser la limite, on fait une phrase avec les mots de la "mémoire" puis on la vide
            if string_lenght + len(word) >= limit:
                # rassemble tous les mots qui étaient dans la "mémoire" dans une seule chaîne de caractère puis l'ajoute à 'text_list'
                texts_list.append(" ".join(words_list))
                words_list.clear() # vide la liste "mémoire"

            # ajouter le mot à la liste "mémoire"
            words_list.append(word)

        # ajouter des mots à la liste de phrases encore s'il en reste encore dans la "mémoire" qui n'ont pas été ajouté
        texts_list.append(" ".join(words_list))

        # convertir les textes en surfaces si c'est demandé
        if to_surface:
            for i in range(len(texts_list)):
                texts_list[i] = font.render(texts_list[i], antialiasing, color)

        return texts_list

    @staticmethod
    def add_pos(first_tuple: tuple[int, int], second_tuple: tuple[int, int]) -> tuple[int, int]:
        """
        Add values of same index in different tuples. First tuple value plus second tuple value
        :return: A new 'int, int' tuple
        """
        return first_tuple[0] + second_tuple[0], first_tuple[1] + second_tuple[1]

    @staticmethod
    def sub_pos(first_tuple: tuple[int, int], second_tuple: tuple[int, int]) -> tuple[int, int]:
        """
        Substract values of same index in different tuples. First tuple value minus second tuple value
        :return: A new 'int, int' tuple
        """
        return first_tuple[0] - second_tuple[0], first_tuple[1] - second_tuple[1]
