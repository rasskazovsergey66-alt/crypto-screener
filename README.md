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
| **16.09.2026 16:13 UTC** | **135** | **26.0 КБ** | **6** снапшотов |

**⭐ Свежий срез:** [`crypto_screener_20260916_161313.csv`](./crypto_screener_20260916_161313.csv)  
**🕓 Архив:** [`history/`](./history/) — все предыдущие генерации

---

## 🏆 Топ-10 монет по рейтингу

| # | 🪙 Монета | 💰 Цена | 📈 Изм. 24ч | 🏦 Рын. кап. | 📊 Объём 24ч |
|:---:|:---|:---:|:---:|:---:|:---:|
| **1** | **BTC** | `75 716,61 USD` | −0,72% | 1,52 T USD | 37,61 B USD |
| **2** | **ETH** | `2 393,40 USD` | −0,81% | 292,12 B USD | 19,58 B USD |
| **3** | **USDT** | `0,99929 USD` | −0,01% | 183,31 B USD | 79,7 B USD |
| **4** | **BNB** | `711,78 USD` | −0,61% | 94,78 B USD | 1,57 B USD |
| **5** | **XRP** | `1,2669 USD` | −8,35% | 79,66 B USD | 6,64 B USD |
| **6** | **USDC** | `0,9998 USD` | −0,05% | 73,68 B USD | 19,21 B USD |
| **7** | **SOL** | `97,205 USD` | −1,72% | 57,07 B USD | 3,76 B USD |
| **8** | **TRX** | `0,33595 USD` | 🟢 +0,19% | 31,9 B USD | 527,25 M USD |
| **9** | **ZEC** | `1 254,00 USD` | 🟢 +12,84% | 21,16 B USD | 1,39 B USD |
| **10** | **HYPE** | `78,833 USD` | 🟢 +2,47% | 19,84 B USD | 906,83 M USD |

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
