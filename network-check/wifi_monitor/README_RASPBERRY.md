# 🍓 라즈베리파이용 WiFi 모니터링 시스템

라즈베리파이에서 실행되는 WiFi 네트워크 모니터링 시스템입니다.

## 🚀 빠른 시작

### 1. 자동 설치
```bash
# 프로젝트 다운로드
git clone <repository-url>
cd wifi_monitor

# 자동 설치 실행
chmod +x install_raspberry.sh
./install_raspberry.sh
```

### 2. 수동 설치
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필요한 패키지 설치
sudo apt install -y python3 python3-pip python3-venv postgresql-client

# 가상환경 생성 및 활성화
python3 -m venv wifi_monitor_env
source wifi_monitor_env/bin/activate

# Python 패키지 설치
pip install -r requirements.txt
```

## ⚙️ 설정

### 환경 변수 설정 (선택사항)
```bash
# .env 파일 생성
cat > .env << EOF
DB_HOST=aws-0-ap-northeast-2.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.ogvxxvrwxorfxhlurora
DB_PASSWORD=FJDKSL123!@#
ROUTER_IP=192.168.0.1
PING_COUNT=4
PING_TIMEOUT=5
CHECK_INTERVAL_MINUTES=1
IS_RASPBERRY_PI=true
EOF
```

## 🎮 실행 방법

### 1. 수동 실행
```bash
# 시작
./start_monitor.sh

# 중지
./stop_monitor.sh
```

### 2. 서비스로 실행 (권장)
```bash
# 서비스 시작
sudo systemctl start wifi-monitor

# 서비스 중지
sudo systemctl stop wifi-monitor

# 서비스 상태 확인
sudo systemctl status wifi-monitor

# 부팅 시 자동 시작 설정
sudo systemctl enable wifi-monitor
```

### 3. 직접 실행
```bash
# 가상환경 활성화
source wifi_monitor_env/bin/activate

# 시스템 실행
python3 main.py
```

## 📊 모니터링

### 로그 확인
```bash
# 실시간 로그 확인
tail -f wifi_monitor.log

# 서비스 로그 확인
sudo journalctl -u wifi-monitor -f

# 에러 로그 확인
tail -f logs/wifi_monitor_error.log
```

### 시스템 상태 확인
```bash
# 프로세스 확인
ps aux | grep python

# 네트워크 연결 확인
ping 192.168.0.1

# 데이터베이스 연결 테스트
python3 test_db_connection.py
```

## 🔧 문제 해결

### 1. ping 권한 문제
라즈베리파이에서는 자동으로 시스템 ping 명령어를 사용하므로 권한 문제가 해결됩니다.

### 2. 메모리 부족
```bash
# 스왑 파일 생성 (선택사항)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### 3. 네트워크 연결 문제
```bash
# 네트워크 인터페이스 확인
ip addr show

# 라우팅 테이블 확인
ip route show

# DNS 확인
nslookup google.com
```

### 4. 서비스 문제
```bash
# 서비스 재시작
sudo systemctl restart wifi-monitor

# 서비스 로그 확인
sudo journalctl -u wifi-monitor --no-pager

# 서비스 비활성화
sudo systemctl disable wifi-monitor
```

## 📈 성능 최적화

### 1. CPU 사용률 최적화
- 체크 간격을 5분으로 늘리기: `CHECK_INTERVAL_MINUTES=5`
- ping 횟수 줄이기: `PING_COUNT=2`

### 2. 메모리 사용률 최적화
```bash
# 가상환경에서 불필요한 패키지 제거
pip uninstall -y <unused-packages>
```

### 3. 로그 파일 관리
```bash
# 로그 로테이션 설정
sudo nano /etc/logrotate.d/wifi-monitor
```

## 🔄 업데이트

```bash
# 코드 업데이트
git pull origin main

# 가상환경 재활성화
source wifi_monitor_env/bin/activate

# 패키지 업데이트
pip install -r requirements.txt --upgrade

# 서비스 재시작
sudo systemctl restart wifi-monitor
```

## 📱 원격 모니터링

### SSH를 통한 원격 접속
```bash
# 라즈베리파이 IP 확인
hostname -I

# SSH 접속
ssh pi@<raspberry-pi-ip>
```

### 웹 인터페이스 (향후 개발 예정)
- Grafana 대시보드 연동
- 실시간 모니터링 웹페이지

## 🛡️ 보안

### 1. 방화벽 설정
```bash
# UFW 방화벽 활성화
sudo ufw enable

# 필요한 포트만 허용
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### 2. SSH 보안 강화
```bash
# SSH 키 인증 설정
ssh-keygen -t rsa -b 4096
ssh-copy-id pi@<raspberry-pi-ip>
```

## 📋 체크리스트

- [ ] 라즈베리파이 OS 업데이트 완료
- [ ] Python3 및 pip 설치 완료
- [ ] 가상환경 생성 및 활성화 완료
- [ ] 필요한 패키지 설치 완료
- [ ] 데이터베이스 연결 테스트 완료
- [ ] 네트워크 연결 확인 완료
- [ ] 서비스 등록 및 시작 완료
- [ ] 로그 확인 및 모니터링 설정 완료

## 🆘 지원

문제가 발생하면 다음을 확인하세요:

1. **로그 파일**: `wifi_monitor.log`
2. **서비스 상태**: `sudo systemctl status wifi-monitor`
3. **네트워크 연결**: `ping 192.168.0.1`
4. **데이터베이스 연결**: `python3 test_db_connection.py`

---

**라즈베리파이에서 안정적으로 WiFi 모니터링을 시작하세요! 🍓**
