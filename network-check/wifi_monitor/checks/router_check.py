import ping3
import logging
import subprocess
import platform
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_router(router_ip: str, ping_count: int = 4, timeout: int = 5) -> Dict[str, Any]:
    """
    공유기에 ping을 보내 연결 상태를 확인합니다.
    
    Args:
        router_ip: 공유기 IP 주소 (예: "192.168.0.1")
        ping_count: ping 횟수
        timeout: 타임아웃 시간 (초)
    
    Returns:
        {
            "timestamp": "2025-10-25 14:30:00",
            "check_type": "router",
            "target": "192.168.0.1",
            "reachable": True,
            "latency_ms": 2.5,
            "packet_loss": 0.0,
            "error_message": None
        }
    """
    timestamp = datetime.now()
    successful_pings = 0
    total_latency = 0.0
    error_message = None
    
    try:
        logger.info(f"{router_ip}에 대한 공유기 체크 시작")
        
        # 라즈베리파이에서는 ping3 대신 시스템 ping 명령어 사용
        if platform.system() == "Linux" and "arm" in platform.machine().lower():
            logger.debug("라즈베리파이 환경에서 시스템 ping 명령어 사용")
            for i in range(ping_count):
                try:
                    # 시스템 ping 명령어 실행
                    result = subprocess.run(
                        ["ping", "-c", "1", "-W", str(timeout), router_ip],
                        capture_output=True,
                        text=True,
                        timeout=timeout + 2
                    )
                    
                    if result.returncode == 0:
                        # ping 결과에서 시간 추출
                        output_lines = result.stdout.split('\n')
                        for line in output_lines:
                            if 'time=' in line:
                                time_part = line.split('time=')[1].split()[0]
                                response_time = float(time_part)
                                successful_pings += 1
                                total_latency += response_time
                                logger.debug(f"Ping {i+1}: {response_time:.2f}ms")
                                break
                    else:
                        logger.debug(f"Ping {i+1}: 타임아웃")
                        
                except Exception as e:
                    logger.debug(f"Ping {i+1} 실패: {e}")
                    continue
        else:
            # 일반 환경에서는 ping3 사용
            for i in range(ping_count):
                try:
                    # ping3.ping()는 응답시간을 초 단위로 반환 (None이면 타임아웃)
                    response_time = ping3.ping(router_ip, timeout=timeout)
                    
                    if response_time is not None:
                        successful_pings += 1
                        total_latency += response_time * 1000  # 초를 밀리초로 변환
                        logger.debug(f"Ping {i+1}: {response_time*1000:.2f}ms")
                    else:
                        logger.debug(f"Ping {i+1}: 타임아웃")
                        
                except Exception as e:
                    logger.debug(f"Ping {i+1} 실패: {e}")
                    continue
        
        # 결과 계산
        packet_loss = (ping_count - successful_pings) / ping_count
        reachable = successful_pings > 0
        
        if reachable:
            avg_latency = total_latency / successful_pings
            logger.info(f"공유기 체크 완료: 접속가능=True, 응답시간={avg_latency:.2f}ms, 패킷손실률={packet_loss:.2f}")
        else:
            avg_latency = None
            error_message = "모든 ping 요청이 실패했습니다"
            logger.warning(f"공유기 체크 실패: {error_message}")
        
        return {
            "timestamp": timestamp,
            "check_type": "router",
            "target": router_ip,
            "reachable": reachable,
            "latency_ms": avg_latency,
            "packet_loss": packet_loss,
            "download_mbps": None,
            "upload_mbps": None,
            "error_message": error_message
        }
        
    except Exception as e:
        error_message = f"공유기 체크 오류: {str(e)}"
        logger.error(error_message)
        
        return {
            "timestamp": timestamp,
            "check_type": "router",
            "target": router_ip,
            "reachable": False,
            "latency_ms": None,
            "packet_loss": 1.0,
            "download_mbps": None,
            "upload_mbps": None,
            "error_message": error_message
        }
