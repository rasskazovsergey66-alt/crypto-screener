# Crypto Screener Parser

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![TradingView](https://img.shields.io/badge/Source-TradingView-1E88E5?style=for-the-badge&logo=tradingview&logoColor=white)](https://ru.tradingview.com/crypto-coins-screener/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)

> 🚀 Автоматический парсер криптовалют с **TradingView Crypto Screener**.
> Собирает данные о **135 монетах** и сохраняет в CSV с разделителем `;` (для Excel).

---

## 📊 Актуальные данные

| 📅 Последнее обновление | 💰 Монет в файле | 💾 Размер | 🕓 История |
|---|---|---|---|
| **19.11.2026 05:39 UTC** | **135** | **26.1 КБ** | **251** снапшотов |

**⭐ Свежий срез:** [`crypto_screener_20261119_053915.csv`](./crypto_screener_20261119_053915.csv)  
**🕓 Архив:** [`history/`](./history/) — все предыдущие генерации

---

## 🏆 Топ-10 монет по рейтингу

| # | 🪙 Монета | 💰 Цена | 📈 Изм. 24ч | 🏦 Рын. кап. | 📊 Объём 24ч |
|:---:|:---|:---:|:---:|:---:|:---:|
| **1** | **BTC** | `63 328,88 USD` | −2,11% | 1,27 T USD | 13,83 B USD |
| **2** | **ETH** | `1 797,31 USD` | −0,92% | 219,69 B USD | 4,91 B USD |
| **3** | **USDT** | `0,99892 USD` | 🟢 +0,01% | 175,25 B USD | 23,73 B USD |
| **4** | **BNB** | `586,13 USD` | −1,07% | 77,08 B USD | 222,28 M USD |
| **5** | **USDC** | `0,99955 USD` | −0,03% | 68,9 B USD | 5,29 B USD |
| **6** | **XRP** | `0,97250 USD` | −1,41% | 61,77 B USD | 1,01 B USD |
| **7** | **SOL** | `74,472 USD` | −0,92% | 44,07 B USD | 1,06 B USD |
| **8** | **TRX** | `0,31153 USD` | 🟢 +1,23% | 29,61 B USD | 116,21 M USD |
| **9** | **HYPE** | `67,825 USD` | −1,67% | 17,13 B USD | 252,32 M USD |
| **10** | **ZEC** | `934,90 USD` | −2,95% | 15,87 B USD | 464,91 M USD |

---

## 🚀 Запуск парсера вручную

[![Запустить вручную](https://img.shields.io/badge/Запустить_вручную-2ea44f?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/rasskazovsergey66-alt/crypto-screener/actions/workflows/scrape-crypto.yml)

**Пошаговая инструкция:**

1. **Перейдите на страницу запуска** — нажмите на зелёную кнопку «Запустить вручную» выше (система попросит войти в аккаунт GitHub, если вы ещё не авторизованы).
2. **Активируйте процесс** — в открывшемся окне в правой части экрана нажмите **Run workflow**, затем во всплывающем меню ещё раз нажмите финальную зелёную кнопку **Run workflow**.
3. **Дождитесь окончания** — процесс сбора занимает **1–2 минуты**. Индикатор будет гореть 🟡 жёлтым, а после успешного завершения сменится на 🟢 зелёную галочку.

> 💡 *Результат:* парсер автоматически загрузит данные по **135 монетам** с TradingView и создаст новый CSV в корне репозитория.

---

## 💻 Локальный запуск

```bash
# 1. Установка зависимостей
pip install -r requirements.txt
playwright install chromium

# 2. Парсинг + сохранение + сортировка CSV + обновление README
python src/main.py

# 3. Только сортировка CSV (свежий остаётся, остальные → history/)
python src/organizer.py

# 4. Пересборка README.md на основе свежего CSV
python src/update_readme.py
```

---

## 📂 Структура репозитория

```
.
├── crypto_screener_ГГГГММДД_ЧЧММСС.csv  # ⭐ свежий срез (только он в корне)
├── history/                             # 🕓 архив предыдущих генераций
├── README.md                            # 📖 этот файл (генерируется)
├── requirements.txt
├── LICENSE
├── .github/
│   └── workflows/
│       └── scrape-crypto.yml
└── src/                                 # 🧩 исходный код
    ├── config.py
    ├── browser.py
    ├── parser.py
    ├── saver.py
    ├── organizer.py
    ├── update_readme.py
    └── main.py
```

---

## 📋 Поля CSV

| Поле | Описание |
|---|---|
| 🔨 `Инструмент` | Тикер монеты (BTC, ETH, …) |
| 🏆 `Рейтинг` | Позиция в рейтинге |
| 💰 `Цена` | Текущая цена |
| 📈 `Изм. %24ч` | Изменение за 24 часа |
| 🏦 `Рын. кап.` | Рыночная капитализация |
| 📊 `Объём USD 24ч` | Объём торгов за 24 часа |
| 🔄 `Циркул. предложение` | Циркулирующее предложение |
| ⚖️ `Объём / Рын. капитализ.` | Отношение объёма к капитализации |
| 💬 `Доминация в соцсетях %` | Социальная доминация |
| 🗂️ `Категория` | Категория монеты |
| ⚙️ `Тех. рейтинг` | Технический рейтинг |

---

<div align="center">

**Crypto Screener Parser**

Данные получены с [TradingView](https://ru.tradingview.com/crypto-coins-screener/) в ознакомительных целях.

⭐ Поставьте звезду, если проект оказался полезен!

</div>
