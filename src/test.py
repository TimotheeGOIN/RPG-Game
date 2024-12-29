import json, pygame, tkinter, time, sys
import pyautogui as pg

a: set[int] = {1, 2, 3}
b: set[int] = {2, 3, 4}

pygame.init()
pos = None
screen = pygame.display.set_mode((720, 480), pygame.RESIZABLE)
running = True


"""
conv_test = int(float("23.23"))
print(f"tests conversions : {conv_test}")
print(f"tests conversions : {float(conv_test)}")

pos_test: tuple = (25, 6)

x = 25
y = 6

print(pg.size())

if (x, y) == pos_test:
    print("Zob")

dark_strenght_lvls = {"high": 7, "mid": 5, "low": 3}

print(dark_strenght_lvls["low"])

# recup les dialogues dans le fichier json
with open('../dialogs/robin_dialogs.json', 'r') as file:
    dialogs: list[str] = json.load(file)

# afficher les dialogues
print(dialogs[0])

if pos_test == (x, y):
    pass
elif pos_test != (25, 6):
    print("Cela n'a pas été skipé")

print(pos_test[0])
print(bool(0))
"""
"""[
<item.Item object at 0x000002516F060CB0>, 
<item.Item object at 0x000002516F0606E0>, 
<item.Item object at 0x000002516F060110>, 
<item.Item object at 0x000002516F0608C0>, 
<item.Item object at 0x000002516F060830>, 
<item.Item object at 0x000002516F060B90>, 
<item.Item object at 0x000002516F060F50>, 
<item.Item object at 0x000002516F0600B0>, 
<item.Item object at 0x000002516F0607A0>
]"""

def fibonacci(n: int) -> int:
    """1, 1, 2, 3, 5, 8, 13, 21, 34, 55"""

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def substract_positions(first_tuple, second_tuple) -> tuple[int, int]:
    return first_tuple[0] + second_tuple[0], first_tuple[1] + second_tuple[1]

print(f"{substract_positions((1, 2), (3, 4))}")


def separate_text(text: str, limit: int, font: pygame.font.Font | None, color: str | tuple[int, int, int] = "black",
                  antialiasing: bool = True, to_surface: bool = False) -> list[str] | list[pygame.Surface] | None:
    text_list = []
    # vérifie que le texte a bien besoin d'être divisé
    if not len(text) > limit:
        return [font.render(text, antialiasing, color)]

    # faire autant de fois qu'il y a de "limite" entière dans le texte (limite par rapport à la longueur du texte)
    for i in range(len(text) // limit):
        # récupère un bout du text de 0 jusqu'à la limite (pour 1er tour de boucle)
        text_list.append(text[limit * i:limit * (i + 1)])

        # ajoute "-" pour le visuel (fin de ligne) si le dernier caractère n'est pas un "." ou un espace " "
        if not text_list[i][-1] in " .":
            text_list[i] += "-"

    # récupère le dernier bout dans le texte (longueur%limite*limite pour aller là où s'arrête le //)
    text_list.append(text[len(text) // limit * limit:len(text) + 1])

    # convertir les textes en surfaces si c'est demandé
    if to_surface:
        for i in range(len(text_list)):
            text_list[i] = font.render(text_list[i], antialiasing, color)

    return text_list

def separate_text_v2(text: str, limit: int, font: pygame.font.Font | None, color: str | tuple[int, int, int] = "black",
                     antialiasing: bool = True, to_surface: bool = False) -> list[str] | list[pygame.Surface] | None:
    # vérifie que le texte a bien besoin d'être divisé
    if not len(text) > limit:
        return [font.render(text, antialiasing, color)]

    # initialiser les listes
    texts_list = []
    words_list = []
    all_words = text.split()

    for word in all_words:
        # actualise la longueur des mots qui sont actuellement dans la "mémoire" de la boucle
        string_lenght = sum([len(wd) for wd in words_list])

        # vérifie si on peut ajouter le mot à la "mémoire" sans dépasser la limite
        if string_lenght + len(word) >= limit:
            # créer une liste à partir de tous les mots jusqu'à présent puis vider la liste "mémoire" des mots
            texts_list.append(" ".join(words_list))
            words_list.clear()

        # ajouter le mot à la liste "mémoire"
        words_list.append(word)
    # ajouter des mots à la liste de phrases encore s'il reste des mots résiduels
    texts_list.append(" ".join(words_list))

    # convertir les textes en surfaces si c'est demandé
    if to_surface:
        for i in range(len(texts_list)):
            texts_list[i] = font.render(texts_list[i], antialiasing, color)

    return texts_list

print(separate_text_v2("Bon ceci est un test et il faut quand même metre pas mal de caractères", 15, None))

test = [1, 6, 8, 2 ,3, 9, 7, 1 ,8]
print([t for t in test])

print(separate_text("je suis la oui j'aime beaucoup Candice de tout mon coeur même", 5, None))