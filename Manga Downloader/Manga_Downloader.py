import os
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

# Update du script :  Demande des informations à l'utilisateur 

#======================================================================================================================================================================
#================================================================== Les variables de départ ===========================================================================
page = 1 # Page de départ
chapter = 1 # Chapitre 
nom_fichier='Chap1' # Nom du fichier
lien_chapitre=str(f'https://www.japscan.lol/lecture-en-ligne/jujutsu-kaisen/{chapter}/{page}.html')
nombre_pages= 51
#======================================================================================================================================================================

# Création du répertoire pour enregistrer les images
if not os.path.exists(nom_fichier):
    os.makedirs(nom_fichier)

# ----- Configuration de Selenium pour utiliser Chrome -----
# Chemin vers le profil Chrome
chrome_profile_path = '/Users/charles-albert/Library/Application Support/Google/Chrome/Default'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
driver = webdriver.Chrome(options=options,executable_path='/Users/charles-albert/Desktop/chromedriver_mac_arm64/chromedriver') # Chemin vers l'exécutable chromedriver
driver.maximize_window() # Ouvrir le navigateur en full size
# -----------------------------------------------------------

# Accès à la page en question avec Selenium
driver.get(lien_chapitre)
soup = BeautifulSoup(driver.page_source, 'html.parser')

def crop(path_image,size):

    # Récupérer l'image capturée
    image = Image.open(path_image)

    # Dimensions de l'image initiale
    initial_width = size['width'] # Largeur initiale image
    initial_height = size['height'] # Hauteur initiale image

    # Dimensions du screenshot
    screen_width = image.width # Largeur screenshot
    screen_height = image.height # Hauteur screenshot

    # Calculer les coordonnées de recadrage
    x = 0,9*(screen_width - initial_width) // 2
    y = 0*9(screen_height - initial_height) // 2

    # Recadrer l'image pour ne conserver que l'élément souhaité
    image = image.crop((x, y, x + initial_width, y + initial_height))

    # Enregistrer l'image recadrée
    image.save(path_image)

# Rechercher l'image => Faire un screenshot => Redimensionner l'image => la télécharger
while page <= nombre_pages:

    # Obtention de la balise contenant l'URL de l'image
    image_element = soup.find('div', id='single-reader')

    # Obtention de l'URL de l'image
    image_url = image_element.find('img', class_='img-fluid')['src']

    # Trouver l'élément souhaité sur la page à partir de l'URL de l'image
    element = driver.find_element_by_xpath('//*[@id="single-reader"]/img')
    size = element.size #size[0]= height et . width

    driver.get(image_url)

    # chemin de sauvegarde de l'image
    path_image = f"{nom_fichier}/page{page}.png"

    # prendre le screenshot de la page entière
    driver.save_screenshot(path_image)
    
    # Crop l'image aux bonnes dimensions et la sauvegarder
    crop(path_image,size)

    print(f"Page {page} téléchargée.")

    # Accès à la page suivante
    page += 1
    if page > nombre_pages:
        break
    else:
        lien_chapitre=str(f'https://www.japscan.lol/lecture-en-ligne/jujutsu-kaisen/{chapter}/{page}.html')
        driver.get(lien_chapitre)
    
# Fermeture du navigateur
driver.quit()

print(f"\nTéléchargement du Chapitre {chapter} terminé.")
