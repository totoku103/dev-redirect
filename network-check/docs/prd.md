# WiFi 모니터링 시스템 - AI 개발 명세서

## 프로젝트 목표
Python으로 가정용 무선 인터넷 품질을 자동 모니터링하는 시스템을 구축합니다. 공유기 상태와 ISP 속도를 병렬로 체크하고 PostgreSQL에 저장합니다.

---

## 필수 구현 요구사항

### 1. 기능 개요
다음 2가지 체크를 병렬로 실행하고 각각 독립적으로 DB에 저장:
1. **공유기 체크**: 공유기 IP로 ping 테스트, 응답시간 측정
2. **속도 체크**: KT 속도 측정 서버로 다운로드/업로드 속도 측정

### 2. 기술 스택
- **언어**: Python 3.9+
- **병렬 처리**: `concurrent.futures.ThreadPoolExecutor`
- **데이터베이스**: PostgreSQL (psycopg2)
- **네트워크 라이브러리**: 
  - `ping3` (ping 테스트)
  - `speedtest-cli` (속도 측정)

---

## 데이터베이스 스키마

### 테이블: network_checks

```sql
CREATE TABLE network_checks (
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

CREATE INDEX idx_timestamp ON network_checks(timestamp);
CREATE INDEX idx_check_type ON network_checks(check_type);
```

### 필드 설명
- `check_type`: 'router' 또는 'speed_test'
- `target`: 체크 대상 (IP 주소 또는 도메인)
- `reachable`: 접속 성공 여부
- `latency_ms`: 응답 시간 (밀리초)
- `packet_loss`: 패킷 손실률 (0.0 ~ 1.0)
- `download_mbps`: 다운로드 속도 (Mbps, speed_test만 해당)
- `upload_mbps`: 업로드 속도 (Mbps, speed_test만 해당)
- `error_message`: 실패 시 에러 메시지

---

## 모듈 구조

```
wifi_monitor/
├── main.py                 # 메인 실행 및 스케줄링
├── config.py               # 설정 로드
├── requirements.txt
├── .env
├── checks/
│   ├── __init__.py
│   ├── router_check.py     # check_router() 함수
│   └── speed_check.py      # check_speed() 함수
├── database/
│   ├── __init__.py
│   └── db.py               # save_result() 함수
└── utils/
    ├── __init__.py
    └── logger.py           # 로깅 설정
```

---

## 구현 명세

### 1. 공유기 체크 함수

**파일**: `checks/router_check.py`

**함수 시그니처**:
```python
def check_router(router_ip: str, ping_count: int = 4, timeout: int = 5) -> dict:
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
    pass
```

**구현 요구사항**:
1. `ping3` 라이브러리 사용
2. `ping_count`만큼 ping 실행
3. 평균 응답시간 계산
4. 패킷 손실률 계산 (실패한 ping 수 / 전체 ping 수)
5. 타임아웃 시 `reachable=False`, `error_message` 설정
6. 예외 발생 시 try-except로 처리하고 에러 메시지 반환

**예외 처리**:
- 네트워크 에러: `error_message` 설정, `reachable=False`
- 타임아웃: `error_message="Timeout"`, `reachable=False`
- 기타 에러: 에러 내용을 `error_message`에 저장

**예시 출력**:
```python
# 성공
{
    "timestamp": "2025-10-25 14:30:00.123456",
    "check_type": "router",
    "target": "192.168.0.1",
    "reachable": True,
    "latency_ms": 2.5,
    "packet_loss": 0.0,
    "error_message": None
}

# 실패
{
    "timestamp": "2025-10-25 14:30:00.123456",
    "check_type": "router",
    "target": "192.168.0.1",
    "reachable": False,
    "latency_ms": None,
    "packet_loss": 1.0,
    "error_message": "Request timeout for ICMP packet"
}
```

---

### 2. 속도 체크 함수

**파일**: `checks/speed_check.py`

**함수 시그니처**:
```python
def check_speed(server_url: str = None, timeout: int = 60) -> dict:
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
    pass
```

**구현 요구사항**:
1. `speedtest-cli` 라이브러리 사용
2. `speedtest.Speedtest()` 인스턴스 생성
3. 서버 선택 (KT 서버 우선, 없으면 자동 선택)
4. 다운로드/업로드 속도 측정 (bps → Mbps 변환)
5. ping 값을 `latency_ms`에 저장
6. 측정 실패 시 `reachable=False`, `error_message` 설정

**속도 변환**:
```python
download_mbps = download_bps / 1_000_000
upload_mbps = upload_bps / 1_000_000
```

**예외 처리**:
- 서버 연결 실패: `error_message` 설정, `reachable=False`
- 측정 타임아웃: `error_message="Speed test timeout"`, `reachable=False`
- 기타 에러: 에러 내용을 `error_message`에 저장

**예시 출력**:
```python
# 성공
{
    "timestamp": "2025-10-25 14:30:05.654321",
    "check_type": "speed_test",
    "target": "speedtest.kt.com",
    "reachable": True,
    "latency_ms": 15.3,
    "packet_loss": None,
    "download_mbps": 94.5,
    "upload_mbps": 45.2,
    "error_message": None
}

# 실패
{
    "timestamp": "2025-10-25 14:30:05.654321",
    "check_type": "speed_test",
    "target": "unknown",
    "reachable": False,
    "latency_ms": None,
    "packet_loss": None,
    "download_mbps": None,
    "upload_mbps": None,
    "error_message": "Unable to connect to speedtest server"
}
```

---

### 3. 데이터베이스 저장 함수

**파일**: `database/db.py`

**함수 시그니처**:
```python
def save_result(result: dict, db_config: dict) -> bool:
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
    pass
```

**구현 요구사항**:
1. `psycopg2` 사용
2. `INSERT` 쿼리 실행:
```sql
INSERT INTO network_checks 
(timestamp, check_type, target, reachable, latency_ms, packet_loss, 
 download_mbps, upload_mbps, error_message)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
```
3. 각 저장은 독립된 트랜잭션 (자동 commit)
4. 연결 실패 시 재시도 없음 (False 반환)
5. 예외 발생 시 로그 출력 후 False 반환

**예외 처리**:
- DB 연결 실패: 로그 출력, False 반환
- INSERT 실패: 로그 출력, False 반환
- 연결 후 반드시 `conn.close()` 실행

---

### 4. 병렬 실행 및 메인 로직

**파일**: `main.py`

**함수 시그니처**:
```python
def run_checks(router_ip: str, db_config: dict) -> tuple:
    """
    공유기 체크와 속도 체크를 병렬로 실행하고 DB에 저장합니다.
    
    Args:
        router_ip: 공유기 IP 주소
        db_config: 데이터베이스 설정
    
    Returns:
        (router_saved: bool, speed_saved: bool)
    """
    pass
```

**구현 요구사항**:
1. `concurrent.futures.ThreadPoolExecutor` 사용
2. 2개의 스레드로 병렬 실행:
   - Thread 1: `check_router()` → `save_result()`
   - Thread 2: `check_speed()` → `save_result()`
3. 각 작업은 완전히 독립적 (한쪽 실패가 다른쪽에 영향 없음)
4. 모든 예외는 각 스레드 내에서 처리
5. 두 작업 모두 완료될 때까지 대기

**구현 예시**:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from checks.router_check import check_router
from checks.speed_check import check_speed
from database.db import save_result
import logging

def check_and_save_router(router_ip: str, db_config: dict) -> bool:
    """공유기 체크 후 저장"""
    try:
        result = check_router(router_ip)
        return save_result(result, db_config)
    except Exception as e:
        logging.error(f"Router check failed: {e}")
        return False

def check_and_save_speed(db_config: dict) -> bool:
    """속도 체크 후 저장"""
    try:
        result = check_speed()
        return save_result(result, db_config)
    except Exception as e:
        logging.error(f"Speed check failed: {e}")
        return False

def run_checks(router_ip: str, db_config: dict) -> tuple:
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_router = executor.submit(check_and_save_router, router_ip, db_config)
        future_speed = executor.submit(check_and_save_speed, db_config)
        
        router_saved = future_router.result()
        speed_saved = future_speed.result()
        
    return (router_saved, speed_saved)
```

**스케줄링**:
```python
import time
import schedule

def main():
    router_ip = os.getenv("ROUTER_IP", "192.168.0.1")
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "network_monitor"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "")
    }
    
    # 5분마다 실행
    schedule.every(5).minutes.do(run_checks, router_ip, db_config)
    
    # 즉시 한 번 실행
    run_checks(router_ip, db_config)
    
    # 스케줄 루프
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
```

---

### 5. 설정 관리

**파일**: `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 데이터베이스 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "network_monitor"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}

# 네트워크 설정
ROUTER_IP = os.getenv("ROUTER_IP", "192.168.0.1")
PING_COUNT = int(os.getenv("PING_COUNT", "4"))
PING_TIMEOUT = int(os.getenv("PING_TIMEOUT", "5"))

# 스케줄 설정
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))
```

**환경 변수 파일**: `.env`
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=network_monitor
DB_USER=postgres
DB_PASSWORD=your_password

ROUTER_IP=192.168.0.1
PING_COUNT=4
PING_TIMEOUT=5

CHECK_INTERVAL_MINUTES=5
```

---

### 6. 로깅 설정

**파일**: `utils/logger.py`

```python
import logging
import sys

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('wifi_monitor.log')
        ]
    )
    return logging.getLogger(__name__)
```

**로그 출력 예시**:
```
[2025-10-25 14:30:00] INFO - Starting network checks
[2025-10-25 14:30:00] INFO - Router check completed: reachable=True, latency=2.5ms
[2025-10-25 14:30:00] INFO - Router result saved to database
[2025-10-25 14:30:10] INFO - Speed test completed: download=94.5Mbps, upload=45.2Mbps
[2025-10-25 14:30:10] INFO - Speed test result saved to database
[2025-10-25 14:30:10] INFO - All checks completed successfully
```

---

## 의존성 라이브러리

**파일**: `requirements.txt`

```
psycopg2-binary==2.9.9
ping3==4.0.4
speedtest-cli==2.1.3
python-dotenv==1.0.0
schedule==1.2.0
```

**설치 명령어**:
```bash
pip install -r requirements.txt
```

---

## 실행 방법

### 1. 데이터베이스 준비
```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE network_monitor;

# 테이블 생성
\c network_monitor
CREATE TABLE network_checks (
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
CREATE INDEX idx_timestamp ON network_checks(timestamp);
CREATE INDEX idx_check_type ON network_checks(check_type);
```

### 2. 환경 설정
`.env` 파일을 생성하고 위의 환경 변수 설정

### 3. 프로그램 실행
```bash
python main.py
```

---

## 테스트 케이스

### 테스트 1: 공유기 체크 - 정상
```python
result = check_router("192.168.0.1", ping_count=4, timeout=5)
assert result["reachable"] == True
assert result["latency_ms"] > 0
assert result["packet_loss"] == 0.0
```

### 테스트 2: 공유기 체크 - 타임아웃
```python
result = check_router("192.168.999.999", ping_count=2, timeout=2)
assert result["reachable"] == False
assert result["error_message"] is not None
assert result["packet_loss"] == 1.0
```

### 테스트 3: 속도 체크 - 정상
```python
result = check_speed()
assert result["reachable"] == True
assert result["download_mbps"] > 0
assert result["upload_mbps"] > 0
assert result["latency_ms"] > 0
```

### 테스트 4: 병렬 실행
```python
import time
start_time = time.time()
router_saved, speed_saved = run_checks("192.168.0.1", db_config)
elapsed_time = time.time() - start_time

# 병렬 실행이므로 순차 실행보다 빨라야 함
assert elapsed_time < 35  # 속도 테스트(~30초) + 여유시간
assert router_saved == True
assert speed_saved == True
```

### 테스트 5: 데이터베이스 저장
```python
result = {
    "timestamp": "2025-10-25 14:30:00",
    "check_type": "router",
    "target": "192.168.0.1",
    "reachable": True,
    "latency_ms": 2.5,
    "packet_loss": 0.0,
    "download_mbps": None,
    "upload_mbps": None,
    "error_message": None
}
saved = save_result(result, db_config)
assert saved == True

# DB에서 확인
# SELECT * FROM network_checks ORDER BY id DESC LIMIT 1;
```

---

## 에러 처리 시나리오

### 시나리오 1: 공유기 오프라인
```python
# check_router()에서 처리
result = {
    "reachable": False,
    "latency_ms": None,
    "packet_loss": 1.0,
    "error_message": "Host unreachable"
}
# 이 결과도 DB에 저장되어야 함
```

### 시나리오 2: 인터넷 끊김
```python
# check_speed()에서 처리
result = {
    "reachable": False,
    "download_mbps": None,
    "upload_mbps": None,
    "error_message": "No internet connection"
}
# 이 결과도 DB에 저장되어야 함
```

### 시나리오 3: DB 연결 실패
```python
# save_result()에서 처리
try:
    conn = psycopg2.connect(**db_config)
except Exception as e:
    logging.error(f"Database connection failed: {e}")
    return False
# 다음 체크 주기에 재시도
```

### 시나리오 4: 한쪽 작업만 실패
```python
# 병렬 실행 중 한쪽만 실패해도 다른쪽은 정상 진행
router_saved, speed_saved = run_checks(router_ip, db_config)
# 예: router_saved=True, speed_saved=False
# 로그에 실패 기록, 다음 주기에 재시도
```

---

## 성공 기준

### 필수 조건
1. ✅ 공유기 ping 테스트 성공
2. ✅ KT 속도 측정 성공
3. ✅ 두 작업이 병렬로 실행됨 (시간 절약 확인)
4. ✅ 각 결과가 개별적으로 DB에 저장됨
5. ✅ 5분마다 자동 실행됨
6. ✅ 에러 발생 시에도 프로그램이 중단되지 않음

### 성능 요구사항
- 공유기 체크: 5초 이내 완료
- 속도 체크: 30초 이내 완료
- 전체 실행 시간: 35초 이내 (병렬 처리로)
- 메모리 사용: 100MB 이하

### 안정성 요구사항
- 24시간 연속 실행 가능
- 한쪽 작업 실패 시에도 다른쪽 작업은 정상 진행
- DB 연결 실패 시에도 프로그램 크래시 없음

---

## 주의사항

### 1. 권한 문제
- ping3는 root 권한이 필요할 수 있음
- Linux에서 실행 시: `sudo python main.py`
- 또는 `setcap` 명령으로 권한 부여

### 2. 타임아웃 설정
- 속도 측정은 네트워크 상태에 따라 시간이 오래 걸릴 수 있음
- 타임아웃을 충분히 여유있게 설정 (60초 권장)

### 3. 데이터베이스 연결
- 연결 풀링 사용하지 않음 (간단한 구조 유지)
- 각 저장마다 새로운 연결 생성/종료
- 프로덕션 환경에서는 연결 풀링 고려

### 4. 에러 복구
- 일시적 네트워크 오류는 다음 주기에 자동 복구됨
- 영구적 오류(DB 설정 오류 등)는 수동 개입 필요
- 로그 파일을 주기적으로 모니터링

---

## 확장 가능성

### Phase 1 (현재 범위)
- 기본 모니터링 기능
- 단일 공유기, 단일 속도 서버
- 로컬 데이터베이스

### Phase 2 (향후 확장)
- 여러 공유기 동시 모니터링
- 여러 ISP 속도 서버 비교
- 웹 대시보드 추가
- 알림 기능 (이메일/SMS)

### Phase 3 (장기 계획)
- 이상 패턴 감지 (AI/ML)
- 클라우드 DB 연동
- 모바일 앱
- 데이터 분석 및 리포트

---

## 개발 체크리스트

- [ ] 프로젝트 구조 생성
- [ ] PostgreSQL 데이터베이스 및 테이블 생성
- [ ] requirements.txt 작성 및 패키지 설치
- [ ] .env 파일 생성 및 설정
- [ ] config.py 구현
- [ ] utils/logger.py 구현
- [ ] database/db.py 구현 (save_result 함수)
- [ ] checks/router_check.py 구현 (check_router 함수)
- [ ] checks/speed_check.py 구현 (check_speed 함수)
- [ ] main.py 구현 (병렬 실행 및 스케줄링)
- [ ] 각 함수 단위 테스트
- [ ] 통합 테스트
- [ ] 24시간 연속 실행 테스트
- [ ] 에러 시나리오 테스트
- [ ] 로그 확인 및 문서화

---

**문서 버전**: 2.0 (AI 개발자용)  
**작성일**: 2025-10-25  
**대상**: AI 코드 생성 엔진
