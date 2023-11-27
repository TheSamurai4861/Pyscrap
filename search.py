import requests
import threading
from bs4 import BeautifulSoup
import re
import csv

class Search:
    
    MAX_PAGES = 200
    def extraire_donnees_fiche(self, titre, id, numero):
        my_data = []
        url = self.obtenir_lien_tmd_id(titre, int(id))
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            document = requests.get(url, headers=headers)
            page_source = document.text

            page_source = page_source.replace("\\/", "/").replace("&quot;", "")

            links = []
            if "films" in url:
                links = self.extract_1fichier_link(url)
                for link in links:
                    with open("SpeedScrap/movies.csv", mode='a', newline='') as fichier_csv:
                        # Créer un écrivain CSV
                        ecrivain_csv = csv.writer(fichier_csv)
                        ecrivain_csv.writerow([f"{id},{link}"])
            else:
                results = self.extract_links_and_episodes(url)
                for chaine in results:
                    with open("SpeedScrap/tvshows.csv", mode='a', newline='') as fichier_csv:
                        # Créer un écrivain CSV
                        ecrivain_csv = csv.writer(fichier_csv)
                        ecrivain_csv.writerow([f"{id},{chaine}"])
                    # Séparer la chaîne en deux parties: avant et après la virgule
                    avant_virgule, apres_virgule = chaine.split(',', 1)

                    # Vérifier si le numéro après la virgule correspond au numéro cible
                    if apres_virgule.strip() == str(numero):
                        # Ajouter les caractères avant la virgule aux résultats
                        links.append(avant_virgule)
            

            for link in links:
                my_data.append(f"{link}")

        except requests.RequestException as e:
            print("Erreur lors de l'extraction des données de la fiche média:", e)

        return my_data

    
    import threading

    def obtenir_lien_tmd_id(self, titre, id_tmdb):
        # Créer une liste pour stocker les résultats des threads
        resultats = []

        # Définir trois fonctions (à remplacer par vos fonctions réelles)
        def tmdb_films():
            # Modifier le titre en minuscules et remplacer les espaces par des '+'
            titre_modifie = titre.lower().replace(" ", "+")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # Construire l'URL de recherche
            url_recherche = f"https://www2.darkino.club/find?search={titre_modifie}&type=posts&category=2"

            # Effectuer la requête pour obtenir la page source
            try:
                response = requests.get(url_recherche, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(f"Erreur HTTP: {err}")
                return None

            # Rechercher les liens avec le regex dans le contenu de la page
            liens_trouves = re.findall(r'https://www2.darkino.club/post/.[^\"]+', response.text)

            # Pour chaque lien trouvé, scrappé le lien à la recherche de l'ID TMDB
            for lien in liens_trouves:
                try:
                    response_lien = requests.get(lien, headers=headers)
                    response_lien.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(f"Erreur HTTP: {err}")
                    continue

                # Rechercher l'ID TMDB dans le contenu de la page scrappée
                id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response_lien.text)

                # Si l'ID TMDB trouvé correspond à celui en paramètre, retourner le lien
                if id_tmdb_trouve and id_tmdb_trouve.group(1) == str(id_tmdb):
                    nonlocal resultats
                    resultats = lien

        def tmdb_series():
            # Modifier le titre en minuscules et remplacer les espaces par des '+'
            titre_modifie = titre.lower().replace(" ", "+")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # Construire l'URL de recherche
            url_recherche = f"https://www2.darkino.club/find?search={titre_modifie}&type=posts&category=15"

            # Effectuer la requête pour obtenir la page source
            try:
                response = requests.get(url_recherche, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(f"Erreur HTTP: {err}")
                return None

            # Rechercher les liens avec le regex dans le contenu de la page
            liens_trouves = re.findall(r'https://www2.darkino.club/post/.[^\"]+', response.text)

            # Pour chaque lien trouvé, scrappé le lien à la recherche de l'ID TMDB
            for lien in liens_trouves:
                try:
                    response_lien = requests.get(lien, headers=headers)
                    response_lien.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(f"Erreur HTTP: {err}")
                    continue

                # Rechercher l'ID TMDB dans le contenu de la page scrappée
                id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response_lien.text)

                # Si l'ID TMDB trouvé correspond à celui en paramètre, retourner le lien
                if id_tmdb_trouve and id_tmdb_trouve.group(1) == str(id_tmdb):
                    nonlocal resultats
                    resultats = lien

        def tmdb_animes():
            # Modifier le titre en minuscules et remplacer les espaces par des '+'
            titre_modifie = titre.lower().replace(" ", "+")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # Construire l'URL de recherche
            url_recherche = f"https://www2.darkino.club/find?search={titre_modifie}&type=posts&category=32"

            # Effectuer la requête pour obtenir la page source
            try:
                response = requests.get(url_recherche, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(f"Erreur HTTP: {err}")
                return None

            # Rechercher les liens avec le regex dans le contenu de la page
            liens_trouves = re.findall(r'https://www2.darkino.club/post/.[^\"]+', response.text)

            # Pour chaque lien trouvé, scrappé le lien à la recherche de l'ID TMDB
            for lien in liens_trouves:
                try:
                    response_lien = requests.get(lien, headers=headers)
                    response_lien.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(f"Erreur HTTP: {err}")
                    continue

                # Rechercher l'ID TMDB dans le contenu de la page scrappée
                id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response_lien.text)

                # Si l'ID TMDB trouvé correspond à celui en paramètre, retourner le lien
                if id_tmdb_trouve and id_tmdb_trouve.group(1) == str(id_tmdb):
                    nonlocal resultats
                    resultats = lien

        # Créer trois threads pour exécuter les fonctions en parallèle
        thread_1 = threading.Thread(target=tmdb_films)
        thread_2 = threading.Thread(target=tmdb_series)
        thread_3 = threading.Thread(target=tmdb_animes)

        # Démarrer les threads
        thread_1.start()
        thread_2.start()
        thread_3.start()

        # Attendre que tous les threads se terminent
        thread_1.join()
        thread_2.join()
        thread_3.join()

        # Retourner les résultats
        return resultats

    def extract_1fichier_link(self, fiche_media):
        lien_1fichier = []
        hoster = "?single_liens_host_5Page="
            
        url = fiche_media + hoster

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            for i in range(1, self.MAX_PAGES + 1):
                one_fichier_links = []

                document = requests.get(url + str(i), headers=headers)
                page_source = document.text

                if "Aucun élément" in page_source:
                    break

                page_source = page_source.replace("\\/", "/").replace("&quot;", "")

                regex = r"https://1fichier.com/.[^,]+"
                one_fichier_links.extend(re.findall(regex, page_source))

                lien_1fichier.extend(one_fichier_links)

        except requests.RequestException as e:
            print("Erreur scrap lien 1fichier:", e)

        unique_set = set(lien_1fichier)
        return list(unique_set)
    
    def extract_links_and_episodes(self, url):
            url1 = url + "?episodes_liens_host_5Page="
            results = []

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            try:
                for i in range(1, 200 + 1):
                    document = requests.get(url1 + str(i), headers=headers)
                    page_source = document.text

                    if "Aucun élément" in page_source:
                        break
                    regex = r'(https:\\\/\\\/1fichier\.com\\\/\?.[^&]*|https:\\\/\\\/darkibox.com\\\/.[^&]*)'

                    # Créer un objet de modèle regex
                    pattern = re.compile(regex)

                    # Trouver toutes les correspondances dans le texte
                    matches = pattern.findall(page_source)

                    # Tableau pour stocker les résultats
                    

                    links = []
                    # Parcourir les correspondances
                    for match in matches:

                        lien_modifie = re.sub(r'\\/', '/', match)
                    
                        links.append(lien_modifie)
                    regex1 = r'episode&quot;:(\d+),'
                    
                    # Créer un objet de modèle regex
                    pattern1 = re.compile(regex1)

                    # Trouver toutes les correspondances dans le texte
                    matches1 = pattern1.findall(page_source)

                    episodes = []
                    for match in matches1:
                        episodes.append(match)

                    for i in range(min(len(links), len(episodes))):
                    # Concaténer les éléments des deux tableaux avec une virgule entre eux
                        ligneconcatenee = links[i] + ',' + episodes[i]
                    
                        # Ajouter la ligne concaténée à la liste des résultats
                        results.append(ligneconcatenee)
            except requests.RequestException as e:
                print("Erreur scrap lien 1fichier:", e)

            unique_set = set(results)
            return list(unique_set)