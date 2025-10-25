#!/usr/bin/env python3
"""
데이터베이스 연결 테스트 스크립트
"""
import psycopg2
from config import DB_CONFIG

def test_database_connection():
    """데이터베이스 연결을 테스트합니다."""
    print("데이터베이스 연결 테스트 시작...")
    print(f"호스트: {DB_CONFIG['host']}")
    print(f"포트: {DB_CONFIG['port']}")
    print(f"데이터베이스: {DB_CONFIG['database']}")
    print(f"사용자: {DB_CONFIG['user']}")
    print("-" * 50)
    
    try:
        # 데이터베이스 연결 시도
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 연결 테스트 쿼리
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("[SUCCESS] 데이터베이스 연결 성공!")
        print(f"PostgreSQL 버전: {version[0]}")
        
        # 테이블 존재 여부 확인
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'network_checks'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("[SUCCESS] network_checks 테이블이 존재합니다.")
            
            # 테이블 구조 확인
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'network_checks'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            print("테이블 구조:")
            for col_name, col_type in columns:
                print(f"  - {col_name}: {col_type}")
        else:
            print("[WARNING] network_checks 테이블이 존재하지 않습니다.")
            print("database_schema.sql을 실행하여 테이블을 생성하세요.")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] 데이터베이스 연결 실패: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 예상치 못한 오류: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n[SUCCESS] 데이터베이스 연결 테스트 완료!")
    else:
        print("\n[FAILED] 데이터베이스 연결 테스트 실패!")
        print("설정을 확인하고 다시 시도하세요.")
