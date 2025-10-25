#!/usr/bin/env python3
"""
Supabase 연결 정보 디버깅 스크립트
"""
import psycopg2
from config import DB_CONFIG

def test_connection_variations():
    """다양한 연결 설정을 테스트합니다."""
    
    print("현재 설정:")
    for key, value in DB_CONFIG.items():
        print(f"  {key}: {value}")
    print("-" * 50)
    
    # 테스트 1: 현재 설정
    print("테스트 1: 현재 설정")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("[SUCCESS] 연결 성공!")
        conn.close()
        return True
    except Exception as e:
        print(f"[FAILED] 연결 실패: {e}")
    
    # 테스트 2: 사용자명을 postgres로 변경
    print("\n테스트 2: 사용자명을 postgres로 변경")
    test_config = DB_CONFIG.copy()
    test_config["user"] = "postgres"
    try:
        conn = psycopg2.connect(**test_config)
        print("[SUCCESS] 연결 성공!")
        conn.close()
        return True
    except Exception as e:
        print(f"[FAILED] 연결 실패: {e}")
    
    # 테스트 3: SSL 없이 연결
    print("\n테스트 3: SSL 없이 연결")
    test_config = DB_CONFIG.copy()
    if "sslmode" in test_config:
        del test_config["sslmode"]
    try:
        conn = psycopg2.connect(**test_config)
        print("[SUCCESS] 연결 성공!")
        conn.close()
        return True
    except Exception as e:
        print(f"[FAILED] 연결 실패: {e}")
    
    # 테스트 4: 다른 포트 (6543 - Supabase pooler 포트)
    print("\n테스트 4: 포트 6543으로 연결")
    test_config = DB_CONFIG.copy()
    test_config["port"] = 6543
    try:
        conn = psycopg2.connect(**test_config)
        print("[SUCCESS] 연결 성공!")
        conn.close()
        return True
    except Exception as e:
        print(f"[FAILED] 연결 실패: {e}")
    
    return False

if __name__ == "__main__":
    success = test_connection_variations()
    if not success:
        print("\n[INFO] 해결 방법:")
        print("1. Supabase 대시보드에서 정확한 연결 정보 확인")
        print("2. 데이터베이스 비밀번호 재설정")
        print("3. 프로젝트 설정에서 연결 문자열 확인")
