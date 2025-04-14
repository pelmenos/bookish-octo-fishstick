import datetime
import json
import logging
from constants import HOT, COLD, ELEC

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_history(file_path):
    try:
        with open(file_path) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Ошибка при загрузке истории: {e}")
        return []


def save_history(file_path, history):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except IOError as e:
        logging.error(f"Ошибка при сохранении истории: {e}")


def calculate_cost(current, previous, rate):
    return (current - previous) * rate


def get_user_input():
    try:
        hot = int(input("Горячая вода: "))
        cold = int(input("Холодная вода: "))
        elec = int(input("Электричество: "))
        return hot, cold, elec
    except ValueError:
        logging.error("Некорректный ввод. Пожалуйста, введите целые числа.")
        return None, None, None


def main():
    history_file = 'history.json'
    history = load_history(history_file)

    if not history:
        logging.info("История показаний пуста. Будет создана новая запись.")
        previous = {'hot': 0, 'cold': 0, 'elec': 0}
    else:
        previous = history[-1]

    hot, cold, elec = get_user_input()

    if hot is None or cold is None or elec is None:
        return

    if hot < previous['hot'] or cold < previous['cold'] or elec < previous['elec']:
        logging.error("Новые показания не могут быть меньше предыдущих.")
        return

    hot_cost = calculate_cost(hot, previous['hot'], HOT)
    cold_cost = calculate_cost(cold, previous['cold'], COLD)
    elec_cost = calculate_cost(elec, previous['elec'], ELEC)

    total_cost = hot_cost + cold_cost + elec_cost
    print(f"Общая стоимость: {total_cost}")

    history.append({
        'hot': hot,
        'cold': cold,
        'elec': elec,
        'total_cost': total_cost,
        'created_at': datetime.datetime.now().strftime("%Y-%m-%d")
    })

    save_history(history_file, history)


if __name__ == "__main__":
    main()
