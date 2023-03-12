from os import path
from setuptools import setup, find_packages

exec(compile(open('cdpDumpingUtils/version.py').read(), 'cdpDumpingUtils/version.py', 'exec'))

def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name="cdpDumpingUtils",
    author="azuxul",
    url="https://github.com/Azuxul/cahier-de-prepa-downloader",
    description="Download all your courses filles from cahier de prepa",
    long_description=readme(),
    long_description_content_type='text/markdown',
    version=__version__,
    license='GPL-3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cdpDumpingUtils=cdpDumpingUtils.main:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        "setuptools>=45.0",
        "beautifulsoup4>=4.11.2",
        "bs4>=0.0.1",
        "html5lib>=1.1",
        "requests>=2.22.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)