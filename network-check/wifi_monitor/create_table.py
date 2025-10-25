#!/usr/bin/env python3
"""
Supabase에 network_checks 테이블 생성 스크립트
"""
import psycopg2
from config import DB_CONFIG

def create_network_checks_table():
    """network_checks 테이블을 생성합니다."""
    
    print("데이터베이스에 연결 중...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("연결 성공! 테이블 생성 중...")
        
        # 테이블 생성 SQL
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS network_checks (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            check_type VARCHAR(20) NOT NULL,
            target VARCHAR(100) NOT NULL,
            reachable BOOLEAN NOT NULL,
            latency_ms FLOAT,
            packet_loss FLOAT,
            download_mbps FLOAT,
            upload_mbps FLOAT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        
        cursor.execute(create_table_sql)
        
        # 인덱스 생성
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON network_checks(timestamp);",
            "CREATE INDEX IF NOT EXISTS idx_check_type ON network_checks(check_type);",
            "CREATE INDEX IF NOT EXISTS idx_reachable ON network_checks(reachable);"
        ]
        
        for index_sql in indexes_sql:
            cursor.execute(index_sql)
        
        conn.commit()
        
        print("[SUCCESS] network_checks 테이블이 성공적으로 생성되었습니다!")
        
        # 테이블 구조 확인
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'network_checks'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        print("\n테이블 구조:")
        for col_name, col_type in columns:
            print(f"  - {col_name}: {col_type}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 테이블 생성 실패: {e}")
        return False

if __name__ == "__main__":
    success = create_network_checks_table()
    if success:
        print("\n[SUCCESS] 데이터베이스 설정이 완료되었습니다!")
        print("이제 main.py를 실행하여 전체 시스템을 테스트할 수 있습니다.")
    else:
        print("\n[FAILED] 테이블 생성에 실패했습니다.")
