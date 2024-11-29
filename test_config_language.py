import subprocess

def run_test(input_text):
    """Выполняет скрипт config_language.py с заданным входным текстом."""
    result = subprocess.run(
        ["python", "config_language.py"],
        input=input_text,
        capture_output=True,
        text=True
    )
    if result.stderr:
        print(f"Ошибка:\n{result.stderr}")
    return result.stdout.strip()

def test_configuration(input_text, expected_output):
    """Сравнивает результат выполнения с ожидаемым выводом."""
    actual_output = run_test(input_text)
    print(f"\nОжидаемый:\n{expected_output}\nПолученный:\n{actual_output}")
    assert actual_output.strip() == expected_output.strip(), \
        f"\nОжидаемый:\n{expected_output}\nПолученный:\n{actual_output}"

if __name__ == "__main__":
    # Тест 1: Веб-приложение
    input_1 = """\
"def port" = 8080
"def env" = 'production'

server = [
    host = '0.0.0.0',
    port = !(port),
    env = !(env),
    routes = { 'home', 'about', 'contact' }
]
"""
    expected_output_1 = """\
def port = 8080
def env = 'production'
[ 
    server => [
        host => '0.0.0.0',
        port => 8080,
        env => 'production',
        routes => { 'home', 'about', 'contact' }
    ]
]
"""
    test_configuration(input_1, expected_output_1)
    print("Тест 1 пройден.")

    # Тест 2: Система мониторинга
    input_2 = """\
"def interval" = 60

monitoring = [
    enabled = true,
    interval = !(interval),
    endpoints = [
        url = 'https://service1.example.com',
        timeout = 30
    ],
    alerts = [
        email = 'alerts@example.com',
        threshold = 80
    ]
]
"""
    expected_output_2 = """\
def interval = 60
[ 
    monitoring => [
        enabled => true,
        interval => 60,
        endpoints => [
            url => 'https://service1.example.com',
            timeout => 30
        ],
        alerts => [
            email => 'alerts@example.com',
            threshold => 80
        ]
    ]
]
"""
    test_configuration(input_2, expected_output_2)
    print("Тест 2 пройден.")
