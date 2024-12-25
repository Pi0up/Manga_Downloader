import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import zipfile
import io

# Fonction de téléchargement des chapitres depuis lelscan.net
def download_chapter_lelscan(manga_name, chapter, base_dir):
    save_dir = base_dir / manga_name
    chapter_dir = save_dir / f"chapitre-{chapter}"
    chapter_dir.mkdir(parents=True, exist_ok=True)

    i = 1
    while True:
        url = f"https://lelscan.net/scan-{manga_name}/{chapter}/{i}"
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, "html.parser")
        image_element = soup.find("img", src=True)
        if not image_element:
            break

        image_url = image_element["src"]
        image_response = requests.get(f"https://lelscan.net/{image_url}")

        if image_response.status_code == 200:
            image_path = chapter_dir / f"{i:02}.jpg"
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
        else:
            break

        i += 1

    return chapter_dir

# Fonction de téléchargement des chapitres depuis fmteam.fr
def download_chapter_fmteam(manga_name, chapter, base_dir):
    save_dir = base_dir / manga_name
    if isinstance(chapter, float):
        url = f"https://fmteam.fr/api/download/{manga_name}/fr/ch/{int(chapter)}/sub/{int((chapter - int(chapter)) * 10)}"
    else:
        url = f"https://fmteam.fr/api/download/{manga_name}/fr/ch/{chapter}"

    response = requests.get(url)

    if response.status_code == 200:
        zip_stream = io.BytesIO(response.content)
        chapter_dir = save_dir / f"chapitre-{chapter}"
        chapter_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_stream, "r") as zip_ref:
            zip_ref.extractall(chapter_dir)

        return chapter_dir
    else:
        print(f"Échec du téléchargement du chapitre {chapter} depuis fmteam.fr.")
        return None

# Fonction pour créer un PDF à partir d'un dossier d'images
def create_pdf_from_chapter(chapter_dir, pdf_path, author, series):
    images = [Image.open(chapter_dir / img) for img in sorted(os.listdir(chapter_dir)) if img.endswith('.jpg') or img.endswith('.png')]
    pdf_images = [img.convert('RGB') for img in images]

    if pdf_images:
        pdf_images[0].save(
            pdf_path,
            save_all=True,
            append_images=pdf_images[1:],
            title=pdf_path.stem,
            author=author,
            subject=series
        )

    for img in images:
        img.close()

# Exemple d'utilisation
if __name__ == "__main__":
    manga_name = "kaiju-no-8"
    author = "Naoya Matsumoto"
    series = "Kaiju no. 8"
    base_dir = Path("./mangas")
    base_dir.mkdir(parents=True, exist_ok=True)

    chapter = 1  # Exemple de chapitre

    # Téléchargement depuis lelscan.net
    chapter_dir = download_chapter_lelscan(manga_name, chapter, base_dir)

    # Téléchargement depuis fmteam.fr
    # chapter_dir = download_chapter_fmteam(manga_name, chapter, base_dir)

    if chapter_dir:
        pdf_path = base_dir / manga_name / f"{author} - Chapitre {chapter} - {series}.pdf"
        create_pdf_from_chapter(chapter_dir, pdf_path, author, series)

    print("Téléchargement et création du PDF terminés.")
