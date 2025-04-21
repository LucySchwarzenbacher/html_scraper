import requests
from bs4 import BeautifulSoup
import json
import re


# URL der Webseite, die du scrapen möchtest

url = "https://liveticker.eisstock.bayern/ligen/game.php?id=38&final"  # Ersetze dies mit der tatsächlichen URL
#url = "https://liveticker.eisstock.bayern/ligen/game.php?id=363" #Heimspiel 1



# Sende die GET-Anfrage an die Webseite
response = requests.get(url)

# Prüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # HTML der Seite parsen
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Alle <tr>-Elemente finden
    div_elements = soup.find_all('div', class_= 'row spielergebnisse')
    h2_elements = soup.find_all('h2', class_= 'fw-bold')

    # Liste, um die Daten zu speichern
    spielergebniss = []
    table_data = []
    prozessed_data = []
    div_contents = []

    for div in div_elements:
        table_data.append(div.get_text(strip=True))

    for h2 in h2_elements:
        spielergebniss.append(h2.get_text(strip=True))


    home_score, away_score = spielergebniss[1].split(":")
    prozessed_data.append({
         'Team 1' : home_score,
         'Team 2' : away_score,
    })


    zähler = 0
    for entry in table_data:
        zähler = zähler + 1
        # Verwende Regex, um alles zu extrahieren
        # Wir suchen nach "EC" gefolgt von Buchstaben für den Vereinsnamen
        match = re.match(r'([A-Za-z\s]+)(\d+)([A-Za-z\s]+)(\d+)', entry)

        if match:
            club_name_1 = match.group(1).strip()  # Erster Klubname (nur Buchstaben)
            numbers_1 = match.group(2).strip()  # Die Zahlen nach dem ersten Klubnamen
            
            club_name_2 = match.group(3).strip()  # Zweiter Klubname (nur Buchstaben)
            numbers_2 = match.group(4).strip()  # Die Zahlen nach dem zweiten Klubnamen

            Kehre_1_1 = numbers_1[0]
            Kehre_2_1 = numbers_1[1]
            Kehre_3_1 = numbers_1[2]
            Kehre_4_1 = numbers_1[3]
            Kehre_5_1 = numbers_1[4]
            Kehre_6_1 = numbers_1[5]
            Spiel_1 = numbers_1[6]

            Kehre_1_2 = numbers_2[0]
            Kehre_2_2 = numbers_2[1]
            Kehre_3_2 = numbers_2[2]
            Kehre_4_2 = numbers_2[3]
            Kehre_5_2 = numbers_2[4]
            Kehre_6_2 = numbers_2[5]
            Spiel_2 = numbers_2[6]

            prozessed_data.append({
                'Spiel' : zähler,
                'club_1': club_name_1,
                'Kehre_1_1': Kehre_1_1,
                'Kehre_2_1': Kehre_2_1,
                'Kehre_3_1': Kehre_3_1,
                'Kehre_4_1': Kehre_4_1,
                'Kehre_5_1': Kehre_5_1,
                'Kehre_6_1': Kehre_6_1,
                'Spiel_1': Spiel_1,

                'club_2': club_name_2,
                'Kehre_1_2': Kehre_1_2,
                'Kehre_2_2': Kehre_2_2,
                'Kehre_3_2': Kehre_3_2,
                'Kehre_4_2': Kehre_4_2,
                'Kehre_5_2': Kehre_5_2,
                'Kehre_6_2': Kehre_6_2,
                'Spiel_2': Spiel_2,
            })


    # Speichere die verarbeiteten Daten in einer JSON-Datei
    def save_to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Speichern der verarbeiteten Daten
    save_to_json(prozessed_data, 'data.json')
