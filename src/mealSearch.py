import sqlite3
# import login as login
import login
# import os

def userActions():
    # os.system('clear')
    menu = {3: ("Blacklist ingredients", get_blacklist), 2: ("Whitelist ingredients", get_whitelist), 1: ("Include ingredients", get_mayinclude), 4: ("Search meal", meal_search), 5 : ("Display Saved Recipes", savedRecipes), 6 : ("Logout", login.loginMenu), 7 : ("End Program", exit)}
    returnVal = menu.get(int(input(f'''Select an action:
        1. {menu[1][0]}
        2. {menu[2][0]}
        3. {menu[3][0]}
        4. {menu[4][0]}
        5. {menu[5][0]}
        6. {menu[6][0]}
        7. {menu[7][0]}
    ''')), None) 
    if returnVal is None:
        print("\nInvalid option selected!\n")
        userActions()
    elif returnVal[1] is not None:
        returnVal[1]()
    return


# function to receive user input for blacklist ingredients
def get_blacklist():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
    DROP TABLE IF EXISTS blacklist;
    ''')
    cursor.execute('''
    CREATE TABLE blacklist(
        ing_name VARCHAR(100)
    );
    ''')
    # ingredients = cursor.execute('''
    # SELECT * FROM ingredients;
    # ''')
    # for x in ingredients: 
    #     print(x[0])
    ing_input = [ing_input for ing_input in input("Select ingredients to blacklist, separated by commas: ").split(", ")]

    for x in ing_input:
        cursor.execute('''
        INSERT OR IGNORE INTO blacklist(ing_name) 
        VALUES (?)
        ''', (x, ))
    conn.commit()
    userActions() #call user actions again
    # ahh thanks, sure, will keep in mind
    # lets just test whether or not it works
    # blacklisted = cursor.execute(''' SELECT * FROM blacklist; ''')
    # for x in blacklisted:
    #     print (x[0])



# function to receive user input for whitelist ingredients
def get_whitelist():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    DROP TABLE IF EXISTS whitelist;
    ''')
    cursor.execute('''
    CREATE TABLE whitelist(
        ing_name VARCHAR(100)
    );
    ''')


    ingredients = cursor.execute('''
    SELECT * FROM ingredients;
    ''')
    for x in ingredients: 
        print(x[0])
    ing_input = [ing_input for ing_input in input("Select ingredients to whitelist, separated by commas: ").split(", ")]

    for x in ing_input:
        cursor.execute('''
        INSERT OR IGNORE INTO whitelist(ing_name) 
        VALUES (?);
        ''', [x])
    
    wlresults = cursor.execute('''
    SELECT * FROM whitelist;
    ''')
    for x in wlresults: 
        print(x)
    conn.commit()
    userActions() #call user actions again


#function to get functions to potentially include
def get_mayinclude():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
    DROP TABLE IF EXISTS mayinclude;
    ''')
    cursor.execute('''
    CREATE TABLE mayinclude(
        ing_name VARCHAR(100)
    );
    ''')

    ingredients = cursor.execute('''
    SELECT * FROM ingredients;
    ''')
    print("\n")
    for x in ingredients: 
        print(x[0], end=" - ")
    print(end="\n\n")
    ing_input = [ing_input for ing_input in input("Select ingredients to search, separated by commas: ").split(", ")]

    for x in ing_input:
        cursor.execute('''
        INSERT OR IGNORE INTO mayinclude(ing_name) 
        VALUES (?);
        ''', [x])
    conn.commit()
    userActions() #call user actions again

def meal_search():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blacklist(
        ing_name VARCHAR(100)
    );
    ''')
    
    # cursor.execute('''
    # DROP TABLE IF EXISTS whitelist;
    # ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS whitelist(
        ing_name VARCHAR(100)
    );
    ''')
    
    # cursor.execute('''
    # DROP TABLE IF EXISTS mayinclude;
    # ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mayiynclude(
        ing_name VARCHAR(100)
    );
    ''')

    conn.commit()



    #if whitelist is empty, add every ingredient to whitelist:
    cursor.execute('''
    SELECT * FROM whitelist;
    ''')
    wlcheck = cursor.fetchone()
    if wlcheck is None:
        cursor.execute(''' 
        SELECT name FROM ingredients; 
        ''')
        ings = cursor.fetchall() 
        print("\n adding stuff to whitelist manually \n")
        for x in ings:
            # print(x[0])
            cursor.executemany('''
            INSERT INTO whitelist(ing_name)
            VALUES (?);
            ''', ([x]))


    #,  ingredient_id   VARCHAR(100)
    #whitelist portion:    
    cursor.execute('''
    DROP TABLE IF EXISTS wl_handled;
    ''')
    cursor.execute('''
    CREATE TABLE wl_handled(
        meal_id         INT
    );
    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO wl_handled (meal_id)
    SELECT DISTINCT MI.meal_id FROM meal_ingredients AS MI WHERE MI.ingredient_id IN 
    (SELECT WL.ing_name FROM whitelist AS WL);
    ''')
    #wl_handled contains meal_id and ingredient_id, has reduced meals to only those which contain a whitelisteed ingredient

    # print("\n whitelist handled \n")
    # results = cursor.execute('''
    # SELECT * FROM wl_handled
    # LIMIT 20;
    # ''')
    # for x in results:
    #     print(x)



    #blacklist query:
    cursor.execute('''
    DROP TABLE IF EXISTS wl_bl_handled;
    ''')
    cursor.execute('''
    CREATE TABLE wl_bl_handled(
        meal_id         INT
    );
    ''')
    cursor.execute('''
    INSERT INTO wl_bl_handled(meal_id)
    SELECT DISTINCT wl.meal_id FROM wl_handled wl 
    JOIN meal_ingredients MI 
    ON (wl.meal_id = MI.meal_id)
    WHERE MI.ingredient_id NOT IN 
    (SELECT BL.ing_name FROM blacklist BL);    
    ''')
    #wl_bl_handled contains meal_id and ingredient_id, and has now also removed recipes with all blacklist ingredients
# lel done
    # print("\n blacklist handled \n")
    # results = cursor.execute('''
    # SELECT * FROM wl_bl_handled
    # LIMIT 20;
    # ''')
    # for x in results:
    #     print(x)



    #generic search query after whitelisting and blacklisting:
    cursor.execute('''
    DROP TABLE IF EXISTS searchresults;
    ''')
    cursor.execute('''
    CREATE TABLE searchresults(
        meal_id     INT,
        scores      INT
    );
    ''')


    results = cursor.execute('''

    SELECT M.meal_id, COUNT(M.meal_id) AS SCORE
    FROM mayinclude MI 
    JOIN wl_bl_handled M

    WHERE MI.ing_name IN (SELECT M2.ingredient_id FROM meal_ingredients M2 WHERE M2.meal_id = M.meal_id)
    GROUP BY M.meal_id
    ORDER BY SCORE DESC
    LIMIT 10;
    ''')

    print("\nSearch Results: \n")

    mealids = [x[0] for x in results] # list used to store ids of meals retrieved
    
    print("#: \t Name: ")
    
    counter = 0
    mealresults = [] #these two here contain the information for those meals
    recipeInfo = [] #so they will always be of the same size. x[0] is the actual meal i returned from queryd

    for x in mealids: 
        cursor.execute(''' 
        SELECT * FROM meal
        WHERE meal_id = (?)
        ''', (x, ))
        mealresults.append(cursor.fetchone());
        print(counter+1, "\t ", mealresults[counter][2]) #print basic meal info

        cursor.execute('''
        SELECT * FROM recipes
        WHERE meal_id = (?)
        ''', (x, ))
        recipeInfo.append(cursor.fetchone())
        counter += 1

    moreInfo = { x+1 : (mealresults[x][2], mealresults[x][3], recipeInfo[x][2] ) for x in range(0, len(mealids)) }
    
    selection = int(input("\nSelect a number to get further information of meal: "))
    info = moreInfo.get(selection)
    #yeah
    #
    print("\nMeal: ", info[0], "\nPrep. Time:", info[1])
    print("\nRecipe:", info[2])

    choice = input("\nDo you wish to bookmark the recipe? (Y/N): ")

    # inserts a tuple of current users email and selected meal_id into relationship table, can later be accessed
    if choice.upper() == "Y": 
        query = f'''
        INSERT OR IGNORE user_recipes(email, meal_id) 
        VALUES ("{login.userEmail[0]}", {mealresults[selection-1][0]});
        '''
        cursor.execute(query)
    conn.commit()
    userActions()



def savedRecipes():
    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()
    #google says operational error occurs when you miss a brace

    # viewSelect = f'''SELECT meal_id FROM "{str(email[0])}" ; '''
    viewSelect = f'''SELECT meal_id FROM user_recipes WHERE email = "{str(login.userEmail[0])}"; '''
    
    cursor.execute(viewSelect)
    savedRecs = cursor.fetchall()
    
    recipelist = {}
    counter = 1
    listofrecipes = []
    listofmeals = []
    print()    
    for x in savedRecs:
        query = f'''SELECT * FROM meal WHERE meal_id = {x[0]};'''
        cursor.execute(query)
        mealresult = cursor.fetchone()

        recipequery = f'''SELECT * FROM recipes WHERE meal_id = {x[0]};'''
        cursor.execute(recipequery) 
        reciperesult = cursor.fetchone() 
        listofrecipes.append(reciperesult)
        listofmeals.append(mealresult)
        # recipelist[counter].append({"Meal" : mealresult[2],"Prep Time": mealresult[3], "Recipe": reciperesult[2]})

        print(counter, ": ", mealresult[2]) #also printing the number of each meal based on counter, should be fine
        counter += 1

    recipelist = { count+1 : (listofmeals[count][2], listofmeals[count][3], listofrecipes[count][2]) for count in range(0, len(listofmeals)) } #looks right

    x = recipelist.get(int(input("\nSelect a meal to get recipe for: ")))

    print("\nMeal: ", x[0])
    print("Prep Time: ", x[1])
    print("\nRecipe: ", x[2], end="\n\n")
    userActions()

