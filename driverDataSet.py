from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class driverDataSet:

    # Déclaration de la variable de classe
    driverGlobal = None
    url = None

    def __init__(self):
        # Création du driver Chrome et affectation à la variable d'instance
        self.driver = webdriver.Chrome()
        # Affectation du driver à la variable de classe
        driverDataSet.driverGlobal = self.driver

    # Méthode pour accéder à une URL spécifiée par l'utilisateur
    def get(self, url):
        self.url = url
        self.driver.get(url)
        time.sleep(6)


        button = self.driver.find_element(By.CLASS_NAME, "swal2-deny")
        button.click()

    def getCode(self, Rbcode):
        barRecherche = self.driver.find_element(By.NAME, "q")
        barRecherche.clear()
        barRecherche.send_keys(Rbcode)
        #barRecherche.send_keys(Keys.RETURN)
        time.sleep(1)

        boutonRecher = self.driver.find_element(By.XPATH, "//button[@class='search-bar__submit']")

        # Cliquer sur le bouton
        boutonRecher.click()

        div_element = self.driver.find_element(By.CSS_SELECTOR, ".boost-pfs-filter-product-item-inner")



        # Récupérer les informations de chaque élément du div
        vendor = div_element.find_element(By.CSS_SELECTOR,"a.boost-pfs-filter-product-item-vendor").text
        product_title = div_element.find_element(By.CSS_SELECTOR,"a.boost-pfs-filter-product-item-title").text
        sku = div_element.find_element(By.CSS_SELECTOR,"p.sku-label").text
        price = div_element.find_element(By.CSS_SELECTOR,"span.boost-pfs-filter-product-item-regular-price").text
        inventory = div_element.find_element(By.CSS_SELECTOR,"span.product-item__inventory").text

        # Afficher les informations extraites
        print("Vendeur :", vendor)
        print("Titre du produit :", product_title)
        print("SKU :", sku)
        print("Prix :", price)
        print("Stock :", inventory)
        print("---------------------------------")
        #eventuellement enregistre l'image répertoire local en .png et récuper sku du fabricant


        skuTransforme = sku.split(":", 1)[1].strip()


        return vendor, product_title, skuTransforme



# Utilisation de la classe
if __name__ == "__main__":
    # Création de l'instance de la classe driverDataSet
    mon_driver = driverDataSet()

    # Utilisation de la méthode get pour ouvrir http://www.google.com


