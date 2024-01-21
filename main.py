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
df = pd.DataFrame({'titres': h1_text})
df2 = pd.DataFrame({'titres': h2_text})

dff = pd.concat([df, df2], axis=0)
dff.reset_index(drop=True, inplace=True) #titre OK

#*****Lien*****

lien_list = []
for h2 in h2_elements:
    if h2.find_parent("a"):
      a = h2.find_parent("a")
      lien_list.append(a["href"])

dfLien = pd.DataFrame({"liens": lien_list})
print(dfLien)

date_list = []
time_list = []

for link in dfLien:
  rLink = requests.get(link)
  soupLink = BeautifulSoup(rLink.content, "html.parser")

  time_element = soupLink.find("time")
  datetime_obj = datetime.datetime.fromisoformat(time_element["datetime"])
  date_str = datetime_obj.date()

  time_str = datetime_obj.time()

  time_list.append(time_str)
  date_list.append(date_str)


"""
import mysql.connector

# Connection à la base de données
connection = mysql.connector.connect(
    host="localhost",
    user="Angelo",
    password="p1ssw0rd",
    database="LeFigaro"
)

#le curseur
cursor = connection.cursor()

#sql
sql = \"""
CREATE TABLE journaux (
  date DATE,
  heure TIME,
  titre_du_journal VARCHAR(255),
  nombre_de_commentaire INT
)
\"""

cursor.execute(sql)

connection.commit()

cursor.close()
connection.close()

print("Table created successfully!")"""


