import requests
from bs4 import BeautifulSoup as bs
import json, csv

url = "http://14.139.252.116:8080/appangr/"

""" Breed List for Cattle (Only) """
cattle_breeds_html = """<select class="w3-select" name="breeds" id="breeds" size="5" onchange="displayheadings()"><option value="301"> Amritmahal</option> <option value="302"> Bachaur</option> <option value="343"> Badri</option> <option value="303"> Bargur</option> <option value="341"> Belahi</option> <option value="336"> Binjharpuri</option> <option value="349"> Dagri</option> <option value="304"> Dangi</option> <option value="305"> Deoni</option> <option value="342"> Gangatiri</option> <option value="306"> Gaolao</option> <option value="335"> Ghumusari</option> <option value="307"> Gir</option> <option value="308"> Hallikar</option> <option value="309"> Hariana</option> <option value="352"> Himachali Pahari</option> <option value="310"> Kangayam</option> <option value="311"> Kankrej</option> <option value="312"> Kenkatha</option> <option value="337"> Khariar</option> <option value="313"> Kherigarh</option> <option value="314"> Khillar</option> <option value="346"> Konkan Kapila</option> <option value="339"> Kosali</option> <option value="315"> Krishna Valley</option> <option value="345"> Ladakhi</option> <option value="344"> Lakhimi</option> <option value="340"> Malnad Gidda</option> <option value="316"> Malvi</option> <option value="317"> Mewati</option> <option value="334"> Motu</option> <option value="318"> Nagori</option> <option value="348"> Nari</option> <option value="319"> Nimari</option> <option value="320"> Ongole</option> <option value="347"> Poda Thurpu</option> <option value="321"> Ponwar</option> <option value="338"> Pulikulam</option> <option value="322"> Punganur</option> <option value="353"> Purnea</option> <option value="323"> Rathi</option> <option value="324"> Red Kandhari</option> <option value="325"> Red Sindhi</option> <option value="326"> Sahiwal</option> <option value="351"> Shweta Kapila</option> <option value="327"> Siri</option> <option value="328"> Tharparkar</option> <option value="350"> Thutho</option> <option value="329"> Umblachery</option> <option value="330"> Vechur</option> </select>"""
soup = bs(cattle_breeds_html,'html.parser')
cattle_breeds = soup.find('select',{'id':'breeds'}).find_all('option')
cattle_breeds_dict = { option.text.strip():option['value'] for option in cattle_breeds }

""" CSV file Write"""
csv_file = open("data.csv","+a")
csv_writer = csv.writer(csv_file)
headers = ["Id", "Breed", "State", "Places", "Longitude", "Latitude",
           "Population","Synonyms","Origin","Major utility","Comments on utility",
           "Comments on breeding tract","Adaptability to environment",
           "Management system","Mobility","Feeding of adults","Comments on Management",
           "Colour","Horn shape and size","Visible characteristics","Height (avg. cm.)",
           "Body Length (avg. cm.)","Heart girth (avg. cm.)","Body weight (avg. kg.)",
           "Birth weight (avg. kg.)","Litter size born", "Age at first parturition (months)",
           "Parturition interval (months)",
           "Milk yield per lactation (kg)", "Milk Fat (%)", "Any Peculiarity of the breed"
    ]
csv_writer.writerow(headers)

""" Fetch and Process Data for each Breed at a time """
for breed, value in cattle_breeds_dict.items():

    """ IMAGES """
    # name format == value_breed_gender
    # value is <option> attribute, let's call it 'id'
    response = requests.get(url+f"traitheadings.php?breed={value}")
    soup = bs(response.content,'html.parser')
    male_img = soup.find('img',{'id':'mImg'})['src']
    female_img = soup.find('img',{'id':'fImg'})['src']
    
    #download the image
    male_img_raw = requests.get(male_img).content
    female_img_raw = requests.get(female_img).content

    with open(f"images/{value}_{breed}_male.jpg",'wb') as handler:
        handler.write(male_img_raw)
    
    with open(f"images/{value}_{breed}_female.jpg",'wb') as handler:
        handler.write(female_img_raw)

    """ HABITAT or BREEDING TRACT """
    response = requests.get(url+f"tract.php?breed={value}")
    soup = bs(response.content,'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    state = rows[0].find_all('td')[0].text.strip().split(':')[1].strip()
    places = [row.find_all('td')[1].text.strip() for row in rows[0:-3]]
    longitude = rows[-2].find_all('td')[1].text.strip()
    latitude = rows[-1].find_all('td')[1].text.strip()
    
    """ POPULATION """
    response = requests.get(url+"population.php?breed="+value)
    soup = bs(response.content, 'html.parser' )
    table=soup.find('table')
    rows=table.find_all('tr')
    population = [ row.find_all('td') for row in rows]
    population_data = { d[1].text.strip():d[2].text.strip() for d in population[1:]}

    """General Information"""
    response = requests.get(url+"general.php?breed="+value)
    soup = bs(response.content,'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    general_info_rows = rows[1:6]
    management_rows = rows[-4:]
    general_info_data = {
        "Synonyms": None,
        "Origin": None,
        "Major utility": None,
        "Comments on utility": None,
        "Comments on breeding tract": None,
        "Adaptability to environment": None,
        "Management system": None,
        "Mobility": None,
        "Feeding of adults": None,
        "Comments on Management": None
    }
    for row in general_info_rows:
        td = row.find_all('td')
        key = td[0].text.strip()
        if key in general_info_data.keys():
            general_info_data[key]= td[1].text.strip().replace(","," ")
    
    for row in management_rows:
        td=row.find_all('td')
        key=td[0].text.strip()
        if key in general_info_data.keys():
            general_info_data[key]= td[1].text.strip().replace(","," ")
        

    """ Morphology """
    response = requests.get(url+"morphology.php?br="+value)
    soup = bs(response.content,'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    morphology_data = []
    for row in rows[:3]:
        tds = row.find_all('td')
        morphology_data.append(tds[1].text.strip().replace(","," "))
    
    for row in rows[5:]:
        tds = row.find_all('td')
        morphology_stats = {}
        morphology_stats['male']=float(tds[1].text.strip())
        morphology_stats['female']=float(tds[2].text.strip())
        morphology_data.append(json.dumps(morphology_stats))
    print(morphology_data)
    
    """ Performance """
    response = requests.get(url+"performance.php?br="+'343')
    soup = bs(response.content,'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    performance_data = {
        "Litter size born": None,
        "Age at first parturition (months)": None,
        "Parturition interval (months)": None,
        "Milk yield per lactation (kg)": None,
        "Milk Fat (%)": None,
        "Any Peculiarity of the breed": None
    }

    for row in rows:
        tds = row.find_all('td')
        if len(tds)>1:
            key=tds[0].text.strip()
            if key in performance_data:
                performance_data[key] = tds[1].text.strip()
    
    csv_writer.writerow(
        [
            value, breed, state, ",".join(places), longitude, latitude,
            json.dumps(population_data), 
            general_info_data["Synonyms"],
            general_info_data["Origin"],
            general_info_data["Major utility"],
            general_info_data["Comments on utility"],
            general_info_data["Comments on breeding tract"],
            general_info_data["Adaptability to environment"],
            general_info_data["Management system"],
            general_info_data["Mobility"],
            general_info_data["Feeding of adults"],
            general_info_data["Comments on Management"],
            morphology_data[1],  # Colour
            morphology_data[2],  # Horn shape and size
            morphology_data[3],  # Visible characteristics
            morphology_data[-3],  # Height (avg. cm.)
            morphology_data[-2],  # Body Length (avg. cm.)
            morphology_data[-1],  # Heart girth (avg. cm.)
            performance_data["Litter size born"],
            performance_data["Age at first parturition (months)"],
            performance_data["Parturition interval (months)"],
            performance_data["Milk yield per lactation (kg)"],
            performance_data["Milk Fat (%)"],
            performance_data["Any Peculiarity of the breed"]
        ]
    )
    break 

    
csv_file.close()