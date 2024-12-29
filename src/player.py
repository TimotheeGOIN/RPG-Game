import pygame

from animation import AnimateSprite
from item import Item, ItemManager


class Entity(AnimateSprite):

    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__(name)
        # partie gestion de l'image du perso
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        # partie déplacement du perso
        self.position = [x, y]
        self.speed = 2
        self.normal_speed = self.speed
        # partie gestion de l'animation primitive du perso
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 16)
        self.old_position = self.position.copy()
        print(f"{name}: rect > {self.rect}")
        print(f"{name}: feet > {self.feet}")

    def save_location(self) -> None:
        self.old_position = self.position.copy()

    def idle_animation(self, fps: int=60) -> None:
        self.change_animation("idle", fps)

    def move_right(self, fps: int=60) -> None:
        """ Makes the entity move to the right.
        :param fps: Pass the main loop fps for synchronization of the animation.
        """
        self.position[0] += self.speed
        self.change_animation("right", fps)

    def move_left(self, fps: int=60) -> None:
        """ Makes the entity move to the left.
        :param fps: Pass the main loop fps for synchronization of the animation.
        """
        self.position[0] -= self.speed
        self.change_animation("left", fps)

    def move_up(self, fps: int=60) -> None:
        """ Makes the entity move upward.
        :param fps: Pass the main loop fps for synchronization of the animation.
        """
        self.position[1] -= self.speed
        self.change_animation("up", fps)

    def move_down(self, fps: int=60) -> None:
        """ Makes the entity move downward.
        :param fps: Pass the main loop fps for synchronization of the animation.
        """
        self.position[1] += self.speed
        self.change_animation("down", fps)

    def update(self) -> None:
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self) -> None:
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):

    def __init__(self) -> None:
        super().__init__("player", 0, 0)
        self.speed = 2
        self.normal_speed = self.speed


class NPC(Entity):

    def __init__(self, name: str, nb_points: int, dialog: list[str], items_to_give: list[tuple[int, int]]=None) -> None:
        super().__init__(name, 0, 0)
        self.name: str = name
        self.speed: float = 0.75
        self.items_to_give: list[Item] = []
        self.dialog: list[str] = dialog
        # caractéristiques pour charger le pnj
        self.nb_points: int = nb_points
        self.points = []
        self.current_point: int = 0
        self.item_manager = ItemManager()

        # initialiser une valeur par défaut
        if items_to_give is None:
            items_to_give = []

        # récupérer les items correspondants aux ids donnés
        for item_id in items_to_give:
            for item in self.item_manager.all_items:
                if item.item_id == item_id:
                    self.items_to_give.append(item)
        print(self.items_to_give)

    def move(self) -> None:
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        # vérifier la position du prochain point et aller dans sa direction
        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 1:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 1:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 1:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 1:
            self.move_right()

        if self.feet.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self) -> None:
        location = self.points[self.current_point]
        self.position[0] = location.x - 16
        self.position[1] = location.y - 16
        self.save_location()

    def load_points(self, tmx_data) -> None:
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
