from chapters.passes import get_passes_rounds
from chapters.archive import get_archive_rounds

def start_game():
    print("=== «REGEX-ДЕТЕКТИВ» ===")
    print("Расследуйте дело, составляя регулярные выражения.\n")

    # Собираем раунды из обеих глав
    all_rounds = get_passes_rounds() + get_archive_rounds()
    clues = []

    for number, current_round in enumerate(all_rounds, start=1):
        print(f"--- Раунд {number}. {current_round.title} ---")
        print(current_round.description)
        print("\nПримеры:")
        print(current_round.examples)

        while True:
            answer = input("\nВведите регулярное выражение (или слово 'подсказка'): ").strip()
            
            if answer.lower() == "подсказка":
                print(f"Подсказка: {current_round.hint}")
                continue

            is_correct, message = current_round.check(answer)
            print(message)

            if is_correct:
                print(f"Улика получена: {current_round.clue}\n")
                clues.append(current_round.clue)
                break

    print("=== РАССЛЕДОВАНИЕ ЗАВЕРШЕНО ===")
    print("Все собранные улики:")
    for clue in clues:
        print(f"- {clue}")

if __name__ == "__main__":
    start_game()

