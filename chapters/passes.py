import re
from base import Round


class PassRound(Round):
    def __init__(self, title, description, examples, hint, clue, valid_codes, invalid_codes):
        super().__init__(title, description, examples, hint, clue)
        self.valid_codes = valid_codes      # правильные пропуски
        self.invalid_codes = invalid_codes  # поддельные пропуски

    def check(self, pattern):
        # 1. Проверяем, нет ли синтаксической ошибки в регулярке
        try:
            regex = re.compile(pattern)
        except re.error:
            return False, "Ошибка в синтаксисе! Проверьте скобки и спецсимволы."

        # 2. Проверяем через fullmatch, что ВСЕ настоящие пропуски подходят целиком
        for code in self.valid_codes:
            if not regex.fullmatch(code):
                return False, f"Ваш шаблон отклонил действительный пропуск: {code}"

        # 3. Проверяем, что НИ ОДИН поддельный пропуск не прошёл
        for code in self.invalid_codes:
            if regex.fullmatch(code):
                return False, f"Ваш шаблон принял поддельный пропуск: {code}"

        return True, "Верно! Все пропуски проверены."


def get_passes_rounds():
    round_1 = PassRound(
        title="Дело № 1. Поддельный пропуск",
        description="Код состоит из 2 заглавных латинских букв, дефиса и 3 цифр от 0 до 9.",
        examples="Действительные: AB-042, ZX-105\nПоддельные: ab-042, A-105, AB-1234",
        hint="Используйте [A-Z]{2}, дефис и \\d{3}.",
        clue="В ночь кражи в архив заходил сотрудник по пропуску KL-908.",
        # Первые два примера видит игрок, остальные — скрытые проверки
        valid_codes=["AB-042", "ZX-105", "KL-908"],
        invalid_codes=["ab-042", "A-105", "AB-1234", "ABC-123"]
    )

    round_2 = PassRound(
        title="Дело № 2. Секретный сектор",
        description="Код начинается с 'SEC-', затем идёт год (только 2024 или 2025), затем буква A, B или C.",
        examples="Действительные: SEC-2024A, SEC-2025C\nПоддельные: SEC-2023A, SEC-2024D, sec-2024A",
        hint="Используйте SEC-, затем (2024|2025), затем [ABC].",
        clue="Пропуск SEC-2025C принадлежит начальнику охраны.",
        valid_codes=["SEC-2024A", "SEC-2025C", "SEC-2024B"],
        invalid_codes=["SEC-2023A", "SEC-2024D", "sec-2024A", "SEC-2024AB"]
    )

    return [round_1, round_2]


# Обязательные тесты через assert (требование задания)
if __name__ == "__main__":
    rounds = get_passes_rounds()

    # Тесты для 1-го раунда
    assert rounds[0].check(r"[A-Z]{2}-\d{3}")[0] is True
    assert rounds[0].check(r"[A-Z]+-\d{3}")[0] is False
    assert rounds[0].check(r"[A-Z")[0] is False  # синтаксическая ошибка

    # Тесты для 2-го раунда
    assert rounds[1].check(r"SEC-(2024|2025)[ABC]")[0] is True
    assert rounds[1].check(r"SEC-\d{4}[A-Z]")[0] is False

    print("Все тесты Главы 1 пройдены!")
