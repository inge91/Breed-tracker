import requests
import re
import time

breeds = ["mops", "Mops", "pug", "Pug"]
species = "hond"


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


def main():
    while(True):
        #time.sleep(300)
        r = requests.get('http://www.ikzoekbaas.nl/rss.php')
        content =  r.text
        split_item = content.split('</item>')
        split_item = split_item[1:]
        for animal in split_item:
            if(find_breed(animal)):
                print "found a pug!"
                print extract_site(animal)
        time.sleep(300)

if __name__ == "__main__":
    main()
