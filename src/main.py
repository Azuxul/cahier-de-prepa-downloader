import credentials
import requests
from bs4 import BeautifulSoup
import json
import re
import os
from pathlib import Path

BASE_URL = "https://cahier-de-prepa.fr/ptsi-*********/"
BASE_DIR = "output"
USERLOG = False
USER = credentials.LOGIN
PASSWORD = credentials.PASSWORD

data = {
  'csrf-token': 'undefined',
  'login': USER,
  'motdepasse': PASSWORD,
  'connexion': '1'
}

session = requests.Session()
jsonRep = None

if USERLOG:
    response = session.post(BASE_URL + '/ajax.php', data=data)

    if response.status_code != 200:
        exit()

    jsonRep = json.loads(response.text)

pages = {}
docs = {}


def explore(explore_page):
    print("Exploring ", BASE_URL + '/docs?rep=' + str(explore_page))
    rep = session.get(BASE_URL + '/docs?rep=' + str(explore_page))
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


rep = session.get(BASE_URL)
sec = BeautifulSoup(rep.text, features="html5lib").find("title")
title = sec.text

if jsonRep is not None and jsonRep['etat'] != 'ok':
    print("Logins incorects")
    exit()

for i in range(100):
    explore(i)

nbDoc = 0
nbDocRef = 0

for p in docs.keys():
    print("Page ", p, ": ", pages[p].replace(" / ", "/"))

    for d in docs[p]:
        dl = session.get(BASE_URL + "/download?id=" + str(d))

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

            direct = BASE_DIR + u"\\" + title + u"\\" + re.sub(r"[:*?\"<>|]", "", pages[p].replace(" / ", u"\\", -1).replace(" /", u"\\", -1))

            if not os.path.exists(u"\\\\?\\" + os.getcwd() + u"\\" + direct):
                Path(u"\\\\?\\" + os.getcwd() + u"\\" + direct).mkdir(parents=True)

            file_name = re.sub(r"[:*?\"<>/|]", "", file_name).encode('latin-1').decode('utf-8').replace(" ", " ", -1)
            with open(u"\\\\?\\" + os.getcwd() + u"\\" + direct + u"\\" + str(file_name), "wb") as file:
                file.write(dl.content)

            nbDoc += 1
    print("--")

print(nbDoc, " documents téléchargés")
print(nbDocRef, " documents protégés")

