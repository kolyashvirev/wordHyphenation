import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Укажите ваш токен бота
BOT_TOKEN = "7522774678:AAEdR9IA4by-acqHMOkymI7OYXFIvdR4kdk"

# Настройка логирования
logdir = f"{os.path.dirname(__file__)}/bot.log"
print(f"Логирование: {logdir}")
os.system(f'touch {logdir}')
logging.basicConfig (
    filename = logdir,
    filemode = 'a',
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)
logger = logging.getLogger(__name__)

# Настройка Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = "/usr/bin/google-chrome"
service = Service('/usr/bin/chromedriver')
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.get("http://perenos-slov.ru")

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправь мне слово, и я помогу тебе его перенести.')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    word = update.message.text
    logger.info(f"Пользователь {update.effective_user.username} переносит слово {word}")
    # await update.message.reply_text('Обрабатываю ваше слово...')

    try:
        # Ожидаем появления поля для ввода слова
        search_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.srch"))
        )
        
        # Вводим слово
        search_input.send_keys(word)

        # Ожидаем появления кнопки и кликаем по ней
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        submit_button.click()

        # Ожидаем, пока загрузится элемент <h1 class="entry-title">
        entry_title = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.entry-title"))
        )
        
        # Проверяем, если текст заголовка равен "К сожалению вы попали куда-то не туда)"
        if entry_title.text == "К сожалению вы попали куда-то не туда)":
            await update.message.reply_text("Не знаю такого слова")
            return

        # После этого продолжаем выполнение, получаем результат переноса
        result = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.pper"))
        ).text

        await update.message.reply_text(result)
    
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

# Основная функция для запуска бота
def main() -> None:
    try:
        # Создаем объект Application с токеном бота
        application = Application.builder().token(BOT_TOKEN).build()

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))

        # Добавляем обработчик для текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Запуск бота
        application.run_polling()

    finally:
        browser.quit()

if __name__ == '__main__':
    main()
