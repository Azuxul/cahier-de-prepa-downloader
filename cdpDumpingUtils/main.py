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

output_dir = None
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

    log_user = username is not None and password is not None

    # Remove trailing slash if present
    if(base_url.endswith("/")):
        base_url = base_url[:-1]

    data = {
        "csrf-token": "undefined",
        "login": username,
        "motdepasse": password,
        "connexion": "1"
    }

    session = requests.Session()
    jsonRep = None

    if log_user:
        response = session.post(base_url + "/ajax.php", data=data)

        if response.status_code != 200:
            exit()

        jsonRep = json.loads(response.text)

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

    if jsonRep is not None and jsonRep["etat"] != "ok":
        print("Informations de connexion incorectes")
        exit()

    print("Exploration de ", title, " en cours...")

    for i in range(100):
        explore(i)

    print("Exploration terminée. (", len(pages), " pages trouvées )")
    print()
    print("Téléchargement des documents...")

    nbDoc = 0
    nbDocRef = 0

    for p in docs.keys():
        print("Page ", p, ": ", pages[p].replace(" / ", "/"))

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
                print("Document ", d, ": ", docs[p][d])
                file_name = dl.headers["Content-Disposition"].replace("filename=", "").replace("attachment; ", "").replace("inline; ", "")

                title = re.sub(r"[:?\"<>/|]", "", re.sub(r"[*]", "(etoile)", title))

                direct = os.path.join(output_dir, title, re.sub(r"[:*?\"<>|]", "", os.path.join(*[i.strip() for i in pages[p].split("/")]) ))

                os.makedirs(os.path.join(os.getcwd(), direct), exist_ok=True)

                file_name = re.sub(r"[:*?\"<>/|]", "", file_name).encode("latin-1").decode("utf-8")
                with open(os.path.join(os.getcwd(), direct, str(file_name)), "wb") as file:
                    file.write(dl.content)

                nbDoc += 1
        print("--")

    print(nbDoc, " documents téléchargés")
    print(nbDocRef, " documents protégés")

def main(args=None):
    global output_dir, base_url, username, password, verbose

    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group("arguments optionnels")
    optional.add_argument("-v", "--verbose", help="Augmente la quantité de texte affiché", action="store_true")
    optional.add_argument("-l", "--username", help="Nom d'utilisateur du compte cahier de prepa (utilisation sans compte possible)")
    optional.add_argument("-p", "--password", help="Mot de passe de connexion cahier de prepa")
    required = parser.add_argument_group("arguments requis")
    required.add_argument("-o", "--output", help="Chemin d'acces du dossier de sortie", required=True)
    required.add_argument("-u", "--url", help="URL de l'instance cahier de prepa", required=True)
    
    args = parser.parse_args()

    if args.username and args.password is None:
        parser.error("--username requiret --password")

    verbose = args.verbose

    output_dir = args.output
    base_url = args.url
    username = args.username
    password = args.password

    print("cdpDumpingUtils v", __version__)
    print()

    start()

if __name__ == "__main__":
    main()
    