import requests
import json
import sqlite3
from win10toast import ToastNotifier


def save_to_json(label, macros):
    food_data = {
        'label': label,
        'macros': macros
    }

    with open('foods.json', 'a') as json_file:
        json.dump(food_data, json_file)
        json_file.write('\n')


def save_to_database(label, macros):
    conn = sqlite3.connect('foods.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO foods (food_name, food_nutrients)
        VALUES (?, ?)''', (label, json.dumps(macros)))

    conn.commit()
    conn.close()


def search_foods(food, app_id, app_key):
    url = "https://api.edamam.com/api/food-database/v2/parser"
    parameters = {
        "ingr": food,
        "app_id": app_id,
        "app_key": app_key
    }
    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        foods = data.get('hints', [])

        if not foods:
            print(f"No information found for {food}")
        else:
            notifier = ToastNotifier()
            for food in foods:
                food_name = food['food']['label']
                food_nutrients = food['food']['nutrients']
                print("Food:", food_name)
                print("Nutrients:", food_nutrients)
                print("----------------------------------")

                save_to_json(food_name, food_nutrients)
                save_to_database(food_name, food_nutrients)

            notifier.show_toast("Database Update", "All foods have been successfully added to the database")


app_id = "ae6766ad"
app_key = "03516ffa795ea934208afb0278c5dacb"
search_foods("chicken", app_id, app_key)
