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

In the RepoVideoGamesSQLHandler.py file the stars will have to be replaced with your local database info. </br>
You should have this information from setting up SQL Server and SSMS.

DatabaseCreation Folder\SQLConnection.py  has got the connection information that needs to be filled out
    
#Fill in information from setting up SQL Server
def connectionString():

    driver = '********'
    server = '********'
    database = '*********'
    username = '*********'
    password = '*********'

    CONNECTION_STRING = 'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';'

    return CONNECTION_STRING

