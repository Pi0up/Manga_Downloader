# Manga Downloader Scripts

## Manga Downloader

**Ancien** Script Python qui **permettait** de télécharger : toutes les pages -> d'un chapitre de manga -> du site '[www.japscan.lol](http://www.japscan.lol)'

Le script exige de préciser :

* Le nom du manga (figurant sur le site [www.japscan.lol](http://www.japscan.lol)),
* Le numéro du chapitre à télécharger
* Le Chemin + le Nom du fichier à créer

Le fichier 'Manga_Downloader.py' était utilisé pour télécharger un chapitre du manga 'jujutsu kaisen'.

## Manga Downloader V2

**Ancien** Script Python qui **permettait** de télécharger : toutes les pages -> d'un chapitre de manga -> du site '[www.japscan.lol](http://www.japscan.lol)'

Le script exige de préciser :

* Le nom du manga (figurant sur le site [www.japscan.lol](http://www.japscan.lol)),
* Le chapitre à télécharger

Le fichier 'Manga_Downloader V2.py' était utilisé pour télécharger un chapitre du manga 'jujutsu kaisen'.

## Manga Downloader V3

**Nouveau** script Python qui permet de télécharger : toutes les pages -> d'un chapitre de manga -> du site '[https://scantrad-vf.co/](https://scantrad-vf.co/)'

Prérequis :

* L'url du manga à télécharger doit être sous la forme '[https://scantrad-vf.co/manga/.../chapitre-.../?style=list](https://scantrad-vf.co/manga/.../chapitre-.../?style=list)'
* Nom du fichier à créer
* Nom du dossier à créer contenant les images

**'?style=list'** permet d'afficher toutes les pages du manga sur une seule page web.

Le fichier 'Manga_Downloader V3.py' est utilisé pour télécharger toutes les pages du premier chapitre du manga 'jujutsu kaisen'.

## Manga Downloader V4

**Nouveau** script Python qui permet de télécharger : toutes les pages -> d'un chapitre de manga -> du site '[https://lelscans.net/](https://lelscans.net/)'

Prérequis :

* Le nom du manga à télécharger
* Le numéro du chapitre à télécharger

### Évolutions depuis les versions précédentes :

* **Téléchargement des images** : Chaque image est téléchargée et sauvegardée sous un format spécifique avec des numéros à deux chiffres.
* **Conversion en PDF** : Après le téléchargement des images, un fichier PDF est créé pour chaque chapitre. Le fichier est sauvegardé avec les métadonnées suivantes :
  * Titre du chapitre
  * Auteur du manga
  * Nom de la série
* **Suppression des images après création du PDF** : Les images sont automatiquement supprimées une fois que le PDF est créé pour économiser de l'espace disque.
* **Nom du fichier PDF** : Le fichier PDF est nommé selon le format suivant :
  `Auteur - Série (Chapitre X) - Série.pdf`
  Exemple : `Naoya Matsumoto - Kaiju no. 8 (Chapitre 2) - Kaiju no. 8.pdf`.

## Manga Downloader V5

**Nouveau** script Python qui permet de télécharger : Tout un chapitre de manga -> du site '[https://fmteam.fr/comics](https://fmteam.fr/comics)'

Prérequis :

* Le nom du manga à télécharger
* Le numéro du chapitre à télécharger
* Le chemin où stocker les téléchargements

Le fichier 'Manga_Downloader V5.py' est utilisé pour télécharger le chapitre 1424 du manga 'hajime-no-ippo'.

---

## Installation des dépendances

Avant de lancer les scripts, vous devez installer les bibliothèques Python nécessaires. Utilisez les commandes suivantes pour installer les dépendances :

1. **Téléchargez ou clonez le repository**
2. **Installez les dépendances :**
   Utilisez `pip` pour installer les bibliothèques nécessaires :

   ```bash
   pip install -r requirements.txt
   ```
3. **Vérifiez l'installation** :
   Assurez-vous que toutes les bibliothèques sont installées correctement en exécutant :

   ```bash
   pip list
   ```
