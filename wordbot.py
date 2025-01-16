import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
from bs4 import BeautifulSoup
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
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Обработчик команды /start
async def start(update: Update) -> None:
	await update.message.reply_text('Привет! Отправь мне слово, и я помогу тебе его перенести.')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context) -> None:
	word = update.message.text
	logger.info(f"Пользователь {update.effective_user.username} переносит слово {word}")

	try:
		url = f"http://perenos-slov.ru/perenos/{word}"
		response = requests.get(url)
		if response.status_code != 200:
			await update.message.reply_text("Не знаю такого слова")
			return

		response.encoding = 'utf-8'
		await update.message.reply_text(
			BeautifulSoup(response.text, 'html.parser').find('p', class_='pper').text.strip()
		)
	
	except Exception as e:
		await update.message.reply_text(f"Произошла ошибка: {e}")
		logger.error(f"Произошла ошибка: {e}")

# Основная функция для запуска бота
def main() -> None:
	application = Application.builder().token(BOT_TOKEN).build()
	application.add_handler(CommandHandler("start", start))
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
	application.run_polling()


if __name__ == '__main__':
	main()
