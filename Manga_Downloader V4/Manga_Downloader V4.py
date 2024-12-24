import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup

# Fonction de téléchargement
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
                print(f"Image {i} téléchargée.")
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

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(__file__).parent

# ========================================== Variables initiales ==================================================================
File_name = 'kaiju-no-8'  # Nom du fichier à créer / nom du manga
chapter = 1  # numéro du chapitre à télécharger
chapter_file = f'chapitre-{chapter}'  # Nom du dossier à créer contenant les images
i = 1  # Page de départ
# =================================================================================================================================

nom_fichier = script_directory / File_name
nom_fichier.mkdir(exist_ok=True)

nom_chapitre = nom_fichier / chapter_file
nom_chapitre.mkdir(exist_ok=True)

while True:  # Téléchargement des images
    url = f"https://lelscans.net/scan-{File_name}/{chapter}/{i}"  # Lien vers le chapitre à télécharger
    print(f"Téléchargement de la page {i} depuis {url}...")
    response_url = requests.get(url)
    save_path = nom_chapitre / f"{i}.jpg"  # Chemin où sauvegarder les images
    response = download_image_from_xpath(response_url, save_path, i)
    if response:
        i += 1
    else:
        print("Téléchargement terminé.") 
        break
