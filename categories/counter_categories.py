import json

# Функция для чтения категорий из JSON-файла
def read_categories_from_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            categories = json.load(json_file)
        return categories
    except FileNotFoundError:
        print(f"Файл {json_file_path} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении JSON-файла: {e}")
        return []

# Чтение категорий из JSON-файла
json_file_path = 'categories.json'  # Укажите путь к вашему JSON-файлу
categories = read_categories_from_json(json_file_path)

# Инициализация счетчиков для каждого уровня
level_one_count = 0
level_two_count = 0
level_three_count = 0

# Подсчет категорий для каждого уровня
for category in categories:
    if 'parent_level_two' in category:
        level_three_count += 1
    elif 'parent' in category and category['parent'] == 1:
        level_one_count += 1
    elif 'parent' in category:
        level_two_count += 1

# Вывод результатов в консоль
print(f"Количество категорий первого уровня: {level_one_count}")
print(f"Количество категорий второго уровня: {level_two_count}")
print(f"Количество категорий третьего уровня: {level_three_count}")
