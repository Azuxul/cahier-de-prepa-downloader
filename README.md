# cdpDumpingUtils

This project exists to dump files form cahier-de-prepa.fr web site. While some students try to recover every file manually, this tool can export most of the files.

DISCLAIMER : THIS TOOL IS NOT MEANT TO DEFEAT INTELLECTUAL PROPERTY, IT IS JUST A TOOL TO HELP STUDENTS.



## Dependency

- Python 3.6.6

- bs4 >= 0.0.1

- requests >= 2.22.0

## Installation

Download the repository : 

`git clone https://github.com/Azuxul/cdpDumpingUtils.git`

Enter the cahier-de-prepa URL and the others settings in main.py

`BASE_URL = "https://cahier-de-prepa.fr/PT-Joliot-Curie/" # Cahier de prepa URL
BASE_DIR = "output" # Output directory, where the downloaded files will go
USERLOG = False # True to login on cahier-de-prepa, False to stay unconnected`



Enter your cahier-de-prepa credentials if USERLOG is set to True

`LOGIN = "***USERNAME***"
PASSWORD = "***PASSWORD***"`



## Usage

You can change parameters, see Installation section



To run the tool 

`python src/main.py`



## Limitations

This tool may be unusable if cahier-de-prepa is updated. This tool only download documents. Grades, calendars and other features of cahier-de-prepa are not implemented.



## License

This project is licensed under the GNU General Public License v3.0




