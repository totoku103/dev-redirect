import logging
import sys

def setup_logger():
    """
    로깅 설정을 초기화합니다.
    
    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('wifi_monitor.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)
