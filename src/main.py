# src/main.py
"""Главный модуль парсера TradingView Crypto Screener."""

from config import CONFIG
from browser import open_page, close_browser
from parser import collect_crypto_data
from saver import save_to_csv, display_results
from organizer import organize_csv_files
from update_readme import update_readme


def run() -> int:
    print("=" * 60)
    print("🔍 ПАРСЕР CRYPTO SCREENER")
    print("=" * 60)
    print(f"🎯 Цель: собрать данные о {CONFIG['max_coins']} криптовалютах")
    print(f"🌐 Источник: {CONFIG['url']}")
    print("=" * 60 + "\n")

    playwright = browser = page = crypto_data = None

    # -------------------------------------------------------------
    # 1. Парсинг
    # -------------------------------------------------------------
    try:
        playwright, browser, page = open_page()
        crypto_data = collect_crypto_data(page, CONFIG['max_coins'])
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        if page:
            try:
                page.screenshot(path="error_screenshot.png")
                print("📸 Скриншот ошибки: error_screenshot.png")
            except Exception:
                pass
    finally:
        if playwright and browser:
            close_browser(playwright, browser)

    if not crypto_data:
        print("❌ Не удалось собрать данные")
        return 1

    # -------------------------------------------------------------
    # 2. Сохранение CSV (в корень с timestamp)
    # -------------------------------------------------------------
    saved_path = save_to_csv(crypto_data)
    if not saved_path:
        print("❌ Ошибка при сохранении файла")
        return 1

    # -------------------------------------------------------------
    # 3. Сортировка: свежий → latest.csv, остальные → history/
    # -------------------------------------------------------------
    organize_csv_files()

    # -------------------------------------------------------------
    # 4. Пересборка README.md на основе latest.csv
    # -------------------------------------------------------------
    update_readme()

    # -------------------------------------------------------------
    # 5. Вывод результатов в консоль
    # -------------------------------------------------------------
    display_results(crypto_data)

    print("\n" + "=" * 60)
    print("✅ ПАРСИНГ ЗАВЕРШЁН УСПЕШНО!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(run())