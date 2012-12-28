import requests
import re
import time
import os
from flask import Flask

breeds = ["mops", "Mops", "pug", "Pug", "Herder"]
species = "hond"

app = Flask(__name__)

@app.route('/')
def display():
    f = open('pugs.txt', 'r')
    return f.read()

@app.route('/update')
def update():
    update_pug_list()
    return "It went well"

def extract_site(animal):
    # Extract species header
    descr_begin = re.search("<link>", animal)
    descr_end = re.search("</link>", animal)
    begin = descr_begin.start()
    end = descr_end.end()
    return  animal[begin + 6:end - 7]


def is_species(animal):
    # Extract species header
    descr_begin = re.search("<title>", animal)
    descr_end = re.search("</title>", animal)
    if descr_end == None or descr_begin == None:
        return False
    begin = descr_begin.start()
    end = descr_end.end()
    title = animal[begin:end]
    if( re.search(species, title)):
        return True
    else: 
        return False

def find_breed(animal):
    # Only look through the species we want 
    if not is_species(animal):
        pass
    else: 
        # Extract descriptopm
        descr_begin = re.search("<description>" , animal )
        descr_end = re.search("</description>", animal)
        begin = descr_begin.start()
        end = descr_end.end()
        description = animal[begin:end]
        for b in breeds:
            if re.search(b, description):
                return True

# updates list of pugs.txt by adding new entries
def update_pug_list():
    r = requests.get('http://www.ikzoekbaas.nl/rss.php')
    content =  r.text
    split_item = content.split('</item>')
    split_item = split_item[1:]
    for animal in split_item:
        if(find_breed(animal)):
            site = extract_site(animal)
            f = open('pugs.txt', 'a')
            wfile = f.readline()
            #duplicate = re.search(str(site), str(wfile))
            #if duplicate == None:
            f.write("<p><a href=" + site + ">" + site + "</a></p>")
            f.close()

def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
