import requests
import re
from bs4 import BeautifulSoup
import datetime
from PIL import Image, ImageDraw, ImageFont
import locale
from io import BytesIO
from textwrap import wrap
from newsapi import NewsApiClient

locale.setlocale(locale.LC_TIME, 'fr_FR')
# URL du site que vous souhaitez scraper
url = "https://maree.info/53"

# Définir un en-tête User-Agent pour simuler une requête provenant d'un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

}

# Utilisation de requests pour obtenir le contenu HTML de la page avec les en-têtes
response = requests.get(url, headers=headers)

# Vérification de l'accès à la page
if response.status_code == 200:
    html_content = response.text
    #print(html_content)
    # Utilisation de BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # XPath simulé pour sélectionner la partie spécifique du HTML
    selected_node = soup.find('tr', class_='MJ MJ0')
    selected_node2 = soup.find('tr', class_="MJ MJ1")

    # Si l'élément est trouvé, récupérer le HTML
    if selected_node:
        selected_html = str(selected_node)
        selected_htmlJ2=str(selected_node2)
    else:
        print("Aucun élément trouvé avec la classe 'MJ MJ0'.")
        selected_html = ""
else:
    print(f"Erreur lors de la récupération de la page, code de statut: {response.status_code}")
    selected_html = ""
print(html_content)

debut_delimiteur = "</td><td><b>"
fin_delimiteur = "</b><br/>"
motif = r"\{debut_delimiteur}(.*?){fin_delimiteur}"
matchss = re.findall(r'</td><td><b>(\w+)</b><br/>', selected_html)
for match in matchss:
 if match and "h" not in match: 
    coeff = match
    print(f"Coeff : {coeff}")
else:
    debut_delimiteur = "<br/><b>"
    fin_delimiteur = "</b><br/>"
    motif = r"\{debut_delimiteur}(.*?){fin_delimiteur}"
    matchsss = re.findall(r'<br/><b>(\w+)</b><br/>', selected_html)

for  match in matchsss:
    if match and "h" not in match:
        coeff = match
        print(f"Coeff : {coeff}")
    else:
        print("no")

coeff2=0
matchssJ2 = re.findall(r'</td><td><b>(\w+)</b><br/>', selected_htmlJ2)
for match in matchssJ2:
 if match and "h" not in match: 
    coeffJ2 = match
    print(f"CoeffJ2 : {coeffJ2}")
else:
    debut_delimiteur = "<br/><b>"
    fin_delimiteur = "</b><br/>"
    motif = r"\{debut_delimiteur}(.*?){fin_delimiteur}"
    matchsssJ2 = re.findall(r'<br/><b>(\w+)</b><br/>', selected_htmlJ2)

for  match in matchsssJ2:
    if match and "h" not in match:
        coeffJ2 = match
        print(f"Coeff : {coeffJ2}")
    else:
        print("no")


# Extraction des horaires et hauteurs
basse_mer = []
haute_mer = []

# Début de la récupération des horaires et hauteurs
debut_delimiteur = "<td>"
fin_delimiteur = "<br>"
motif = r"{debut_delimiteur}(.*?){fin_delimiteur}"

matches=re.findall(r'<br/>(\w+)<br/>', selected_html)
matches+=re.findall(r'</b><br/>(\w+)</td><td>', selected_html)
matches+=re.findall(r'<td>(\w+)<br/><b>', selected_html)
for match in matches:
    valeur_extraite = match
    if "h" in valeur_extraite:
       
     basse_mer.append(valeur_extraite)
     print("Basse mer :"+valeur_extraite)

def dessiner_jauge(coefficient, hauteur=200, largeur=50):
    """
    Dessine une jauge verticale avec des coins arrondis, style thermomètre.
    
    :param coefficient: Valeur entre 30 et 120 (coefficient de marée)
    :param hauteur: Hauteur totale de la jauge
    :param largeur: Largeur totale de la jauge
    :return: Image PIL
    """
    # Assurer que le coefficient est bien dans la plage 30-120
    coefficient = max(20, min(coefficient, 120))
    
    # Normalisation : 30 → 0% et 120 → 100% de remplissage
    niveau = int(((coefficient - 20) / (120 - 20)) * hauteur)

    # Création de l'image avec fond transparent
    img = Image.new("RGBA", (largeur, hauteur), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Rayon des arrondis (demi-largeur pour un effet bulle en bas)
    radius = largeur // 2  

    # Contour de la jauge avec coins arrondis
    draw.rounded_rectangle([(5, 5), (largeur - 5, hauteur - 5)], radius=radius, outline="black", width=2)

    # Remplissage arrondi en rouge (jauge qui monte)
    draw.rounded_rectangle([(10, hauteur - 10 - niveau), (largeur - 10, hauteur - 10)], radius=radius, fill="red")

    return img


image = dessiner_jauge(int(coeff))


matchess = re.findall(r'<b>(\w+)</b>', selected_html)

for match in matchess:
    valeur_extraite = match
    if "h" in valeur_extraite:
     valeur_extraite = match
     haute_mer.append(valeur_extraite)
     print("Haute mer :"+valeur_extraite)   


url="https://serpapi.com/search?engine=google_news&gl=fr&hl=FR&api_key=b467fa4ed236b5917a826f01ad9b6003d8d595fcd5cb8a6ca7d6fffc15dfbb0d"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    html_content = response.text
selected_html1=re.search(r'"name": "(.*?)"', html_content)
selected_html2=re.search(r'"title": "(.*?)",', html_content)
icon=re.search(r'"icon": "(.*?)"', html_content)

print(selected_html1.group(1)," : ",selected_html2.group(1))
iconurl = icon.group(1)  # Remplace par l'URL de ton image
response = requests.get(iconurl)
image_dl = Image.open(BytesIO(response.content))

url="https://serpapi.com/search?engine=google&gl=fr&hl=FR&q=meteo%20saint%20jacut%20de%20la%20mer&api_key=b467fa4ed236b5917a826f01ad9b6003d8d595fcd5cb8a6ca7d6fffc15dfbb0d"
response = requests.get(url, headers=headers)
if response.status_code == 200:
 html_content=response.text
 match = re.search(r'"answer_box".*', html_content, re.DOTALL)
 html_content=match.group(0)


print('test')
selected_html2str=str(selected_html2.group(1))
selected_html2str=selected_html2str.replace("/","")
selected_html2str=selected_html2str.replace("\\","")

date=re.findall(r'"day": "(.*?)"', html_content)
temp_max=re.findall(r'"high": "(.*?)"', html_content)
temp_min=re.findall(r'"low": "(.*?)"', html_content)
wind=re.findall(r'"wind": "(.*?)"', html_content)
precip=re.findall(r'"precipitation": "(.*?)"', html_content)
weather=re.findall(r'"weather": "(.*?)"', html_content)
weather_icon=re.findall(r'"thumbnail": "(.*?)"', html_content)
humidity=re.findall(r'"humidity": "(.*?)"', html_content)
meteo_demain = [
             
            "Demain",
             weather[2],
            "Temp : "+temp_min[1]+" à "+temp_max[1] + "°C",
            "Vent : " +wind[2] + "",
            
            ]
for i in range(0,len(weather)) :
 weather[i] = weather[i].replace("x27", "'")
 if weather[i]=="Partiellement couvert" or weather[i]=="Temps clair avec quelques ":
    weather_icon[i]="https://cdn-icons-png.flaticon.com/512/5213/5213449.png"
 if "Nuageux" in weather[i] :
    weather_icon[i]="https://cdn-icons-png.flaticon.com/512/7084/7084486.png"
 if "Averses" in weather[i] or "pluie" in weather[i] or "Pluie" in weather[i]:
    weather_icon[i]="https://cdn-icons-png.flaticon.com/512/9755/9755309.png"
 if "Temps clair" in weather[i] or "Ensoleillé" in weather[i]:
    weather_icon[i]="https://cdn-icons-png.flaticon.com/512/979/979585.png"
 if "Orage" in weather[i] or "orag" in weather[i]:
    weather_icon[i]="https://cdn-icons-png.flaticon.com/512/7105/7105037.png"
meteo_apresdemain = [
             
            date[2].capitalize(),
             weather[3],
            "Temp : "+temp_min[2]+" à "+temp_max[2] + "°C",
            "Vent : " +wind[3] + "",
            
            ]



match = re.search(r'"hourly_forecast".*', html_content, re.DOTALL)
html_content=match.group(0)


date2=re.findall(r'"time": "(.*?)"', html_content)
temperature=re.findall(r'"temperature": "(.*?)"', html_content)

wind2=re.findall(r'"wind": "(.*?)"', html_content)
precip2=re.findall(r'"precipitation": "(.*?)"', html_content)
weather2=re.findall(r'"weather": "(.*?)"', html_content)
weather_icon2=re.findall(r'"thumbnail": "(.*?)"', html_content)
humidity2=re.findall(r'"humidity": "(.*?)"', html_content)
meteo_ajd=[]
for i in range(0,len(weather2)) :
  weather2[i] = weather2[i].replace("x27", "'") 

c=0
a=9
while str(a) not in str(date2[c]): 
        c += 1  
    
meteo_ajd_9=[
        str(a)+"h00",
        weather2[c],
        "Temp : " + temperature[c] ,
        "Vent : " + wind2[c]]
a+=6 
while str(a) not in str(date2[c]): 
        c += 1    
meteo_ajd_15=[
        str(a)+"h00",
        weather2[c],
        "Temp : " + temperature[c] ,
        "Vent : " + wind2[c]]
a+=5   
while str(a) not in str(date2[c]): 
        c += 1  
meteo_ajd_20=[
        str(a)+"h00",
        weather2[c],
        "Temp : " + temperature[c] ,
        "Vent : " + wind2[c]]


    
def draw_arrow():

# Dimensions de l'image
 width, height = 200, 200

# Créer une image blanche
 img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
 draw = ImageDraw.Draw(img)
 if img == "RGBA":
    new_image = Image.new("RGB", img, (255, 255, 255))  # Créer un fond blanc
    new_image.paste(img, (0, 0), img)  # Appliquer l'image par-dessus
    img = new_image
# Dessiner une flèche vers le haut avec un trait fin
 draw.line([(width // 2, height - 20), (width // 2, 20)], fill='black', width=5)  # Lignes verticales
 if int(coeff)<=int(coeffJ2):
  draw.line([(width // 2 - 10, 40), (width // 2, 20)], fill='black', width=5)  # Partie gauche de la flèche
  draw.line([(width // 2 + 10, 40), (width // 2, 20)], fill='black', width=5)  # Partie droite de la flèche
 else :
  draw.line([(width // 2 - 10, height - 40), (width // 2, height - 20)], fill='black', width=5)  # Partie gauche de la flèche
  draw.line([(width // 2 + 10, height - 40), (width // 2, height - 20)], fill='black', width=5)  # Partie droite de la flèche

 return(img)
    
    

fleche_haut=draw_arrow()


# Dessin de l'image avec la date du jour
today= datetime.datetime.now().strftime('%A %d %B')  
jour, date, mois = today.split()  # Sépare "mercredi", "03", et "février"

# Mettre la première lettre du jour et du mois en majuscule
jour = jour.capitalize()
mois = mois.capitalize()
font_bold = ImageFont.truetype("arialbd.ttf", size=40)
# Reconstruire la date avec la première lettre de chaque mot en majuscule
today = f"{jour} {date} {mois}" # "Vendredi 03 janvier"
print(today)
# Créer une image vierge
img = Image.new('RGB', (842, 1123), color=(255, 255, 255))
d = ImageDraw.Draw(img)

font_petit=ImageFont.truetype("arial.ttf", 25) 
font_petitbd=ImageFont.truetype("arialbd.ttf", 25) 
# Utiliser une police par défaut
font = ImageFont.truetype("arial.ttf", 40) 
font_date=ImageFont.truetype("arialbd.ttf", size=60)

meteo_image_ajd=requests.get(weather_icon[1])
image_meteo_ajds= Image.open(BytesIO(meteo_image_ajd.content))

if image_meteo_ajds.mode == "RGBA":
    new_image = Image.new("RGB", image_meteo_ajds.size, (255, 255, 255))  # Créer un fond blanc
    new_image.paste(image_meteo_ajds, (0, 0), image_meteo_ajds)  # Appliquer l'image par-dessus
    image_meteo_ajds = new_image  # Remplacer l'image d'origine

image_meteo_ajds = image_meteo_ajds.resize((150, 150), Image.LANCZOS)
img.paste(image_meteo_ajds, (20, 695)) 
n=1
x, y = 200,695
for item in meteo_ajd_9:
              if n<=2:
                if len(item)>15:
                 wrapped_meteo = wrap(item+"." , width=15)  
                 d.text((x, y), f"{wrapped_meteo[0]}", fill="black", font=font_petitbd)
                 d.text((x, y+30), f"{wrapped_meteo[1]}", fill="black", font=font_petitbd)
                 y+=30
                else :
                  d.text((x, y), f"{item}", fill="black", font=font_petitbd)
              else:
                if len(item)>15:
                 wrapped_meteo = wrap(item+"." , width=15)  
                 d.text((x, y), f"{wrapped_meteo[0]}", fill="black", font=font_petit)
                 d.text((x, y+30), f"{wrapped_meteo[1]}", fill="black", font=font_petit)
                 y+=30
                else :
                  d.text((x, y), f"{item}", fill="black", font=font_petit)
              n+=1
              y +=30  # Décalage vertical
n=1
x, y = 410,695
for item in meteo_ajd_15:
            if n<=2:
                if len(item)>15:
                 wrapped_meteo = wrap(item+"." , width=15)  
                 d.text((x, y), f"{wrapped_meteo[0]}", fill="black", font=font_petitbd)
                 d.text((x, y+30), f"{wrapped_meteo[1]}", fill="black", font=font_petitbd)
                 y+=30
                else :
                  d.text((x, y), f"{item}", fill="black", font=font_petitbd)
            else:
             if len(item)>15:
                 wrapped_meteo = wrap(item+"." , width=15)  
                 d.text((x, y), f"{wrapped_meteo[0]}", fill="black", font=font_petit)
                 d.text((x, y+30), f"{wrapped_meteo[1]}", fill="black", font=font_petit)
                 y+=30
             else :
                  d.text((x, y), f"{item}", fill="black", font=font_petit)
            n+=1
            y +=30  # Décalage vertical
n=1
x, y = 600,695
for item in meteo_ajd_20:
              if n<=2:
                if len(item)>15:
                 wrapped_meteo = wrap(item+"." , width=15)  
                 d.text((x, y), f"{wrapped_meteo[0]}", fill="black", font=font_petitbd)
                 d.text((x, y+30), f"{wrapped_meteo[1]}", fill="black", font=font_petitbd)
                 y+=30
                else :
                  d.text((x, y), f"{item}", fill="black", font=font_petitbd)
              else:
                if len(item)>15:
                 wrapped_meteo = wrap(item+"." , width=15)  
                 d.text((x, y), f"{wrapped_meteo[0]}", fill="black", font=font_petit)
                 d.text((x, y+30), f"{wrapped_meteo[1]}", fill="black", font=font_petit)
                 y+=30
                else :
                  d.text((x, y), f"{item}", fill="black", font=font_petit)
              n+=1
              y +=30  # Décalage vertical


x, y = 150, 855
meteoimagedemain = requests.get(weather_icon[2])
image_meteo_demain= Image.open(BytesIO(meteoimagedemain.content))


if image_meteo_demain.mode == "RGBA":
    new_image = Image.new("RGB", image_meteo_demain.size, (255, 255, 255))  # Créer un fond blanc
    new_image.paste(image_meteo_demain, (0, 0), image_meteo_demain)  # Appliquer l'image par-dessus
    image_meteo_demain = new_image  # Remplacer l'image d'origine

image_meteo_demain.thumbnail((100,100), Image.LANCZOS)
img.paste(image_meteo_demain, (30,865)) 


print(weather_icon[8])
        # Ajouter le texte sur l'image
n=1
for item in meteo_demain:
            if n<=2:
             d.text((x, y), f"{item}", fill="black", font=font_petitbd)
            else:
             d.text((x, y), f"{item}", fill="black", font=font_petit)
            n+=1
            y +=30  # Décalage vertical
x, y = 540, 865
n=1
for item in meteo_apresdemain:
            if n<=2:
             if len(item)>15:
                wrapped_meteo_apd = wrap(item+"." , width=15)  
                d.text((x, y), f"{wrapped_meteo_apd[0]}", fill="black", font=font_petitbd)
                d.text((x, y+30), f"{wrapped_meteo_apd[1]}", fill="black", font=font_petitbd)
                y+=30
             else :
              d.text((x, y), f"{item}", fill="black", font=font_petitbd)
            else:
             if len(item)>15:
                wrapped_meteo_apd = wrap(item+"." , width=15)  
                d.text((x, y), f"{wrapped_meteo_apd[0]}", fill="black", font=font_petit)
                d.text((x, y+30), f"{wrapped_meteo_apd[1]}", fill="black", font=font_petit)
                y+=30
             else :
              d.text((x, y), f"{item}", fill="black", font=font_petit)
            n+=1
            y +=30  # Décalage vertical

meteoimageapresdemain = requests.get(weather_icon[3])
image_meteo_apresdemain= Image.open(BytesIO(meteoimageapresdemain.content))


if image_meteo_apresdemain.mode == "RGBA":
    new_image = Image.new("RGB", image_meteo_apresdemain.size, (255, 255, 255))  # Créer un fond blanc
    new_image.paste(image_meteo_apresdemain, (0, 0), image_meteo_apresdemain)  # Appliquer l'image par-dessus
    image_meteo_apresdemain = new_image  # Remplacer l'image d'origine
if weather_icon[3]=="https://cdn-icons-png.flaticon.com/512/5213/5213449.png":
   image_meteo_apresdemain.thumbnail((100,100), Image.LANCZOS)
   img.paste(image_meteo_apresdemain, (420, 865)) 
else :
 image_meteo_apresdemain = image_meteo_apresdemain.resize((100, 100), Image.LANCZOS)
 img.paste(image_meteo_apresdemain, (420, 865)) 
img.paste(fleche_haut,(220,150))
img.paste(image,(250,150))

font_bm2=ImageFont.truetype("arial.ttf", size=30)
# Ajouter le texte sur l'image
font_max=ImageFont.truetype("arialbd.ttf", size=130)
d.text((120, 50), today, font=font_date, fill=(0, 0, 0))
d.text((00, 10), ".", font=font_bm2, fill=(0, 0, 0))
# Ajouter le coefficient en dessous de la date
d.text((80, 170), f"coeff", font=font, fill=(0, 0, 0))
if int(coeff)>=100:
 d.text((20, 200), f"{coeff}", font=font_max, fill=(0, 0, 0))
else:
 d.text((50, 200), f"{coeff}", font=font_max, fill=(0, 0, 0))

if image_dl.mode == "RGBA":
    new_image = Image.new("RGB", image_dl.size, (255, 255, 255))  # Créer un fond blanc
    new_image.paste(image_dl, (0, 0), image_dl)  # Appliquer l'image par-dessus
    image_dl = new_image  # Remplacer l'image d'origine
image_dl.thumbnail((200,200), Image.LANCZOS)


draw = ImageDraw.Draw(img)
draw.line((0,415, 320 ,415 ), fill="black", width=5)
draw.line((475,415, 1123 ,415 ), fill="black", width=5)
img.paste(image_dl, (350, 370)) 
wrapped_text = wrap(selected_html2str+"." , width=38)
for i in range(0,len(wrapped_text)):
 d.text((30, 470+i*45), wrapped_text[i] , font=font_bold, fill=(0, 0, 0))

# Ajouter un titre pour les tableaux
font_pm=ImageFont.truetype("arialbd.ttf", size=60)
d.text((360, 170), "Pleine mer ", font=font, fill=(0, 0, 0))
y_offset_haute_mer = 210  # Position initiale pour la liste Haute mer
for value in haute_mer:
    d.text((360, y_offset_haute_mer), f"{value}", font=font_pm, fill=(0, 0, 0))
    y_offset_haute_mer += 60  # Décaler la ligne pour la prochaine valeur
font_bm=ImageFont.truetype("arialbd.ttf", size=40)
font_bm2=ImageFont.truetype("arial.ttf", size=30)
y_offset_haute_mer=190
d.text((600, y_offset_haute_mer), "Basse mer ", font=font_bm2, fill=(0, 0, 0))
# Ajouter les valeurs Basse mer sous forme de liste
y_offset_basse_mer = y_offset_haute_mer+40  # Position initiale pour la liste Basse mer
for value in basse_mer:
    d.text((610, y_offset_basse_mer), f"{value}", font=font_bm, fill=(0, 0, 0))
    y_offset_basse_mer += 40  # Décaler la ligne pour la prochaine valeur

# Ajouter les valeurs Haute mer sous forme de liste


# Enregistrer l'image
img.save(r'D:/téléchargement/test.jpg')

# Afficher l'image
img.show()


"""
app = Flask(__name__)

# Répertoire où l'image est stockée
image_folder = "D:/téléchargement"

@app.route('/image')
def get_image():
    # Remplace 'image.png' par le nom de ton fichier image
    return send_from_directory(image_folder, 'test.jpg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=500)
"""