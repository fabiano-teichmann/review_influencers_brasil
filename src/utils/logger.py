import logging
import os

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "app.log")

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_file_path,
    filemode="a"
)


logger = logging.getLogger("app_logger")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(console_handler)
