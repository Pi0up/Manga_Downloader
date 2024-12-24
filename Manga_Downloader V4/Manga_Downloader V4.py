import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image

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
    
    # Format du nom du PDF : Auteur - Titre (nom du livre, exemple chapitre 2) - Série.pdf
    pdf_filename = f"{author_name} - {series_name} (Chapitre {chapter}) - {series_name}.pdf"
    pdf_path = pdf_path.parent / pdf_filename

    # Ajouter les métadonnées du PDF
    metadata = {
        "Title": f"Chapitre {chapter}",
        "Author": author_name,
        "Subject": series_name,  # Nom de la série comme groupe
        "Creator": "Python Script",
        "Producer": series_name  # Alias pour les liseuses qui reconnaissent ce champ
    }

    images[0].save(pdf_path, save_all=True, append_images=images[1:], author=metadata["Author"], producer=metadata["Producer"], title=metadata["Title"], subject=metadata["Subject"])
    print(f"PDF créé : {pdf_path}")
    
    # Supprimer les images après la création du PDF
    for img_path in image_files:
        img_path.unlink()
    print(f"Images supprimées dans {image_folder}.")
    return True

# Fonction pour télécharger un chapitre
def download_chapter(file_name, chapter, script_directory, author_name, series_name):
    i = 1  # Page de départ
    chapter_file = f'chapitre-{chapter}'  # Nom du dossier à créer pour le chapitre
    nom_fichier = script_directory / file_name
    nom_fichier.mkdir(exist_ok=True)
    nom_chapitre = nom_fichier / chapter_file
    nom_chapitre.mkdir(exist_ok=True)

    while True:  # Téléchargement des images
        url = f"https://lelscans.net/scan-{file_name}/{chapter}/{i}"  # Lien vers le chapitre à télécharger
        print(f"Téléchargement de la page {i:02d} depuis {url}...")
        response_url = requests.get(url)
        save_path = nom_chapitre / f"{i:02d}.jpg"  # Chemin où sauvegarder les images avec numérotation à deux chiffres
        response = download_image_from_xpath(response_url, save_path, i)
        if response:
            i += 1
        else:
            print(f"Téléchargement du chapitre {chapter} terminé.") 
            break

    # Générer un PDF pour le chapitre
    pdf_path = script_directory / file_name / f"{file_name}-chapitre-{chapter}.pdf"
    create_pdf_from_images(nom_chapitre, pdf_path, author_name, series_name, chapter)

# Fonction principale pour télécharger plusieurs chapitres
def download_manga(file_name, start_chapter, end_chapter, script_directory, author_name, series_name):
    for chapter in range(start_chapter, end_chapter + 1):
        print(f"Début du téléchargement du chapitre {chapter}...")
        download_chapter(file_name, chapter, script_directory, author_name, series_name)
        print(f"Chapitre {chapter} terminé.\n")

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(__file__).parent

# ========================================== Variables initiales ==================================================================
file_name = 'kaiju-no-8'  # Nom du fichier à créer / nom du manga
start_chapter = 1  # Numéro du premier chapitre à télécharger
end_chapter = 5  # Numéro du dernier chapitre à télécharger
author_name = "Naoya Matsumoto"  # Auteur du manga
series_name = "Kaiju no. 8"  # Nom de la série
# =================================================================================================================================

# Lancer le téléchargement
download_manga(file_name, start_chapter, end_chapter, script_directory, author_name, series_name)
