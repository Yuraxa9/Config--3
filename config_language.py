import toml
import sys
import re

class Translator:
    def __init__(self):
        self.constants = {}  # Хранилище для констант
    
    def parse_toml(self, input_text):
        try:
            return toml.loads(input_text)
        except toml.TomlDecodeError as e:
            sys.stderr.write(f"Ошибка разбора TOML: {str(e)}\n")
            sys.exit(1)

    def translate_value(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, int) or isinstance(value, float):
            return str(value)
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, list):
            return '{ ' + '. '.join(self.translate_value(item) for item in value) + ' }'
        elif isinstance(value, dict):
            return '[\n' + ',\n'.join(f"    {k} => {self.translate_value(v)}" for k, v in value.items()) + '\n]'
        else:
            raise ValueError("Неизвестный тип данных")

    def translate_constants(self, input_text):
        pattern = r'def\s+([a-z][a-z0-9_]*)\s*=\s*(.+)'
        matches = re.finditer(pattern, input_text)
        for match in matches:
            name, value = match.groups()
            self.constants[name] = value.strip()  # Убираем лишние пробелы вокруг значений

    def replace_constants(self, text):
        pattern = r'!\s*\((\w+)\)'  # Регулярное выражение для поиска констант
        while re.search(pattern, text):
            text = re.sub(pattern, lambda m: self.constants.get(m.group(1), 'undefined'), text)
        return text

    def translate(self, toml_data):
        output_lines = []
        for key, value in toml_data.items():
            if isinstance(value, dict):
                output_lines.append(f"{key} => {self.translate_value(value)}")
            else:
                output_lines.append(f"{key} => {self.translate_value(value)}")
        return '\n'.join(output_lines)


def main():
    input_text = sys.stdin.read()
    translator = Translator()
    
    # Обработка констант
    translator.translate_constants(input_text)
    input_text = translator.replace_constants(input_text)
    
    toml_data = translator.parse_toml(input_text)
    translated_text = translator.translate(toml_data)
    
    sys.stdout.write(translated_text + '\n')

if __name__ == "__main__":
    main()
