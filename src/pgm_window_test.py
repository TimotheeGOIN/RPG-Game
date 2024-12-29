import pygame
from moviepy.editor import *

FPS: int = 60
running: bool = True
menu: bool = False

screen = pygame.display.set_mode((720, 480), pygame.RESIZABLE)
clock = pygame.time.Clock()

class SlidingButton:

    def __init__(self, button_function: str, position: tuple[int, int], bar_lenght: int=360) -> None:
        # charger l'illumination des contours des boutons
        self.button_illumination = pygame.image.load("../assets/menus/illumination.png")
        self.button_function: str = button_function
        self.filling: float = 0.0

        # gérer l'image du bouton
        self.image = pygame.image.load("../assets/menus/button.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.x = position[0]
        self.image_rect.y = position[1]

        # gérer la barre glissante
        self.bar_image = pygame.transform.smoothscale(pygame.image.load("../assets/menus/button_bar.png"), (bar_lenght, 4))
        self.bar_rect = self.bar_image.get_rect()
        self.bar_rect.x = round(self.image_rect.x + (self.image_rect.width - self.bar_rect.width) / 2)
        self.bar_rect.y = round(self.image_rect.y + (self.image_rect.height - self.bar_rect.height) / 2)

        # gérer le curseur de la barre
        self.cursor_image = pygame.image.load("../assets/menus/sliding_cursor.png")
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_rect.x = self.bar_rect.x + round(self.bar_rect.width * self.filling)
        self.cursor_rect.y = round(self.bar_rect.y + (self.bar_rect.height - self.cursor_rect.height) / 2)

        # gérer la barre glissante blanche (partie remplie de la barre)
        self.bar_completion_image = pygame.image.load("../assets/menus/button_bar_completion.png")
        self.bar_completion_rect = self.bar_image.get_rect()
        self.bar_completion_rect.x = self.bar_rect.x
        self.bar_completion_rect.y = self.bar_rect.y

        # # actualiser la partie coloriée de la barre (ici l'initialiser)
        self.actualize_bar_completion()

    def display_button(self, surface: pygame.Surface) -> None:

        # afficher le bouton puis la barre
        surface.blit(self.image, self.image_rect)
        surface.blit(self.bar_image, self.bar_rect)
        surface.blit(self.bar_completion_image, self.bar_completion_rect)
        surface.blit(self.cursor_image, self.cursor_rect)

        # illuminer le bouton si la souris passe dessus
        self.light_up(surface)
        # actualiser la position du curseur (si le joueur le bouge)
        self.actualize_cursor_position()

    def actualize_cursor_position(self) -> None:
        # vérifier que la souris touche bien le bouton
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):

            # vérifier que le clic droit est bien pressé
            if pygame.mouse.get_pressed()[0]: # 0 pour le clic gauche, 1 : pour clic molette et 2 : pour clic droit

                # récupérer seulement la position en x de la souris
                mouse_pos_x = pygame.mouse.get_pos()[0]

                # vérifier que la position x de la souris se trouve bien dans les limites de la barre du bouton
                if self.bar_rect.x < mouse_pos_x < self.bar_rect.width + self.bar_rect.x:

                    # placer le curseur sur le même x que la souris et centrer le curseur
                    self.cursor_rect.x = mouse_pos_x - round(self.cursor_rect.width / 2)
                    # actualiser la partie coloriée de la barre
                    self.actualize_bar_completion()

    def actualize_bar_completion(self) -> None:
        # calculer la longueur de la barre "coloriée"
        bar_completion_lenght = self.bar_rect.width * self.get_bar_percentage()
        self.bar_completion_image = pygame.transform.scale(self.bar_completion_image, (bar_completion_lenght, self.bar_completion_rect.height))

    def get_bar_percentage(self) -> float:
        """ Returns the bar completion of the button.
        :return: A float between 0 and 1.
        """
        percentage = self.cursor_rect.x - self.bar_rect.x # avoir longueur "utilisée" ou "coloriée" de la barre
        percentage += round(self.cursor_rect.width / 2) # annuler l'imprecision de la barre dûe au centrage du curseur
        percentage = round(percentage / self.bar_rect.width, 2) # diviser la longueur "coloriée" par la longueur totale de la barre pour transformer en un pourcentage (de 0 à 1)

        return percentage

    def light_up(self, surface: pygame.Surface) -> None:
        # check si la pos de la souris touche le rect du bouton
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):
            # fais apparaitre le contour blanc pour illuminer et modifie la couleur du texte en blanc
            surface.blit(self.button_illumination, (self.image_rect.x, self.image_rect.y))

def open_menu() -> None:
    global menu
    menu = True
    # faire apparaitre la souris dans les menus
    pygame.mouse.set_visible(True)

def quit_menu() -> None:
    global menu
    menu = False

def center_btn_on_x() -> int:
    return round(screen.get_width() / 2 - 480 / 2)

# créer les boutons qui coulissent
sliding_buttons_list: list[SlidingButton] = [
    SlidingButton("volume_bar", (center_btn_on_x(), 230), 360)
]


# boucle du jeu
while running:
    # afficher le titre et le nombre de fps (et l'arrondir à 1 décimale)
    pygame.display.set_caption(f"Test Fenêtre Pygame (Home) - FPS: {clock.get_fps():.1f}")
    # afficher un écran gris
    screen.fill("lightgray")
    # actualiser
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                open_menu()
        if event.type == pygame.QUIT:
            running = False # quitter la fenêtre

    # actualiser et imposer une clock
    pygame.display.update()
    clock.tick(FPS)


    # le menu de tests
    while menu:
        # afficher le titre et le nombre de fps (et l'arrondir à 1 décimale)
        pygame.display.set_caption(f"Test Fenêtre Pygame (Menus)  - FPS: {clock.get_fps():.1f}")
        # afficher un écran gris
        screen.fill("gray")

        # gérer les boutons du menu pause
        for button in sliding_buttons_list:
            button.display_button(screen)
            print(button.get_bar_percentage())


        for event in pygame.event.get():
            #print(event)
            #print(event.type)
            """

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.key == pygame.BUTTON_LEFT:
                    print("button_left")
                elif event.key == pygame.BUTTON_RIGHT:
                    print("button_right")
                elif event.key == pygame.BUTTON_MIDDLE:
                    print("button_middle")
                elif event.key == pygame.BUTTON_WHEELUP:
                    print("button_wheel_up")
                elif event.key == pygame.BUTTON_WHEELDOWN:
                    print("button_wheel_down")
                elif event.key == pygame.BUTTON_X1:
                    print("button_x1")
                elif event.key == pygame.BUTTON_X2:
                    print("button_x2")

            if event.type == MOUSEWHEEL:
                print(event)
                print(event.x, event.y)
                print(event.flipped)"""
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    quit_menu()

            if event.type == pygame.QUIT:
                menu = False
                running = False  # quitter la fenêtre

        pygame.display.update()
        clock.tick(FPS)

# quitter pygame à la toute fin
pygame.quit()
















