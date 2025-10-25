import time
import schedule
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple

from config import DB_CONFIG, ROUTER_IP, PING_COUNT, PING_TIMEOUT, CHECK_INTERVAL_MINUTES
from utils.logger import setup_logger
from checks.router_check import check_router
from checks.speed_check import check_speed
from database.db import save_result

logger = setup_logger()

def check_and_save_router(router_ip: str, db_config: dict) -> bool:
    """공유기 체크 후 저장"""
    try:
        result = check_router(router_ip, PING_COUNT, PING_TIMEOUT)
        logger.info(f"공유기 체크 결과: 접속가능={result['reachable']}, 응답시간={result['latency_ms']}ms")
        
        # 데이터베이스 저장 시도
        try:
            saved = save_result(result, db_config)
            if saved:
                logger.info("공유기 체크 결과가 데이터베이스에 저장되었습니다")
            else:
                logger.warning("공유기 체크 결과 저장에 실패했습니다")
            return saved
        except Exception as db_error:
            logger.warning(f"공유기 체크 데이터베이스 저장 실패: {db_error}")
            return False
            
    except Exception as e:
        logger.error(f"공유기 체크 실패: {e}")
        return False

def check_and_save_speed(db_config: dict) -> bool:
    """속도 체크 후 저장"""
    try:
        result = check_speed()
        logger.info(f"속도 테스트 결과: 접속가능={result['reachable']}, 다운로드={result['download_mbps']}Mbps, 업로드={result['upload_mbps']}Mbps")
        
        # 데이터베이스 저장 시도
        try:
            saved = save_result(result, db_config)
            if saved:
                logger.info("속도 테스트 결과가 데이터베이스에 저장되었습니다")
            else:
                logger.warning("속도 테스트 결과 저장에 실패했습니다")
            return saved
        except Exception as db_error:
            logger.warning(f"속도 테스트 데이터베이스 저장 실패: {db_error}")
            return False
            
    except Exception as e:
        logger.error(f"속도 체크 실패: {e}")
        return False

def run_checks(router_ip: str, db_config: dict) -> Tuple[bool, bool]:
    """
    공유기 체크와 속도 체크를 병렬로 실행하고 DB에 저장합니다.
    
    Args:
        router_ip: 공유기 IP 주소
        db_config: 데이터베이스 설정
    
    Returns:
        (router_saved: bool, speed_saved: bool)
    """
    logger.info("네트워크 체크 시작")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 두 작업을 병렬로 실행
        future_router = executor.submit(check_and_save_router, router_ip, db_config)
        future_speed = executor.submit(check_and_save_speed, db_config)
        
        # 결과 대기
        router_saved = future_router.result()
        speed_saved = future_speed.result()
    
    # 결과 로깅
    if router_saved and speed_saved:
        logger.info("모든 체크가 성공적으로 완료되었습니다")
    elif router_saved:
        logger.warning("공유기 체크는 완료되었지만 속도 테스트가 실패했습니다")
    elif speed_saved:
        logger.warning("속도 테스트는 완료되었지만 공유기 체크가 실패했습니다")
    else:
        logger.error("모든 체크가 실패했습니다")
    
    return (router_saved, speed_saved)

def main():
    """메인 실행 함수"""
    logger.info("WiFi 모니터링 시스템 시작...")
    logger.info(f"공유기 IP: {ROUTER_IP}")
    logger.info(f"체크 간격: {CHECK_INTERVAL_MINUTES}분")
    logger.info(f"데이터베이스: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    # 스케줄 설정
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(run_checks, ROUTER_IP, DB_CONFIG)
    
    # 즉시 한 번 실행
    logger.info("초기 체크 실행 중...")
    run_checks(ROUTER_IP, DB_CONFIG)
    
    # 스케줄 루프
    logger.info(f"{CHECK_INTERVAL_MINUTES}분마다 자동 체크 시작")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("사용자에 의해 WiFi 모니터링 시스템이 중지되었습니다")
    except Exception as e:
        logger.error(f"메인 루프에서 예상치 못한 오류 발생: {e}")

if __name__ == "__main__":
    main()
