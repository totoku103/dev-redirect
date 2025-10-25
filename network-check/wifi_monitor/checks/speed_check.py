import speedtest
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def check_speed(server_url: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    """
    인터넷 속도를 측정합니다.
    
    Args:
        server_url: 속도 측정 서버 URL (None이면 자동 선택)
        timeout: 타임아웃 시간 (초)
    
    Returns:
        {
            "timestamp": "2025-10-25 14:30:05",
            "check_type": "speed_test",
            "target": "speed.kt.com",
            "reachable": True,
            "latency_ms": 15.3,
            "download_mbps": 94.5,
            "upload_mbps": 45.2,
            "error_message": None
        }
    """
    timestamp = datetime.now()
    
    try:
        logger.info("속도 테스트 시작")
        
        # Speedtest 인스턴스 생성
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # 서버 정보 가져오기
        server_info = st.get_best_server()
        target_server = server_info.get('host', 'unknown')
        latency_ms = server_info.get('latency', 0)
        
        logger.info(f"선택된 서버: {target_server}, 응답시간: {latency_ms:.2f}ms")
        
        # 다운로드 속도 측정
        logger.info("다운로드 속도 측정 중...")
        download_bps = st.download()
        download_mbps = download_bps / 1_000_000  # bps를 Mbps로 변환
        
        # 업로드 속도 측정
        logger.info("업로드 속도 측정 중...")
        upload_bps = st.upload()
        upload_mbps = upload_bps / 1_000_000  # bps를 Mbps로 변환
        
        logger.info(f"속도 테스트 완료: 다운로드={download_mbps:.2f}Mbps, 업로드={upload_mbps:.2f}Mbps")
        
        return {
            "timestamp": timestamp,
            "check_type": "speed_test",
            "target": target_server,
            "reachable": True,
            "latency_ms": latency_ms,
            "packet_loss": None,
            "download_mbps": round(download_mbps, 2),
            "upload_mbps": round(upload_mbps, 2),
            "error_message": None
        }
        
    except speedtest.ConfigRetrievalError as e:
        error_message = f"속도 테스트 설정 오류: {str(e)}"
        logger.error(error_message)
        
        return {
            "timestamp": timestamp,
            "check_type": "speed_test",
            "target": "unknown",
            "reachable": False,
            "latency_ms": None,
            "packet_loss": None,
            "download_mbps": None,
            "upload_mbps": None,
            "error_message": error_message
        }
        
    except speedtest.ServersRetrievalError as e:
        error_message = f"속도 테스트 서버 검색 오류: {str(e)}"
        logger.error(error_message)
        
        return {
            "timestamp": timestamp,
            "check_type": "speed_test",
            "target": "unknown",
            "reachable": False,
            "latency_ms": None,
            "packet_loss": None,
            "download_mbps": None,
            "upload_mbps": None,
            "error_message": error_message
        }
        
    except Exception as e:
        error_message = f"속도 테스트 오류: {str(e)}"
        logger.error(error_message)
        
        return {
            "timestamp": timestamp,
            "check_type": "speed_test",
            "target": "unknown",
            "reachable": False,
            "latency_ms": None,
            "packet_loss": None,
            "download_mbps": None,
            "upload_mbps": None,
            "error_message": error_message
        }
