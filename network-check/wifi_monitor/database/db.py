import psycopg2
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def save_result(result: Dict[str, Any], db_config: Dict[str, Any]) -> bool:
    """
    체크 결과를 데이터베이스에 저장합니다.
    
    Args:
        result: check_router() 또는 check_speed()의 반환값
        db_config: {
            "host": "localhost",
            "port": 5432,
            "database": "network_monitor",
            "user": "postgres",
            "password": "password"
        }
    
    Returns:
        성공: True, 실패: False
    """
    conn = None
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # INSERT 쿼리 실행
        insert_query = """
        INSERT INTO network_checks 
        (timestamp, check_type, target, reachable, latency_ms, packet_loss, 
         download_mbps, upload_mbps, error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            result.get("timestamp"),
            result.get("check_type"),
            result.get("target"),
            result.get("reachable"),
            result.get("latency_ms"),
            result.get("packet_loss"),
            result.get("download_mbps"),
            result.get("upload_mbps"),
            result.get("error_message")
        )
        
        cursor.execute(insert_query, values)
        conn.commit()
        
        logger.info(f"{result.get('check_type')} 결과가 데이터베이스에 저장되었습니다")
        return True
        
    except psycopg2.Error as e:
        logger.error(f"데이터베이스 오류: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        logger.error(f"데이터베이스 저장 중 예상치 못한 오류: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
