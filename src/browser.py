# browser.py
"""Модуль работы с браузером: создание, переход на сайт, закрытие"""

import time
from playwright.sync_api import sync_playwright

from config import CONFIG, TABLE_SELECTOR


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
            "height": CONFIG['viewport_height'],
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
    page.locator(TABLE_SELECTOR).first.wait_for(state="visible", timeout=30000)
    print("✅ Таблица загружена")


def wait_for_data_load():
    """Дополнительное ожидание загрузки данных"""
    print(f"⏳ Ожидание {CONFIG['wait_after_load']} секунд для загрузки данных...")
    time.sleep(CONFIG['wait_after_load'])
    print("✅ Данные загружены")


def close_browser(playwright, browser):
    """Закрытие браузера"""
    print("🔒 Закрытие браузера...")
    try:
        browser.close()
    finally:
        playwright.stop()
    print("✅ Браузер закрыт")


def open_page():
    """
    Удобная обёртка: создаёт браузер, контекст, страницу и
    переходит на сайт. Возвращает (playwright, browser, page).
    """
    playwright, browser = create_browser()
    context = create_context(browser)
    page = create_page(context)
    navigate_to_url(page)
    wait_for_table(page)
    wait_for_data_load()
    return playwright, browser, page