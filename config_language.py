import toml
import sys

# Хранилище констант
constants = {}

def parse_input():
    """Читает и парсит TOML из стандартного ввода."""
    try:
        return toml.loads(sys.stdin.read())
    except toml.TomlDecodeError as e:
        sys.exit(f"Ошибка синтаксиса TOML: {e}")

def process_constants(data):
    """Рекурсивно обрабатывает объявления и вычисления констант."""
    if isinstance(data, dict):
        for key, value in list(data.items()):
            # Объявление константы (удаляем префикс "def ")
            if key.startswith("def "):
                name = key.split(" ", 1)[1]  # Убираем префикс "def "
                constants[name] = process_constants(value)
                del data[key]  # Удаляем определение константы из данных
            # Замена вычисляемой константы
            elif isinstance(value, str) and value.startswith("!(") and value.endswith(")") :
                const_name = value[2:-1]
                data[key] = constants.get(const_name, f"Ошибка: не найдена константа '{const_name}'")
            else:
                data[key] = process_constants(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str) and data[i].startswith("!(") and data[i].endswith(")") :
                const_name = data[i][2:-1]
                data[i] = constants.get(const_name, f"Ошибка: не найдена константа '{const_name}'")
            else:
                data[i] = process_constants(data[i])
    return data

def generate_output(data, indent=0):
    """Генерирует текст на учебном конфигурационном языке с учетом отступов."""
    spacer = " " * (indent * 4)
    if isinstance(data, dict):
        items = ",\n".join(f"{spacer}    {key} => {generate_output(value, indent + 1)}" for key, value in data.items())
        return "[\n" + items + f"\n{spacer}]"
    elif isinstance(data, list):
        items = ". ".join(generate_output(value, indent) for value in data)
        return "{ " + items + " }"
    elif isinstance(data, str):
        return f"'{data}'"
    elif isinstance(data, (int, float)):
        return str(data)
    else:
        raise TypeError(f"Неизвестный тип данных: {type(data)}")

if __name__ == "__main__":
    input_data = parse_input()
    processed_data = process_constants(input_data)
    output = generate_output(processed_data)
    
    # Печать констант в правильном формате
    for name, value in constants.items():
        print(f"def {name} = {value}")
    print(output)