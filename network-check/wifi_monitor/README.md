# WiFi 모니터링 시스템

Python으로 가정용 무선 인터넷 품질을 자동 모니터링하는 시스템입니다. 공유기 상태와 ISP 속도를 병렬로 체크하고 PostgreSQL에 저장합니다.

## 주요 기능

- **공유기 체크**: 공유기 IP로 ping 테스트, 응답시간 측정
- **속도 체크**: KT 속도 측정 서버로 다운로드/업로드 속도 측정
- **병렬 처리**: 두 체크를 동시에 실행하여 시간 절약
- **자동 스케줄링**: 5분마다 자동 실행
- **데이터 저장**: PostgreSQL에 모든 결과 저장

## 기술 스택

- **언어**: Python 3.9+
- **병렬 처리**: `concurrent.futures.ThreadPoolExecutor`
- **데이터베이스**: PostgreSQL (psycopg2)
- **네트워크 라이브러리**: 
  - `ping3` (ping 테스트)
  - `speedtest-cli` (속도 측정)

## 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 설정

PostgreSQL에서 데이터베이스와 테이블을 생성합니다:

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE network_monitor;

# 테이블 생성
\c network_monitor
\i database_schema.sql
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 설정합니다:

```env
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

## 실행 방법

```bash
python main.py
```

## 프로젝트 구조

```
wifi_monitor/
├── main.py                 # 메인 실행 및 스케줄링
├── config.py               # 설정 로드
├── requirements.txt        # 의존성 패키지
├── database_schema.sql     # 데이터베이스 스키마
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

## 로그 확인

실행 중인 로그는 콘솔과 `wifi_monitor.log` 파일에 저장됩니다:

```
[2025-10-25 14:30:00] INFO - Starting network checks
[2025-10-25 14:30:00] INFO - Router check completed: reachable=True, latency=2.5ms
[2025-10-25 14:30:00] INFO - Router result saved to database
[2025-10-25 14:30:10] INFO - Speed test completed: download=94.5Mbps, upload=45.2Mbps
[2025-10-25 14:30:10] INFO - Speed test result saved to database
[2025-10-25 14:30:10] INFO - All checks completed successfully
```

## 데이터베이스 스키마

### network_checks 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | SERIAL | 기본키 |
| timestamp | TIMESTAMP | 체크 실행 시간 |
| check_type | VARCHAR(20) | 체크 유형 ('router' 또는 'speed_test') |
| target | VARCHAR(100) | 체크 대상 (IP 주소 또는 도메인) |
| reachable | BOOLEAN | 접속 성공 여부 |
| latency_ms | FLOAT | 응답 시간 (밀리초) |
| packet_loss | FLOAT | 패킷 손실률 (0.0 ~ 1.0) |
| download_mbps | FLOAT | 다운로드 속도 (Mbps) |
| upload_mbps | FLOAT | 업로드 속도 (Mbps) |
| error_message | TEXT | 실패 시 에러 메시지 |
| created_at | TIMESTAMP | 레코드 생성 시간 |

## 성능 요구사항

- 공유기 체크: 5초 이내 완료
- 속도 체크: 30초 이내 완료
- 전체 실행 시간: 35초 이내 (병렬 처리)
- 메모리 사용: 100MB 이하

## 주의사항

### 1. 권한 문제
- ping3는 root 권한이 필요할 수 있습니다
- Linux에서 실행 시: `sudo python main.py`

### 2. 타임아웃 설정
- 속도 측정은 네트워크 상태에 따라 시간이 오래 걸릴 수 있습니다
- 타임아웃을 충분히 여유있게 설정 (60초 권장)

### 3. 에러 복구
- 일시적 네트워크 오류는 다음 주기에 자동 복구됩니다
- 영구적 오류(DB 설정 오류 등)는 수동 개입이 필요합니다
- 로그 파일을 주기적으로 모니터링하세요

## 중지 방법

프로그램을 중지하려면 `Ctrl+C`를 누르세요.

## 문제 해결

### 데이터베이스 연결 실패
- PostgreSQL 서비스가 실행 중인지 확인
- 데이터베이스 설정 정보가 올바른지 확인
- 방화벽 설정 확인

### ping 권한 오류
- Linux/Mac: `sudo python main.py`로 실행
- Windows: 관리자 권한으로 실행

### 속도 측정 실패
- 인터넷 연결 상태 확인
- 방화벽에서 speedtest-cli 허용 확인
