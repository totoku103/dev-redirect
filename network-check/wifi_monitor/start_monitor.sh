#!/bin/bash
# WiFi 모니터링 시스템 시작 스크립트

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

echo "🍓 WiFi 모니터링 시스템을 시작합니다..."

# 가상환경 활성화
source wifi_monitor_env/bin/activate

# Python 경로 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 로그 디렉토리 생성
mkdir -p logs

# 시스템 실행
echo "🚀 시스템 시작 중..."
python3 main.py
