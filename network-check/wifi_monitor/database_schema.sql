-- WiFi 모니터링 시스템 데이터베이스 스키마
-- PostgreSQL용

-- 데이터베이스 생성 (필요시)
-- CREATE DATABASE network_monitor;

-- 테이블 생성
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

-- 인덱스 생성
CREATE INDEX idx_timestamp ON network_checks(timestamp);
CREATE INDEX idx_check_type ON network_checks(check_type);
CREATE INDEX idx_reachable ON network_checks(reachable);

-- 테이블 설명
COMMENT ON TABLE network_checks IS '네트워크 체크 결과 저장 테이블';
COMMENT ON COLUMN network_checks.check_type IS '체크 유형: router 또는 speed_test';
COMMENT ON COLUMN network_checks.target IS '체크 대상 (IP 주소 또는 도메인)';
COMMENT ON COLUMN network_checks.reachable IS '접속 성공 여부';
COMMENT ON COLUMN network_checks.latency_ms IS '응답 시간 (밀리초)';
COMMENT ON COLUMN network_checks.packet_loss IS '패킷 손실률 (0.0 ~ 1.0)';
COMMENT ON COLUMN network_checks.download_mbps IS '다운로드 속도 (Mbps, speed_test만 해당)';
COMMENT ON COLUMN network_checks.upload_mbps IS '업로드 속도 (Mbps, speed_test만 해당)';
COMMENT ON COLUMN network_checks.error_message IS '실패 시 에러 메시지';
