#Fill in information from setting up SQL Server
def connectionString():

    driver = '********'
    server = '********'
    database = '*********'
    username = '*********'
    password = '*********'

    CONNECTION_STRING = 'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';'

    return CONNECTION_STRING