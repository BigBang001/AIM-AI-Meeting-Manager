from datetime import datetime

def word_count(text):
    return len(text.split())

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")