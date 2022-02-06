import sqlite3
import rsa
# import menu
import mealSearch as ms

publicKey, privateKey = rsa.newkeys(64)
userEmail = []

def loginMenu():
    menu = {1: ("Login", login), 2: ("Register", signup), 3: ("End Program", endProgram)}

    menu.get(int(input(f'''Select an action:
        1. {menu[1][0]}
        2. {menu[2][0]}
        3. {menu[3][0]}
    ''')), None)[1]()

def login():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()
    email = input("Enter email address for login: ")
    password = input("Enter the password for your account: ")
    # cursor.execute('''SELECT AES_ENCRYPT(?, ?);''', (password, encryptKey))
    # encryptedPassword = cursor.fetchone()
    cursor.execute("SELECT * FROM user WHERE email = ? AND password = ?;", (email, password)) 
    data = cursor.fetchone()
    
    if data is None:
        print("\nInvalid email/password!", end="\n\n")
        loginMenu() 
    else:
        print("Successfully logged in.\n")
        userEmail.clear()
        userEmail.append(email)
        ms.userActions()

def signup():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()
    email = input("Enter email address for signup: ")
    cursor.execute('SELECT email FROM user WHERE email = ?', (email,))
    emailData = cursor.fetchone()
    if emailData is not None:
        print("An account already exists with that email address!", end="\n\n")
        loginMenu()
    else:
        password = input("Enter the password for your account: ")
        cursor.execute('SELECT password FROM user WHERE email = ?', (email,))
        
        # cursor.execute('''SELECT AES_ENCRYPT(?, ?);''', (password, encryptKey))
        # encryptedPass = str(cursor.fetchone())
        cursor.execute('''INSERT INTO user(email, password) VALUES(?, ?)''', (email, password))
        print("Account successfully registered. You're now automatically logged in.")
        userEmail.clear()
        userEmail.append(email)

        viewQuery = f'''
        CREATE VIEW {userEmail[0]} (meal_id, email) AS 
        SELECT meal_id, email FROM user_recipes
        WHERE email = {userEmail[0]};
        '''
        cursor.execute(viewQuery)
        conn.commit()
        ms.userActions()

def endProgram(): # using it for printing
  print("Program terminated.", end="")
  exit()