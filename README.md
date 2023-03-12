# cdpDumpingUtils

This project exists to dump files form cahier-de-prepa.fr web site. While some students try to recover every file manually, this tool can export most of the files.

DISCLAIMER : THIS TOOL IS NOT MEANT TO DEFEAT INTELLECTUAL PROPERTY, IT IS JUST A TOOL TO HELP STUDENTS.


## Installation

Install [Python3](https://www.python.org/downloads/) 

- Automatic installation (recommended)

```
pip install cdpDumpingUtils
```

- Manual installation

Download the repository: 

```
git clone https://github.com/Azuxul/cdpDumpingUtils.git
```

Install the dependency:

```
pip install -r requirements.txt
```

Now you can use cdpDumpingUtils but instead of the `cdpDumpingUtils` command you have to use this command: `python cdpDumpingUtils/main.py`

## Usage


```
cdpDumpingUtils -h
```

```
usage: cdpDumpingUtils [-h] [--edit-cfg] [-v] [-l USERNAME] [-p PASSWORD] [-o OUTPUT] [-u URL]

options:
  -h, --help            show this help message and exit

arguments optionnels:
  --edit-cfg            Modification du fichier de configuration
  -v, --verbose         Augmente la quantité de texte affiché
  -l USERNAME, --username USERNAME
                        Nom d'utilisateur du compte cahier de prepa (utilisation sans compte possible)
  -p PASSWORD, --password PASSWORD
                        Mot de passe de connexion cahier de prepa
  -o OUTPUT, --output OUTPUT
                        Chemin d'acces du dossier de sortie, par default le dossier actuel
  -u URL, --url URL     URL de l'instance cahier de prepa
```

To run cdpDumpingUtils with a config file (if no config file it will be created) :
```
cdpDumpingUtils -o ./output
```

To run cdpDumpingUtils and specify an url without an account:
```
cdpDumpingUtils -u https://cahier-de-prepa.fr/XXX/ -o ./output
```

To run cdpDumpingUtils  and specify an url  with an account:
```
cdpDumpingUtils -u https://cahier-de-prepa.fr/XXX/ -l username -p password -o ./output
```

## Limitations

This tool may be unusable if cahier-de-prepa is updated. This tool only download documents. Grades, calendars and other features of cahier-de-prepa are not implemented.

## License

This project is licensed under the GNU General Public License v3.0
