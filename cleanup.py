#!/usr/bin/env python3
"""
Удаляет все CSV-файлы, созданные не сегодня.
Файлы имеют формат: crypto_screener_YYYYMMDD_HHMMSS.csv
"""

import os
import glob
from datetime import datetime

def get_today_str():
    """Возвращает сегодняшнюю дату в формате YYYYMMDD"""
    return datetime.now().strftime('%Y%m%d')

def cleanup_old_csv():
    """Удаляет CSV-файлы, дата в имени которых не совпадает с сегодняшней"""
    today = get_today_str()
    pattern = 'crypto_screener_*.csv'
    removed_count = 0

    for file_path in glob.glob(pattern):
        filename = os.path.basename(file_path)
        # Имя должно начинаться с crypto_screener_
        if not filename.startswith('crypto_screener_'):
            continue
        # Извлекаем 8 символов после префикса (это дата)
        date_part = filename[len('crypto_screener_'):len('crypto_screener_') + 8]
        # Проверяем, что это дата и она не сегодня
        if date_part != today:
            try:
                os.remove(file_path)
                removed_count += 1
                print(f"🗑️ Удалён старый файл: {file_path}")
            except Exception as e:
                print(f"⚠️ Не удалось удалить {file_path}: {e}")

    print(f"✅ Удалено {removed_count} старых CSV-файлов")

if __name__ == "__main__":
    cleanup_old_csv()