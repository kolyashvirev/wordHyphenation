from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import time

# Укажите ваш токен бота
BOT_TOKEN = "Ваш_токен_бота"

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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне слово, и я помогу тебе его перенести.')

def handle_message(update: Update, context: CallbackContext) -> None:
    word = update.message.text
    update.message.reply_text('Обрабатываю ваше слово...')

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
        update.message.reply_text(f"Результат переноса: {result}")
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {e}")
    finally:
        browser.quit()

def main() -> None:
    # Создаем Updater и передаем токен
    updater = Updater(BOT_TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()

    # Работает до тех пор, пока не нажмем Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
