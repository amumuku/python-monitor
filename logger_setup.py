import logging
import logging.handlers
import re

# 配置日志记录器
logging.basicConfig(
    filename="monitor-token.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(lineno)d] - %(message)s",  # 添加 %(lineno)d
    datefmt="%Y-%m-%d %H:%M:%S"
)
log_filename = "monitor-token.log"

log_handler = logging.handlers.TimedRotatingFileHandler(
    log_filename, when="midnight", interval=1, backupCount=0
)
log_handler.suffix = "%Y-%m-%d"  # 日志文件名后缀格式
log_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # 匹配后缀的正则表达式

# 创建一个日志记录器
logger = logging.getLogger()
logger.addHandler(log_handler)
