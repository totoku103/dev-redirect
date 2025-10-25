#!/bin/bash
# 라즈베리파이용 WiFi 모니터링 시스템 설치 스크립트

echo "🍓 라즈베리파이용 WiFi 모니터링 시스템 설치를 시작합니다..."

# 시스템 업데이트
echo "📦 시스템 패키지 업데이트 중..."
sudo apt update && sudo apt upgrade -y

# Python3 및 pip 설치 확인
echo "🐍 Python3 및 pip 설치 확인 중..."
sudo apt install -y python3 python3-pip python3-venv

# 필요한 시스템 패키지 설치
echo "🔧 필요한 시스템 패키지 설치 중..."
sudo apt install -y postgresql-client git

# 가상환경 생성
echo "🌐 Python 가상환경 생성 중..."
python3 -m venv wifi_monitor_env

# 가상환경 활성화
echo "⚡ 가상환경 활성화 중..."
source wifi_monitor_env/bin/activate

# Python 패키지 설치
echo "📚 Python 패키지 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 실행 권한 부여
echo "🔑 실행 권한 부여 중..."
chmod +x start_monitor.sh
chmod +x stop_monitor.sh

# 서비스 파일 복사
echo "⚙️ 시스템 서비스 설정 중..."
sudo cp wifi-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable wifi-monitor.service

echo "✅ 설치가 완료되었습니다!"
echo ""
echo "🚀 실행 방법:"
echo "1. 수동 실행: ./start_monitor.sh"
echo "2. 서비스 시작: sudo systemctl start wifi-monitor"
echo "3. 서비스 중지: sudo systemctl stop wifi-monitor"
echo "4. 서비스 상태 확인: sudo systemctl status wifi-monitor"
echo ""
echo "📝 로그 확인:"
echo "- 실시간 로그: tail -f wifi_monitor.log"
echo "- 서비스 로그: sudo journalctl -u wifi-monitor -f"
