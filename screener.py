import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
# Импортируем Image из библиотеки Pillow для работы с PDF
from PIL import Image

def create_pdf_from_screenshots(screenshot_files, output_pdf_name):
    """Объединяет скриншоты в один PDF и удаляет исходные PNG файлы"""
    if not screenshot_files:
        print("Нет скриншотов для объединения.")
        return

    print(f"\nНачинаем сборку PDF-файла: {output_pdf_name}...")
    try:
        # Открываем первую картинку и конвертируем её в RGB режим (требуется для PDF)
        first_img = Image.open(screenshot_files[0]).convert('RGB')
        
        # Открываем остальные картинки и тоже конвертируем их в RGB
        other_imgs = [Image.open(f).convert('RGB') for f in screenshot_files[1:]]
        
        # Сохраняем всё в один PDF-файл
        first_img.save(output_pdf_name, save_all=True, append_images=other_imgs)
        print(f"Успешно! PDF-файл сохранен: {os.path.abspath(output_pdf_name)}")
        
        # Удаляем временные PNG скриншоты после успешного сохранения PDF
        print("Удаление временных скриншотов...")
        for file in screenshot_files:
            try:
                os.remove(file)
                print(f"Файл удален: {file}")
            except Exception as e:
                print(f"Не удалось удалить файл {file}: {e}")
                
    except Exception as e:
        print(f"Ошибка при создании PDF: {e}")

def take_screenshots_by_steps(url, target_total_coins=135, coins_per_screen=18):
    print(f"Запуск браузера для: {url}...")
    
    # Список, куда мы будем записывать пути к созданным скриншотам
    created_screenshots = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print("Страница загружена. Ожидаем появление таблицы...")
            
            table_row_selector = "table tr"
            page.locator(table_row_selector).first.wait_for(state="visible", timeout=30000)
            
            # Время на окончательную прогрузку элементов
            time.sleep(5) 
            
            current_index = 0
            step = 1
            
            print(f"Начинаем пошаговое создание скриншотов (по {coins_per_screen} строк)...")
            
            while current_index < target_total_coins:
                print(f"\n--- Шаг {step} (Монеты с {current_index + 1} по {current_index + coins_per_screen}) ---")
                print("Ожидаем прогрузки данных на экране...")
                time.sleep(3.5) 
                
                filename = f"step_{step}.png"
                page.screenshot(path=filename, full_page=False)
                print(f"Скриншот сохранен: {filename}")
                
                # Добавляем имя файла в наш список для последующей сборки в PDF
                created_screenshots.append(filename)
                
                next_index = current_index + coins_per_screen
                if next_index >= target_total_coins:
                    break
                
                loaded_rows_count = page.locator(table_row_selector).count()
                
                # Если новые строки еще не подгрузились, заставляем скроллить вниз
                while next_index >= loaded_rows_count:
                    print("Подгружаем новые строки с сервера...")
                    page.locator(table_row_selector).last.scroll_into_view_if_needed()
                    time.sleep(2.0)
                    loaded_rows_count = page.locator(table_row_selector).count()
                
                # Принудительный JS-скролл строки строго к верхнему краю экрана
                print(f"Сдвигаем таблицу: строка №{next_index} уходит наверх...")
                page.evaluate(
                    f"""
                    const rows = document.querySelectorAll('{table_row_selector}');
                    if (rows[{next_index}]) {{
                        rows[{next_index}].scrollIntoView({{ block: "start", inline: "nearest" }});
                    }}
                    """
                )
                
                current_index = next_index
                step += 1
                
            print(f"\nВсе скриншоты сделаны. Всего шагов: {step}")
            
        except Exception as e:
            print(f"Произошла ошибка при работе браузера: {e}")
        finally:
            try:
                context.close()
                browser.close()
                print("Браузер успешно закрыт.")
            except Exception:
                pass
                
    # Формируем имя PDF файла с текущей датой
    current_date = datetime.now().strftime("%d-%m-%Y")
    pdf_name = f"tradingview.com-crypto-coins-screener-{current_date}.pdf"
    
    # Запускаем функцию объединения и очистки
    create_pdf_from_screenshots(created_screenshots, pdf_name)

if __name__ == "__main__":
    target_url = "https://ru.tradingview.com/crypto-coins-screener/"
    take_screenshots_by_steps(url=target_url, target_total_coins=135, coins_per_screen=18)
