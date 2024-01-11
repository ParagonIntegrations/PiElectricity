from pathlib import Path
import logging

class Settings:

	base_dir = Path(__file__).resolve().parent
	log_dir = base_dir.joinpath('data','log')
	log_dir.mkdir(parents=True, exist_ok=True)
	log_name = str(log_dir.joinpath('Log.txt'))
	log_maxbytes = 10485760
	log_maxnum = 5
	file_loglevel = logging.INFO
	console_loglevel = logging.DEBUG
	telegram_loglevel = logging.WARNING
	telegram_token = '6041241784:AAF0Tzx-2zJj6mMewDzwe0zlVUY2S1kiutk'
	telegram_chat_id = '1769119635'
	readings_dir = base_dir.joinpath('data','readings')
	readings_dir.mkdir(parents=True, exist_ok=True)
	readings_file = readings_dir.joinpath('minutedata.csv')
	voltage = 230
	id = 0