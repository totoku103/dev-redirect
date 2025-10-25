#!/usr/bin/env python3
"""
네트워크 체크 기능 테스트 스크립트 (데이터베이스 없이)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from checks.router_check import check_router
from checks.speed_check import check_speed
from utils.logger import setup_logger

def test_router_check():
    """공유기 체크 기능을 테스트합니다."""
    print("=" * 60)
    print("공유기 체크 테스트")
    print("=" * 60)
    
    # Google DNS 서버로 테스트 (일반적으로 접근 가능)
    test_ip = "8.8.8.8"
    print(f"테스트 대상: {test_ip} (Google DNS)")
    
    try:
        result = check_router(test_ip, ping_count=3, timeout=5)
        
        print(f"결과:")
        print(f"  - 접속 가능: {result['reachable']}")
        print(f"  - 응답시간: {result['latency_ms']}ms")
        print(f"  - 패킷 손실률: {result['packet_loss']}")
        print(f"  - 에러 메시지: {result['error_message']}")
        
        if result['reachable']:
            print("[SUCCESS] 공유기 체크 기능이 정상 작동합니다!")
            return True
        else:
            print("[WARNING] 공유기 체크에서 연결 실패 (네트워크 상태 확인 필요)")
            return False
            
    except Exception as e:
        print(f"[ERROR] 공유기 체크 중 오류 발생: {e}")
        return False

def test_speed_check():
    """속도 체크 기능을 테스트합니다."""
    print("\n" + "=" * 60)
    print("속도 체크 테스트")
    print("=" * 60)
    
    try:
        print("속도 측정을 시작합니다... (시간이 걸릴 수 있습니다)")
        result = check_speed()
        
        print(f"결과:")
        print(f"  - 접속 가능: {result['reachable']}")
        print(f"  - 서버: {result['target']}")
        print(f"  - 응답시간: {result['latency_ms']}ms")
        print(f"  - 다운로드 속도: {result['download_mbps']} Mbps")
        print(f"  - 업로드 속도: {result['upload_mbps']} Mbps")
        print(f"  - 에러 메시지: {result['error_message']}")
        
        if result['reachable']:
            print("[SUCCESS] 속도 체크 기능이 정상 작동합니다!")
            return True
        else:
            print("[WARNING] 속도 체크에서 연결 실패 (인터넷 연결 확인 필요)")
            return False
            
    except Exception as e:
        print(f"[ERROR] 속도 체크 중 오류 발생: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("WiFi 모니터링 시스템 - 네트워크 체크 기능 테스트")
    print("데이터베이스 연결 없이 네트워크 체크 기능만 테스트합니다.")
    
    # 로거 설정
    logger = setup_logger()
    
    # 테스트 실행
    router_success = test_router_check()
    speed_success = test_speed_check()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    print(f"공유기 체크: {'성공' if router_success else '실패'}")
    print(f"속도 체크: {'성공' if speed_success else '실패'}")
    
    if router_success and speed_success:
        print("\n[SUCCESS] 모든 네트워크 체크 기능이 정상 작동합니다!")
        print("데이터베이스 설정 후 전체 시스템을 실행할 수 있습니다.")
    elif router_success or speed_success:
        print("\n[PARTIAL] 일부 기능만 작동합니다.")
        print("네트워크 연결 상태를 확인하세요.")
    else:
        print("\n[FAILED] 네트워크 체크 기능에 문제가 있습니다.")
        print("네트워크 연결과 방화벽 설정을 확인하세요.")

if __name__ == "__main__":
    main()
