#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Copyright (C) 2019-2020  Lancelot H. (Azuxul)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import argparse
import json
import os
import re
import requests
from bs4 import BeautifulSoup

from cdpDumpingUtils.version import __version__

import os
import configparser

config_file = 'cdpDumpingUtils.cfg'

output_dir = os.getcwd()
base_url = None
username = None
password = None

verbose = False

def start():
    global output_dir, base_url, username, password, verbose

    # base_url = "https://cahier-de-prepa.fr/PT-Joliot-Curie/"  # Cahier de prepa URL
    # output_dir = "output"  # Output directory, where the downloaded files will go
    # log_user = False  # True to login on cahier-de-prepa, False to stay unconnected
    # username = credentials.LOGIN
    # password = credentials.PASSWORD

    log_user = username is not None and password is not None and username != "" and password != ""

    # Remove trailing slash if present
    if(base_url.endswith("/")):
        base_url = base_url[:-1]

    session = requests.Session()
    jsonRep = None

    if log_user:
        print("Connexion en cours...")

        data = {
            "csrf-token": "undefined",
            "login": username,
            "motdepasse": password,
            "connexion": "1"
        }

        response = session.post(base_url + "/ajax.php", data=data)

        if response.status_code != 200:
            print("Erreur lors de la connexion")
            exit()

        jsonRep = json.loads(response.text)
        if jsonRep is not None and jsonRep["etat"] != "ok":
            print("Informations de connexion incorectes")
            exit()

        print("Connexion réussie")

    pages = {}
    docs = {}


    def explore(explore_page):
        if verbose:
            print("Exploring ", base_url + "/docs?rep=" + str(explore_page))
        
        rep = session.get(base_url + "/docs?rep=" + str(explore_page))
        sec = BeautifulSoup(rep.text, features="html5lib").find("section")

        if sec is not None:
            txt = sec.find("div", "warning")
            if txt is not None and (txt.string == "Mauvais paramètre d'accès à cette page." or txt.string == "Ce contenu est protégé. Vous devez vous connecter pour l'afficher."):
                return
        else:
            return

        pages[explore_page] = sec.find("span", "nom").get_text().rstrip()

        for r in sec.findAll("a", href=re.compile("rep=")):
            page = int(r["href"].replace("docs", "").replace("?rep=", ""))
            if page not in pages:
                explore(page)

        docs[explore_page] = {}
        for d in sec.findAll("p", "doc"):
            id = int(d.find("a", href=re.compile("download"))["href"].replace("download?id=", ""))
            docs[explore_page][id] = d.find("span", "nom").string


    rep = session.get(base_url)
    sec = BeautifulSoup(rep.text, features="html5lib").find("title")
    title = sec.text

    print("Exploration de", title, "en cours...")

    for i in range(100):
        explore(i)

    print("Exploration terminée. (", len(pages), "pages trouvées )")
    print()
    print("Téléchargement des documents...")

    nbDoc = 0
    nbDocRef = 0

    for p in docs.keys():
        print("Page", p, ":", pages[p].replace(" / ", "/"))

        for d in docs[p]:
            dl = session.get(base_url + "/download?id=" + str(d) + "&dl")
            # &dl argument is needed because some documents offers previews
            # (some videos for example)

            access = True

            if dl.headers["Content-Type"].lower().startswith("text/html"):
                page = BeautifulSoup(dl.text, features="html5lib").find("section")
                if page is not None:
                    txt = page.find("div", "warning")
                    if txt is not None and (txt.string == "Mauvais paramètre d'accès à cette page." or txt.string == "Ce contenu est protégé. Vous devez vous connecter pour l'afficher."):
                        access = False
                        nbDocRef += 1

            if access:
                print("Document", d, ":", docs[p][d])
                file_name = dl.headers["Content-Disposition"].replace("filename=", "").replace("attachment; ", "").replace("inline; ", "")

                title = re.sub(r"[:?\"<>/|]", "", re.sub(r"[*]", "(etoile)", title))

                direct = os.path.join(output_dir, title, re.sub(r"[:*?\"<>|]", "", os.path.join(*[i.strip() for i in pages[p].split("/")]) ))

                os.makedirs(os.path.join(os.getcwd(), direct), exist_ok=True)

                file_name = re.sub(r"[:*?\"<>/|]", "", file_name).encode("latin-1").decode("utf-8")
                with open(os.path.join(os.getcwd(), direct, str(file_name)), "wb") as file:
                    file.write(dl.content)

                nbDoc += 1
        print("--")

    print(nbDoc, "documents téléchargés")
    print(nbDocRef, "documents protégés")

def prompt_config_setup():
    global config_file, output_dir

    config_path = os.path.join(output_dir, config_file)
    
    if os.path.isfile(config_path):
        # Load the existing config file
        config = configparser.ConfigParser()
        config.read(config_path)
    else:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create a new config file
        config = configparser.ConfigParser()
        config["cahier_de_prepa"] = {}

    url = input("URL de l'instance cahier de prepa : ")
    if url is not None and url != "":
        config["cahier_de_prepa"]["url"] = url

    login = input("Connexion avec compte utilisateur ? (y/n): ")
    if login.lower() == "y":
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        config["cahier_de_prepa.credentials"] = {"username": username, "password": password}
    else:
        config["cahier_de_prepa.credentials"] = {"username": '', "password": ''}

    # Save the config file
    with open(config_path, "w") as f:
        config.write(f)
        
def load_config(prompt_no_config=False):
    global config_file, output_dir, base_url, username, password

    config_path = os.path.join(output_dir, config_file)
    
    if os.path.isfile(config_path):
        # Load the existing config file
        config = configparser.ConfigParser()
        config.read(config_path)

        if "cahier_de_prepa" in config:
            
            base_url = config["cahier_de_prepa"]["url"]
            
            if "username" in config["cahier_de_prepa.credentials"] and "password" in config["cahier_de_prepa.credentials"]:
                username = config["cahier_de_prepa.credentials"]["username"]
                password = config["cahier_de_prepa.credentials"]["password"]
        else:
            print("Impossible de lire le fichier de configuration")
            exit()

    else:
        if prompt_no_config:
            prompt_config_setup()
            load_config()
        else:
            print("Impossible de trouver le fichier de configuration")
            exit()
        
    
def main(args=None):
    global output_dir, base_url, username, password, verbose

    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group("arguments optionnels")
    optional.add_argument("--edit-cfg", help="Modification du fichier de configuration", action="store_true")
    optional.add_argument("-v", "--verbose", help="Augmente la quantité de texte affiché", action="store_true")
    optional.add_argument("-l", "--username", help="Nom d'utilisateur du compte cahier de prepa (utilisation sans compte possible)")
    optional.add_argument("-p", "--password", help="Mot de passe de connexion cahier de prepa")
    optional.add_argument("-o", "--output", help="Chemin d'acces du dossier de sortie, par default le dossier actuel")
    optional.add_argument("-u", "--url", help="URL de l'instance cahier de prepa")
    
    args = parser.parse_args()

    if args.username and args.password is None:
        parser.error("--username requiret --password")

    verbose = args.verbose

    if args.output is not None:
        output_dir = args.output

    if args.edit_cfg:
        prompt_config_setup()
        exit()

    load_config(prompt_no_config=args.url is None)

    if args.url is not None:
        base_url = args.url

    if args.username is not None:
        username = args.username

    if args.password is not None:
        password = args.password

    print("cdpDumpingUtils v", __version__)
    print()

    start()

if __name__ == "__main__":
    main()
    