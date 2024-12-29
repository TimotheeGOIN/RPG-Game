import pygame, moviepy.editor
from moviepy.editor import *
from moviepy.video.fx import resize
from pygame.locals import *

from player import Player
from map import MapManager
from item import ItemManager, Item
from interfaces import InterfaceManager, Inventory, ItemInfosWindow, Button
from dialog import DialogBox

pygame.init()

class Game:

    def __init__(self) -> None:
        self.map: str = 'overworld'
        self.FPS: int = 60
        self.running: bool = True
        self.menu: bool = False
        self.video_test = moviepy.editor.VideoFileClip("C:/Users/timot/Desktop/Pygamon/test.mp4")
        self.video_test = self.video_test.resize(height=240)
        # sous valeurs des menus
        self.pause: bool = False
        self.settings: bool = False
        self.show_inv: bool = False
        # régler la prochaine action en attente sur quelque chose de neutre
        self.next_action: str = "nothing"
        # créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((720, 480), pygame.RESIZABLE)
        # importer la clock
        self.clock = pygame.time.Clock()
        # générer le joueur
        self.player = Player()
        # importer les classes des autres fichiers
        self.interface = InterfaceManager(self.screen)
        self.inventory = Inventory(self.screen)
        self.item_infos = ItemInfosWindow(self.screen)
        self.item_manager = ItemManager()
        self.dialog_box = DialogBox(self.screen)
        self.map_manager = MapManager(self.screen, self.player)

    def handle_input(self) -> None:
        # récupérer la liste des boutons pressés
        pressed = pygame.key.get_pressed()
        if not self.dialog_box.reading:
            if pressed[pygame.K_UP]:
                self.player.move_up(self.FPS)
            elif pressed[pygame.K_DOWN]:
                self.player.move_down(self.FPS)
            elif pressed[pygame.K_LEFT]:
                self.player.move_left(self.FPS)
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right(self.FPS)
            else:
                self.player.idle_animation(self.FPS)

        # commande de triche
        if pressed[pygame.K_LSHIFT]:
            self.player.speed = self.player.normal_speed * 4
        else:
            self.player.speed = self.player.normal_speed

    def update(self) -> None:
        self.map_manager.update()
        
    def darken_item_count(self, darken_pos: tuple[int, int], item_quantity: int) -> None:
        # calculer la longueur en fonction du nombre d'items → longueur du nombre (1 à 4 chiffres) et le *
        darken_lenght = len(str(item_quantity)) * 10
        # rogner la case sombre en fonction de la longueur du nombre
        self.inventory.darken_items = pygame.transform.smoothscale(self.inventory.darken_items, (darken_lenght, 20))
        # assombrir l'arrière du nombre d'items dans l'inventaire
        self.inventory.window.blit(self.inventory.darken_items, darken_pos)

    def display_item_infos(self, item: Item | None = None) -> None:
        if item is None:
            self.screen.blit(self.item_infos.window, self.item_infos.window_rect)
            return
        # actualise les infos de l'item sélectionné
        self.item_infos.actualize_item_infos(item)
        self.screen.blit(self.item_infos.window, self.item_infos.window_rect)
        # afficher les caractéristiques (nom, quantité...)
        self.screen.blit(self.item_infos.item_name, self.interface.add_pos(self.item_infos.item_name_rect.topleft,
                                                                           self.item_infos.window_rect.topleft))
        self.screen.blit(self.item_infos.item_quantity, self.interface.add_pos(self.item_infos.item_quantity_rect,
                                                                               self.item_infos.window_rect.topleft))

        if self.item_infos.desc_texts is not None:
            self.item_infos.item_desc_rect.y = 10 + self.item_infos.text_padding * 2
            for i, part in enumerate(self.item_infos.desc_texts):
                self.item_infos.item_desc_rect.y += self.item_infos.text_padding
                self.screen.blit(part, self.interface.add_pos(self.item_infos.item_desc_rect,
                                                              self.item_infos.window_rect.topleft))

    def check_next_action(self) -> None:
        if self.next_action == "pause":
            self.open_pause()
            self.next_action = "nothing"
            
        elif self.next_action == "settings":
            self.open_settings()
            self.next_action = "nothing"

    def open_menu(self) -> None:
        self.menu = True
        # faire apparaitre la souris dans les menus
        pygame.mouse.set_visible(True)

    def quit_menu(self) -> None:
        # faire disparaitre la souris en jeu
        pygame.mouse.set_visible(False)
        self.show_inv = False
        self.settings = False
        self.pause = False
        self.menu = False
        self.interface.darken = True

    def open_inventory(self) -> None:
        self.open_menu()
        self.show_inv = True

    def quit_inventory(self) -> None:
        self.item_manager.selected_item = None
        self.show_inv = False
        self.quit_menu()

    def open_pause(self) -> None:
        self.open_menu()
        self.pause = True
    
    def open_settings(self) -> None:
        self.open_menu()
        self.settings = True

    def quit_settings(self) -> None:
        # placer le menu pause en prochaine action et quitter tous les menus
        self.next_action = "pause"
        self.quit_menu()
    
    # quitter le jeu (sortir de toutes les boucles)
    def quit_game(self, save: bool=True) -> None:
        """ Does every actions that need to be done at the closing of the game
        like saves and breaking all actives loops.
        :param save: Precise if it saves the datas of the game. Is True by default"""
        if save:
            self.save_all_datas()
        self.settings = False
        self.menu = False
        self.running = False

    # sauvegarder toutes les données (regrouper toutes les fonctions de sauvegarde)
    def save_all_datas(self) -> None:
        # sauvegarder l'inventaire
        self.item_manager.save_inventory()
        # sauvegarder les infos spatiales (position, map, époque...)
        self.map_manager.save_map_infos()

    # charger toutes les données (regrouper toutes les fonctions de chargement de données)
    def load_all_datas(self) -> None:
        # sauvegarder l'inventaire
        self.item_manager.load_inventory()
        # sauvegarder les infos spatiales (position, map, époque...)
        self.map_manager.load_map_infos()

    # menu de démarrage du jeu
    def main_menu(self) -> None:
        # boucle du menu principal
        while self.running:
            pygame.display.update()

            self.screen.fill("grey")

            # afficher les boutons de toute la liste
            for button in self.interface.main_menu_button_list:
                button.display(self.screen)

            # gérer les entrées
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # vérifier si un bouton est cliqué
                    for button in self.interface.main_menu_button_list:
                        # lancer le menu des options
                        if button.image_rect.collidepoint(event.pos):

                            # actions pour chaque fonction d'un bouton
                            match button.button_function:
                                # lancer le menu des options
                                case "settings":
                                    self.settings = True
                                # retourner au jeu
                                case "play":
                                    return
                                # quitter le jeu
                                case "quit":
                                    self.quit_game()

                elif event.type == pygame.KEYDOWN:
                    # ouvrir pause
                    if event.key == pygame.K_ESCAPE:
                        self.open_pause()

                elif event.type == pygame.QUIT:
                    self.quit_game(save=False)

    def run(self) -> None:
        # lancer le menu principal dès le lancement du jeu
        self.main_menu()

        # charger les données de sauvegarde
        self.load_all_datas()
        # faire disparaitre la souris au lancement du jeu
        pygame.mouse.set_visible(False)
        # à mettre pour garder le focus dans le jeu (la souris ne sort pas) mais chiant pour tester
        #pygame.event.set_grab(True)

        # boucle du jeu
        while self.running:

            # afficher le nombre de fps dans le titre de la fenêtre (et l'arrondir à 1 décimale)
            pygame.display.set_caption(f"Pygamon - FPS: {self.clock.get_fps():.1f}")

            # verifier si une acton n'est pas en attente
            self.check_next_action()

            # sauvegarder la position du joueur
            self.player.save_location()
            self.map_manager.check_with_path_collisions()
            # dessiner et actualiser la carte, #1 récupérer les touches pressées, #3 centrer la caméra sur le joueur
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    # touche pour lancer des tests
                    if event.key == pygame.K_BACKSPACE:
                        self.video_test.preview()
                        #self.map_manager.change_epoch("past")
                    elif event.key == pygame.K_a:
                        self.map_manager.change_epoch("past")
                    elif event.key == pygame.K_z:
                        self.map_manager.change_epoch("present")
                    elif event.key == pygame.K_p:
                        self.map_manager.change_epoch("test_epoch")

                    # touche d'interaction
                    if event.key == pygame.K_SPACE:
                        # discuter avec les pnjs
                        self.map_manager.check_npc_collisions(self.dialog_box)
                        # ramasser les objets au sol
                        if self.map_manager.check_on_ground_item_collisions() is not None:
                            # ajouter l'item dans l'inventaire
                            self.item_manager.add_item(self.map_manager.check_on_ground_item_collisions()[0])
                            # détruire l'entité au sol représentant l'item
                            self.map_manager.check_on_ground_item_collisions()[1].kill()

                    # ouvrir pause
                    if event.key == pygame.K_ESCAPE:
                        self.open_pause()

                    # ouvrir l'inventaire
                    if event.key == pygame.K_TAB:
                        self.open_inventory()

                elif event.type == pygame.WINDOWRESIZED:
                    print(self.screen.get_size())

                    # resize la fenêtre au ratio 1,6 en fonction de la width de la fenêtre (d'où le 0.625)
                    self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_width()*0.625), pygame.RESIZABLE)
                    print(self.screen.get_size())

                elif event.type == pygame.QUIT:
                    self.quit_game()

            # boucle (stoppant le jeu) qui gère les menus
            while self.menu:

                # afficher le nombre de fps dans le titre de la fenêtre (et l'arrondir à 1 décimale)
                pygame.display.set_caption(f"Pygamon - FPS: {self.clock.get_fps():.1f}")

                # assombrir le fond
                self.interface.darken_back()
                # sortir le focus du jeu
                #pygame.event.set_grab(False)

                # l'inventaire
                if self.show_inv:
                    self.show_inventory()
                # menu pause
                elif self.pause:
                    self.pause_menu()
                # menu des options
                elif self.settings:
                    self.settings_menu()

                self.clock.tick(self.FPS)

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()

    def show_inventory(self) -> None:

        pygame.display.update()
        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))

        # correspond à fenêtre collée à la gauche et centrée au milieu niveau hauteur
        self.screen.blit(self.inventory.window, self.inventory.window_rect)
        # pour centre texte "inventaire" et /20 correspond au 16 pixel entre haut et le texte
        self.inventory.window.blit(self.inventory.title, (
        self.inventory.window.get_width() / 2 - self.inventory.title.get_width() / 2,
        self.inventory.window.get_height() / 20))

        # afficher la fenêtre des infos des items
        self.screen.blit(self.item_infos.window, self.item_infos.window_rect)

        # afficher les slots de l'inventaire
        for position in self.item_manager.inventory_positions:
            self.inventory.window.blit(self.inventory.slot_img, position)
            """"""

        # afficher les items dans l'inventaire
        for i, item in enumerate(self.item_manager.inventory):
            # placer l'item dans la case correspondant à son index dans l'inventaire
            item.image_rect.x, item.image_rect.y = self.item_manager.inventory_positions[i]
            # afficher l'item
            self.inventory.window.blit(item.image, item.image_rect)
            # illuminer ses contours
            self.inventory.light_up_slot(item)

            # afficher la quantité de l'objet s'il y en a plus d'un
            if item.quantity > 1:
                # créer le texte qui indique le nombre d'items
                text = self.inventory.font.render(f"{item.quantity}", True, "white")
                text_rect = text.get_rect(bottomright=self.item_manager.quantity_positions[i])
                self.darken_item_count(text_rect.topleft, item.quantity)
                self.inventory.window.blit(text, text_rect)

            # afficher les caractéristiques de l'objet (à gauche) s'il est sélectionné
            if item == self.item_manager.selected_item:
                self.display_item_infos(item)

        # boucle pour gérer les entrées
        for event in pygame.event.get():

            # afficher les caractéristiques de l'item
            if event.type == pygame.MOUSEBUTTONDOWN:
                # si la souris clique sur l'item est alors selectionné
                for item in self.item_manager.inventory:
                    if item.image_rect.collidepoint(
                            self.interface.sub_pos(pygame.mouse.get_pos(), self.inventory.window_rect.topleft)):
                        self.item_manager.selected_item = item

            if event.type == pygame.KEYDOWN:  # appui sur les touches du clavier
                # retirer pause
                if event.key == pygame.K_TAB:
                    self.quit_inventory()

                # ajouter/retirer les items de l'inventaire de façon provisoire
                for item in self.item_manager.all_items:
                    if event.type == KEYDOWN and event.key == item.adding:
                        self.item_manager.add_item(item)

                    elif event.type == KEYDOWN and event.key == item.removing:
                        self.item_manager.remove_item(item)

            if event.type == pygame.QUIT:  # sortir du jeu en quittant la fenêtre
                self.quit_game()

    def pause_menu(self) -> None:

        pygame.display.update()

        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))

        # afficher les boutons de toute la liste
        for button in self.interface.pause_button_list:
            button.display(self.screen)

        # boucle pour gérer les entrées
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:  # appui sur la souris

                # vérifier si un bouton est cliqué
                for button in self.interface.pause_button_list:
                    # lancer le menu des options
                    if button.image_rect.collidepoint(event.pos):

                        # actions pour chaque fonction d'un bouton
                        match button.button_function:
                            # lancer le menu des options
                            case "settings":
                                self.next_action = "settings"
                                self.quit_menu()
                            # retourner au jeu
                            case "resume":
                                self.quit_menu()
                            # quitter le jeu
                            case "quit":
                                self.quit_game()

            if event.type == pygame.QUIT:  # sortir du jeu en quittant la fenêtre
                self.quit_game()

            if event.type == pygame.KEYDOWN:  # appui sur les touches du clavier
                # retirer pause
                if event.key == pygame.K_ESCAPE:
                    self.quit_menu()

    def settings_menu(self) -> None:

        pygame.display.update()

        self.screen.blit(pygame.transform.grayscale(self.screen), (0, 0))

        # afficher les boutons de toute la liste
        for button in self.interface.settings_button_list:
            button.display(self.screen)

        # boucle pour gérer les entrées
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:  # appui sur la souris

                # vérifier si un bouton est cliqué
                for button in self.interface.settings_button_list:
                    # lancer le menu des options
                    if button.image_rect.collidepoint(event.pos):
                        # actions pour chaque fonction d'un bouton
                        match button.button_function:

                            # mode plein écran
                            case "fullscreen":
                                self.interface.set_fullscreen()

                            # changer la luminosité (si le bouton est cliqué, passer au niveau de luminosité suivante)
                            case "luminosity":
                                # changer le texte et la luminosité
                                if self.interface.dark_strenght == "high":  # → basse
                                    self.interface.dark_strenght = "low"
                                    button.modify_text("Luminosité : Basse")
                                elif self.interface.dark_strenght == "mid":  # → haute
                                    self.interface.dark_strenght = "high"
                                    button.modify_text("Luminosité : Haute")
                                elif self.interface.dark_strenght == "low":  # → moyenne
                                    self.interface.dark_strenght = "mid"
                                    button.modify_text("Luminosité : Moyenne")

                            # retourner au menu pause
                            case "back":
                                self.quit_settings()

            if event.type == pygame.QUIT:  # sortir du jeu en quittant la fenêtre
                self.quit_game()

            if event.type == pygame.KEYDOWN:  # appui sur les touches du clavier
                # retirer pause
                if event.key == pygame.K_ESCAPE:
                    self.quit_menu()
