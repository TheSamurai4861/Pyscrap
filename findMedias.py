import csv

class FindMedias:

    def rechercher_par_id(self, id_recherche):
        lignes_trouvees = []

        with open("../BD/movies.csv", mode='r') as fichier_csv:
            lecteur_csv = csv.reader(fichier_csv)
            
            for ligne in lecteur_csv:
                # Vérifier si l'id recherché est dans la ligne
                if id_recherche in ligne:
                    lignes_trouvees.append(ligne)

        return lignes_trouvees

    def rechercher_id_et_episode(self, id_recherche, numero_episode_recherche):
        resultats = []

        with open("../BD/tvshows.csv", mode='r') as fichier_csv:
            lecteur_csv = csv.reader(fichier_csv)

            for ligne in lecteur_csv:
                # Diviser la ligne en parties séparées par des virgules
                parties = ligne[0].split(',')

                # Vérifier si l'id recherché est dans la première partie de la ligne
                if id_recherche in parties[0]:
                    # Récupérer le dernier numéro après la virgule de la ligne
                    dernier_numero_episode = parties[-1].strip()

                    # Vérifier si le dernier numéro correspond au numéro recherché
                    if dernier_numero_episode == numero_episode_recherche:
                        resultats.append((id_recherche, dernier_numero_episode))

        return resultats