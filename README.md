# VideoGameScanner

Setup

Python Packages:

I upgraded to pip3 and installed these packages

Pyside6:  https://pypi.org/project/PySide6/ </br>
re:       Regular expressions </br>
bs4:      https://pypi.org/project/beautifulsoup4/ </br>
pyodbc    https://pypi.org/project/pyodbc/


https://www.datacamp.com/community/tutorials/how-to-install-sql-server to set up SQL server locally

Installed SQL Server Management Studio

After installing SSMS, Create a database named VideoGames

In the RepoVideoGamesSQLHandler.py file the stars will have to be replaced with your local database info

class SqlHandler():
    def __init__(self):

        self.driver = '********'
        self.server = '********'
        self.database = '*********'
        self.username = '*********'
        self.password = '*********'


