def userLogin(username,inputedPassword):

    import sqlite3
    import sql
    password = None
    goodPasswordFlag = 0
    exitFlag = 0
    wrongPasswordCounter = 0
    wrongUsernameCounter = 0
    # username = input('Username:')
    password = sql.getPass(username)
    if password == None:
        return 0
        # wrongUsernameCounter = wrongUsernameCounter + 1
        # if wrongUsernameCounter == 5:
        # exitFlag = 1
        # password = ['1']

    if password[0] == inputedPassword:
        goodPasswordFlag = 1
        return 1
    if inputedPassword != password[0]:
        print('Incorrect Password Please Try Again')
        return 2