<div align="center">

# 🇻🇳 TaxAI VietNam

### Trợ lý Thuế TNCN Thông Minh — Multi-Agent System

*Hỏi bằng tiếng Việt, trả lời chính xác, có căn cứ pháp lý*

[![Version](https://img.shields.io/badge/version-2.0.0-0078D4?style=for-the-badge)](https://github.com/viduvan/TaxAI-VietNam)
[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![n8n](https://img.shields.io/badge/n8n-1.116-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

</div>

---

## 📖 Giới Thiệu

**TaxAI Vietnam** là hệ thống AI multi-agent giúp người dùng tra cứu thuế Thu nhập Cá nhân (TNCN) Việt Nam theo Luật mới **109/2025/QH15** (có hiệu lực từ 01/01/2026). Hệ thống cung cấp:

- Chatbot AI — hỏi đáp thuế bằng ngôn ngữ tự nhiên
- Máy tính thuế — tính thuế tương tác 5 bậc lũy tiến
- Lịch nhắc thuế — cá nhân hóa theo nhóm đối tượng
- Cập nhật luật tự động — crawl văn bản pháp luật mới

> **Disclaimer:** Thông tin chỉ mang tính tham khảo, KHÔNG thay thế tư vấn thuế chuyên nghiệp.

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Browser)                          │
│                      localhost:3000                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│  IMAGE 1: Web UI                                                │
│  React 19 + Vite 8 + TypeScript                                 │
│  Port: 3000                                                     │
└──────────────────────────┬───────────────────────────────────────┘
                           │ REST API
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│  IMAGE 2: Tax Service (FastAPI)                                  │
│  /api/chat → /api/calculate → /api/calendar → /api/updates      │
│  Port: 8000                                                      │
└────────┬─────────────────┬───────────────────┬───────────────────┘
         │                 │                   │
         ▼                 ▼                   ▼
┌────────────────┐ ┌───────────────┐ ┌─────────────────────────────┐
│  PostgreSQL    │ │  Ollama (LLM) │ │  IMAGE 3: n8n (Queue Mode)  │
│  + pgvector    │ │  GPU-enabled  │ │  Orchestrator → 4 Agents    │
│  Port: 5432    │ │  Port: 11434  │ │  Port: 5678                 │
└────────────────┘ └───────────────┘ │  + Redis (Queue)            │
                                     │  + n8n-workers (x2)         │
                                     └─────────────────────────────┘
```

### 4 AI Agents (n8n Sub-workflows)

| Agent | Chức năng | Workflow |
|-------|----------|----------|
| 🔀 **Orchestrator** | Phân loại câu hỏi → route đến agent phù hợp | `orchestrator.json` |
| 💬 **QA Agent** | RAG search knowledge base → LLM trả lời → Verify | `qa-agent.json` |
| 🧮 **Calculator Agent** | Parse thu nhập → Tính thuế 5 bậc → Format kết quả | `calculator-agent.json` |
| 📅 **Calendar Agent** | Tra deadline từ DB → Áp SOP → Format lịch | `calendar-agent.json` |
| 🕷️ **Law Crawler Agent** | Crawl 4 nguồn luật → Phân tích → Lưu DB | `law-crawler-agent.json` |

---

## 📊 Số Liệu Thuế Nhanh (2026)

| Chỉ số | Giá trị | Căn cứ |
|--------|---------|--------|
| Giảm trừ bản thân | **15,5 tr/tháng** (186 tr/năm) | NQ 110/2025/UBTVQH15 |
| Giảm trừ người phụ thuộc | **6,2 tr/tháng** | NQ 110/2025/UBTVQH15 |
| Ngưỡng miễn thuế HKD | **1 tỷ/năm** *(cũ: 500tr)* | NĐ 141/2026/NĐ-CP |
| Biểu thuế lũy tiến | **5 bậc** (5% → 35%) | Luật 109/2025/QH15 |
| Thuế khoán | **Bãi bỏ** từ 01/01/2026 | NQ 198/2025/QH15 |
| Lệ phí môn bài | **Bãi bỏ** từ 01/01/2026 | Luật 109/2025/QH15, Đ.35 |

---

## 🚀 Cài Đặt & Chạy

### Yêu cầu

- Docker & Docker Compose v2+
- GPU (khuyến nghị, cho Ollama LLM)
- 8GB+ RAM

### 1. Clone & cấu hình

```bash
git clone https://github.com/viduvan/TaxAI-VietNam.git
cd TaxAI-VietNam

# Tạo file .env từ template
cp .env.example .env
# Sửa các biến: DB password, Redis password, LLM provider...
```

### 2. Khởi động toàn bộ hệ thống

```bash
docker compose up -d
```

### 3. Import n8n workflows

```bash
open http://localhost:5678
```

### 4. Ingest knowledge base

```bash
cd scripts
python ingest_knowledge.py
```

### 5. Truy cập

- 🌐 **Web UI:** http://localhost:3000
- 📡 **API Docs:** http://localhost:8000/docs
- ⚙️ **n8n Dashboard:** http://localhost:5678

---

## 📁 Cấu Trúc Dự Án

```
TaxAI-VietNam/
│
├── backend/                          # FastAPI backend
│   ├── main.py                       # Entry point
│   ├── routes/                       # API endpoints
│   │   ├── chat.py                   #   /api/chat
│   │   ├── calculator.py             #   /api/calculate
│   │   ├── calendar.py               #   /api/calendar
│   │   └── updates.py                #   /api/updates
│   ├── services/                     # Business logic
│   │   ├── database.py               #   PostgreSQL connection
│   │   ├── llm_provider.py           #   Multi-LLM adapter
│   │   └── n8n_client.py             #   n8n webhook client
│   ├── requirements.txt
│   └── Dockerfile
│
├── web/                              # React frontend (Vite)
│   ├── src/
│   │   ├── App.tsx                   # Main application
│   │   ├── index.css                 # Design system
│   │   └── App.css                   # Component styles
│   ├── package.json
│   └── Dockerfile
│
├── n8n-workflows/                    # n8n exported workflows
│   ├── orchestrator.json             # Main routing workflow
│   ├── qa-agent.json                 # Q&A with RAG
│   ├── calculator-agent.json         # Tax calculator
│   ├── calendar-agent.json           # Deadline tracker
│   └── law-crawler-agent.json        # Legal document crawler
│
├── references/                       # 📚 Knowledge base
│   ├── tong-quan-thue.md             # Biểu thuế 5 bậc, giảm trừ gia cảnh
│   ├── vi-du-tinh-thue.md            # 7 ví dụ tính thuế
│   ├── sop-quyet-toan.md             # SOP quyết toán eTax Mobile
│   ├── freelancer-guide.md           # Freelancer, KOL, seller
│   ├── nguoi-nuoc-ngoai-guide.md     # Expat, cư trú, DTA
│   ├── thue-khoan-guide.md           # Thuế khoán bãi bỏ 2026
│   ├── bhxh-rut-mot-lan-guide.md     # BHXH rút 1 lần
│   ├── bhtn-tro-cap-guide.md         # Trợ cấp thất nghiệp
│   ├── deadline-tracker.md           # Lịch nộp thuế 2026
│   ├── faq.md                        # Câu hỏi thường gặp
│   ├── system-flow.md                # Flow diagrams
│   ├── changelog.md                  # Lịch sử cập nhật
│   └── sources.md                    # Nguồn tham khảo
│
├── scripts/
│   └── ingest_knowledge.py           # Script nạp knowledge vào pgvector
│
├── SKILL.md                          # 📚 Master AI prompt
├── docker-compose.yml                # 7-container orchestration
├── init.sql                          # Database schema + seed data
├── bao-cao-exe-khoi-nghiep.md        # Báo cáo ý tưởng khởi nghiệp
└── .env                              # Environment variables (not committed)
```

---

## 🛠️ Tech Stack

| Layer | Công nghệ |
|-------|----------|
| **Frontend** | React 19, Vite 8, TypeScript 6 |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic |
| **AI/LLM** | Ollama (local), OpenAI, Anthropic, Groq (multi-provider) |
| **Orchestration** | n8n 1.116 (Queue Mode), Redis 7.2 |
| **Database** | PostgreSQL 15 + pgvector 0.6 (RAG embeddings) |
| **Infra** | Docker Compose, multi-container deployment |

---

## 🔐 Tính Năng An Toàn

Hệ thống được thiết kế với **3 Verification Gates + 8 Anti-Hallucination Rules**:

- 🔒 **Gate 1 — Freshness Check:** Kiểm tra data có còn hiệu lực không
- 🔒 **Gate 2 — Cross-Verify:** Đối chiếu số liệu giữa các nguồn
- 🔒 **Gate 3 — Source Citation:** Bắt buộc ghi căn cứ pháp lý mỗi output
- 🚫 Không bao giờ bịa số liệu thuế
- 🚫 Không tự suy luận quy định khi chưa có trong knowledge base
- 📐 Tính thuế bắt buộc tách từng bậc (Calculation Checklist 8 bước)

---

## 👥 Nhóm Đối Tượng Hỗ Trợ

| Nhóm | Mô tả |
|------|-------|
| 💼 Người làm công ăn lương | Quyết toán thuế, eTax Mobile, giảm trừ gia cảnh |
| 🎨 Freelancer / KOL | Ngưỡng doanh thu, kê khai theo quý/năm |
| 🛒 Người bán hàng online | Shopee, TikTok Shop, Facebook — thuế TMĐT |
| 🌏 Người nước ngoài (Expat) | Cư trú/không cư trú, DTA, flat 20% |
| 📋 Nghỉ việc / Rút BHXH | Điều kiện rút 1 lần, 2 nhóm, 4 case study |
| 🛡️ Thất nghiệp / BHTN | Trợ cấp 60% lương, quy trình đăng ký |

---

## 📜 Bản Quyền & Attribution

#### Các file thuộc bản quyền tác giả gốc (dotanminh)

| File | Mô tả |
|------|-------|
| `SKILL.md` | Master AI prompt + workflow 7 bước + 8 Anti-Hallucination Rules |
| `references/tong-quan-thue.md` | Biểu thuế 5 bậc, giảm trừ gia cảnh |
| `references/vi-du-tinh-thue.md` | 7 ví dụ tính thuế |
| `references/sop-quyet-toan.md` | SOP quyết toán eTax Mobile |
| `references/freelancer-guide.md` | Hướng dẫn Freelancer/KOL/Seller |
| `references/nguoi-nuoc-ngoai-guide.md` | Thuế người nước ngoài |
| `references/thue-khoan-guide.md` | Thuế khoán bãi bỏ 2026 |
| `references/bhxh-rut-mot-lan-guide.md` | BHXH rút 1 lần |
| `references/bhtn-tro-cap-guide.md` | Trợ cấp thất nghiệp |
| `references/deadline-tracker.md` | Lịch nộp thuế 2026 |
| `references/faq.md` | Câu hỏi thường gặp |
| `references/system-flow.md` | Flow diagrams |
| `references/changelog.md` | Lịch sử cập nhật |
| `references/sources.md` | Nguồn tham khảo |

### Multi-Agent System — Phát triển bởi viduvan

Toàn bộ **hạ tầng kỹ thuật multi-agent** được phát triển bởi [**@viduvan**](https://github.com/viduvan), bao gồm:

- `backend/` — FastAPI backend, routes, services, LLM provider adapter
- `web/` — React 19 frontend (Vite + TypeScript)
- `n8n-workflows/` — 5 workflow AI agents (orchestrator + 4 sub-agents)
- `docker-compose.yml` — 7-container orchestration
- `init.sql` — Database schema (pgvector RAG + deadline + conversations + law updates)
- `scripts/` — Knowledge ingestion pipeline
- `bao-cao-exe-khoi-nghiep.md` — Báo cáo ý tưởng khởi nghiệp

---

## 🔗 Liên Kết

| | |
|---|---|
| 🛠️ **Multi-Agent System** | [viduvan/TaxAI-VietNam](https://github.com/viduvan/TaxAI-VietNam) |
| 📡 **Tổng cục Thuế** | https://gdt.gov.vn |
| 📱 **Cổng thuế cá nhân** | https://canhan.gdt.gov.vn |

---

## 📄 License

Dự án được phát hành theo giấy phép [MIT License](LICENSE).

---

<div align="center">

*Cập nhật: 20/05/2026 | Luật 109/2025/QH15 | NĐ 141/2026/NĐ-CP | NĐ 68/2026/NĐ-CP*

**Developed with ❤️ by [@viduvan](https://github.com/viduvan)**

</div>
