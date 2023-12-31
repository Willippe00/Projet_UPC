from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from DataBaseManager import DataBaseManager

from  traitementDonnée import traitementDonnée


import os
import urllib.request
import shutil

import time

class driverDataSet:

    # Déclaration de la variable de classe
    driverGlobal = None
    url = None
    driverBarcode = None
    urlBarcode = "https://www.barcodelookup.com"
    DataBase = None
    traitementDonnéeInstance = None

    def __init__(self):
        # Création du driver Chrome et affectation à la variable d'instance
        self.driver = webdriver.Chrome()
        # Affectation du driver à la variable de classe
        driverDataSet.driverGlobal = self.driver
        self.initBarcode()
        self.DataBase = DataBaseManager()
        self.DataBase.startTest()
        self.traitementDonnéeInstance = traitementDonnée()




    def initBarcode(self):


        # Vérifier si le répertoire existe
        if os.path.exists("./image/barcode"):
            try:
                # Si le répertoire est vide, utilisez os.rmdir()
                if not os.listdir("./image/barcode"):
                    os.rmdir("./image/barcode")
                    print("Répertoire vidé et supprimé avec succès :", "./image/barcode")
                else:
                    # Si le répertoire n'est pas vide, utilisez shutil.rmtree() pour le supprimer avec tous les fichiers et sous-répertoires
                    shutil.rmtree("./image/barcode")
                    print("Répertoire et son contenu supprimés avec succès :", "./image/barcode")
            except Exception as e:
                print("Une erreur est survenue lors de la suppression du répertoire :", e)
        else:
            print("Le répertoire spécifié n'existe pas.")








    def getCorespondance(self, RB_product):
        dictionnaire = self.traitementDonnéeInstance.CreerDictionnaire(RB_product)

        for mot in dictionnaire:

            self.addCorespondanceDatabase(self.getCorespondanceBarcode(mot),RB_product)











    def addCorespondanceDatabase(self, corespondances, RB_product):

        for corespondance in corespondances:
            self.DataBase.addCorespondance(corespondance, RB_product)
    def getCorespondanceBarcode(self, recherche):

        # Générer un User-Agent aléatoire
        user_agent = UserAgent()
        user_agent_string = user_agent.random
        #user_agent.chrome

        # Créer les options de Chrome avec le User-Agent aléatoire
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-agent={user_agent_string}")

        self.driverBarcode = webdriver.Chrome(options=chrome_options)


        self.driverBarcode.get(self.urlBarcode + "/"+recherche)
        time.sleep(2)

        try:
          elements = self.driverBarcode.find_elements(By.CSS_SELECTOR,"#product-search-results li")
        except Exception as e:
          print("produit RB inactif")
          return None, None, None, None, None

        produits = []
        for element in elements:

            #url = element.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
            nom = element.find_element(By.CSS_SELECTOR,".product-search-item-text p:nth-of-type(1)").text
            barcode = element.find_element(By.CSS_SELECTOR,".product-search-item-text p:nth-of-type(2)").text
            try:

              categorie = element.find_element(By.CSS_SELECTOR,".product-search-item-text p:nth-of-type(3)").text
            except Exception as e:
                print("pas de fabricant ")
                categorie = None
            try:
               fabricant = element.find_element(By.CSS_SELECTOR,".product-search-item-text p:nth-of-type(4)").text # possibiliter de fabricant absent mettre un try
            except Exception as e:
                print("pas de fabricant ")
                fabricant = None
            image_url = element.find_element(By.CSS_SELECTOR,".product-search-item-img img").get_attribute("src")

            produit = {
                'nom': nom,
                'barcode': barcode,
                'categorie': categorie,
                'image_url': image_url
            }

            produit = []
            produit.append(nom)
            produit.append(barcode)
            produit.append(categorie)
            produit.append(image_url)

            print("nom")
            print(nom)



            produits.append(produit)
        self.driverBarcode.quit()
        print("pause")
        time.sleep(1)
        print("lancement chrome")
        return produits







    # Méthode pour accéder à une URL spécifiée par l'utilisateur
    def get(self, url):
        # Vérifier si le répertoire existe
        if os.path.exists("./image/Rb"):
            try:
                # Si le répertoire est vide, utilisez os.rmdir()
                if not os.listdir("./image/Rb"):
                    os.rmdir("./image/Rb")
                    print("Répertoire vidé et supprimé avec succès :", "./image/Rb")
                else:
                    # Si le répertoire n'est pas vide, utilisez shutil.rmtree() pour le supprimer avec tous les fichiers et sous-répertoires
                    shutil.rmtree("./image/Rb")
                    print("Répertoire et son contenu supprimés avec succès :", "./image/Rb")
            except Exception as e:
                print("Une erreur est survenue lors de la suppression du répertoire :", e)
        else:
            print("Le répertoire spécifié n'existe pas.")

        self.url = url
        self.driver.get(url)
        time.sleep(6)


        button = self.driver.find_element(By.CLASS_NAME, "swal2-deny")
        button.click()

    def getCode(self, Rbcode):
        barRecherche = self.driver.find_element(By.NAME, "q")
        barRecherche.clear()
        barRecherche.send_keys(Rbcode)
        time.sleep(1)

        boutonRecher = self.driver.find_element(By.XPATH, "//button[@class='search-bar__submit']")

        # Cliquer sur le bouton
        time.sleep(2)
        boutonRecher.click()
        time.sleep(2)

        div_element = self.driver.find_element(By.CSS_SELECTOR, ".boost-pfs-filter-product-item-inner")



        # Récupérer les informations de chaque élément du div
        vendor = div_element.find_element(By.CSS_SELECTOR,"a.boost-pfs-filter-product-item-vendor").text
        product_title = div_element.find_element(By.CSS_SELECTOR,"a.boost-pfs-filter-product-item-title").text
        sku = div_element.find_element(By.CSS_SELECTOR,"p.sku-label").text
        #price = div_element.find_element(By.CSS_SELECTOR,"span.boost-pfs-filter-product-item-regular-price").text
        #inventory = div_element.find_element(By.CSS_SELECTOR,"span.product-item__inventory").text

        sku = sku.split(":", 1)[1].strip()


        repertoire_local = "./image/Rb/"+vendor+"/"+sku

        if not os.path.exists(repertoire_local):
            os.makedirs(repertoire_local)



        # Afficher les informations extraites
        print("Vendeur :", vendor)
        print("Titre du produit :", product_title)
        print("SKU :", sku)
        print("---------------------------------")

        div_element.find_element(By.CSS_SELECTOR, "a.boost-pfs-filter-product-item-vendor").click()


        time.sleep(1)


        # Rechercher l'élément a contenant le lien
        elements = self.driver.find_elements(By.CSS_SELECTOR,'a.product-gallery__thumbnail')
        index  = 1



        for element in elements:

           lien_photo = element.get_attribute("href")
           print(lien_photo)

           if lien_photo:
                nom_fichier = os.path.join(repertoire_local,"image_"+index.__str__()+".png")  # Remplacez "nom_image.jpg" par le nom souhaité
                urllib.request.urlretrieve(lien_photo, nom_fichier)
                print("Image téléchargée et enregistrée avec succès :", nom_fichier)
                index = index +1
           else:
                print("Impossible de trouver l'URL de l'image.")

        print("titre")

        titres = self.driver.find_elements(By.CSS_SELECTOR, 'span.product-meta__sku-number')
        sku_manifacture = titres[1].text
        print("sku_manifacture")
        print(sku_manifacture)

        self.DataBase.addRbProduct(vendor, product_title, sku, repertoire_local, sku_manifacture)
        return vendor, product_title, sku, repertoire_local, sku_manifacture



# Utilisation de la classe
if __name__ == "__main__":
    # Création de l'instance de la classe driverDataSet
    mon_driver = driverDataSet()



