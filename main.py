from driverDataSet import driverDataSet
from explorateurTableur import explorateurTableur

import time



# Press the green button in the gutter to run the script.


def execute():
    mon_driver.get("https://www.robotshop.com/")

    for code in listeCode:
        fournisseur, Nom_produit, RB_Code, repertoir_path, sku_manifacturier = mon_driver.getCode(code)

        mon_driver.getCorespondance(RB_Code)

if __name__ == '__main__':
    #Création de l'instance de la classe driverDataSet
    mon_driver = driverDataSet()
    Tableur = explorateurTableur()

    listeCode = Tableur.parcourir(1,5)

    #mon_driver.getCorespondanceBarcode("bague")
    #mon_driver.getCorespondanceBarcode("pinpin")
    #mon_driver.getCorespondanceBarcode("philoupidoupidou")
    #mon_driver.getCorespondance("DFRobot")





    #DataBase.test("miron")
    execute()





    time.sleep(3000)






