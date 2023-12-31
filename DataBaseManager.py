import psycopg2

class DataBaseManager:
    conn = None
    cur = None

    def __init__(self):
        print("sa marche")
        self.conn = psycopg2.connect(
            host="localhost",
            database="barcode_local",
            user="postgres",
            password="willippe"
        ) #a changer pour la mise en production
        print("sa connecte")
        self.cur = self.conn.cursor()



    def close(self):
        self.cur.close()
        self.conn.close()

    def initTable(self):
        print("rentre dans init")
        # Requête pour créer la table "fournisseur"
        create_table_fournisseur = """
        CREATE TABLE fournisseur
        (
          Nom_Fournisseur VARCHAR(255) NOT NULL,
          PRIMARY KEY (Nom_Fournisseur)
        );
        """


        # Requête pour créer la table "produit_Rb"
        create_table_produit_Rb = """
        CREATE TABLE produit_Rb
        (
          Nom VARCHAR(255) NOT NULL,
          Code_Rb VARCHAR(255) NOT NULL,
          Path_photo VARCHAR(255) NOT NULL,
          Nom_Fournisseur VARCHAR(255) NOT NULL,
          Code_Fournisseur VARCHAR(255) NOT NULL,
          PRIMARY KEY (Code_Rb),
          FOREIGN KEY (Nom_Fournisseur) REFERENCES fournisseur(Nom_Fournisseur)
        );
        """


        # Requête pour créer la table "Correspondances"
        create_table_correspondances = """
        CREATE TABLE Correspondances
        (
          Path_photo VARCHAR(255) NOT NULL,
          Code_UPC VARCHAR(255) NOT NULL,
          Code_EAN VARCHAR(255) NOT NULL,
          Nom VARCHAR(255) NOT NULL,
          Code_Rb VARCHAR(255) NOT NULL,
          Pourcentage_corespo_image FLOAT NOT NULL,
          Pourcentage_corespo_ponderer FLOAT NOT NULL,
          PRIMARY KEY (Code_UPC),
          FOREIGN KEY (Code_Rb) REFERENCES produit_Rb(Code_Rb)
          );
        """



        try:
            # Exécution des requêtes de création de table
            self.cur.execute(create_table_fournisseur)
            print("fournissseur creer")
            self.cur.execute(create_table_produit_Rb)
            print("rb_produit creer")
            self.cur.execute(create_table_correspondances)
            print("correspondance creer")

            # Valider les changements dans la base de données
            self.conn.commit()
            print("Tables créées avec succès.")

        except psycopg2.Error as e:
            print("Erreur lors de la création des tables :", e)



    def dropAllTable(self):

        try:
            # Désactiver la contrainte de clé étrangère pour éviter les erreurs lors de la suppression des tables
            self.cur.execute("SET session_replication_role = 'replica';")

            # Obtenir la liste de toutes les tables dans la base de données
            self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = self.cur.fetchall()

            # Supprimer chaque table
            for table in tables:
                self.cur.execute(f"DROP TABLE {table[0]} CASCADE;")
                print(f"Table '{table[0]}' supprimée avec succès.")

            # Réactiver la contrainte de clé étrangère
            self.cur.execute("SET session_replication_role = 'origin';")

            # Valider les changements dans la base de données
            self.conn.commit()

        except psycopg2.Error as e:
            print("Erreur lors de la suppression des tables :", e)



    def getproductRB(self, RB_code):

        select_query = f"SELECT * FROM produit_Rb WHERE Code_Rb = '{RB_code}'"

        try:
            # Exécution de la requête SELECT
            self.cur.execute(select_query)

            # Récupérer le résultat de la requête
            produit_existe = self.cur.fetchone()

            print(produit_existe)
            #print(produit_existe[0])
            nom = produit_existe[0]
            Rb_sku = produit_existe[1]
            Image_path = produit_existe[2]
            fournisseur = produit_existe[3]
            fournisseur_sku = produit_existe[4]
            return nom, Rb_sku, Image_path, fournisseur, fournisseur_sku
        except psycopg2.Error as e:
            print("Erreur lors de la recherche du produit :", e)
            return None

    def getCorespondanceDatabase(self, RB_product):
        select_query = f"SELECT * FROM Correspondances WHERE Code_Rb = '{RB_product}' "
        try:
            # Exécution de la requête SELECT
            self.cur.execute(select_query)

            # Récupérer le résultat de la requête
            corespondances = self.cur.fetchall()

            return corespondances

        except psycopg2.Error as e:
            print("Erreur lors de la recherche du produit :", e)
            return None



    def addRbProduct(self, fournisseur, Nom_produit, Rb_sku, repertoire_path, code_fournisseur):

        #ajouter éventuellment le path de l'image et le sku du founisseur

        self.addRbFournisseur(fournisseur)



        select_query = f"SELECT * FROM produit_Rb WHERE Code_Rb = '{Rb_sku}' "

        try:
            # Exécution de la requête SELECT
            self.cur.execute(select_query)

            # Récupérer le résultat de la requête
            produit_existe = self.cur.fetchone() is not None

            if produit_existe:
                print("Le produit existe déjà dans la table produit_Rb.")
            else:
                insert_query = f"""
                INSERT INTO produit_Rb (Nom, Code_Rb, Path_photo, Nom_Fournisseur, Code_Fournisseur)
                VALUES ('{Nom_produit}', '{Rb_sku}', '{repertoire_path}', '{fournisseur}','{code_fournisseur}');
                """
                print("Le produit n'existe pas dans la table produit_Rb.")
                try:
                    # Exécution de la requête INSERT
                    self.cur.execute(insert_query)

                    # Valider les changements dans la base de données
                    self.conn.commit()
                    print("Produit inséré avec succès dans la table produit_Rb.")

                except psycopg2.Error as e:
                    print("Erreur lors de l'insertion du produit :", e)

        except psycopg2.Error as e:
            print("Erreur lors de la recherche du produit :", e)

    def addCorespondance(self, product, RB_code):

        barcode_produit_raw = product[1].split(" ", 1)
        barcode_produit = barcode_produit_raw[1]

        select_query = f"SELECT * FROM Correspondances WHERE code_upc = '{barcode_produit}'  or code_ean = '{barcode_produit}'and Code_Rb = '{RB_code}'"

        nom_produit_raw = product[0]
        nom_produit = nom_produit_raw.replace("'", " ")

        categorie_produit = product[2]
        image_url_produit = product[3]




        try:
            # Exécution de la requête SELECT
            self.cur.execute(select_query)

            # Récupérer le résultat de la requête
            produit_existe = self.cur.fetchone() is not None

            if produit_existe:
                print("Le produit existe déjà dans la table correspondance.")
            else:
                insert_query = f"""
                       INSERT INTO Correspondances (Path_photo, Code_UPC, Code_EAN, Nom, Code_Rb, Pourcentage_corespo_image,Pourcentage_corespo_ponderer)
                       VALUES ('{image_url_produit}','{barcode_produit}','{barcode_produit}', '{nom_produit}', '{RB_code}','{-1}','{-1}');
                       """
                print("La correspondance n'existe pas dans la table correspondance.")
                try:
                    # Exécution de la requête INSERT
                    self.cur.execute(insert_query)

                    # Valider les changements dans la base de données
                    self.conn.commit()
                    print("Correspondance inséré avec succès dans la table correspondance.")

                except psycopg2.Error as e:
                    print("Erreur lors de l'insertion de la correspondance :", e)

        except psycopg2.Error as e:
            print("Erreur lors de la recherche de la croorespondance :", e)






    def addRbFournisseur(self, fournisseur):
        # Requête SELECT pour vérifier si le fournisseur existe avec la clé primaire spécifiée
        select_query = f"SELECT * FROM fournisseur WHERE nom_Fournisseur = '{fournisseur}' "

        try:
            # Exécution de la requête SELECT
            self.cur.execute(select_query)

            # Récupérer le résultat de la requête
            produit_existe = self.cur.fetchone() is not None

            if produit_existe:
                print("Le fournisseur existe déjà dans la table produit_Rb.")
            else:

                # Requête d'insertion
                insert_query = "INSERT INTO fournisseur (nom_fournisseur) VALUES (%s);"
                self.cur.execute(insert_query, (fournisseur,))


                # reste a coder l'ajout de fournisseur
                print("Le fournisseur n'existe pas dans la table produit_Rb. donc on l'ajoutte")
                # Valider les changements dans la base de données
                self.conn.commit()

        except psycopg2.Error as e:
            print("Erreur lors de la recherche du produit :", e)







    def startTest(self):
        self.dropAllTable()
        self.initTable()

    def test(self, fournisseur):
        insert_query = "INSERT INTO fournisseur (nom_fournisseur) VALUES (%s);"
        self.cur.execute(insert_query, (fournisseur,))

        self.conn.commit()
        print(fournisseur)

        select_query = f"SELECT * FROM fournisseur WHERE nom_fournisseur = '{fournisseur}'"
        self.cur.execute(select_query)
        #print(select_query)

        rows = self.cur.fetchall()
        for row in rows:

            colonne1_value = row[0]

            print(f"Colonne 1 : {colonne1_value}")

        print("le prochain select ne devrais pas marcher")
        mauvais_query = f"SELECT * FROM fournisseur WHERE nom_fournisseur = 'pinpon'"
        self.cur.execute(mauvais_query)
        #print(mauvais_query)
        rows = self.cur.fetchall()

        for row in rows:
            colonne1_value = row[0]

            print(f"Colonne 1 : {colonne1_value}")
        print("----------")

    def modifier_pourcentage_corespondance(self,RB_code, code_upc, nouveau_pourcentage_ponderer, ouveau_pourcentage_image):

        sql_query = f"UPDATE Correspondances SET Pourcentage_corespo_ponderer = '{nouveau_pourcentage_ponderer}', Pourcentage_corespo_image ='{ouveau_pourcentage_image}' WHERE Code_UPC = '{code_upc}' and Code_Rb = '{RB_code}' "
        self.cur.execute(sql_query)
        self.conn.commit()







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Création de l'instance de la classe driverDataSet
    Database = DataBaseManager()
    produit  = Database.getproductRB("RB-Lyn-316")
    print("produit")
    print(produit)
