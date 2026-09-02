# Используем официальный готовый образ от создателей Playwright
FROM ://microsoft.com

# Создаем рабочую папку в контейнере
WORKDIR /app

# Копируем список библиотек и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код бота и скринера в контейнер
COPY . .

# Открываем порт для нашего веб-сервера
EXPOSE 8080

# Запускаем нашего бота
CMD ["python", "bot.py"]
