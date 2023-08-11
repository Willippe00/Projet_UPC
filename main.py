from driverDataSet import driverDataSet
from explorateurTableur import explorateurTableur
from traitementDonnée import  traitementDonnée
from presentationResultas import presentationResultas

import time



# Press the green button in the gutter to run the script.


def execute():
    mon_driver.get("https://www.robotshop.com/")

    for code in listeCode:
        fournisseur, Nom_produit, RB_Code, repertoir_path, sku_manifacturier = mon_driver.getCode(code)
        if (Nom_produit != None) & (RB_Code == code):
          mon_driver.getCorespondance(RB_Code)
          analyseDonnée.analyseCorespondance(RB_Code)
          maprésentation.présenterCorespondance(RB_Code)
        #mon_driver.analyseCorespondance(RB_Code)

if __name__ == '__main__':
    #Création de l'instance de la classe driverDataSet
    mon_driver = driverDataSet()
    Tableur = explorateurTableur()
    analyseDonnée = traitementDonnée()
    maprésentation = presentationResultas()

    listeCode = Tableur.parcourir(30,33)


    execute()





    time.sleep(3000)






