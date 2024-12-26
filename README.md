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

## Disclaimer

Ce script est fourni à des fins éducatives et personnelles uniquement. En utilisant ce script, vous acceptez les conditions suivantes :

1. **Respect des droits d'auteur** :
   Vous êtes seul responsable de l'utilisation de ce script. Les œuvres téléchargées peuvent être protégées par des droits d'auteur. Vous devez obtenir l'autorisation explicite des détenteurs de droits avant de télécharger, de distribuer ou d'utiliser tout contenu. L'auteur de ce script décline toute responsabilité en cas d'utilisation non autorisée.
2. **Utilisation légale** :
   Ce script est conçu pour être utilisé uniquement dans des contextes où les téléchargements et l'utilisation des œuvres sont conformes aux lois en vigueur dans votre juridiction. Toute utilisation à des fins illégales est strictement interdite.
3. **Absence de garantie** :
   Ce script est fourni "tel quel", sans aucune garantie d'aucune sorte. L'auteur n'assume aucune responsabilité pour les dommages ou les conséquences résultant de son utilisation.
4. **Responsabilité individuelle** :
   Il est de votre responsabilité de vérifier les lois locales concernant les téléchargements d'œuvres protégées par des droits d'auteur et de respecter les conditions d'utilisation des sites que vous utilisez avec ce script.

En utilisant ce script, vous déclarez avoir lu, compris et accepté ce disclaimer. Si vous n'acceptez pas ces termes, vous ne devez pas utiliser ce script.
