# n8n Workflows

Thư mục chứa exported JSON workflows cho n8n.

## Danh sách Workflows

| File | Workflow | Mô tả |
|------|---------|-------|
| `orchestrator.json` | TaxAI Orchestrator | Main: Webhook → Classify → Route |
| `qa-agent.json` | TaxAI QA Agent | RAG search → LLM answer → Verify |
| `calculator-agent.json` | TaxAI Calculator | Parse → Math → Format |
| `calendar-agent.json` | TaxAI Calendar | DB query → SOP → Format |
| `law-crawler-agent.json` | TaxAI Law Crawler | Crawl 4 nguồn → Analyze → Save |

## Import

1. Mở n8n UI: `http://localhost:5678`
2. Settings → Import Workflow
3. Import lần lượt từng file JSON

## Webhook Endpoints

Sau khi import, các webhook sẽ available tại:
- `POST /webhook/taxai-chat` (Orchestrator)
- `POST /webhook/taxai-calculate` (Calculator)
- `POST /webhook/taxai-calendar` (Calendar)
- `POST /webhook/taxai-update` (Law Update)
