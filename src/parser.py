import pandas as pd
import sqlite3


def parse():
    f = open("./recipes.db", "r+")
    f.seek(0)
    f.truncate()

    conn = sqlite3.connect("./recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE user
    (
        email       TINYTEXT PRIMARY KEY,
        password    TINYTEXT NOT NULL
    );
    ''')
 
    # cursor.execute('''INSERT INTO user VALUES ("munim", "munim");''')
    # cursor.execute('''INSERT INTO user(email, password) VALUES ('really', 'dumdum');''') # try again with this input set
 
    cursor.execute('''
    CREATE TABLE cuisines
    (
        cuisine_id      INT PRIMARY KEY,
        name            VARCHAR(50)
    );
    ''')

    cursor.execute('''
    CREATE TABLE meal
    (
        meal_id      INT PRIMARY KEY,
        cuisine_id   INT REFERENCES cuisines(cuisine_id),
        name         VARCHAR(50),
        cook_time    VARCHAR(20)
    );
    ''')

    # cursor.execute('''
    # CREATE TABLE ingredient_type
    # (
    #     type_id     INT PRIMARY KEY,
    #     name        VARCHAR(100) NOT NULL
    # );
    # ''')

    cursor.execute('''
    CREATE TABLE ingredients
    (
        name            VARCHAR(100) PRIMARY KEY
    );
    ''')

    #ingredient_type INT
    # FOREIGN KEY (ingredient_type) REFERENCES ingredient_type(type_id)

    cursor.execute('''
    CREATE TABLE recipes
    (
        recipe_id       INT PRIMARY KEY,
        servings        INT,
        instructions    VARCHAR(1000),
        meal_id         INT REFERENCES meal(meal_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE user_recipes
    (
        email           TINYTEXT,
        meal_id         INT,

        PRIMARY KEY (email, meal_id),
        FOREIGN KEY (email) REFERENCES user(email)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (meal_id) REFERENCES recipes(meal_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE meal_ingredients
    (
        meal_id         INT,
        ingredient_id   VARCHAR(100),

        PRIMARY KEY (meal_id, ingredient_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(name)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (meal_id) REFERENCES meal(meal_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE keywords
    (
        name            VARCHAR(50) PRIMARY KEY
    );
    ''')

    cursor.execute('''
    CREATE TABLE meal_keywords
    (
        meal_id         INT,
        keyword_id      INTHAR(50),

        PRIMARY KEY (meal_id, keyword_id),
        FOREIGN KEY (meal_id) REFERENCES meal(meal_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE nutritional_information
    (
        meal_id         INT PRIMARY KEY,
        calories        FLOAT,
        fat_content     FLOAT,
        carbohydrates   FLOAT,
        sugar           FLOAT,
        protein         FLOAT,

        FOREIGN KEY (meal_id) REFERENCES meal(meal_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TRIGGER checkSaved ON recipes.user_recipes
    FOR INSERT AS
        IF EXISTS(
            SELECT * FROM user_recipes
            WHERE user_recipes.email IN (SELECT i.email FROM inserted i)
            AND user_recipes.meal_id IN (SELECT i2.meal_id FROM inserted i2)
        )
        BEGIN 
        ROLLBACK
        END;
    ''')

    data = pd.read_csv (r'./recipes.csv')   
    df = pd.DataFrame(data)

    meal_counter = 1
    for row in df.itertuples():
        for x in row.Keywords.lstrip('c(').rstrip(')').split(", "):
            #print(row)
            #print(row.Keywords[2:-1].split(", "))
            cursor.execute('''
                        INSERT OR IGNORE INTO keywords (name)
                        VALUES  (?)
                        ''', 
                        (x.strip('"'),)
                        )
        for x in row.RecipeIngredientParts.lstrip('c(').rstrip(')').split(", "):
            cursor.execute('''
                        INSERT OR IGNORE INTO ingredients (name)
                        VALUES  (?)
                        ''', 
                        (x.strip('"').rstrip(','),)
                        )
            
        cursor.execute('''
                        INSERT INTO meal(meal_id, name, cook_time)
                        VALUES (?, ?, ?)
                        ''',
                        (meal_counter, row.Name, row.TotalTime, ))
        for x in row.Keywords.lstrip('c(').rstrip(')').split(", "):        
            cursor.execute('''
                        INSERT INTO meal_keywords(meal_id, keyword_id)
                        VALUES (?, ?)''',
                        ( meal_counter,x.strip('"')),)

        for x in row.RecipeIngredientParts.lstrip('c(').rstrip(')').split(", "):
            cursor.execute('''
                        INSERT OR IGNORE INTO meal_ingredients(meal_id, ingredient_id)
                        VALUES (?, ?)''',
                        ( meal_counter,x.strip('"').rstrip(','),))

        cursor.execute('''
                        INSERT INTO nutritional_information(meal_id, calories, fat_content, carbohydrates, sugar, protein)
                        VALUES(?, ?, ?, ?, ?, ?)''',
                        (meal_counter, row.Calories, row.FatContent, row.CarbohydrateContent, row.SugarContent, row.ProteinContent,))
                        
        cursor.execute('''
                        INSERT INTO recipes(recipe_id, servings, instructions, meal_id)
                        VALUES (?, ?, ?, ?)''',
                        (meal_counter, row.RecipeServings, " ".join([x.strip('"') for x in row.RecipeInstructions[2:-1].split(", ")]), meal_counter, ))
        meal_counter += 1

    conn.commit()



