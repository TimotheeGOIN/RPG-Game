import pygame

# classe gérant l'animation des sprites
class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name: str) -> None:
        super().__init__()
        # initialiser vitesse par défaut (peut être supprimé d'ici dans l'absolu)
        self.speed = 2
        self.sprite_sheet = pygame.image.load(f'sprites/{name}.png')
        self.is_idling = False
        self.active_animation = ""
        self.animation_index = 0
        self.clock = 0
        # récupérer les images tous les 32 pixels
        self.images = {
            'down': self.get_list_images(0, 3),
            'left': self.get_list_images(32, 3),
            'right': self.get_list_images(64, 3),
            'up': self.get_list_images(96, 3),
            'idle': self.get_list_images(128, 5)
        }

    def change_animation(self, animation: str, fps: int) -> None:
        # si l'animation qui va être jouée est nouvelle (pas comme celle qui se jouait actuellement)
        # alors la clock se reset
        if animation != self.active_animation:
            self.active_animation = animation
            self.animation_index = 0
            self.clock = 0

        # jouer l'animation pour l'idle
        if animation == "idle":
            # vitesse de l'animation 'idle'
            if self.is_idling:
                self.clock += 30

            # attendre 5 secondes avant de jouer 'idle'
            elif not self.is_idling:
                if self.clock >= fps * 10:
                    self.clock = 0
                    self.is_idling = True
                else:
                    self.clock += 2
                return

        # jouer l'animation pour les déplacements
        elif animation == "right" or animation == "left" or animation == "up" or animation == "down":
            # reset l'idling
            self.is_idling = False
            # vitesse d'animation pour les déplacements
            self.clock += self.speed * 48

        # 600 correspond à 60 (nombre de fps du jeu) x10 (pour plus de précision)
        if self.clock >= fps * 10:  # fps * 10 correspond à 600

            # passer à l'image suivante et reset la clock
            self.animation_index += 1
            self.clock = 0

            # remettre au debut de l'animation
            if self.animation_index >= len(self.images[animation]):
                self.animation_index = 0

        # jouer l'animation
        # vérifier que l'index ne dépasse pas le nombre d'images de l'animation en cours
        # par exemple passage de 'idle' → index = 4 à 'down' dysfonctionne car 'down' a seulement 3 images (0 à 2)
        if self.animation_index >= len(self.images[animation]):
            self.animation_index = 0

        # récupérer l'image correspondant à l'animation et à l'index
        self.image: pygame.Surface = self.images[animation][self.animation_index]
        self.image.set_colorkey(0, 0)

    def get_list_images(self, y: int, images_amount: int=3) -> list[pygame.Surface]:
        images = []

        # récupérer le nombre d'images demandé sur le sprite sheet
        for i in range(0, images_amount):
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)

        return images

    def get_image(self, x: int, y: int) -> pygame.Surface:
        # définir une image par une taille de 32x32
        image = pygame.Surface([32, 32])
        # découper l'image de 32x32 puis la renvoyer
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
