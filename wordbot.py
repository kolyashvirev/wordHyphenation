from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import time

# Укажите ваш токен бота
BOT_TOKEN = "7522774678:AAEdR9IA4by-acqHMOkymI7OYXFIvdR4kdk"

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = "/usr/bin/google-chrome"
service = Service('/usr/bin/chromedriver')

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправь мне слово, и я помогу тебе его перенести.')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    word = update.message.text
    await update.message.reply_text('Обрабатываю ваше слово...')

    # Инициализация браузера
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        browser.get("http://perenos-slov.ru")
        search_input = browser.find_element(By.CSS_SELECTOR, "input.srch")
        search_input.send_keys(word)

        submit_button = browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        # Ожидание, пока не появится результат
        time.sleep(2)  # Лучше использовать WebDriverWait для динамических элементов

        result = browser.find_element(By.CSS_SELECTOR, "p.pper").text
        await update.message.reply_text(f"Результат переноса: {result}")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")
    finally:
        browser.quit()

# Основная функция для запуска бота
def main() -> None:
    # Создаем объект Application с токеном бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Добавляем обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
