# parser.py
"""Модуль получения и парсинга таблицы"""

import time

from config import CONFIG, ROW_SELECTORS


def scroll_to_load_all_rows(page, target_count=135, max_attempts=20):
    """
    Прокручивает страницу, пока не будет загружено target_count строк
    или пока количество строк не перестанет увеличиваться.
    """
    print(f"🔄 Начинаем прокрутку для загрузки {target_count} монет...")

    previous_count = 0
    current_count = 0

    row_selector = "tbody[data-testid='selectable-rows-table-body'] tr"
    fallback_selector = "tr[class*='row-']"

    for attempt in range(1, max_attempts + 1):
        try:
            rows = page.locator(row_selector).all()
            if not rows:
                rows = page.locator(fallback_selector).all()
            current_count = len(rows)
        except Exception:
            current_count = 0

        print(f"   Попытка {attempt}: загружено {current_count} монет")

        if current_count >= target_count:
            print(f"✅ Достигнуто {current_count} монет (цель {target_count})")
            break

        if previous_count == current_count and attempt > 1:
            print(f"⚠️ Количество не увеличилось (остановились на {current_count})")
            break

        try:
            last_row = page.locator(f"{row_selector}:last-child")
            if not last_row.count():
                last_row = page.locator(f"{fallback_selector}:last-child")
            last_row.scroll_into_view_if_needed()
            time.sleep(2)
        except Exception:
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(2)

        previous_count = current_count

    try:
        rows = page.locator(row_selector).all()
        if not rows:
            rows = page.locator(fallback_selector).all()
        final_count = len(rows)
    except Exception:
        final_count = 0

    print(f"📊 Итоговое количество строк после прокрутки: {final_count}")
    return final_count


def get_table_rows(page):
    """Получение всех строк таблицы с несколькими стратегиями"""
    print("📊 Получение строк таблицы...")

    rows = []
    for selector in ROW_SELECTORS:
        try:
            temp_rows = page.locator(selector).all()
            if temp_rows:
                rows = temp_rows
                print(f"   ✅ Найдено {len(rows)} строк по селектору: {selector}")
                break
        except Exception:
            continue

    if not rows:
        print("   ❌ Строки не найдены!")
        return []

    # Фильтрация: убираем заголовки и пустые строки
    valid_rows = []
    for row in rows:
        try:
            cells = row.locator("td").all()
            if len(cells) >= 3:
                first_cell_text = cells[0].inner_text().strip() if cells else ''
                if first_cell_text and not first_cell_text.lower().startswith(
                    ('инструмент', 'символ', 'название')
                ):
                    valid_rows.append(row)
        except Exception:
            continue

    if valid_rows:
        rows = valid_rows
        print(f"   ✅ После фильтрации осталось {len(rows)} строк с данными")

    return rows


def parse_cell_text(cell):
    """Извлечение текста из ячейки с очисткой"""
    try:
        text = cell.inner_text().strip()
        return ' '.join(text.split())
    except Exception:
        return ''


def get_cells_from_row(row):
    """Получение всех ячеек из строки"""
    cells = row.locator("td").all()
    return [parse_cell_text(cell) for cell in cells]


def extract_instrument(cell_texts):
    """Извлечение названия инструмента из ячейки"""
    if not cell_texts:
        return ''
    parts = cell_texts[0].split()
    if len(parts) >= 2:
        return parts[0]
    return cell_texts[0]


def parse_coin_data(cell_texts):
    """
    Парсинг данных одной монеты из ячеек таблицы.
    Порядок столбцов:
        0 - Инструмент, 1 - Рейтинг, 2 - Цена, 3 - Изм. %24ч,
        4 - Рын. кап., 5 - Объём USD 24ч, 6 - Циркул. предложение,
        7 - Объём / Рын. капитализ., 8 - Доминация в соцсетях %,
        9 - Категория, 10 - Тех. рейтинг
    """
    instrument = extract_instrument(cell_texts)

    def get(i):
        return cell_texts[i] if len(cell_texts) > i else ''

    return {
        'Инструмент': instrument,
        'Рейтинг': get(1),
        'Цена': get(2),
        'Изм. %24ч': get(3),
        'Рын. кап.': get(4),
        'Объём USD 24ч': get(5),
        'Циркул. предложение': get(6),
        'Объём / Рын. капитализ.': get(7),
        'Доминация в соцсетях %': get(8),
        'Категория': get(9),
        'Тех. рейтинг': get(10),
    }


def process_rows(rows, max_coins):
    """Обработка строк таблицы и извлечение данных"""
    print(f"📝 Начинаем сбор данных о {max_coins} монетах...")

    crypto_data = []
    for index, row in enumerate(rows[:max_coins], 1):
        try:
            cell_texts = get_cells_from_row(row)
            if len(cell_texts) >= 3:
                crypto_data.append(parse_coin_data(cell_texts))
                if index % 10 == 0:
                    print(f"   Обработано {index} монет...")
        except Exception as e:
            print(f"⚠️ Ошибка в строке {index}: {e}")
            continue

    print(f"✅ Собрано {len(crypto_data)} криптовалют")
    return crypto_data


def collect_crypto_data(page, max_coins=CONFIG['max_coins']):
    """Полный цикл: прокрутка -> получение строк -> парсинг"""
    scroll_to_load_all_rows(page, target_count=max_coins)

    rows = get_table_rows(page)

    # Если строк всё ещё меньше — дополнительная прокрутка
    if len(rows) < max_coins:
        print("   🔄 Повторная прокрутка...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        rows = get_table_rows(page)

    return process_rows(rows, max_coins)