import os.path
from datetime import datetime

LOG_PATH = "entry_log.txt"
TIME_FORMAT = "%Y/%m/%d_%H:%M:%S"

# csvファイルの作成
def initCsv():
    data = datetime.now().strftime(TIME_FORMAT) + ","
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write(data)

# ファイルの読み込み
def getEntryLog(path: str) -> list[str]:
    with open(path, mode="r", encoding="utf-8") as f:
        log_list = f.read().split(",")
    
    return log_list

def writeEntryLog(path:str, data:list[str]) -> None:
    data_str = ",".join(data)
    with open(LOG_PATH, mode="w", encoding="utf-8") as f:
        f.write(data_str)

# csvファイルの初期化
def checkCsv():
    if not(os.path.isfile(LOG_PATH)):
        initCsv()
        return
    
    log_list = getEntryLog(LOG_PATH)
    log_created = datetime.strptime(log_list[0], TIME_FORMAT)
    today_start = datetime.now().replace(hour=0, minute=0, second=0)

    if log_created < today_start: checkCsv()

# 入力者の入室記録確認
def referenceEntryLog(number: str):
    """
    引数の学生番号等の入室履歴があるかを確認
    
    Parameters
    ----------
    number : str
        確認対象のID。
    """
    if not(os.path.isfile(LOG_PATH)):
        initCsv()
        return 0
    
    entry_log = getEntryLog(LOG_PATH)

    if number in entry_log: return 1
    else: return 0

def addEntryLog(number: str):
    if not(os.path.isfile(LOG_PATH)):
        initCsv()
    
    entry_log = getEntryLog(LOG_PATH)
    entry_log.append(number)
    writeEntryLog(LOG_PATH, entry_log)

def removeEntryLog(number: str):
    if not(os.path.isfile(LOG_PATH)):
        initCsv()
    
    entry_log = getEntryLog(LOG_PATH)
    entry_log.remove(number)
    writeEntryLog(LOG_PATH, entry_log)
    