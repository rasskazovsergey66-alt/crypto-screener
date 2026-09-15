# src/config.py
"""Конфигурация парсера."""

from pathlib import Path

# src/config.py → src → корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_DIR = BASE_DIR / "history"

CONFIG = {
    'url': 'https://ru.tradingview.com/crypto-coins-screener/',
    'max_coins': 135,
    'user_agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'viewport_width': 1920,
    'viewport_height': 1080,
    'timeout': 60000,
    'wait_after_load': 5,
}

ROW_SELECTORS = [
    "tbody[data-testid='selectable-rows-table-body'] tr",
    "tr[class*='row-']",
    "table tbody tr",
    "tbody tr",
]

TABLE_SELECTOR = "table tbody tr"

CSV_FIELDS = [
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
    'Тех. рейтинг',
]