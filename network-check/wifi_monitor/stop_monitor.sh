#!/bin/bash
# WiFi 모니터링 시스템 중지 스크립트

echo "🛑 WiFi 모니터링 시스템을 중지합니다..."

# Python 프로세스 찾기 및 종료
PIDS=$(pgrep -f "python.*main.py")
if [ ! -z "$PIDS" ]; then
    echo "프로세스 종료 중: $PIDS"
    kill $PIDS
    sleep 2
    
    # 강제 종료가 필요한 경우
    PIDS=$(pgrep -f "python.*main.py")
    if [ ! -z "$PIDS" ]; then
        echo "강제 종료 중: $PIDS"
        kill -9 $PIDS
    fi
else
    echo "실행 중인 WiFi 모니터링 프로세스가 없습니다."
fi

echo "✅ WiFi 모니터링 시스템이 중지되었습니다."
