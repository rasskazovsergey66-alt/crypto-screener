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
| **31.10.2026 06:33 UTC** | **135** | **26.0 КБ** | **182** снапшотов |

**⭐ Свежий срез:** [`crypto_screener_20261031_063345.csv`](./crypto_screener_20261031_063345.csv)  
**🕓 Архив:** [`history/`](./history/) — все предыдущие генерации

---

## 🏆 Топ-10 монет по рейтингу

| # | 🪙 Монета | 💰 Цена | 📈 Изм. 24ч | 🏦 Рын. кап. | 📊 Объём 24ч |
|:---:|:---|:---:|:---:|:---:|:---:|
| **1** | **BTC** | `77 159,34 USD` | −1,59% | 1,55 T USD | 35,56 B USD |
| **2** | **ETH** | `2 240,58 USD` | −0,19% | 273,75 B USD | 15,1 B USD |
| **3** | **USDT** | `0,99891 USD` | 🟢 +0,08% | 179,93 B USD | 75,41 B USD |
| **4** | **BNB** | `702,11 USD` | −1,76% | 92,34 B USD | 2,22 B USD |
| **5** | **XRP** | `1,2452 USD` | −1,57% | 78,88 B USD | 2,92 B USD |
| **6** | **USDC** | `0,99982 USD` | 🟢 +0,06% | 71,79 B USD | 14,05 B USD |
| **7** | **SOL** | `95,806 USD` | −2,27% | 56,53 B USD | 3,57 B USD |
| **8** | **TRX** | `0,32430 USD` | −3,90% | 30,82 B USD | 1,59 B USD |
| **9** | **HYPE** | `88,117 USD` | −5,82% | 22,34 B USD | 1,63 B USD |
| **10** | **ZEC** | `1 264,24 USD` | −0,56% | 21,42 B USD | 966,9 M USD |

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
