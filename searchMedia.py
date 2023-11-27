import csv
import re
import requests
import threading

class SearchMedia:
    MAX_PAGES = 200  # Ajout de la déclaration manquante pour MAX_PAGES

    def extract_movies_by_id(self, id, title):
        link = self.obtenir_lien_tmd_id(id, title)
        my_links = self.extract_1fichier_link(link)
        with open("BD/movies.csv", mode='a', newline='') as fichier_csv:
            ecrivain_csv = csv.writer(fichier_csv)
            for my_link in my_links:
                ecrivain_csv.writerow([my_link])
        return my_links

    def extract_tvshows_by_id(self, id, title, episode):
        link = self.obtenir_lien_tmd_id(id, title)
        if link:
            my_links = self.extract_with_link_and_episode(link, episode)
            with open("BD/tvshows.csv", mode='a', newline='') as fichier_csv:
                ecrivain_csv = csv.writer(fichier_csv)
                for my_link in my_links:
                    ecrivain_csv.writerow([my_link])
            return my_links
        else:
            print("Aucun lien trouvé.")
            return []
    
    def obtenir_lien_tmd_id(self, id, titre):
        # Créer une variable pour stocker le résultat
        resultat = None

        # Définir trois fonctions (à remplacer par vos fonctions réelles)
        def tmdb_films():
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
            id_tmdb_trouve = ""
            # Pour chaque lien trouvé, scrappé le lien à la recherche de l'ID TMDB
            for lien in liens_trouves:
                print(lien)
                try:
                    response_lien = requests.get(lien, headers=headers)
                    id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response_lien.text)
                    
                    if id_tmdb_trouve and int(id_tmdb_trouve.group(1)) == int(id):
                        resultat = lien
                        break  # Sortir de la boucle une fois que la correspondance est trouvée
                except requests.exceptions.HTTPError as err:
                    print(f"Erreur HTTP: {err}")
                    continue
# Sélectionner le premier lien trouvé

        def tmdb_series():
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
            id_tmdb_trouve = ""
            # Pour chaque lien trouvé, scrappé le lien à la recherche de l'ID TMDB
            for lien in liens_trouves:
                try:
                    response_lien = requests.get(lien, headers=headers)
                    response_lien.raise_for_status()
                    id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response_lien.text)
                except requests.exceptions.HTTPError as err:
                    print(f"Erreur HTTP: {err}")
                    continue

            nonlocal resultat
            if id_tmdb_trouve == id:
                resultat = liens_trouves[0]

        def tmdb_animes():
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

            id_tmdb_trouve = ""
            # Pour chaque lien trouvé, scrappé le lien à la recherche de l'ID TMDB
            for lien in liens_trouves:
                try:
                    response_lien = requests.get(lien, headers=headers)
                    response_lien.raise_for_status()
                    id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response_lien.text)
                except requests.exceptions.HTTPError as err:
                    print(f"Erreur HTTP: {err}")
                    continue

            nonlocal resultat
            if id_tmdb_trouve == id:
                resultat = liens_trouves[0]

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

        # Retourner le résultat
        return resultat
     
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
    
    def extract_with_link_and_episode(self, link, episode):
        my_links = self.extract_links_and_episodes(link)
        my_linksOK = []
        for my_link in my_links:
            if f",{episode}" in my_link:
                temp1 = my_link.split(',')[0]
                my_linksOK.append(temp1)  # Correction ici
        return my_linksOK       
    
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

result = SearchMedia()
results = result.extract_movies_by_id(19995, "avatar")
for ligne in results : 
    print(ligne)