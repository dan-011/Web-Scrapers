from fileinput import filename
import requests
import bs4
import os
from datetime import date
import sys

def getMeals(location, meal):
    location = location.lower()
    meal = meal.lower()
    output = open(meal + ".txt", "w")
    take_meals = False
    food = ""
    search_allergens = False
    meals = {"breakfast","lunch","brunch","dinner"}

    with open(location + ".txt", "r+") as file:
        for line in file:
            if(len(line.strip()) > 0):
                if(line.strip() in meals):
                    take_meals = line.strip() == meal.strip()
                if(take_meals):
                    if(take_meals and "allergens" in line and "wheat" not in line and "gluten" not in line):
                        if(len(food) > 0):
                            output.write(food + '\n')
                        search_allergens = False
                    elif(not(line and "wheat" not in line and "gluten" not in line)):
                        food = ""
                        search_allergens = False
                    if take_meals and "allergens" not in line and len(line.strip()) > 0 and "-" not in line and meal not in line and "menu" not in line:
                        if(search_allergens and len(food) > 0):
                            output.write(food + '\n')
                        food = line.strip()
                        search_allergens = True
    output.close()
    with open(meal + ".txt", "r+") as file:
        print("At " + meal.upper() + " " + location.capitalize() + " has:")
        for line in file:
            print(" - " + line.strip().capitalize())
    os.remove(meal + ".txt")

def buildURL(dininghall, hasDay = None):
    url1 = "http://nutritionanalysis.dds.uconn.edu/shortmenu.aspx?sName=UCONN+Dining+Services&locationNum="
    after_num = "&locationName="
    dining_halls = {"putnam": ("Putnam+Dining+Hall", "06"), "south": ("South+Campus+Marketplace", "16"), "buckley" : ("Buckley+Dining+Hall", "03"), "towers" : ("Gelfenbien+Commons,%20Halal+%26+Kosher", "42"), "mcmahon" : ("McMahon+Dining+Hall", "05"), "north" : ("North+Campus+Dining+Hall", "07"), "northwest" : ("Northwest+Marketplace", "15"), "whitney" : ("Whitney+Dining+Hall", "01")}
    url2 = "&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate="
    _date = str(date.today())
    name = dining_halls[dininghall][0]
    location_number = dining_halls[dininghall][1]
    month = _date[5:7] if _date[5:7][0] != '0' else _date[6:7]
    url3 = "%2f"
    day = _date[8:] if _date[8:][0] != '0' else _date[9]
    url4 = "%2f"
    year = _date[:4]
    if(hasDay is None):
        print("Day?")
        hasDay = str(sys.stdin.readline().strip().lower())
    if(hasDay != "today" and hasDay != "tomorrow"):
        day = hasDay
    if(hasDay == "tomorrow"):
        d = int(day) + 1
        day = str(d)
    full_url = url1 + location_number + after_num + name + url2 + month + url3 + day + url4 + year
    #print(full_url)
    return full_url
def getMenu(dininghall, hasDay = None):
    url = buildURL(dininghall, hasDay)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    output = open(dininghall + ".txt", "w")
    output.write(soup.get_text().lower())
    output.close()
def searchFood(location, food):
    fileName = location if location[:-4] == ".txt" else location + ".txt"
    hasCheck = "has" in food
    _f = ""
    if(hasCheck):
        _f = food[3:].strip()
    meal = food.strip()
    if("breakfast" == meal or "brunch" == meal or "lunch" == meal or "dinner" == meal):
        getMeals(location, meal)
    hasFood = False
    previous_line = ""
    meal = ""
    afood = ""
    allergens = ""
    checkFood = False
    with open(fileName, "r+") as f:
        for line in f:
            l = line.strip()
            if("=" in line): continue
            if("breakfast" == l or "brunch" == l or "lunch" == l or "dinner" == l):
                meal = l
            if(contains_letter(line) and "allergens" not in line):
                previous_line = line[:-2]
            if("allergens" in line and checkFood):
                checkFood = False
                if not("wheat" in line or "gluten" in line):
                    print(afood)
            if("allergens" in line and ((food[:3] == "has" and food[3:].strip() in line) or food in line) and "wheat" not in line and "gluten" not in line):
                hasFood = True
                print(" - " + previous_line.capitalize() + " at " + meal.upper())
            elif(food in line and "allergens" not in line):
                hasFood = True
                checkFood = True
                print( " - " + line[:-2].capitalize() + " at " + meal.upper())
        """if(not(hasFood)):
            if(hasCheck):
                print(location.capitalize() + " does not have foods with " + _f + " today")
            else: print(location.capitalize() + " does not have " + food + " today")"""    
def searchMenu(location):
    fileName = location if location[:-4] == ".txt" else location + ".txt"
    while(True):
        print("\nFood?")
        food = sys.stdin.readline()[:-1].lower()
        if(food == "exit"): break
        if(food == "change"):
            #os.remove(fileName)
            print("Enter Dining Hall:")
            location = sys.stdin.readline()[:-1].lower()
            fileName = location if location[:-4] == ".txt" else location + ".txt"
            getMenu(location)
            continue
        hasCheck = "has" in food
        _f = ""
        if(hasCheck):
            _f = food[3:].strip()
        meal = food.strip()
        if("breakfast" == meal or "brunch" == meal or "lunch" == meal or "dinner" == meal):
            getMeals(location, meal)
            continue
        if("has" in food):
            print("Searching for foods that have " + _f + "...\n")
        else: print("Searching for " + food + "...\n")
        hasFood = False
        previous_line = ""
        meal = ""
        afood = ""
        allergens = ""
        checkFood = False
        with open(fileName, "r+") as f:
            for line in f:
                l = line.strip()
                if("=" in line): continue
                if("breakfast" == l or "brunch" == l or "lunch" == l or "dinner" == l):
                    meal = l
                if(contains_letter(line) and "allergens" not in line):
                    previous_line = line[:-2]
                if("allergens" in line and checkFood):
                    checkFood = False
                    if not("wheat" in line or "gluten" in line):
                        print(afood)
                if("allergens" in line and ((food[:3] == "has" and food[3:].strip() in line) or food in line) and "wheat" not in line and "gluten" not in line):
                    hasFood = True
                    print(" - " + previous_line.capitalize() + " at " + meal.upper())
                elif(food in line and "allergens" not in line):
                    hasFood = True
                    checkFood = True
                    print( " - " + line[:-2].capitalize() + " at " + meal.upper())
            if(not(hasFood)):
                if(hasCheck):
                    print(location.capitalize() + " does not have foods with " + _f + " today")
                else: print(location.capitalize() + " does not have " + food + " today")
    print("Enjoy your meal!")
def has_food(location, food):
    fileName = location if location[:-4] == ".txt" else location + ".txt"
    with open(fileName, "r+") as file:
        for line in file:
            if(len(line.strip()) > 0):
                if(food in line):
                    return True
    return False
def contains_letter(string):
    s = string.lower()
    return 'a' in s or 'b' in s or 'c' in s or 'd' in s or 'e' in s or 'f' in s or 'g' in s or 'h' in s or 'i' in s or 'j' in s or 'k' in s or 'l' in s or 'm' in s or 'n' in s or 'o' in s or 'p' in s or 'q' in s or 'r' in s or 's' in s or 't' in s or 'u' in s or 'v' in s or 'w' in s or 'x' in s or 'y' in s or 'z' in s

def clean():
    dining_halls = {"putnam", "south", "buckley", "towers", "mcmahon", "north", "northwest", "whitney"}
    for hall in dining_halls:
        try:
            os.remove(hall + ".txt")
        except Exception:
            1 == 1

def Main():
    dining_halls = {"putnam", "south", "buckley", "towers", "mcmahon", "north", "northwest", "whitney"}
    print("Enter Dining Hall:")
    while(True):
        key = sys.stdin.readline()[:-1].lower()
        if(key in dining_halls or key == "all"):
            break
        else:
            print("Not a valid dining hall, try again:")
    if(key == "all"):
        print("Day?")
        hasDay = str(sys.stdin.readline().strip().lower())
        for hall in dining_halls:
            getMenu(hall, hasDay)
        while(True):
            print("\nFood?")
            food = sys.stdin.readline()
            food = food.strip().lower()
            if("exit" == food):
                print("Enjoy your meal!")
                break
            if("has" in food):
                _f = food[3:]
                print("Searching for foods that have " + _f + "...\n")
            else: print("Searching for " + food + "...\n")
            for hall in dining_halls:
                if(has_food(hall, food)):
                    print(hall.upper() + " has:")
                    searchFood(hall, food)
            print()
        clean()
    else:
        getMenu(key)
        searchMenu(key)
        clean()

Main()