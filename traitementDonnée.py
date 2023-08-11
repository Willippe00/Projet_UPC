from DataBaseManager import DataBaseManager
import itertools
from skimage import io
from skimage.metrics import structural_similarity as ssim
import os
import urllib.request
from skimage.transform import resize
import shutil
class traitementDonnée:
    DataBase = None

    def __init__(self):
        self.DataBase = DataBaseManager()

    def CreerDictionnaire(self, RB_product):

        nom, Rb_sku, Image_path, fournisseur, fournisseur_sku = self.DataBase.getproductRB(RB_product)

        dictionnaire = []

        if nom == None:
            return []
        else:
            dictionnaire.append(fournisseur_sku)
            dictionnaire.append(fournisseur_sku + " "+fournisseur)
            dictionnaire.append(fournisseur)
            dictionnaire.append(Rb_sku)

            dictionnaire.append(nom.split('(', 1)[0])

            dictionnaire.extend(self.recombinaison_paquets(nom))

            print("dictionnaire")
            print(dictionnaire)

            return dictionnaire

    def recombinaison_paquets(self, Rb_code):
        # Séparation de la chaîne en mots



        #mots = Rb_code.split()
        mots = self.retirer_mots_deux_lettres(Rb_code)
        mots = mots.split()


        # Vérification du nombre de mots pour s'assurer qu'il y en a au moins 3
        if len(mots) < 3:
            return []

        # Séparer les mots en paquets de 4
        paquets = [mots[i:i + 3] for i in range(0, len(mots), 3)]

        # Générer toutes les permutations des paquets
        permutations_paquets = list(itertools.permutations(paquets))

        # Rejoindre les mots pour former les chaînes possibles
        chaines_possibles = [' '.join(itertools.chain.from_iterable(permutation)) for permutation in
                             permutations_paquets]

        return chaines_possibles

    def CreerlisteKeyWord(self, RB_product):

        nom, Rb_sku, Image_path, fournisseur, fournisseur_sku = self.DataBase.getproductRB(RB_product)

        dictionnaire = []

        if nom == None:
            return []
        else:
            dictionnaire.append(fournisseur)
            dictionnaire.extend(nom.split())
            dictionnaire.append(fournisseur_sku)
            dictionnaire.append(Rb_sku)
            return dictionnaire

    def analyseCorespondance(self, RB_product):
        listMots = self.CreerlisteKeyWord(RB_product)

        corespondances = self.DataBase.getCorespondanceDatabase(RB_product)

        for corespondance in corespondances:

            titre = corespondance[3]
            pourcentage_titre = self.calculer_pourcentage_mots_dans_liste(titre, listMots)
            print("Poucentage : --------------------------------------------------------" + RB_product + "  " + titre)

            print(self.afficher_texte_couleur_pourcentage(pourcentage_titre))
            print()

            self.DataBase.modifier_pourcentage_corespondance(RB_product, corespondance[1],pourcentage_titre, -1)
            pourcentage_image = -1

            if pourcentage_titre >= 20:
                repertoire_local = "./image/barcode/" + RB_product + "/" + corespondance[1]
                try:
                    if not os.path.exists(repertoire_local):
                        os.makedirs(repertoire_local)

                    if corespondance[0]:
                        nom_fichier = os.path.join(repertoire_local, corespondance[1])
                        urllib.request.urlretrieve(corespondance[0], nom_fichier)
                        print("Image téléchargée et enregistrée avec succès :", nom_fichier)

                        # Lancer l'analyse de l'image uniquement si le téléchargement a réussi
                        pourcentage_image = self.traitement_image(RB_product, corespondance[1])


                    else:
                        print("Impossible de trouver l'URL de l'image.")
                        pourcentage_image = -1
                except Exception as e:
                    print("Une erreur s'est produite lors du téléchargement de l'image :", str(e))

                self.DataBase.modifier_pourcentage_corespondance(RB_product, corespondance[1], pourcentage_titre, pourcentage_image)

    def retirer_mots_deux_lettres(self, chaine):
        mots = chaine.split()
        mots_filtrés = [mot for mot in mots if len(mot) > 2]
        nouvelle_chaine = " ".join(mots_filtrés)
        return nouvelle_chaine

    def calculer_pourcentage_mots_dans_liste(self,titre, liste_de_mots ):
        mots_du_titre = titre.split()
        mots_trouves = [mot for mot in liste_de_mots if mot in mots_du_titre]
        pourcentage = (len(mots_trouves) / len(liste_de_mots)) * 100
        return pourcentage

    def afficher_texte_couleur_pourcentage(self, pourcentage):
        if pourcentage < 10:
            couleur_code = "\033[31m"  # Rouge
        elif pourcentage < 50:
            couleur_code = "\033[33m"  # Jaune
        elif pourcentage < 75:
            couleur_code = "\033[32;2m"  # Vert terne
        else:
            couleur_code = "\033[92m"  # Vert pétant

        texte_formate = f"{couleur_code}{pourcentage:.2f}%\033[0m"
        return texte_formate

    def traitement_image(self, RB_code, code_upc):
        nom, Rb_sku, Image_path, fournisseur, fournisseur_sku = self.DataBase.getproductRB(RB_code)
        image_path_Rb = Image_path
        image_path_UPC = "./image/barcode/"+RB_code+"/"+code_upc

        print(image_path_Rb)
        print(image_path_UPC)

        maxvalue = 0

        try:
            files = self.list_files_in_directory(image_path_Rb)

            for file_path in files:
                print(file_path)
                image_Rb = io.imread(file_path)  # Lire l'image à partir du chemin de fichier
                image_UPC = io.imread(image_path_UPC+"/"+code_upc)  # Lire l'autre image

                # Déterminer les dimensions des images RB et UPC
                shape_Rb = image_Rb.shape
                #print(shape_Rb)
                shape_UPC = image_UPC.shape
                #print(shape_UPC)

                # Vérifier si les images ont déjà la même dimension
                if shape_Rb == shape_UPC:
                    image_Rb_resized = image_Rb
                    image_UPC_resized = image_UPC
                else:
                    # Redimensionner l'image UPC en fonction de la plus petite image (RB ou UPC)
                    if shape_Rb[0] < shape_UPC[0] or shape_Rb[1] < shape_UPC[1]:
                        # Si l'image RB est plus petite, redimensionner l'image UPC
                        image_Rb_resized = resize(image_Rb, (shape_UPC[0], shape_UPC[1]), anti_aliasing=True)
                        image_UPC_resized = image_UPC
                    else:
                        # Si l'image UPC est plus petite, redimensionner l'image RB
                        image_Rb_resized = image_Rb
                        image_UPC_resized = resize(image_UPC, (shape_Rb[0], shape_Rb[1]), anti_aliasing=True)

                # Déterminer la taille de la fenêtre en fonction de la plus petite dimension de l'image redimensionnée
                win_size = min(image_Rb_resized.shape[0], image_Rb_resized.shape[1])
                win_size = min(win_size, 9)  # Assurer que la taille de la fenêtre est au maximum 7 (valeur impaire)

                shape_Rb_resized = image_Rb_resized.shape
                #print(shape_Rb_resized)
                shape_UPC_resized = image_UPC_resized.shape
                #print(shape_UPC_resized)

                valeur_ssim, _ = ssim(image_Rb_resized, image_UPC_resized, win_size=win_size, full=True, channel_axis=2, data_range=255)


                if valeur_ssim > maxvalue:
                    maxvalue = valeur_ssim
                    resized_images = [image_Rb_resized, image_UPC_resized]


        except ValueError as e:
            print(e)


        print("image correspondante a %:")
        print(maxvalue*100)
        print()
        return maxvalue*100

    def list_files_in_directory(self, directory_path):
        if not os.path.isdir(directory_path):
            raise ValueError("Le chemin spécifié n'est pas un répertoire valide.")

        file_paths = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                file_paths.append(file_path)
        return file_paths

if __name__ == '__main__':
    #Création de l'instance de la classe driverDataSet

    analyseDonnée = traitementDonnée()

    pourcentage_image = analyseDonnée.traitement_image("RB-Lyn-316", "993246378203")
    print("pourcentage image :")
    print(pourcentage_image)