import time


def log_message(file_name:str, message:str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
