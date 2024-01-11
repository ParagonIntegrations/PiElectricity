import logging
from logging import Handler, Formatter
from logging.handlers import RotatingFileHandler
import requests
from settings import Settings
import datetime

# Create a rotating logger
def create_rotating_log(path):
	# Create the logger
	logger = logging.getLogger("Main Logger")
	logger.setLevel(logging.DEBUG)
	# Create a rotating filehandler
	filehandler = RotatingFileHandler(path, maxBytes=Settings.log_maxbytes, backupCount=Settings.log_maxnum)
	filehandler.setLevel(Settings.file_loglevel)
	# Create a streamhandler to print to console
	consolehandler = logging.StreamHandler()
	consolehandler.setLevel(Settings.console_loglevel)
	# Create a formatter and add to filehandler and consolehandler
	formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(funcName)s - %(message)s')
	filehandler.setFormatter(formatter)
	consolehandler.setFormatter(formatter)
	# Create the requestshandler to send to Telegram
	telegramhandler = TelegramRequestsHandler()
	telegramhandler.setLevel(Settings.telegram_loglevel)
	telegramformatter = TelegramFormatter()
	telegramhandler.setFormatter(telegramformatter)
	# Add the filehandler and consolehandler to the logger
	logger.addHandler(filehandler)
	logger.addHandler(consolehandler)
	logger.addHandler(telegramhandler)
	return logger

class TelegramRequestsHandler(Handler):
	def emit(self, record):
		log_entry = self.format(record)
		payload = {
			'chat_id': Settings.telegram_chat_id,
			'text': log_entry,
			'parse_mode': 'HTML'
		}
		return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=Settings.telegram_token),
							 data=payload).content

class TelegramFormatter(Formatter):
	def __init__(self):
		super(TelegramFormatter, self).__init__()

	def format(self, record):
		t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		msg = record.msg
		if record.exc_text:
			msg += '\n' + record.exc_text

		return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=msg, datetime=t)