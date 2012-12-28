import requests
import re
import time
import os
import smtplib
from flask import Flask

gmail_user = "breed.tracker@gmail.com"
gmail_pwd = "i love them squishy pugs"

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

def send_mail(receiver):
    fromaddr = gmail_user
    toaddrs = receiver
    msg = """A new pug is detected! Go to http://serene-depths-3318.herokuapp.com/
    to see the new pugs"""

    #provide gmail user name and password
    username =  gmail_user
    password = gmail_pwd

    # functions to send an email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# updates list of pugs.txt by adding new entries
def update_pug_list():
    r = requests.get('http://www.ikzoekbaas.nl/rss.php')
    content =  r.text
    split_item = content.split('</item>')
    split_item = split_item[1:]
    for animal in split_item:
        if(find_breed(animal)):
            site = extract_site(animal)
            f = open('pugs.txt', 'r')
            wfile = f.read()
            f.close()
            f = open('pugs.txt', 'a')
            if site in wfile:
                pass
            else:
                f.write("<p><a href=" + site + ">" + site + "</a></p>")
                send_mail("inge.becht91@gmail.com")
            f.close()

def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
