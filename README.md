# cdpDumpingUtils

This project exists to dump files form cahier-de-prepa.fr web site. While some students try to recover every file manually, this tool can export most of the files.

DISCLAIMER : THIS TOOL IS NOT MEANT TO DEFEAT INTELLECTUAL PROPERTY, IT IS JUST A TOOL TO HELP STUDENTS.


## Installation

Install [Python3](https://www.python.org/downloads/) 

Download the repository: 

```
git clone https://github.com/Azuxul/cdpDumpingUtils.git
```

Install the dependency:

```
pip install -r requirements.txt
```

## Usage


```
python cdpDumpingUtils/main.py -h
```

```
usage: main.py [-h] [-v] [-l USERNAME] [-p PASSWORD] -o OUTPUT -u URL

options:
  -h, --help            show this help message and exit

arguments optionnels:
  -v, --verbose         Augmente la quantité de texte affiché
  -l USERNAME, --username USERNAME
                        Nom d'utilisateur du compte cahier de prepa (utilisation sans compte possible)
  -p PASSWORD, --password PASSWORD
                        Mot de passe de connexion cahier de prepa

arguments requis:
  -o OUTPUT, --output OUTPUT
                        Chemin d'acces du dossier de sortie
  -u URL, --url URL     URL de l'instance cahier de prepa
```

To run cdpDumpingUtils without an account:
```
python cdpDumpingUtils/main.py -u https://cahier-de-prepa.fr/XXX/ -o ./output
```

To run cdpDumpingUtils with an account:
```
python cdpDumpingUtils/main.py -u https://cahier-de-prepa.fr/XXX/ -l username -p password -o ./output
```

## Limitations

This tool may be unusable if cahier-de-prepa is updated. This tool only download documents. Grades, calendars and other features of cahier-de-prepa are not implemented.

## License

This project is licensed under the GNU General Public License v3.0




