import os
from dotenv import load_dotenv

# .env 파일 로드 (파일이 없어도 에러 없이 진행)
load_dotenv()

# 데이터베이스 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "aws-0-ap-northeast-2.pooler.supabase.com"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres.ogvxxvrwxorfxhlurora"),
    "password": os.getenv("DB_PASSWORD", "FJDKSL123!@#"),
    "sslmode": "require"
}

# 네트워크 설정
ROUTER_IP = os.getenv("ROUTER_IP", "192.168.0.1")
PING_COUNT = int(os.getenv("PING_COUNT", "4"))
PING_TIMEOUT = int(os.getenv("PING_TIMEOUT", "5"))

# 라즈베리파이용 설정
IS_RASPBERRY_PI = os.getenv("IS_RASPBERRY_PI", "false").lower() == "true"

# 스케줄 설정
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "1"))
