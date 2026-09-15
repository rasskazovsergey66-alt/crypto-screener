# src/saver.py
"""Модуль сохранения данных: пишет CSV с timestamp в корень проекта."""

import csv
from datetime import datetime

from config import CONFIG, CSV_FIELDS, BASE_DIR


def get_csv_filename():
    """Путь к файлу с уникальным timestamp-именем в корне проекта."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return BASE_DIR / f"crypto_screener_{timestamp}.csv"


def _write_csv(data, path):
    """Низкоуровневая запись CSV (разделитель ';' для Excel)."""
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=CSV_FIELDS,
            delimiter=';',
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n',
        )
        writer.writeheader()
        writer.writerows(data)


def save_to_csv(data):
    """
    Сохраняет данные в корень проекта с timestamp-именем.
    Возвращает Path сохранённого файла или None при ошибке.
    """
    if not data:
        print("❌ Нет данных для сохранения")
        return None

    try:
        path = get_csv_filename()
        _write_csv(data, path)
        print(f"💾 Данные сохранены: {path.name}")
        print(f"📊 Всего записей: {len(data)}")
        return path
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return None


def display_results(data):
    """Отображение результатов парсинга в консоли."""
    if not data:
        print("❌ Нет данных для отображения")
        return

    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ПАРСИНГА")
    print("=" * 60)

    total = len(data)
    expected = CONFIG['max_coins']
    if total == expected:
        print(f"✅ Получены данные о всех {expected} монетах!")
    else:
        print(f"⚠️ Получено {total} из {expected} монет")

    print("\n📋 ПЕРВЫЕ 5 ЗАПИСЕЙ:")
    print("-" * 80)
    print(f"{'Рейтинг':<8} {'Инструмент':<12} {'Цена':<18} {'Изм. %24ч':<12}")
    print("-" * 80)
    for coin in data[:5]:
        print(f"{coin['Рейтинг']:<8} {coin['Инструмент']:<12} "
              f"{coin['Цена']:<18} {coin['Изм. %24ч']:<12}")
    print("-" * 80)