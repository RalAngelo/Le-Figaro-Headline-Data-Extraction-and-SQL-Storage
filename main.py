import requests
from bs4 import BeautifulSoup
import pandas as pd

# Obtenez le contenu de la page Web
r = requests.get("https://www.lefigaro.fr/")
soup = BeautifulSoup(r.content, "html.parser")

# Trouvez tous les éléments h1 et h2
h1_elements = soup.find_all('h1')
h2_elements = soup.find_all('h2')

# Obtenez le texte de chaque élément h1 et h2
h1_text = [h1.text for h1 in h1_elements]
h2_text = [h2.text for h2 in h2_elements]

# Créez un dataframe pandas
df = pd.DataFrame({'TITRE': h1_text})
df2 = pd.DataFrame({'TITRE': h2_text})

#titre
dff = pd.concat([df, df2], axis=0)
dff.reset_index(drop=True, inplace=True) #titre OK

#*****Lien*****
#lien du titre h2
lien_list = []
for h2 in h2_elements:
    if h2.find_parent("a"):
      a = h2.find_parent("a")
      lien_list.append(a["href"])

#lien du titre h1
lien_list_h1 = []
for h1 in h1_elements:
    if h1.find_parent("a"):
      a = h1.find_parent("a")
      lien_list_h1.append(a["href"])

dfLienH2 = pd.DataFrame({"LIEN": lien_list})
dfLienH1 = pd.DataFrame({"LIEN": lien_list_h1})

dffLien = pd.concat([dfLienH1, dfLienH2], axis=0)
dffLien.reset_index(drop=True, inplace=True)

date_list = []
time_list = []
nombre_de_commentaires_list = []
auteur_list = []

import datetime

for i in range(len(dffLien["LIEN"])):
  
  print(i)
  print(dffLien["LIEN"][i])
  
  rLink = requests.get(dffLien["LIEN"][i])
  soupLink = BeautifulSoup(rLink.content, "html.parser")

  auteur_element = soupLink.find("a", class_="fig-content-metas__author")
  if auteur_element is not None:
    textAuteur = auteur_element.text.strip()
  else:
    textAuteur = "Le Figaro"

  nbComElement = soupLink.find("div", class_="fig-comments__title")
  if nbComElement:
    text = nbComElement.text.strip()
    if "Aucun commentaire" in text.lower():
      nombre_de_commentaires = 0
    else:
      try:
        nombre_de_commentaires = int(text.replace("commentaires", ""))
      except ValueError:
        nombre_de_commentaires = 0
  else:
     nombre_de_commentaires = 0
  
  time_element = soupLink.find("time")
  
  from dateutil.parser import isoparse
  if time_element:
    datetime_obj = isoparse(time_element["datetime"])
  else:
    datetime_obj = None
  if datetime_obj:
    date_str = datetime_obj.date()
    time_str = datetime_obj.time()
  else:
    date_str = None
    time_str = None

  nombre_de_commentaires_list.append(nombre_de_commentaires)
  time_list.append(time_str)
  date_list.append(date_str)
  auteur_list.append(textAuteur)

#date et heure
dfHeure = pd.DataFrame({"HEURE": time_list})
dfDate = pd.DataFrame({"DATE": date_list})

#nombre de commentaire
dfNbCommentaire = pd.DataFrame({"NBR_Commentaire": nombre_de_commentaires_list})

#Auteur
dfAuteur = pd.DataFrame({"AUTEUR": auteur_list})

#data
data = pd.concat([dfDate, dfHeure, dff, dfAuteur, dffLien, dfNbCommentaire], axis=1)

#*******************SQL*****************
import mysql.connector

# Connection à la base de données
connection = mysql.connector.connect(
    host="localhost",
    user="Angelo",
    password="p1ssw0rd",
    database="LeFigaro"
)

"""CREATE TABLE Figaro (
       Date DATE,
       Heure TIME,
       Titre VARCHAR(255),
       Lien VARCHAR(255),
       Auteur VARCHAR(255),
       Nombre_de_commentaire INT
     );"""

Date = data["DATE"].fillna(pd.NA).to_list()
Heure = data["HEURE"].fillna(pd.NA).to_list()
Titre = data["TITRE"].fillna(" ").to_list()
Lien = data["LIEN"].fillna(" ").to_list()
Auteur = data["AUTEUR"].fillna(" ").to_list()
Nombre_de_commentaire = data["NBR_Commentaire"].fillna(0).to_list()

for i in range(len(data)):
  sql = """
    INSERT INTO Figaro (Date, Heure, Titre, Lien, Auteur, Nombre_de_commentaire)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
  cursor = connection.cursor()
  cursor.execute(sql, (Date[i] if not pd.isna(Date[i]) else None,
                         Heure[i] if not pd.isna(Heure[i]) else None,
                         Titre[i], Lien[i], Auteur[i], Nombre_de_commentaire[i]))
  connection.commit()

connection.close()

print('OK SUCCESS!!')