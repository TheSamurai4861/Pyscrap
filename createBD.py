import requests
import re
import csv

class CreateBD:

    MAX_PAGES = 200

    def scrapper_medias(self, page_debut, page_fin, media_type):
        fiches_medias = self.extract_media_files(page_debut, page_fin, media_type)
        mes_liens = self.extraire_donnees_fiche(fiches_medias, media_type)
        for ligne in mes_liens:
            if media_type == 2:
                with open("BD/movies.csv", mode='a', newline='') as fichier_csv:
                    ecrivain_csv = csv.writer(fichier_csv)
                    ecrivain_csv.writerow([ligne.strip('"')])
            elif media_type in [15, 32]:
                with open("BD/tvshows.csv", mode='a', newline='') as fichier_csv:
                    ecrivain_csv = csv.writer(fichier_csv)
                    ecrivain_csv.writerow([ligne.strip('"')])
        print("Done")
        return None

    def extract_media_files(self, first_page, end_page, media_type):
        liens_trouvesOK = []
        url = f"https://www2.darkino.club/posts?category={media_type}&sort=-news_read&page="
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        try:
            for i in range(first_page, end_page + 1):
                document = requests.get(url + str(i), headers=headers)
                source_page = document.text
                source_page = source_page.replace("\\/", "/").replace("&quot;", "")

                liens_trouves = re.findall(r'https://www2.darkino.club/post/.[^\"]+', source_page)
                temp1 = set(liens_trouves)
                temp2 = list(temp1)

                liens_trouvesOK.extend(temp2)
        except requests.RequestException as e:
            print("Erreur lors de l'extraction des données des fiches média:", e)

        return liens_trouvesOK

    def extraire_donnees_fiche(self, media_files, media_type):
        my_data = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        for file in media_files:
            try:
                id_tmdb = self.obtenir_lien_tmd_id(file)
                document = requests.get(file, headers=headers)
                document.raise_for_status()
                page_source = document.text

                page_source = page_source.replace("\\/", "/").replace("&quot;", "")

                links = []
                if media_type == 2:
                    links = self.extract_1fichier_link(file)
                    for link in links:
                        my_data.append(f"{id_tmdb},{link}")
                elif media_type in [15, 32]:
                    results = self.extract_links_and_episodes(file)
                    for link in results:
                        my_data.append(f"{id_tmdb},{link}")

            except requests.RequestException as e:
                print("Erreur lors de l'extraction des données de la fiche média:", e)

        return my_data

    def obtenir_lien_tmd_id(self, fiche):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        try:
            response = requests.get(fiche, headers=headers)
            response.raise_for_status()

            # Rechercher l'ID TMDB dans le contenu de la page scrappée
            id_tmdb_trouve = re.search(r'https://www.themoviedb.org/.*/(\d+)[^\"]+', response.text)

            return id_tmdb_trouve.group(1)

        except requests.RequestException as err:
            print(f"Erreur HTTP lors de la récupération de l'ID TMDB: {err}")
            return None

    def extract_1fichier_link(self, file):
        lien_1fichier = []
        hoster = "?single_liens_host_5Page="

        url = file + hoster

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            for i in range(1, self.MAX_PAGES + 1):
                one_fichier_links = []

                document = requests.get(url + str(i), headers=headers)
                document.raise_for_status()
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
                document.raise_for_status()
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
