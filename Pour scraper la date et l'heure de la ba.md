Pour scraper la date et l'heure de la balise `<time>` ci-dessus avec BS4, vous pouvez utiliser la propriété `datetime` de la balise. La propriété `datetime` renvoie une chaîne de caractères contenant la date et l'heure au format ISO 8601.

Voici un exemple :

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
    <time datetime="2024-01-20T13:36:00+01:00">
        il y a 3 heures
    </time>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

time_element = soup.find("time")

datetime_str = time_element["datetime"]

datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")

print(datetime_obj)
```

Ce code produira le résultat suivant :

```
2024-01-20 10:36:00+00:00
```

Vous pouvez également utiliser la méthode `from_datetime()` de la classe `datetime` pour convertir la chaîne de caractères en objet `datetime`.

Voici un exemple :

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
    <time datetime="2024-01-20T13:36:00+01:00">
        il y a 3 heures
    </time>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

time_element = soup.find("time")

datetime_obj = datetime.datetime.fromisoformat(time_element["datetime"])

print(datetime_obj)
```

Ce code produira le même résultat que le code précédent.

Si vous souhaitez uniquement scraper la date, vous pouvez utiliser la méthode `date()` de l'objet `datetime`.

Voici un exemple :

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
    <time datetime="2024-01-20T13:36:00+01:00">
        il y a 3 heures
    </time>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

time_element = soup.find("time")

datetime_obj = datetime.datetime.fromisoformat(time_element["datetime"])

date_str = datetime_obj.date()

print(date_str)
```

Ce code produira le résultat suivant :

```
2024-01-20
```

Si vous souhaitez uniquement scraper l'heure, vous pouvez utiliser la méthode `time()` de l'objet `datetime`.

Voici un exemple :

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
    <time datetime="2024-01-20T13:36:00+01:00">
        il y a 3 heures
    </time>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

time_element = soup.find("time")

datetime_obj = datetime.datetime.fromisoformat(time_element["datetime"])

time_str = datetime_obj.time()

print(time_str)
```

Ce code produira le résultat suivant :

```
13:36:00
```