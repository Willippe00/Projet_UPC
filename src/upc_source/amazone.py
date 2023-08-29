import requests
class amazoneScrapper:


    def __init__(self):
        #login_url = "https://www.google.ca/"
        login_url = "https://sellercentral.amazon.ca/ap/signin"

        # Demander à l'utilisateur d'entrer le nom d'utilisateur et le mot de passe
        #username = input("Entrez votre nom d'utilisateur: ")
        #password = input("Entrez votre mot de passe: ")
        #
        username = "wroberge@robotshop.com"
        password = "Willippe100*"
        otp = "00000"

        # Créez une session
        session = requests.Session()

        # En-têtes
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

        # Données du formulaire de connexion
        login_data = {
            "email": username,
            "password": password,
            "otp": otp,
        }

        # Effectuer la requête POST pour se connecter
        response = requests.post(login_url, data=login_data, headers=headers)

        # Chargez la page de connexion pour obtenir les cookies et les en-têtes
        #response = session.get(login_url)

        # Assurez-vous que la réponse a réussi (code 200)
        if response.status_code == 200:
            print("Page de connexion chargée avec succès.")
        else:
            print("Échec du chargement de la page de connexion.")
            exit()

        # Parsez le contenu HTML de la page de connexion pour extraire les cookies et autres éléments nécessaires
        # (vous devez inspecter la page pour trouver les détails spécifiques)

        # Les cookies sont maintenant stockés dans la session, vous pouvez les récupérer

        cookies = session.cookies.get_dict()

        print("Cookies récupérés:")
        for name, value in cookies.items():
           print(f"{name}: {value}")




if __name__ == '__main__':
    print("amazone test")
    amazone = amazoneScrapper()