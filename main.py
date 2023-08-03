from driverDataSet import driverDataSet
from explorateurTableur import explorateurTableur
from traitementDonnée import  traitementDonnée

import time



# Press the green button in the gutter to run the script.


def execute():
    mon_driver.get("https://www.robotshop.com/")

    for code in listeCode:
        fournisseur, Nom_produit, RB_Code, repertoir_path, sku_manifacturier = mon_driver.getCode(code)

        mon_driver.getCorespondance(RB_Code)
        analyseDonnée.analyseCorespondance(RB_Code)
        #mon_driver.analyseCorespondance(RB_Code)

if __name__ == '__main__':
    #Création de l'instance de la classe driverDataSet
    mon_driver = driverDataSet()
    Tableur = explorateurTableur()
    analyseDonnée = traitementDonnée()

    listeCode = Tableur.parcourir(1,5)


    execute()





    time.sleep(3000)






