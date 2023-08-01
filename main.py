from driverDataSet import driverDataSet
from explorateurTableur import explorateurTableur
from DataBaseManager import DataBaseManager
import time



# Press the green button in the gutter to run the script.
def Test():
    DataBase.startTest()

def execute():
    mon_driver.get("https://www.robotshop.com/")

    for code in listeCode:
        fournisseur, Nom_produit, RB_Code, repertoir_path, sku_manifacturier = mon_driver.getCode(code)
        DataBase.addRbProduct(fournisseur, Nom_produit, RB_Code, repertoir_path,sku_manifacturier)

if __name__ == '__main__':
    #Création de l'instance de la classe driverDataSet
    mon_driver = driverDataSet()
    Tableur = explorateurTableur()
    DataBase = DataBaseManager()
    listeCode = Tableur.parcourir(1,5)




    Test()
    #DataBase.test("miron")
    execute()





    time.sleep(3000)






