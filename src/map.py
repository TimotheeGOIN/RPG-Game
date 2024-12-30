import pygame, pytmx, pyscroll
import json

from typing import Any
from dataclasses import dataclass
from pytmx import TiledObject, TiledElement

from player import NPC, Player
from item import OnGroundItem, ItemManager, Item



@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    epoch: str
    walls: list[pygame.Rect]
    paths: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    on_ground_items: list[OnGroundItem]


class MapManager:

    def __init__(self, screen: pygame.Surface, player: Player) -> None:
        self.game_save_file: str = "save_files/game_save.json"
        # possibilité d'utiliser dict[str, dict[str, Map]]() comme pour self.maps['present']['overworld']
        self.maps = dict[str, Map]()
        self.item_manager = ItemManager()
        self.current_epoch: str = "present"
        self.current_map: str = f"{self.current_epoch}_overworld"
        self.screen = screen
        self.player = player

        # enregistrer la map de tests
        self.register_map("overworld", "test_epoch", npcs=[], on_ground_items=[])

        # ensemble des cartes (monde / maison / sous sol...)
        self.register_map("overworld","present",
                          npcs=[
                              NPC("robin", nb_points=4, dialog=self.load_dialogs_from_json("robin"), items_to_give=[(101, 105)]),
                              NPC("paul", nb_points=6, dialog=self.load_dialogs_from_json("paul"))
                          ],
                          on_ground_items=[
                              OnGroundItem(106, 3, "assets/items/gold_stone.png", 160, 160)]
                          ),
        self.register_map("overworld","past",
                          npcs=[
                              NPC("robin", nb_points=4, dialog=self.load_dialogs_from_json("robin"), items_to_give=[(101, 105)]),
                              NPC("paul", nb_points=6, dialog=self.load_dialogs_from_json("paul"))
                          ],
                          on_ground_items=[
                              OnGroundItem(106, 3, "assets/items/gold_stone.png", 160, 160)]
                          )

        """
        self.register_map("monde", portals=[
            Portal(from_world="overworld", origin_point="enter_dungeon", target_world="dungeon",
                   teleport_point="spawn1_dungeon"),
            Portal(from_world="overworld", origin_point="enter_red_house", target_world="red_house",
                   teleport_point="spawn_house"),
            Portal(from_world="overworld", origin_point="enter_green_house", target_world="green_house",
                   teleport_point="spawn_house")
        ],
        npcs=[
            NPC("paul", nb_points=5,
                dialog=["Hallo !!!", "Che me dénomme... PAUL !!!!!", "Bonne afentur cheune padafouane"]),
            # METTRE 1 DE PLUS SINON CA MARCHE PAS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            NPC("robin", nb_points=7, dialog=["Bonjour, je ma pelle teuse...", "Non, je déconne je ma pelle Robin"])
            # SOIT UN CHEMIN EN CARRE, LE CHEMIN PERDRA 1x1 DE LA THEORIE AU JEU: 5x5 -> 4x4 en jeu
        ])
        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit1_dungeon", target_world="world",
                   teleport_point="dungeon_exit_spawn"),
        ], npcs=[
            NPC("boss", nb_points=7, dialog=["Je garde ces lieux", "Mwaaahaahahaha"])
        ])"""
        

        self.teleport_player("Spawn")  # "Spawn" pour apparition 'classique' mais le joueur apparaîtra aux dernières coordonnées si elles ont été sauvegardées.
        self.teleport_npcs()
    
    def check_npc_collisions(self, dialog_box) -> None:
        """Simply checks if the player collides a npc and then activate that npc's dialog.
        Must soon be moved to the check_collisions function.
        :param dialog_box: Must be an DialogBox object (src.dialogs)
        """
        for sprite in self.get_group().sprites():
            # verifier SI le sprite est un pnj puis la collision avec le joueur 
            if type(sprite) is NPC and sprite.feet.colliderect(self.player.rect):
                dialog_box.execute(sprite.dialog)

    def check_on_ground_item_collisions(self) -> tuple[Item, OnGroundItem]:
        """Simply checks if the players collides an item on the ground and then activate a function to collect that item.
        Must soon be moved to the check_collisions function.
        :return: Returns the item on the ground that is collided and the "example" item that corresponds to the item on the ground
        """
        for item_sprite in self.get_group().sprites():
            # verifier SI le sprite est un item au sol puis la collision avec le joueur
            if type(item_sprite) is OnGroundItem and item_sprite.rect.colliderect(self.player.rect):
                # retourne l'item retourné après (faire remonter l'item jusqu'à game) et l'item au sol
                return self.item_manager.collect_on_ground_item(item_sprite)

    def check_with_path_collisions(self) -> None:
        """Simply checks if the player collides a path and then increases his speed a bit (+50%).
        Must soon be moved to the check_collisions function.
        """
        # checker la collision avec un élément des zones de chemin
        for path_piece in self.get_map().paths:
            # augmenter légèrement la vitesse du joueur
            if self.player.feet.colliderect(path_piece):
                self.player.speed = self.player.normal_speed * 1.5
                return

    def check_collisions(self) -> None:
        """Simply checks if the player collides a portal (area in which the player must be teleported) or a npc.
        If the player collides a portal, calls a function that teleports the player. If it's a npc, the npc stops walking.
        """
        # gérer les portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # gérer les collisions joueur-pnj ou joueur-mur
        for sprite in self.get_group().sprites():

            if not type(sprite) is OnGroundItem:

                # si un pnj touche un joueur, alors il s'arrête
                if type(sprite) is NPC:
                    if sprite.feet.colliderect(self.player.rect):
                        sprite.speed = 0
                    else:
                        sprite.speed = 0.75

                if sprite.feet.collidelist(self.get_walls()) > -1:
                    sprite.move_back()

    # téléporter le joueur à un endroit (comme à l'entrée d'une map lorsqu'il change de map)
    def teleport_player(self, name: str) -> None:
        point = self.get_object(name)
        # si le point est un spawn de map (point d'entrée d'une map, un par côté : nord / sud / est / ouest)
        # en fonction actualise seulement la position x ou y pour garder l'alignement du personnage
        # si le joueur change de map par la droite, si position en y ne change pas
        if name == "spawn_n" or name == "spawn_s":
            self.player.position[1] = point.y - 16
        elif name == "spawn_e" or name == "spawn_w":
            self.player.position[0] = point.x - 16
        # sinon téléporte simplement le joueur aux coordonnées du point
        else:
            self.player.position[0] = point.x - 16
            self.player.position[1] = point.y - 16
        self.player.save_location()

    def change_epoch(self, epoch: str) -> None:
        """Changes the current epoch without changing the current map and player position. Actually, it compares all the
        maps in the way to find the same map as the current but in the demanded epoch."""
        # chercher la map correspondant à la map actuelle mais à l'époque demandée
        for map in self.maps:

            # compare le nom de la map testée avec celle actuelle (nom "normal" → overworld)
            # et compare l'époque demandée avec l'époque de la map testée
            if self.maps[map].name == self.maps[self.current_map].name and self.maps[map].epoch == epoch:
                # change la map actuelle par la nouvelle
                self.current_epoch = epoch
                self.current_map = map
                print(self.current_epoch)
                break

    @staticmethod
    def load_dialogs_from_json(npc_name: str) -> list[str]:
        """Basically gets a list of strings from a json file. Encoding must be ISO-8859-1 for good characters recovering.
        ISO-8859-1 seems to be natively compatible with python 3.12.
        :param npc_name: Name of the npc. Will be used to get that npc's dialog file (as f"dialogs/{npc_name}_dialogs.json").
        :return: Returns a list of strings.
        """
        # dialogue par défaut
        default_dialog: list[str] = ["Bonjour, désolé je n'ai pas le temps.", "Bonne aventure"]
        # charger les dialogues depuis un fichier sinon retourne le dialogue par défaut
        try:
            # ouvrir le fichier correspondant au nom du pnj
            with open(f"dialogs/{npc_name}_dialogs.json", "r") as file:
                # retourner la liste des dialogues
                return json.load(file)

        except FileNotFoundError:
            return default_dialog

    def save_map_infos(self) -> None:
        """Saves map datas (like player position, current map, current epoch...) in a json file."""
        # récupérer l'entièreté des données sauvegardées
        with open(self.game_save_file, "r") as file:
            # lire et stocker les données
            saved_data: dict[str, Any] = json.loads(file.read())

        # remplacer (mettre à jour) les données qui nous intéressent (position, map, époque...)
        saved_data["Map"] = self.current_map
        saved_data["Position"] = self.player.position
        saved_data["Epoch"] = self.current_epoch

        # ensuite remplacer les anciennes données par les nouvelles actuelles
        with open(self.game_save_file, "w+") as file:
            # écraser les anciennes données par les nouvelles
            file.seek(0)
            json.dump(saved_data, file, indent=4)

        print("Tout est sauvegardé !")

    def load_map_infos(self) -> None:
        """Loads map datas like player position, current map, current epoch... And sets these values as current
        values in the script"""
        # récupérer les données dans le fichier
        with open(self.game_save_file, "r") as file:
            # choper les données
            save_data: dict[str, Any] = json.loads(file.read())

        # instancier les données qui ont été sauvegardées
        self.current_map = save_data["Map"]
        self.player.position = save_data["Position"]
        self.current_epoch = save_data["Epoch"]

    def register_map(self, name: str, epoch: str, portals: list=None, npcs: list[NPC]=None, on_ground_items: list[OnGroundItem]=None) -> None:
        """Crée (l'instance) d'une carte avec tous les paramètres donnés. Elle ne retourne rien. map ajoute la map créée (sous un objet Map) dans le dict self.maps.
        :param name: Nom de la carte. Il sera utilisé pour trouver le fichier de la carte dans le projet (f"maps/{epoch}/{epoch}_{name}.tmx") et sera aussi utilisé en tant que clé dans le dictionnaire répertoriant les toutes cartes (f"{epoch}_{name}").
        :param epoch: L'époque de la carte peut prendre 3 valeurs : past, present ou future. Il sera utilisé aux mêmes niveaux que le nom (voir description du paramètre 'name')
        :param portals: Liste des zones de téléportation de la map comme les entrées dans les maisons ou les bords de la map pour changer de map.
        :param npcs: Liste des pnjs présents dans la map
        :param on_ground_items: Liste des items au sol présents dans la map
        """

        # valeurs par défault de paramètres (non mutable)
        if portals is None:
            portals = []
        if npcs is None:
            npcs = []
        if on_ground_items is None:
            on_ground_items = []

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"maps/{epoch}/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # créer une liste qui contient les zones de collision
        walls: list[pygame.Rect] = [] # wall désigne ici aussi l'eau et tout ce qu'on ne peut pas traverser
        paths: list[pygame.Rect] = [] # calques représentant toutes les zones de chemin

        # boucle qui récupère tous les calques de la map 
        for obj_group in tmx_data.objectgroups:
            # vérifie s'il s'appelle "Collisions"
            if obj_group.name == "Collisions":
                # pour tout ce qu'il y a dans "Collisions" l'ajoute dans walls
                for obj in obj_group:
                    walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            # récupérer le calque "Paths"
            if obj_group.name == "Paths Areas":
                # ajouter toutes les zones considérées comme chemin
                for obj in obj_group:
                    paths.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques / les tuiles de la carte
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        # récupérer les pnjs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # ajouter au groupe tous les items au sol
        for item in on_ground_items:
            group.add(item)

        # enregistrer la carte chargée
        map_name = f"{epoch}_{name}" # nom de la carte dans le dictionnaire (en tant que key) (par exemple → present_overworld: Map())
        self.maps[map_name]: Map = Map(name, epoch, walls, paths, group, tmx_data, portals, npcs, on_ground_items)

    def get_map(self) -> Map:
        return self.maps[self.current_map]

    def get_group(self) -> pyscroll.PyscrollGroup:
        return self.get_map().group

    def get_walls(self) -> list[pygame.Rect]:
        return self.get_map().walls

    def get_object(self, name: str) -> TiledObject | TiledElement:
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self) -> None:
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self) -> None:
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self) -> None:
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()
