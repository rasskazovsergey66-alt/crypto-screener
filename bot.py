import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import subprocess  # Для запуска внешнего скрипта screener.py
from aiogram.types import FSInputFile  # Для отправки локальных файлов в Telegram

# ==========================================
# 1. НАСТРОЙКИ И ИНИЦИАЛИЗАЦИЯ
# ==========================================
API_TOKEN = '8651631806:AAFLclg2HiiAY7J_xHqAP9txWfR-b-VZ2Ts'
FILE_PATH = "settings.json"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ==========================================
# 2. МИНИ-МОДУЛЬ JSON (Хранение расписания)
# ==========================================
def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==========================================
# 3. СЛЭШ-КОМАНДЫ БОТА
# ==========================================

# /start - Показать список доступных команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    help_text = (
         "👋 **Привет! Я автоматический Крипто-Скринер 135 монет.**\n"
        "Я работаю без кнопок и управляюсь только быстрыми слэш-командами.\n\n"
        
        "📊 **Получение отчетов:**\n"
        "• `/report` — Сгенерировать и получить PDF-срез рынка прямо сейчас\n\n"
        
        "⏰ **Управление расписанием:**\n"
        "• `/set 14:30` — Добавить время для автоматического отчета\n"
        "• `/list` — Показать мое активное расписание и часовой пояс\n"
        "• `/del 14:30` — Удалить конкретное время из рассылки\n"
        "• `/clear` — Полностью стереть всё мое расписание\n\n"
        
        "⚙️ **Синхронизация времени (Важно!):**\n"
        "• `/time` — Проверить текущее системное время сервера\n"
        "• `/sync 15` — Синхронизировать бота с вашими часами (введите только ваш текущий час)\n\n"
        
        "🛡 _Умная автоматизация: если сервер уйдет на перезагрузку или упадет на 5-15 минут, "
        "бот автоматически нагонит упущенное время и пришлет пропущенный отчет сразу после включения._"
    )
    await message.answer(help_text, parse_mode="Markdown")


# /report - Мгновенный срез рынка
# /report - Запуск screener.py и отправка сгенерированного PDF
# /report - Бесшумный запуск и отправка PDF с последующим удалением
# /report - Исправленная версия с безопасным удалением
@dp.message(Command("report"))
async def cmd_report(message: types.Message):
    # Короткое и строгое сервисное сообщение
    status_msg = await message.answer("⏳ Формирую отчет... Пожалуйста, подождите.")
    
    try:
        # 1. Запускаем ваш скрипт генерации PDF
        subprocess.run([sys.executable, "screener.py"], check=True)
        
        # 2. Получаем текущую дату для поиска файла
        current_date_str = datetime.now().strftime("%d-%m-%Y")
        pdf_filename = f"tradingview.com-crypto-coins-screener-{current_date_str}.pdf"
        
        # 3. Если файл успешно создан — отправляем и стираем
        if os.path.exists(pdf_filename):
            # Сразу убираем текст загрузки из чата
            await status_msg.delete()
            
            # Отправляем только чистый файл без каких-либо подписей
            document = FSInputFile(path=pdf_filename, filename=pdf_filename)
            await message.answer_document(document=document)
            
            # ⏱ Даем Windows 2 секунды, чтобы Telegram гарантированно догрузил файл
            await asyncio.sleep(2)
            
            # 🔥 Безопасно удаляем файл, если он все еще существует на диске
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)
        else:
            await message.answer("❌ Ошибка: Файл отчета не найден.")
            
    except Exception as e:
        # В случае сбоя отправляем НОВОЕ сообщение, а не редактируем старое удаленное
        logging.error(f"Ошибка в cmd_report: {e}")
        await message.answer("❌ Не удалось сформировать или отправить отчет.")





# /set ЧЧ:ММ - Установка (добавление) времени отчета
@dp.message(Command("set"))
async def cmd_set(message: types.Message):
    time_input = message.text.replace("/set", "").strip()
    
    try:
        # Проверяем правильность ввода времени
        valid_time = datetime.strptime(time_input, "%H:%M").strftime("%H:%M")
    except ValueError:
        await message.answer("❌ Ошибка! Напишите время после команды, пример: `/set 18:45`")
        return

    uid = str(message.from_user.id)
    data = load_data()
    
    # Извлекаем данные пользователя или создаем новую структуру
    user_info = data.get(uid, {"times": [], "history": []})
    
    # Если данные были в старом формате (просто список), конвертируем их
    if isinstance(user_info, list):
        user_info = {"times": user_info, "history": []}
        
    user_times = user_info.get("times", [])
    
    if valid_time not in user_times:
        user_times.append(valid_time)
        user_times.sort()
        user_info["times"] = user_times
        data[uid] = user_info
        save_data(data)
        await message.answer(f"✅ Время **{valid_time}** добавлено в ваше расписание!")
    else:
        await message.answer(f"ℹ️ Время {valid_time} уже есть в вашем расписании.")


# /list - Просмотр своего расписания
# /list - Просмотр расписания с учетом калибровки часового пояса
@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    data = load_data()
    uid = str(message.from_user.id)
    user_info = data.get(uid, {"times": [], "history": [], "offset": 0})
    
    if isinstance(user_info, list):
        user_times = user_info
        offset = 0
    else:
        user_times = user_info.get("times", [])
        offset = user_info.get("offset", 0)
    
    if not user_times:
        await message.answer("📋 Ваше расписание пусто. Добавьте время с помощью `/set ЧЧ:ММ`")
        return
        
    # Вычисляем текущее локальное время пользователя для сверки
    from datetime import timedelta
    user_now = datetime.now() + timedelta(hours=offset)
    user_now_str = user_now.strftime("%H:%M")
    
    times_str = ", ".join([f"🔔 {t}" for t in user_times])
    
    sign = "+" if offset >= 0 else ""
    await message.answer(
        f"📋 **Ваше активное расписание отчетов:**\n\n"
        f"{times_str}\n\n"
        f"⚙️ Поправка пояса: `{sign}{offset} ч.`\n"
        f"🕒 Ваше время по мнению бота: **{user_now_str}**",
        parse_mode="Markdown"
    )



# /del ЧЧ:ММ - Удаление конкретного времени из расписания
@dp.message(Command("del"))
async def cmd_del(message: types.Message):
    time_to_del = message.text.replace("/del", "").strip()
    uid = str(message.from_user.id)
    data = load_data()
    
    user_info = data.get(uid, {"times": [], "history": []})
    if isinstance(user_info, list):
        user_info = {"times": user_info, "history": []}
        
    user_times = user_info.get("times", [])
    
    if time_to_del in user_times:
        user_times.remove(time_to_del)
        user_info["times"] = user_times
        
        # Если расписание пустое — можно удалить пользователя целиком, чтобы не занимать место
        if not user_times:
            del data[uid]
        else:
            data[uid] = user_info
            
        save_data(data)
        await message.answer(f"❌ Время **{time_to_del}** успешно удалено из расписания.")
    else:
        await message.answer(f"❓ Время {time_to_del} не найдено в вашем списке. Проверьте команду `/list`")


# /clear - Полный сброс расписания пользователя
# /clear - Полный сброс расписания с сохранением часового пояса
@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    data = load_data()
    uid = str(message.from_user.id)
    
    if uid in data:
        user_info = data[uid]
        
        # Если данные в старом формате (список), то просто удаляем всё
        if isinstance(user_info, list):
            del data[uid]
        else:
            # 🟢 КЛЮЧЕВОЙ МОМЕНТ: Очищаем только время и историю, а offset оставляем!
            user_info["times"] = []
            user_info["history"] = []
            # offset не трогаем, он сохраняется
            data[uid] = user_info
            
        save_data(data)
        await message.answer("🗑 **Ваше расписание отчетов очищено.**\nℹ️ _Настройки часового пояса сохранены, заново синхронизировать время не нужно!_")
    else:
        await message.answer("📋 Ваше расписание и так было пусто.")

# ==========================================
# 4. ФОНОВЫЙ ТАЙМЕР РАССЫЛКИ (РАСПИСАНИЕ)
# ==========================================
async def check_reports_loop():
    """Фоновый цикл рассылки: правильный метод send_document + защита от падений"""
    while True:
        try:
            # Базовое системное время сервера прямо сейчас
            server_now = datetime.now()
            
            data = load_data()
            updated = False
            
            for user_id, user_info in data.items():
                if isinstance(user_info, list):
                    user_info = {"times": user_info, "history": [], "offset": 0}
                    data[user_id] = user_info
                    updated = True
                
                user_times = user_info.get("times", [])
                history = user_info.get("history", [])
                user_offset = user_info.get("offset", 0)
                
                # 🧩 Вычисляем текущую дату и время конкретного пользователя с учетом его смещения
                from datetime import timedelta
                user_now = server_now + timedelta(hours=user_offset)
                user_today_str = user_now.strftime("%d-%m-%Y")
                
                # Очищаем историю от записей прошлых дней пользователя
                history = [h for h in history if user_today_str in h]
                user_info["history"] = history
                
                for t_str in user_times:
                    # Уникальный ключ отчета привязан к локальной дате пользователя
                    report_key = f"{t_str}_{user_today_str}"
                    
                    if report_key in history:
                        continue
                        
                    try:
                        # Формируем объект запланированного времени в часовом поясе пользователя
                        scheduled_time = datetime.strptime(f"{user_today_str} {t_str}", "%d-%m-%Y %H:%M")
                    except ValueError:
                        continue
                    
                    # 🟢 ЗАЩИТА ОТ ПАДЕНИЙ: Если локальное время пользователя ДОГНАЛО или ПЕРЕГНАЛО 
                    # время расписания, а отметки в истории (history) за сегодня нет — запускаем отправку!
                    if user_now >= scheduled_time:
                        try:
                            # Запуск вашего внешнего скрипта-скринера
                            subprocess.run(["python", "screener.py"], check=True)
                            
                            # Важно: скрипт screener.py должен создавать файл по дате пользователя
                            pdf_filename = f"tradingview.com-crypto-coins-screener-{user_today_str}.pdf"
                            
                            if os.path.exists(pdf_filename):
                                document = FSInputFile(path=pdf_filename, filename=pdf_filename)
                                
                                # 🟢 ИСПРАВЛЕНО: Используем правильный метод send_document вместо send_message!
                                await bot.send_document(chat_id=int(user_id), document=document)
                                
                                # Даем системе Windows зафиксировать отправку и стираем PDF
                                await asyncio.sleep(2)
                                if os.path.exists(pdf_filename):
                                    os.remove(pdf_filename)
                                
                                # Добавляем ключ в историю, закрывая слот
                                history.append(report_key)
                                updated = True
                                logging.info(f"⏰ Отчет для {user_id} за слот {t_str} успешно доставлен по расписанию.")
                                
                        except Exception as send_error:
                            logging.error(f"Ошибка отправки отчета в слоте {t_str} для {user_id}: {send_error}")
            
            if updated:
                save_data(data)
                
        except Exception as loop_error:
            logging.error(f"Ошибка в фоновом цикле рассылки: {loop_error}")
            
        await asyncio.sleep(60)


# /sync ЧЧ - Синхронизация часового пояса пользователя и сервера
# /sync ЧЧ - Точная калибровка часового пояса
@dp.message(Command("sync"))
async def cmd_sync(message: types.Message):
    hour_input = message.text.replace("/sync", "").strip()
    
    if not hour_input.isdigit():
        await message.answer(
            "ℹ️ **Как синхронизировать время:**\n\n"
            "Введите команду и укажите только количество полных часов на вашем телефоне прямо сейчас.\n"
            "Пример: `/sync 12`"
        )
        return
        
    user_hour = int(hour_input)
    if user_hour < 0 or user_hour > 23:
        await message.answer("❌ Ошибка: Введите час от 0 до 23.")
        return
        
    uid = str(message.from_user.id)
    server_hour = datetime.now().hour
    
    # Расчет разницы часовых поясов
    offset = user_hour - server_hour
    if offset > 12: offset -= 24
    if offset < -12: offset += 24
        
    data = load_data()
    user_info = data.get(uid, {"times": [], "history": [], "offset": 0})
    if isinstance(user_info, list):
        user_info = {"times": user_info, "history": [], "offset": 0}
        
    user_info["offset"] = offset
    data[uid] = user_info
    save_data(data)
    
    sign = "+" if offset >= 0 else ""
    await message.answer(
        f"✅ **Время успешно синхронизировано!**\n\n"
        f"Смещение часового пояса: `{sign}{offset} ч.`\n"
        f"Бот будет корректно нагонять упущенные отчеты даже при падениях сервера."
    )



# ==========================================
# 5. ТОЧКА ВХОДА (ТУПО ЗАПУСК)
# ==========================================
async def main():
    # Запускаем фоновый таймер отправки отчетов по расписанию
    asyncio.create_task(check_reports_loop())
    
    print("🚀 Бот на слэш-командах успешно запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
