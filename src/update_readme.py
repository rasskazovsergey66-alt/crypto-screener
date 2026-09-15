# src/update_readme.py
"""Генератор README.md на основе самого свежего CSV в корне."""

import csv
import re
from datetime import datetime, timezone
from pathlib import Path

# src/update_readme.py → src → корень проекта
BASE_DIR    = Path(__file__).resolve().parent.parent
HISTORY_DIR = BASE_DIR / "history"
README      = BASE_DIR / "README.md"

REPO_OWNER    = "rasskazovsergey66-alt"
REPO_NAME     = "crypto-screener"
REPO_URL      = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
WORKFLOW_FILE = "scrape-crypto.yml"
ACTIONS_URL   = f"{REPO_URL}/actions/workflows/{WORKFLOW_FILE}"

TIMESTAMP_RE = re.compile(r'(\d{8}_\d{6})')


# -----------------------------------------------------------------
# Поиск свежего CSV в корне
# -----------------------------------------------------------------
def find_latest_csv() -> Path | None:
    """Самый свежий *.csv в корне проекта."""
    csvs = [p for p in BASE_DIR.glob("*.csv") if p.is_file()]
    if not csvs:
        return None

    def key(p: Path) -> str:
        m = TIMESTAMP_RE.search(p.stem)
        if m:
            return m.group(1)
        return f"{p.stat().st_mtime:020.6f}"

    csvs.sort(key=key)
    return csvs[-1]


# -----------------------------------------------------------------
# Утилиты
# -----------------------------------------------------------------
def read_csv(path: Path) -> list[dict]:
    if not path or not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f, delimiter=";"))
    except Exception as e:
        print(f"⚠️  Не удалось прочитать {path.name}: {e}")
        return []


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"


def human_time(ts: float) -> str:
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%d.%m.%Y %H:%M UTC")


def count_history() -> int:
    if not HISTORY_DIR.exists():
        return 0
    return sum(1 for _ in HISTORY_DIR.glob("*.csv"))


# -----------------------------------------------------------------
# Блоки README
# -----------------------------------------------------------------
def build_header() -> str:
    return (
        "# Crypto Screener Parser\n\n"
        "[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)\n"
        "[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)\n"
        "[![TradingView](https://img.shields.io/badge/Source-TradingView-1E88E5?style=for-the-badge&logo=tradingview&logoColor=white)](https://ru.tradingview.com/crypto-coins-screener/)\n"
        "[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)\n\n"
        "> 🚀 Автоматический парсер криптовалют с **TradingView Crypto Screener**.\n"
        "> Собирает данные о **135 монетах** и сохраняет в CSV с разделителем `;` (для Excel).\n\n"
        "---\n"
    )


def build_latest_block(rows: list[dict], csv_path: Path | None) -> str:
    if not rows or not csv_path:
        return (
            "## 📊 Актуальные данные\n\n"
            "> ⚠️ CSV-файл ещё не сгенерирован. Запустите парсер.\n\n"
            "---\n"
        )

    size = human_size(csv_path.stat().st_size)
    mtime = human_time(csv_path.stat().st_mtime)
    count = len(rows)
    history_count = count_history()

    return (
        "## 📊 Актуальные данные\n\n"
        "| 📅 Последнее обновление | 💰 Монет в файле | 💾 Размер | 🕓 История |\n"
        "|---|---|---|---|\n"
        f"| **{mtime}** | **{count}** | **{size}** | **{history_count}** снапшотов |\n\n"
        f"**⭐ Свежий срез:** [`{csv_path.name}`](./{csv_path.name})  \n"
        "**🕓 Архив:** [`history/`](./history/) — все предыдущие генерации\n\n"
        "---\n"
    )


def build_top_table(rows: list[dict], limit: int = 10) -> str:
    if not rows:
        return ""

    def color_change(value: str) -> str:
        v = value.strip().replace(",", ".").replace("%", "").replace("\u00a0", "")
        try:
            num = float(v)
        except ValueError:
            return value
        if num > 0:
            return f"🟢 {value}"
        if num < 0:
            return f"🔴 {value}"
        return f"⚪ {value}"

    lines = [
        f"## 🏆 Топ-{limit} монет по рейтингу\n",
        "| # | 🪙 Монета | 💰 Цена | 📈 Изм. 24ч | 🏦 Рын. кап. | 📊 Объём 24ч |",
        "|:---:|:---|:---:|:---:|:---:|:---:|",
    ]
    for i, coin in enumerate(rows[:limit], 1):
        name   = coin.get("Инструмент", "—")
        price  = coin.get("Цена", "—")
        change = color_change(coin.get("Изм. %24ч", "—"))
        mcap   = coin.get("Рын. кап.", "—")
        vol    = coin.get("Объём USD 24ч", "—")
        lines.append(f"| **{i}** | **{name}** | `{price}` | {change} | {mcap} | {vol} |")
    lines.append("\n---\n")
    return "\n".join(lines)


def build_run_block() -> str:
    return (
        "## 🚀 Запуск парсера вручную\n\n"
        f"[![Запустить вручную](https://img.shields.io/badge/Запустить_вручную-2ea44f?style=for-the-badge&logo=githubactions&logoColor=white)]({ACTIONS_URL})\n\n"
        "**Пошаговая инструкция:**\n\n"
        "1. **Перейдите на страницу запуска** — нажмите на зелёную кнопку «Запустить вручную» выше "
        "(система попросит войти в аккаунт GitHub, если вы ещё не авторизованы).\n"
        "2. **Активируйте процесс** — в открывшемся окне в правой части экрана нажмите "
        "**Run workflow**, затем во всплывающем меню ещё раз нажмите финальную зелёную кнопку **Run workflow**.\n"
        "3. **Дождитесь окончания** — процесс сбора занимает **1–2 минуты**. "
        "Индикатор будет гореть 🟡 жёлтым, а после успешного завершения сменится на 🟢 зелёную галочку.\n\n"
        "> 💡 *Результат:* парсер автоматически загрузит данные по **135 монетам** "
        "с TradingView и создаст новый CSV в корне репозитория.\n\n"
        "---\n"
    )


def build_local_run_block() -> str:
    return (
        "## 💻 Локальный запуск\n\n"
        "```bash\n"
        "# 1. Установка зависимостей\n"
        "pip install -r requirements.txt\n"
        "playwright install chromium\n\n"
        "# 2. Парсинг + сохранение + сортировка CSV + обновление README\n"
        "python src/main.py\n\n"
        "# 3. Только сортировка CSV (свежий остаётся, остальные → history/)\n"
        "python src/organizer.py\n\n"
        "# 4. Пересборка README.md на основе свежего CSV\n"
        "python src/update_readme.py\n"
        "```\n\n"
        "---\n"
    )


def build_structure_block() -> str:
    return (
        "## 📂 Структура репозитория\n\n"
        "```\n"
        ".\n"
        "├── crypto_screener_ГГГГММДД_ЧЧММСС.csv  # ⭐ свежий срез (только он в корне)\n"
        "├── history/                             # 🕓 архив предыдущих генераций\n"
        "├── README.md                            # 📖 этот файл (генерируется)\n"
        "├── requirements.txt\n"
        "├── LICENSE\n"
        "├── .github/\n"
        "│   └── workflows/\n"
        "│       └── scrape-crypto.yml\n"
        "└── src/                                 # 🧩 исходный код\n"
        "    ├── config.py\n"
        "    ├── browser.py\n"
        "    ├── parser.py\n"
        "    ├── saver.py\n"
        "    ├── organizer.py\n"
        "    ├── update_readme.py\n"
        "    └── main.py\n"
        "```\n\n"
        "---\n"
    )


def build_fields_block() -> str:
    return (
        "## 📋 Поля CSV\n\n"
        "| Поле | Описание |\n"
        "|---|---|\n"
        "| 🔨 `Инструмент` | Тикер монеты (BTC, ETH, …) |\n"
        "| 🏆 `Рейтинг` | Позиция в рейтинге |\n"
        "| 💰 `Цена` | Текущая цена |\n"
        "| 📈 `Изм. %24ч` | Изменение за 24 часа |\n"
        "| 🏦 `Рын. кап.` | Рыночная капитализация |\n"
        "| 📊 `Объём USD 24ч` | Объём торгов за 24 часа |\n"
        "| 🔄 `Циркул. предложение` | Циркулирующее предложение |\n"
        "| ⚖️ `Объём / Рын. капитализ.` | Отношение объёма к капитализации |\n"
        "| 💬 `Доминация в соцсетях %` | Социальная доминация |\n"
        "| 🗂️ `Категория` | Категория монеты |\n"
        "| ⚙️ `Тех. рейтинг` | Технический рейтинг |\n\n"
        "---\n"
    )


def build_footer() -> str:
    return (
        "<div align=\"center\">\n\n"
        "**Crypto Screener Parser**\n\n"
        "Данные получены с [TradingView](https://ru.tradingview.com/crypto-coins-screener/) "
        "в ознакомительных целях.\n\n"
        "⭐ Поставьте звезду, если проект оказался полезен!\n\n"
        "</div>\n"
    )


# -----------------------------------------------------------------
# Сборка
# -----------------------------------------------------------------
def build_readme() -> str:
    csv_path = find_latest_csv()
    rows = read_csv(csv_path) if csv_path else []
    parts = [
        build_header(),
        build_latest_block(rows, csv_path),
        build_top_table(rows, limit=10),
        build_run_block(),
        build_local_run_block(),
        build_structure_block(),
        build_fields_block(),
        build_footer(),
    ]
    return "\n".join(p for p in parts if p.strip())


def update_readme() -> bool:
    content = build_readme()
    try:
        README.write_text(content, encoding="utf-8")
        print(f"✅ README.md обновлён ({len(content)} символов)")
        return True
    except Exception as e:
        print(f"❌ Ошибка записи README.md: {e}")
        return False


if __name__ == "__main__":
    update_readme()