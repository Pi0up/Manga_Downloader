import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import json


# Fonction pour extraire les chapitres depuis le select de la page
def update_chapters_list(manga_url, file_name, mangas_folder, mangas_json_path):
    response = requests.get(manga_url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page {manga_url}.")
        return False
    
    soup = BeautifulSoup(response.content, "html.parser")
    select_element = soup.select_one("#header-image > h2 > form > select:nth-child(1)")

    if not select_element:
        print(f"Aucun élément 'select' trouvé pour {file_name}.")
        return False
    
    chapters = []
    for option in select_element.find_all("option"):
        chapter_url = option["value"]
        chapter_number = option.get_text()
        chapters.append({"chapter_number": chapter_number, "chapter_url": chapter_url})
    
    # Charger les mangas existants depuis le fichier JSON
    if mangas_json_path.exists():
        with open(mangas_json_path, "r") as f:
            mangas_data = json.load(f)
    else:
        mangas_data = []
    
    # Mettre à jour la liste des chapitres pour ce manga
    for manga in mangas_data:
        if manga["file_name"] == file_name:
            manga["chapters"] = chapters
            break
    else:
        # Si le manga n'est pas encore dans le JSON, l'ajouter
        mangas_data.append({
            "file_name": file_name,
            "chapters": chapters,
            "author_name": "Unknown",  # Vous pouvez ajuster cela selon vos besoins
            "series_name": "Unknown",  # Vous pouvez ajuster cela selon vos besoins
        })

    # Sauvegarder les données mises à jour dans le fichier JSON
    with open(mangas_json_path, "w") as f:
        json.dump(mangas_data, f, indent=4)
    
    print(f"Liste des chapitres mise à jour pour {file_name}.")
    return chapters  # Retourne la liste des chapitres


# Fonction de téléchargement d'une image
def download_image_from_xpath(response_url, save_path, i):
    if response_url.status_code == 200:
        # Parser le contenu HTML
        soup = BeautifulSoup(response_url.content, "html.parser")
        image_element = soup.find("img", src=True)
        
        if image_element:
            image_url = image_element["src"]

            # Construire l'URL complète si nécessaire
            full_image_url = image_url if image_url.startswith("http") else f"https://lelscans.net/{image_url}"

            # Télécharger l'image
            image_response = requests.get(full_image_url)

            if image_response.status_code == 200:
                # Sauvegarder l'image dans le fichier spécifié
                with open(save_path, 'wb') as f:
                    f.write(image_response.content)
                print(f"Image {i:02d} téléchargée.")  # Affichage du numéro formaté
                return True
            else:
                print(f"Échec du téléchargement de l'image. Code d'état : {image_response.status_code}")
                return False
        else:
            print("Aucune image trouvée sur la page.")
            return False
    else:
        print(f"Échec de la requête HTTP. Code d'état : {response_url.status_code}")
        return False


# Fonction pour convertir les images en PDF avec métadonnées
def create_pdf_from_images(image_folder, pdf_path, author_name, series_name, chapter):
    image_files = sorted(image_folder.glob("*.jpg"))  # Trier les images par numéro de page
    if not image_files:
        print(f"Aucune image trouvée dans {image_folder}.")
        return False

    images = [Image.open(img_path).convert("RGB") for img_path in image_files]
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Format du nom du PDF
    pdf_filename = f"{author_name} - {series_name} (Chapitre {chapter}) - {series_name}.pdf"
    pdf_path = pdf_path.parent / pdf_filename

    # Ajouter les métadonnées du PDF
    metadata = {
        "Title": f"Chapitre {chapter}",
        "Author": author_name,
        "Subject": series_name,
        "Creator": "Python Script",
        "Producer": series_name,
    }

    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"PDF créé : {pdf_path}")

    # Supprimer les images après la création du PDF
    for img_path in image_files:
        img_path.unlink()

    # Supprimer le dossier du chapitre après suppression des images
    try:
        image_folder.rmdir()
        print(f"Dossier du chapitre supprimé : {image_folder}")
    except OSError:
        print(f"Impossible de supprimer le dossier {image_folder}. Il n'est peut-être pas vide.")
    
    return True


# Fonction pour télécharger un chapitre
def download_chapter(file_name, chapter, script_directory, author_name, series_name, downloaded_chapters, mangas_folder):
    # Vérifier si la clé existe dans le dictionnaire global
    if file_name not in downloaded_chapters:
        downloaded_chapters[file_name] = []

    # Vérification si le PDF existe déjà
    manga_folder = mangas_folder / file_name
    pdf_path = manga_folder / f"{file_name} - {series_name} (Chapitre {chapter}) - {series_name}.pdf"
    if pdf_path.exists():
        print(f"Le PDF du chapitre {chapter} existe déjà. Mise à jour du fichier de suivi.")
        if chapter not in downloaded_chapters[file_name]:
            downloaded_chapters[file_name].append(chapter)  # Mise à jour
        return False  # Sauter ce chapitre

    # Créer le dossier pour les images
    chapter_folder = manga_folder / f"chapitre-{chapter}"
    chapter_folder.mkdir(parents=True, exist_ok=True)

    # Téléchargement des images
    i = 1
    while True:
        url = f"https://lelscans.net/scan-{file_name}/{chapter}/{i}"
        print(f"Téléchargement de la page {i:02d} depuis {url}...")
        response_url = requests.get(url)
        save_path = chapter_folder / f"{i:02d}.jpg"
        if download_image_from_xpath(response_url, save_path, i):
            i += 1
        else:
            break

    # Génération du PDF
    if create_pdf_from_images(chapter_folder, pdf_path, author_name, series_name, chapter):
        downloaded_chapters[file_name].append(chapter)  # Mise à jour après création du PDF
        print(f"Chapitre {chapter} de {file_name} ajouté à la liste des chapitres téléchargés.")
        return True
    else:
        print(f"Échec de la création du PDF pour le chapitre {chapter}.")
        return False


# Fonction principale pour télécharger plusieurs chapitres à partir de mangas.json
def download_manga(file_name, script_directory, author_name, series_name, downloaded_chapters, mangas_folder, json_file):
    # Charger les chapitres depuis le fichier JSON
    with open(json_file, "r") as f:
        mangas_data = json.load(f)

    # Trouver le manga dans la liste
    manga = next((m for m in mangas_data if m["file_name"] == file_name), None)
    if not manga:
        print(f"Manga {file_name} introuvable dans {json_file}.")
        return

    # Mettre à jour la liste des chapitres disponibles
    manga_url = f"https://lelscans.net/scan-{file_name}/1"
    if not update_chapters_list(manga_url, file_name, mangas_folder, Path(json_file)):
        print(f"Impossible de mettre à jour les chapitres pour {file_name}.")
        return

    # Recharger le fichier JSON pour avoir les mises à jour
    with open(json_file, "r") as f:
        mangas_data = json.load(f)
    manga = next((m for m in mangas_data if m["file_name"] == file_name), None)
    chapters = manga.get("chapters", [])

    if not chapters:
        print(f"Aucun chapitre disponible pour {file_name}.")
        return

    # Créer le dossier du manga
    manga_folder = mangas_folder / file_name
    manga_folder.mkdir(parents=True, exist_ok=True)

    # Téléchargement des chapitres
    for chapter in chapters:
        chapter_number = chapter["chapter_number"]
        chapter_url = chapter["chapter_url"]

        print(f"\nTéléchargement du chapitre {chapter_number} de {series_name} ({file_name})...")
        if chapter_number in downloaded_chapters.get(file_name, []):
            print(f"Chapitre {chapter_number} déjà téléchargé. Passage au suivant.")
            continue

        if download_chapter(file_name, chapter_number, script_directory, author_name, series_name, downloaded_chapters, mangas_folder):
            print(f"Chapitre {chapter_number} de {file_name} téléchargé avec succès.")
        else:
            print(f"Échec du téléchargement du chapitre {chapter_number} de {file_name}.")

        # Sauvegarder la progression
        with open(downloaded_chapters_file, "w") as f:
            json.dump(downloaded_chapters, f, indent=4)




# Fonction pour lire les mangas depuis un fichier JSON et lancer leur téléchargement
def download_mangas_from_json(json_file, script_directory, downloaded_chapters_file, mangas_folder):
    # Charger les chapitres déjà téléchargés depuis le fichier global
    if Path(downloaded_chapters_file).exists():
        with open(downloaded_chapters_file, 'r') as f:
            downloaded_chapters = json.load(f)
    else:
        downloaded_chapters = {}

    with open(json_file, 'r') as f:
        data = json.load(f)

    for manga in data:
        file_name = manga['file_name']
        author_name = manga['author_name']
        series_name = manga['series_name']

        if file_name not in downloaded_chapters:
            downloaded_chapters[file_name] = []

        print(f"\nTéléchargement de {series_name} ({file_name})...")
        download_manga(file_name, script_directory, author_name, series_name, downloaded_chapters, mangas_folder, json_file)

        # Sauvegarder les chapitres téléchargés dans le fichier global
        with open(downloaded_chapters_file, 'w') as f:
            json.dump(downloaded_chapters, f)

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(__file__).parent

# Dossier principal pour les mangas
mangas_folder = script_directory / "mangas"
mangas_folder.mkdir(parents=True, exist_ok=True)

# Chemin vers le fichier JSON contenant les informations des mangas et le fichier de suivi des chapitres téléchargés
json_file = script_directory / "mangas.json"
downloaded_chapters_file = script_directory / "downloaded_chapters.json"

# Lancer le téléchargement des mangas
download_mangas_from_json(json_file, script_directory, downloaded_chapters_file, mangas_folder)