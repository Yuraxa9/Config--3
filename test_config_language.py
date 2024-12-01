# Ожидаемый вывод для task_manager_config
expected_task_manager_config = """
[
def default_priority = 'Medium',
def max_tasks_per_user = 10,
task_manager => [
    users => [
        user1 => [
            name => 'Alice',
            tasks => {
[
                    name => 'Task 1',
                    priority => 'Medium'
                    ],
[
                    name => 'Task 2',
                    priority => 'High'
                    ]
                }
            ],
        user2 => [
            name => 'Bob',
            tasks => {
[
                    name => 'Task 3',
                    priority => 'Medium'
                    ],
[
                    name => 'Task 4',
                    priority => 'Low'
                    ]
                }
            ]
        ],
    max_tasks_per_user => 10
    ]
]
"""

# Ожидаемый вывод для cloud_storage_config
expected_cloud_storage_config = """
[
def storage_limit = 100,
def storage_used = 75,
cloud_storage => [
    users => {
[
            name => 'user1',
            storage_used => 75
            ],
[
            name => 'user2',
            storage_used => 50
            ]
        },
    total_limit => 100
    ]
]

"""

# Функция для генерации конфигурационного языка
def generate_output(data, indent=0):
    """Генерирует текст на учебном конфигурационном языке с учетом отступов."""
    spacer = " " * (indent * 4)
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            if key.startswith("def "):  # Обрабатываем константы
                name = key.split(" ", 1)[1]
                items.append(f"{spacer}def {name} = {generate_output(value, indent)}")
            else:
                items.append(f"{spacer}{key} => {generate_output(value, indent + 1)}")
        return "[\n" + ",\n".join(items) + "\n" + spacer + "]"
    elif isinstance(data, list):
        items = [generate_output(value, indent + 1) for value in data]
        return "{\n" + ",\n".join(items) + "\n" + spacer + "}"
    elif isinstance(data, str):
        return f"'{data}'"
    elif isinstance(data, (int, float)):
        return str(data)
    else:
        raise TypeError(f"Неизвестный тип данных: {type(data)}")

# Функция для тестирования
def test_config_language():
    all_tests_passed = True  # Переменная для отслеживания статуса всех тестов

    # Входные данные для task_manager_config
    input_data_task_manager = {
        "def default_priority": "Medium",
        "def max_tasks_per_user": 10,
        "task_manager": {
            "users": {
                "user1": {
                    "name": "Alice",
                    "tasks": [
                        {"name": "Task 1", "priority": "Medium"},
                        {"name": "Task 2", "priority": "High"}
                    ]
                },
                "user2": {
                    "name": "Bob",
                    "tasks": [
                        {"name": "Task 3", "priority": "Medium"},
                        {"name": "Task 4", "priority": "Low"}
                    ]
                }
            },
            "max_tasks_per_user": 10
        }
    }

    # Входные данные для cloud_storage_config
    input_data_cloud_storage = {
        "def storage_limit": 100,
        "def storage_used": 75,
        "cloud_storage": {
            "users": [
                {"name": "user1", "storage_used": 75},
                {"name": "user2", "storage_used": 50}
            ],
            "total_limit": 100
        }
    }

    # Преобразование и вывод для task_manager_config
    output_task_manager = generate_output(input_data_task_manager)

    # Преобразование и вывод для cloud_storage_config
    output_cloud_storage = generate_output(input_data_cloud_storage)

    # Сравнение с ожидаемым результатом для task_manager_config
    if expected_task_manager_config.strip() == output_task_manager.strip():
        print("test_task_manager_config PASSED")
    else:
        all_tests_passed = False
        print("test_task_manager_config FAILED")
        print("Expected output:")
        print(expected_task_manager_config)
        print("Actual output:")
        print(output_task_manager)

    # Сравнение с ожидаемым результатом для cloud_storage_config
    if expected_cloud_storage_config.strip() == output_cloud_storage.strip():
        print("test_cloud_storage_config PASSED")
    else:
        all_tests_passed = False
        print("test_cloud_storage_config FAILED")
        print("Expected output:")
        print(expected_cloud_storage_config)
        print("Actual output:")
        print(output_cloud_storage)

    # Итоговый вывод о статусе всех тестов
    if all_tests_passed:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed.")

# Запуск теста
test_config_language()
