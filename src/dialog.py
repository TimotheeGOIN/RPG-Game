import pygame

from interfaces import ItemInfosWindow
from src.interfaces import InterfaceManager


class DialogBox:

    def __init__(self, screen: pygame.Surface):
        # initialiser les valeurs de bases du texte (police, espacement entre chaque ligne)
        self.reading = False
        self.font_size = 18
        self.font = pygame.font.Font("dialogs/dialog_font.ttf", self.font_size)
        self.text_padding: int = round(self.font_size * 4/3) # 4/3 correspond au ratio 1.333
        # créer la boite de texte
        self.box = pygame.image.load("dialogs/dialog_box_test.png")
        self.box = pygame.transform.scale(self.box, (650, 100))
        # gérer sa position
        self.box_rect = self.box.get_rect()
        self.box_rect.x = screen.get_width() / 2 - self.box_rect.width / 2
        self.box_rect.y = screen.get_height() * (1 - 0.05) - self.box_rect.height
        # définir le texte et ses caractéristiques
        self.texts: list[str] = []
        self.text_index: int = 0
        self.letter_index: int = 25

    def execute(self, dialog: list[str]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render(self, screen: pygame.Surface):
        if self.reading:
            self.letter_index += 1

            # si l'index de la lettre est au max le stopper
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            # afficher la boite de dialogue et le texte dedans
            screen.blit(self.box, self.box_rect)
            for i, text in enumerate(InterfaceManager.separate_text(self.texts[self.text_index][0:self.letter_index], 40, self.font, "black", True, True)):

                screen.blit(text, (self.box_rect.x + 35, self.box_rect.y + 15 + i*self.text_padding))

    # passer au dialogue suivant
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            # fermer le dialogue
            self.reading = False
