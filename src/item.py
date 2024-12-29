from encodings.utf_8 import decode

import pygame, json
from pygame import *

# classe gérant les instance des items, créer l'objet item
class Item:
    def __init__(self, item_id: int, name: str, image: pygame.Surface, is_stackable: bool, description: str | None, key1, key2) -> None:
        # caractéristiques
        self.item_id: int = item_id
        self.name: str = name
        self.quantity: int = 1
        self.is_stackable: bool = is_stackable
        self.description: str = description
        # générer l'image et le rect
        self.image: pygame.Surface = image
        self.image_rect: pygame.Rect = self.image.get_rect()
        self.image_rect.x = 0
        self.image_rect.y = 0
        # provisoire
        self.adding = key1
        self.removing = key2


    def __str__(self) -> str:
        return f"{self.name} en x{self.quantity}"

class OnGroundItem(pygame.sprite.Sprite):
    def __init__(self, item_id: int, quantity: int, image_link: pygame.image, x: int, y: int) -> None:
        super().__init__()
        self.item_id = item_id
        self.quantity = quantity
        self.position = [x, y]
        # partie gestion de l'image de l'item
        self.image = pygame.image.load(image_link)
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()

    def update(self) -> None:
        # actualisation du rect de l'item et du rect des pieds
        self.rect.topleft = self.position

# classe gérant tout ce qui concerne les items (initialisation, inventaire, ajout/retrait...)
class ItemManager:
        
    def __init__(self) -> None:
        self.item_list_file: str = "save_files/all_items.json"
        self.inventory_save_file: str = "save_files/inventory_save.json"
        self.items_size: tuple[int, int] = (40, 40)
        # coordonnées des cases de l'inventaire
        self.inventory_positions: list[tuple[int, int]] = [(x, y) for y in range(60, 310, 50) for x in range(10, 260, 50)]
        self.quantity_positions: list[tuple[int, int]] = [(x, y) for y in range(100, 350, 50) for x in range(50, 300, 50)]
        self.selected_item: Item | None = None
        # liste de tous les items du jeu (une fois initialisés)
        self.all_items: list[Item] = []
        # liste des items dans l'inventaire (initialisée à vide)
        self.inventory: list[Item] = []
        self.inventory_max_size: int = len(self.inventory_positions)
        # chopper la liste de tous les items dans le fichier json avec tous les items jeu
        with open(self.item_list_file, "r") as file:
            items_list = json.loads(file.read())

        for item in items_list:
            # ajouter les items en récupérant leur nom dans le fichier et en important puis redimensionnant l'image en une seule ligne
            self.all_items.append(
                Item(item["ID"],
                     item["Name"],
                     pygame.transform.scale(pygame.image.load(item["Link"]), self.items_size),
                     item["Stackable"],
                     item["Description"],
                     K_a,
                     K_z
                     ))

    # créer une instance d'un item
    @staticmethod
    def create_item(example_item: Item) -> Item:
        """Creates a new instance of an item by copying an item from the "example" list.
        :param example_item: Example item that will be copied
        :return: New instance of an item (same item as passed in parameter)
        """
        return Item(example_item.item_id,
                    example_item.name,
                    example_item.image,
                    example_item.is_stackable,
                    example_item.description,
                    K_a, K_z)

    # ajouter un item à l'inventaire
    def add_item(self, added_item: Item, quantity: int=1) -> None:
        """
        :param added_item: Item that will be added to the inventory. Must be of Item type.
        :param quantity: Copy amount of the item that will be added. By default, 1 copy is added.
        """
        for _ in range(quantity):

            # ajouter l'item si l'inventaire n'est pas plein
            if len(self.inventory) < self.inventory_max_size:

                # ajouter l'item sur une pile existante s'il est stackable
                if added_item.is_stackable:

                    for item in self.inventory:
                        if item.name == added_item.name:
                            item.quantity += 1
                            #print(f"Le {item.name} a été ajouté de 1")
                            # le return stoppe la fonction donc le reste n'est pas executé
                            return

                self.inventory.append(self.create_item(added_item))
                print(self.inventory)

    # retirer un item de l'inventaire
    def remove_item(self, removed_item: Item) -> None:
        for item in self.inventory:
            if item.name == removed_item.name:
                if item.quantity > 1:
                    item.quantity -= 1
                else:
                    self.inventory.remove(item) # retire l'exemplaire de l'item dans l'inventaire
                return
            
    def collect_on_ground_item(self, on_ground_item: OnGroundItem) -> tuple[Item, OnGroundItem]:
        # ajouter les items dans l'inventaire en jeu
        for item in self.all_items:
            # chercher les items via leur ID 
            if on_ground_item.item_id == item.item_id:
                # une fois l'item identifié, on le retourne
                return item, on_ground_item
                
            
    def save_inventory(self) -> None:
        # récupérer l'inventaire dans une liste qui va être sauvegardé
        save_data: list = []
        for item in self.inventory:
            save_data.append({
                "ID": item.item_id,
                "Quantity": item.quantity
            })

        # écrire cette liste dans le fichier de sauvegarde
        with open(self.inventory_save_file, "w+") as file:
            # cibler la ligne 0 du fichier (placer le pointeur)
            file.seek(0)
            json.dump(save_data, file, indent=4)

            print("C'est sauvegardé")

    # récupérer les items de la sauvegarde puis les mettre dans l'inventaire
    def load_inventory(self) -> None:
        with open(self.inventory_save_file, "r") as file:
            # charger la liste des items qui ont été sauvegardés
            saved_inventory: list = json.loads(file.read())
        
        for saved_item in saved_inventory:
            # ajouter les items dans l'inventaire en jeu
            for item in self.all_items:
                # chercher les items via leur ID 
                if saved_item["ID"] == item.item_id:
                    # ajouter les items le nombre de fois qu'il y en a dans l'inventaire
                    for _ in range(saved_item["Quantity"]):
                        self.add_item(item)
            
            
