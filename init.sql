-- ═══════════════════════════════════════
-- TaxAI Vietnam - Database Initialization
-- Creates: n8n database + taxai tables
-- ═══════════════════════════════════════

-- Create separate database for n8n
CREATE DATABASE n8n;

-- ═══════════════════════════════════════
-- TaxAI tables (on default 'taxai' database)
-- ═══════════════════════════════════════

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ───────────────────────────────────────
-- 1. Knowledge Base chunks for RAG
-- ───────────────────────────────────────
CREATE TABLE knowledge_chunks (
    id SERIAL PRIMARY KEY,
    source_file VARCHAR(100) NOT NULL,
    section_title VARCHAR(200),
    chunk_text TEXT NOT NULL,
    embedding VECTOR(768),
    confidence VARCHAR(10) DEFAULT 'HIGH',
    law_reference VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chunks_source ON knowledge_chunks(source_file);
CREATE INDEX idx_chunks_confidence ON knowledge_chunks(confidence);
-- ivfflat index will be created after data ingestion (needs rows first)

-- ───────────────────────────────────────
-- 2. Tax Deadlines (Agent 3)
-- ───────────────────────────────────────
CREATE TABLE tax_deadlines (
    id SERIAL PRIMARY KEY,
    deadline_date DATE NOT NULL,
    description TEXT NOT NULL,
    user_type VARCHAR(50) NOT NULL,
    quarter VARCHAR(10),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_deadlines_date ON tax_deadlines(deadline_date);
CREATE INDEX idx_deadlines_type ON tax_deadlines(user_type);

-- Seed deadline data (from deadline-tracker.md)
INSERT INTO tax_deadlines (deadline_date, description, user_type, quarter, status) VALUES
-- Quyết toán 2025
('2026-04-30', 'Nộp hồ sơ quyết toán thuế TNCN 2025', 'salaried', NULL, 'passed'),
('2026-04-30', 'Nộp tiền thuế phải nộp thêm (QT 2025)', 'salaried', NULL, 'passed'),
-- Kê khai quý (DT > 1 tỷ)
('2026-04-30', 'Kê khai thuế quý 1/2026 (01/01 - 31/03)', 'hkd_over_1ty', 'Q1', 'passed'),
('2026-07-31', 'Kê khai thuế quý 2/2026 (01/04 - 30/06)', 'hkd_over_1ty', 'Q2', 'pending'),
('2026-10-31', 'Kê khai thuế quý 3/2026 (01/07 - 30/09)', 'hkd_over_1ty', 'Q3', 'pending'),
('2027-01-31', 'Kê khai thuế quý 4/2026 (01/10 - 31/12)', 'hkd_over_1ty', 'Q4', 'pending'),
-- Kê khai năm (DT ≤ 1 tỷ)
('2027-01-31', 'Kê khai doanh thu năm 2026', 'hkd_under_1ty', NULL, 'pending'),
-- Quyết toán 2026
('2027-04-30', 'Nộp hồ sơ quyết toán thuế TNCN 2026', 'salaried', NULL, 'pending'),
('2027-04-30', 'Nộp hồ sơ quyết toán thuế TNCN 2026', 'freelancer', NULL, 'pending'),
-- Freelancer/KOL kê khai quý
('2026-07-31', 'Kê khai thuế quý 2/2026', 'freelancer', 'Q2', 'pending'),
('2026-10-31', 'Kê khai thuế quý 3/2026', 'freelancer', 'Q3', 'pending'),
('2027-01-31', 'Kê khai thuế quý 4/2026', 'freelancer', 'Q4', 'pending');

-- ───────────────────────────────────────
-- 3. Conversations Log
-- ───────────────────────────────────────
CREATE TABLE conversations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id VARCHAR(100),
    agent_type VARCHAR(20) NOT NULL,
    user_message TEXT NOT NULL,
    agent_response TEXT,
    sources_cited JSONB,
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_agent ON conversations(agent_type);
CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_conversations_created ON conversations(created_at);

-- ───────────────────────────────────────
-- 4. Law Updates (Agent 4 - Crawler)
-- ───────────────────────────────────────
CREATE TABLE law_updates (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(200) UNIQUE NOT NULL,
    document_number VARCHAR(100),
    source_url TEXT,
    source_site VARCHAR(50),
    summary TEXT,
    full_text TEXT,
    changes JSONB,
    affected_files JSONB,
    impact_level VARCHAR(10) DEFAULT 'LOW',
    patch_suggestions JSONB,
    effective_date DATE,
    is_reviewed BOOLEAN DEFAULT FALSE,
    crawled_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_law_updates_impact ON law_updates(impact_level);
CREATE INDEX idx_law_updates_crawled ON law_updates(crawled_at);

-- ───────────────────────────────────────
-- 5. Notifications
-- ───────────────────────────────────────
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    related_law_update_id INTEGER REFERENCES law_updates(id),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_unread ON notifications(is_read) WHERE is_read = FALSE;
