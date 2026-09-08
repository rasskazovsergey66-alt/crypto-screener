import time
import csv
from datetime import datetime
from playwright.sync_api import sync_playwright

# ============================================
# КОНФИГУРАЦИЯ
# ============================================
CONFIG = {
    'url': 'https://ru.tradingview.com/crypto-coins-screener/',
    'max_coins': 135,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'viewport_width': 1920,
    'viewport_height': 1080,
    'timeout': 60000,
    'wait_after_load': 5
}

# ============================================
# ФУНКЦИИ РАБОТЫ С БРАУЗЕРОМ
# ============================================

def create_browser():
    """Создание экземпляра браузера"""
    print("🌐 Создание браузера...")
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    return playwright, browser

def create_context(browser):
    """Создание контекста браузера"""
    print("📋 Создание контекста браузера...")
    context = browser.new_context(
        user_agent=CONFIG['user_agent'],
        viewport={
            "width": CONFIG['viewport_width'],
            "height": CONFIG['viewport_height']
        }
    )
    return context

def create_page(context):
    """Создание новой страницы"""
    print("📄 Создание страницы...")
    return context.new_page()

def navigate_to_url(page):
    """Переход на целевой URL"""
    print(f"🔗 Переход на сайт: {CONFIG['url']}")
    page.goto(CONFIG['url'], wait_until="domcontentloaded", timeout=CONFIG['timeout'])
    print("✅ Страница загружена")

def wait_for_table(page):
    """Ожидание загрузки таблицы"""
    print("⏳ Ожидание загрузки таблицы...")
    table_selector = "table tbody tr"
    page.locator(table_selector).first.wait_for(state="visible", timeout=30000)
    print("✅ Таблица загружена")

def wait_for_data_load():
    """Дополнительное ожидание загрузки данных"""
    print(f"⏳ Ожидание {CONFIG['wait_after_load']} секунд для загрузки данных...")
    time.sleep(CONFIG['wait_after_load'])
    print("✅ Данные загружены")

def close_browser(playwright, browser):
    """Закрытие браузера"""
    print("🔒 Закрытие браузера...")
    browser.close()
    playwright.stop()
    print("✅ Браузер закрыт")

# ============================================
# ФУНКЦИЯ ПРОКРУТКИ ДЛЯ ПОДГРУЗКИ ВСЕХ МОНЕТ
# ============================================

def scroll_to_load_all_rows(page, target_count=135, max_attempts=20):
    """
    Прокручивает страницу до тех пор, пока не будет загружено target_count строк
    или пока количество строк не перестанет увеличиваться.
    """
    print(f"🔄 Начинаем прокрутку для загрузки {target_count} монет...")
    
    previous_count = 0
    current_count = 0
    
    # Селектор для строк с данными (используем точный из вашего HTML)
    row_selector = "tbody[data-testid='selectable-rows-table-body'] tr"
    fallback_selector = "tr[class*='row-']"
    
    for attempt in range(1, max_attempts + 1):
        try:
            rows = page.locator(row_selector).all()
            if not rows:
                rows = page.locator(fallback_selector).all()
            current_count = len(rows)
        except:
            current_count = 0
        
        print(f"   Попытка {attempt}: загружено {current_count} монет")
        
        if current_count >= target_count:
            print(f"✅ Достигнуто {current_count} монет (цель {target_count})")
            break
        
        if previous_count == current_count and attempt > 1:
            print(f"⚠️ Количество не увеличилось (остановились на {current_count})")
            break
        
        # Прокручиваем к последней строке
        try:
            last_row = page.locator(f"{row_selector}:last-child")
            if not last_row.count():
                last_row = page.locator(f"{fallback_selector}:last-child")
            last_row.scroll_into_view_if_needed()
            time.sleep(2)
        except:
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(2)
        
        previous_count = current_count
    
    try:
        rows = page.locator(row_selector).all()
        if not rows:
            rows = page.locator(fallback_selector).all()
        final_count = len(rows)
    except:
        final_count = 0
    
    print(f"📊 Итоговое количество строк после прокрутки: {final_count}")
    return final_count

# ============================================
# ФУНКЦИИ ПАРСИНГА
# ============================================

def get_table_rows(page):
    """Получение всех строк таблицы с несколькими стратегиями"""
    print("📊 Получение строк таблицы...")
    
    selectors = [
        "tbody[data-testid='selectable-rows-table-body'] tr",
        "tr[class*='row-']",
        "table tbody tr",
        "tbody tr"
    ]
    
    rows = []
    for selector in selectors:
        try:
            temp_rows = page.locator(selector).all()
            if temp_rows and len(temp_rows) > 0:
                rows = temp_rows
                print(f"   ✅ Найдено {len(rows)} строк по селектору: {selector}")
                break
        except:
            continue
    
    if not rows:
        print("   ❌ Строки не найдены!")
        return []
    
    # Фильтрация: удаляем заголовки и пустые строки
    valid_rows = []
    for row in rows:
        try:
            cells = row.locator("td").all()
            if len(cells) >= 3:
                first_cell_text = cells[0].inner_text().strip() if len(cells) > 0 else ''
                if first_cell_text and not first_cell_text.lower().startswith(('инструмент', 'символ', 'название')):
                    valid_rows.append(row)
        except:
            continue
    
    if valid_rows:
        rows = valid_rows
        print(f"   ✅ После фильтрации осталось {len(rows)} строк с данными")
    
    return rows

def parse_cell_text(cell):
    """Извлечение текста из ячейки с очисткой"""
    try:
        text = cell.inner_text().strip()
        text = ' '.join(text.split())
        return text
    except:
        return ''

def get_cells_from_row(row):
    """Получение всех ячеек из строки"""
    cells = row.locator("td").all()
    return [parse_cell_text(cell) for cell in cells]

def extract_instrument(cell_texts):
    """Извлечение названия инструмента из ячейки"""
    if not cell_texts:
        return ''
    instrument_parts = cell_texts[0].split()
    if len(instrument_parts) >= 2:
        return instrument_parts[0]
    return cell_texts[0]

def parse_coin_data(cell_texts):
    """
    Парсинг данных одной монеты из ячеек таблицы.
    Предполагаемый порядок столбцов (на основе HTML):
        0 - Инструмент (символ + название)
        1 - Рейтинг
        2 - Цена
        3 - Изм. %24ч
        4 - Рын. кап.
        5 - Объём USD 24ч
        6 - Циркул. предложение
        7 - Объём / Рын. капитализ.
        8 - Доминация в соцсетях %
        9 - Категория
        10 - Тех. рейтинг
    """
    # Извлекаем символ инструмента (например, "BTC" из "BTC Bitcoin")
    instrument = extract_instrument(cell_texts)
    
    # Берём данные по индексам
    rating = cell_texts[1] if len(cell_texts) > 1 else ''
    price = cell_texts[2] if len(cell_texts) > 2 else ''
    change_24h = cell_texts[3] if len(cell_texts) > 3 else ''
    market_cap = cell_texts[4] if len(cell_texts) > 4 else ''
    volume = cell_texts[5] if len(cell_texts) > 5 else ''
    supply = cell_texts[6] if len(cell_texts) > 6 else ''
    volume_mcap_ratio = cell_texts[7] if len(cell_texts) > 7 else ''
    social_dominance = cell_texts[8] if len(cell_texts) > 8 else ''
    category = cell_texts[9] if len(cell_texts) > 9 else ''
    tech_rating = cell_texts[10] if len(cell_texts) > 10 else ''
    
    return {
        'Инструмент': instrument,
        'Рейтинг': rating,
        'Цена': price,
        'Изм. %24ч': change_24h,
        'Рын. кап.': market_cap,
        'Объём USD 24ч': volume,
        'Циркул. предложение': supply,
        'Объём / Рын. капитализ.': volume_mcap_ratio,
        'Доминация в соцсетях %': social_dominance,
        'Категория': category,
        'Тех. рейтинг': tech_rating
    }

def process_rows(rows, max_coins):
    """Обработка строк таблицы"""
    print(f"📝 Начинаем сбор данных о {max_coins} монетах...")
    
    crypto_data = []
    rows_to_process = rows[:max_coins]
    
    for index, row in enumerate(rows_to_process, 1):
        try:
            cell_texts = get_cells_from_row(row)
            if len(cell_texts) >= 3:   # минимум 3 ячейки
                coin_data = parse_coin_data(cell_texts)   # больше не передаём index
                crypto_data.append(coin_data)
                if index % 10 == 0:
                    print(f"   Обработано {index} монет...")
        except Exception as e:
            print(f"⚠️ Ошибка в строке {index}: {e}")
            continue
    
    print(f"✅ Собрано {len(crypto_data)} криптовалют")
    return crypto_data

# ============================================
# ФУНКЦИИ СОХРАНЕНИЯ
# ============================================

def get_csv_filename():
    """Генерация имени файла CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"crypto_screener_{timestamp}.csv"

def save_to_csv(data, filename):
    """Сохранение данных в CSV с разделителем ; для корректного открытия в Excel"""
    if not data:
        print("❌ Нет данных для сохранения")
        return False
    
    fieldnames = [
        'Инструмент',
        'Рейтинг',
        'Цена',
        'Изм. %24ч',
        'Рын. кап.',
        'Объём USD 24ч',
        'Циркул. предложение',
        'Объём / Рын. капитализ.',
        'Доминация в соцсетях %',
        'Категория',
        'Тех. рейтинг'
    ]
    
    try:
        # Используем разделитель ; и кодировку utf-8-sig (BOM для Excel)
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=fieldnames, 
                delimiter=';',          # <--- точка с запятой
                quoting=csv.QUOTE_MINIMAL,
                lineterminator='\n'
            )
            writer.writeheader()
            writer.writerows(data)
        print(f"💾 Данные сохранены в: {filename}")
        print(f"📊 Всего записей: {len(data)}")
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return False

# ============================================
# ОСНОВНАЯ ФУНКЦИЯ ПАРСИНГА
# ============================================

def scrape_tradingview():
    """Основная функция парсинга"""
    print("🚀 ЗАПУСК ПАРСЕРА")
    print("="*60)
    
    playwright = None
    browser = None
    
    try:
        playwright, browser = create_browser()
        context = create_context(browser)
        page = create_page(context)
        navigate_to_url(page)
        wait_for_table(page)
        wait_for_data_load()
        
        # --- ВАЖНО: ПРОКРУТКА ДЛЯ ЗАГРУЗКИ ВСЕХ 135 МОНЕТ ---
        loaded_count = scroll_to_load_all_rows(page, target_count=CONFIG['max_coins'])
        # --------------------------------------------------
        
        # Получаем строки после прокрутки
        rows = get_table_rows(page)
        
        # Если строк всё равно меньше, дополнительная прокрутка
        if len(rows) < CONFIG['max_coins']:
            print("   🔄 Повторная прокрутка...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            rows = get_table_rows(page)
        
        crypto_data = process_rows(rows, CONFIG['max_coins'])
        close_browser(playwright, browser)
        return crypto_data
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        if browser:
            try:
                page.screenshot(path="error_screenshot.png")
                print("📸 Сохранен скриншот ошибки: error_screenshot.png")
            except:
                pass
        return None

# ============================================
# ФУНКЦИЯ ВЫВОДА РЕЗУЛЬТАТОВ
# ============================================

def display_results(data):
    """Отображение результатов парсинга"""
    if not data:
        print("❌ Нет данных для отображения")
        return
    
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТЫ ПАРСИНГА")
    print("="*60)
    
    total = len(data)
    expected = CONFIG['max_coins']
    if total == expected:
        print(f"✅ Получены данные о всех {expected} монетах!")
    else:
        print(f"⚠️ Получено {total} из {expected} монет")
    
    print("\n📋 ПЕРВЫЕ 5 ЗАПИСЕЙ:")
    print("-"*80)
    print(f"{'Рейтинг':<8} {'Инструмент':<12} {'Цена':<18} {'Изм. %24ч':<12}")
    print("-"*80)
    for coin in data[:5]:
        print(f"{coin['Рейтинг']:<8} {coin['Инструмент']:<12} {coin['Цена']:<18} {coin['Изм. %24ч']:<12}")
    print("-"*80)

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    """Главная функция программы"""
    print("="*60)
    print("🔍 ПАРСЕР CRYPTO SCREENER")
    print("="*60)
    print(f"🎯 Цель: собрать данные о {CONFIG['max_coins']} криптовалютах")
    print(f"🌐 Источник: {CONFIG['url']}")
    print("="*60 + "\n")
    
    crypto_data = scrape_tradingview()
    
    if crypto_data:
        filename = get_csv_filename()
        if save_to_csv(crypto_data, filename):
            display_results(crypto_data)
            print("\n" + "="*60)
            print("✅ ПАРСИНГ ЗАВЕРШЕН УСПЕШНО!")
            print(f"📁 Файл сохранен: {filename}")
            print("="*60)
        else:
            print("❌ Ошибка при сохранении файла")
            exit(1)
    else:
        print("❌ Не удалось собрать данные")
        exit(1)

if __name__ == "__main__":
    main()