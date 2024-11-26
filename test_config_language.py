from config_language import Translator
import toml
import re

# Пример конфигурации 1
toml_data_game = """
[settings]
resolution = "1920x1080"
fullscreen = true
sound_volume = 80

[graphics]
quality = "high"
anti_aliasing = true

[controls]
movement = "WASD"
action_button = "Space"
"""

# Пример конфигурации 2
toml_data_research = """
[research]
project_name = "Quantum Computing"
budget = 5000000
deadline = "2025-12-31"

[team]
lead = "Dr. Smith"
members = ["Alice", "Bob", "Charlie"]

[resources]
computing_power = 1000
funding_sources = ["Government", "Private Sector"]
"""

# Пример с константами
input_text_with_constants = """
def pi = 3.14159
def radius = 10
def area = pi * radius * radius
"""

def run_tests():
    translator = Translator()  # Используем класс Translator
    
    # Тест 1: Преобразование TOML в формат конфигурации (игра)
    print("Тест 1: Конфигурация игры")
    toml_data = translator.parse_toml(toml_data_game)
    result = translator.translate(toml_data)
    expected_output_game = """settings => [
    resolution => '1920x1080',
    fullscreen => true,
    sound_volume => 80
]
graphics => [
    quality => 'high',
    anti_aliasing => true
]
controls => [
    movement => 'WASD',
    action_button => 'Space'
]"""
    test1_success = result == expected_output_game
    print("Ожидаемый результат:\n", expected_output_game)
    print("Полученный результат:\n", result)
    print("Тест 1 успешен:", test1_success)
    print("\n")

    # Тест 2: Преобразование TOML в формат конфигурации (ученый)
    print("Тест 2: Конфигурация для ученого")
    toml_data = translator.parse_toml(toml_data_research)
    result = translator.translate(toml_data)
    # Это просто три словаря
    expected_output_research = """research => [ 
    project_name => 'Quantum Computing',
    budget => 5000000,
    deadline => '2025-12-31'
]
team => [
    lead => 'Dr. Smith',
    members => { 'Alice', 'Bob', 'Charlie' }
]
resources => [
    computing_power => 1000,
    funding_sources => { 'Government', 'Private Sector' }
]"""
    test2_success = result == expected_output_research
    print("Ожидаемый результат:\n", expected_output_research)
    print("Полученный результат:\n", result)
    print("Тест 2 успешен:", test2_success)
    print("\n")

    # Тест 3: Замена констант
    print("Тест 3: Замена констант")
    translator.translate_constants(input_text_with_constants)
    replaced_text = translator.replace_constants("area = ! (pi) * radius * radius")  # Обратите внимание на пробелы
    expected_replacement = "area = 3.14159 * radius * radius"
    test3_success = replaced_text == expected_replacement
    print("Ожидаемый результат:\n", expected_replacement)
    print("Полученный результат:\n", replaced_text)
    print("Тест 3 успешен:", test3_success)
    print("\n")

    # Тест 4: Некорректная константа
    print("Тест 4: Некорректная константа")
    replaced_text_invalid = translator.replace_constants("circumference = ! (diameter) * pi")  # Пробелы добавлены
    expected_invalid_replacement = "circumference = undefined * pi"
    test4_success = replaced_text_invalid == expected_invalid_replacement
    print("Ожидаемый результат:\n", expected_invalid_replacement)
    print("Полученный результат:\n", replaced_text_invalid)
    print("Тест 4 успешен:", test4_success)
    print("\n")

    # Итоговые результаты
    all_tests_successful = test1_success and test2_success and test3_success and test4_success
    print("Все тесты успешны:", all_tests_successful)


run_tests()
