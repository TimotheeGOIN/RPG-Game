import json, os

item_list_file = "save_files/all_items.json"
language_file = "langs/french.json"

files: list[str] = [item_list_file, language_file]


class ItemAdder:

    @staticmethod
    def help_command() -> None:
        print(" -a pour ajouter un item"
              "\n -ca pour ajouter une caractéristique à tous les items"
              "\n -cr pour retirer une caractéristique à tous les items"
              "\n -h pour afficher les commandes d'aide"
              "\n -l pour la liste d'items"
              "\n -r pour retirer un item grâce à son ID")

    @staticmethod
    def ensure_files_exist() -> None:
        # verif si le fichier existe sinon le créer (osef pour cette utilisation)
        for file_path in files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Le fichier à {file_path} n'existe pas ou n'a pas pu être chargé.")

    @staticmethod
    def sort_languages_files() -> None:
        # charger le dictionnaire de traduction
        with open(language_file, "r") as file:
            raw_dictionary: dict[str, str] = json.loads(file.read())

        sorted_words_list: list[str] = list(raw_dictionary.keys())
        sorted_words_list.sort()

        # tout remettre dans un nouveau dictionnaire dans le bon ordre
        sorted_dict = {word: raw_dictionary[word] for word in sorted_words_list}

        # actualiser le fichier de traduction
        ia.actualize_json_file(language_file, sorted_dict)

    @staticmethod
    def get_type_from_str(input_value: str) -> bool | int | float | str | None:

        # vérifier si c'est un booléen
        if input_value == "True" or input_value == "true": return True
        elif input_value == "False" or input_value == "false": return False
        elif input_value == "None" or input_value == "none": return None

        try: # sinon tester de le convertir en nombre
            if int(float(input_value)) == float(input_value): # vérifier si c'est un entier
                return int(input_value)
            else:
                return float(input_value)
        except ValueError: # sinon retourne un str
            return input_value

    # choper la liste d'items dans le fichier (avec un return)
    @staticmethod
    def item_list() -> list[dict[str, any]]:
        with open(item_list_file, "r") as f:
            return json.loads(f.read())

    @staticmethod
    def actualize_json_file(json_file: str, new_content: list | dict) -> None:

        with open(json_file, "w") as f:
            f.write(json.dumps(new_content, indent=4))

    @staticmethod
    def add_caracteristic() -> None:
        item_list = ia.item_list()
        new_carac = input("Quelle est la nouvelle caractéristique à ajouter ? \n> ")

        # demander la valeur, la convertir de str à la valeur concernée puis l'ajouter
        print("Pour chaque item, vous entrerez la valeur de cette caractéristique qu'il doit posséder.")
        for item in item_list:
            new_carac_value = input(f"Saisissez la valeur pour {item['Name']} : ")
            new_carac_value = ia.get_type_from_str(new_carac_value)

            # l'ajouter
            item[new_carac] = new_carac_value

        # écrire la nouvelle liste dans le fichier
        ia.actualize_json_file(item_list_file, item_list)
        print("Caractéristique ajoutée")

    @staticmethod
    def remove_caracteristic() -> None:
        item_list = ia.item_list()
        to_remove_carac = input("Quelle est la caractéristique à retirer ? \n> ")

        for item in item_list:
            item.pop(to_remove_carac)

        # écrire la nouvelle liste dans le fichier
        ia.actualize_json_file(item_list_file, item_list)
        print("Suppression effectuée")

    @staticmethod
    def add_item() -> None:
        item_list = ia.item_list()
        item_id = len(ia.item_list()) + 100
        item_name = input("Quel est son nom ? \n> ")
        item_image_link = input("Quel est le nom du fichier de son image ? \n> ")
        is_item_stackable = bool(input("Est ce que l'objet est stackable ? 1 pour True et 0 pour False\n"))

        # format des caractéristiques des items dans le fichier btw
        new_item = {
            "ID": item_id,
            "Name": item_name,
            "Link": f"assets/items/{item_image_link}",
            "Stackable" : is_item_stackable
            }

        # ajouter l'item à la liste
        item_list.append(new_item)

        # écrire la nouvelle liste dans le fichier
        ia.actualize_json_file(item_list_file, item_list)
        print("L'item a été ajouté")

    # retirer un item
    @staticmethod
    def remove_item() -> None:

        item_list = ia.item_list()
        item_id = input("Quel est l'id de l'item à supprimer ? \n> ")

        # dégager l'item à supprimer
        for i, item in enumerate(item_list):

            if item["ID"] == int(item_id):

                item_list.pop(i)

        # écrire la nouvelle liste dans le fichier
        ia.actualize_json_file(item_list_file, item_list)
        print("Suppression effectuée")

    @staticmethod
    def actualize_to_utf_8(name: str) -> None:
        # charger les dialogues depuis un fichier sinon marque une erreur
        try:
            # ouvrir le fichier correspondant au nom du pnj
            with open(f"dialogs/{name}_dialogs.json", "r") as file:

                dialogs = json.load(file)


        except FileNotFoundError:
            print("Le fichier de dialogue ciblé n'existe pas")
            return

        with open(f"dialogs/{name}_dialogs.json", "w+") as file:

            file.write(json.dumps(dialogs, indent=4))


print(f"Bienvenue ! -h pour de l'aide")

while True:

    ia = ItemAdder
    ia.ensure_files_exist()

    text = input("> ")

    match text:
        case "-a":
            ia.add_item()
        case "-ca":
            ia.add_caracteristic()
        case "-cr":
            ia.remove_caracteristic()
        case "-h":
            ia.help_command()
        case "-l":
            for item in ia.item_list():
                print(item["Name"])
        case "-s":
            ia.sort_languages_files()
        case _:
            print("Commande invalide")