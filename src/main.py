#this link tells how to view the django site on repl https://replit.com/talk/learn/Tutorial-Building-a-Django-web-application/6660

#https://www.programmableweb.com/search/recipe
#https://opendata.stackexchange.com/questions/4283/open-downloadable-recipe-database
#https://github.com/hhursev/recipe-scrapers
#https://www.supercook.com/#/desktop
#MUST HAVE https://eightportions.com/datasets/Recipes/#fn:1

#for gui PysimpleGUI
#yummly recipe database https://www.dropbox.com/s/f0tduqyvgfuin3l/yummly.json?dl=0
#yummlu proj github https://github.com/vishnuvikash/Recipe-Detector-
#2m recipes https://github.com/typesense/showcase-recipe-search
#stackexchange https://opendata.stackexchange.com/questions/4283/open-downloadable-recipe-database

# import parser
# parser.parse() #parse the CSV data file

import login
import mealSearch as ms
# import sqlite3
# # ms.meal_search()

# conn = sqlite3.connect("./recipes.db")
# cursor = conn.cursor()
# result = cursor.execute('''
# SELECT * FROM ingredients;
# ''')
# for x in result:
#     print(x[0])
# print("\n\n")
# cursor.execute('''
# DROP TABLE IF EXISTS whitelist;
# ''')
# cursor.execute('''
# DROP TABLE IF EXISTS mayinclude;
# ''')
# mealings = cursor.execute('''
# SELECT * FROM meal_ingredients;
# ''')

# for x in mealings:
#     print(x)

# ings = cursor.execute('''
# SELECT * FROM ingredients;
# ''')

# for x in ings:
#     print(x)

login.loginMenu()
# ms.meal_search() 
#sorry aboot that, just adding stuff of my own



# import sqlite3

# conn = sqlite3.connect("./recipes.db")
# cursor = conn.cursor()

# result = cursor.execute('''
# SELECT * FROM meal;
# ''')

# for x in result: 
#     print(x)