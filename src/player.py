import pygame

from animation import AnimateSprite
from item import Item, ItemManager


class Entity(AnimateSprite):

    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__(name)
        self.name = name
        # initialiser l'image et son rect
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        # initialiser les valeurs concernant les déplacements
        self.position = [x, y]
        self.speed = 2
        self.normal_speed = self.speed
        # initialiser la hitbox du personnage et l'historique de la dernière position
        self.feet = pygame.Rect(0, 0, self.rect.width / 2, self.rect.height / 2)
        self.old_position = self.position.copy()

    def save_location(self) -> None:
        self.old_position = self.position.copy()

    def idle_animation(self, fps: int=60) -> None:
        self.change_animation("idle", fps)

    def move_right(self, fps: int=60) -> None:
        """ Makes the entity move to the right and initiate the corresponding animation.
        :param fps: Main loop framerate. Used to sync the animation to the main loop speed.
        """
        self.position[0] += self.speed
        self.change_animation("right", fps)

    def move_left(self, fps: int=60) -> None:
        """ Makes the entity move to the left and initiate the corresponding animation.
        :param fps: Main loop framerate. Used to sync the animation to the main loop speed.
        """
        self.position[0] -= self.speed
        self.change_animation("left", fps)

    def move_up(self, fps: int=60) -> None:
        """ Makes the entity move upward and initiate the corresponding animation.
        :param fps: Main loop framerate. Used to sync the animation to the main loop speed.
        """
        self.position[1] -= self.speed
        self.change_animation("up", fps)

    def move_down(self, fps: int=60) -> None:
        """ Makes the entity move downward and initiate the corresponding animation.
        :param fps: Main loop framerate. Used to sync the animation to the main loop speed.
        """
        self.position[1] += self.speed
        self.change_animation("down", fps)

    def update(self) -> None:
        """ Updates entity's rect's position and hitbox's position

        """
        self.rect.topleft = self.position
        self.feet.midtop = self.rect.center

    def move_back(self) -> None:
        """ Set entity's position to its previous position and updates. (like a position rollback)

        """
        self.position = self.old_position
        self.update()


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
        self.points: list[pygame.Rect] = []
        self.current_point: int = 0
        self.item_manager = ItemManager()

        # initialiser une valeur par défaut non mutable
        if items_to_give is None:
            items_to_give = []

        # récupérer les items correspondants aux ids donnés
        for item_id in items_to_give:
            for item in self.item_manager.all_items:
                if item.item_id == item_id:
                    self.items_to_give.append(item)

    def move(self) -> None:
        """ Makes the npc follow its path. Defines which direction to go and uses regular moving functions
        (move_up(), move_down(), move_left() and move_right()) to make the npc move. When the target point is reached, do
        it again with the next one.
        """

        # définir le point actuel et le point suivant
        current_point = self.current_point
        target_point = self.current_point + 1

        # repartir au premier point (si le prochain point dépasse le nombre de points)
        if target_point >= self.nb_points:
            target_point = 0

        # récupérer le rect du point actuel et du suivant
        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        # vérifier si le pnj a atteint la position du point cible
        if self.feet.topleft == target_rect.topleft:
            # passer au point suivant et sortir de la fonction (pour ne pas avancer plus et se décaler)
            self.current_point = target_point
            return

        # vérifier la position du prochain point et aller dans sa direction
        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) == 0:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) == 0:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) == 0:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) == 0:
            self.move_right()

    def teleport_spawn(self) -> None:
        location = self.points[self.current_point]
        self.position[0] = location.x - 16
        self.position[1] = location.y - 16
        self.save_location()

    def load_points(self, tmx_data) -> None:
        """Load all npc's paths points as rects
        :param tmx_data: Data of the map where points are. (loads npc's paths points of the given map)
        :return: A list of Rect
        """
        for num in range(1, self.nb_points + 1):
            # récupérer le point
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            # extraire les données du point et les rassembler dans un Rect
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
