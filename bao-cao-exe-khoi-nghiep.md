# BÁO CÁO Ý TƯỞNG KHỞI NGHIỆP — MÔN EXE
> **Dự án:** TaxAI Vietnam — Trợ lý thuế TNCN thông minh

---

## 1. TÊN Ý TƯỞNG

**TaxAI Vietnam**
*(Phụ đề: "Trợ lý thuế cá nhân thông minh — Đúng luật, Tức thì, Miễn phí")*

---

## 2. LĨNH VỰC / NGÀNH

- **Lĩnh vực chính:** FinTech × AI (Tài chính công nghệ + Trí tuệ nhân tạo)
- **Phân khúc:** LegalTech / Tax Technology
- **Thị trường:** Việt Nam (giai đoạn 1), mở rộng khu vực ASEAN (giai đoạn 2)

---

## 3. VẤN ĐỀ CẦN GIẢI QUYẾT

### Bối cảnh

Năm 2026, hệ thống thuế TNCN Việt Nam trải qua **thay đổi lớn nhất trong lịch sử**:
- Biểu thuế rút từ 7 bậc → **5 bậc** (Luật 109/2025/QH15)
- Giảm trừ gia cảnh tăng **+40%** (từ 11tr → 15,5tr/tháng)
- Ngưỡng miễn thuế kinh doanh tăng gấp đôi: **1 tỷ/năm**
- Thuế khoán **bãi bỏ** hoàn toàn từ 01/01/2026
- Sàn TMĐT **tự động khấu trừ thuế** từ 01/07/2025

### Vấn đề người dùng gặp phải

| # | Vấn đề | Nhóm bị ảnh hưởng |
|---|--------|-------------------|
| 1 | **Không biết mình có phải nộp thuế không** — luật thay đổi quá nhanh, thông tin cũ lan tràn | Freelancer, KOL, seller online |
| 2 | **Tính thuế sai** — nhầm biểu thuế cũ/mới, nhầm trần BHXH/BHTN theo vùng | Người lao động lương cao |
| 3 | **Không biết thủ tục quyết toán** — eTax Mobile, Cổng thuế, hạn nộp... | Toàn bộ người nộp thuế |
| 4 | **Sợ hỏi kế toán/luật sư** vì tốn tiền, ngại tiếp xúc | Lao động trẻ, freelancer |
| 5 | **Thông tin trên mạng chồng chéo, lỗi thời** — tra Google ra kết quả cũ từ 2020-2024 | Tất cả |

### Quy mô vấn đề (số liệu thực tế)

- **~52 triệu** người có thu nhập chịu thuế tại Việt Nam (Tổng cục Thuế, 2025)
- **~8 triệu** freelancer / lao động tự do (không có kế toán hỗ trợ)
- **~3,5 triệu** người bán hàng online trên Shopee, TikTok, Facebook (2025)
- Hàng năm có **hàng triệu** hồ sơ quyết toán thuế TNCN chậm nộp do không biết thủ tục

---

## 4. GIẢI PHÁP / CHI TIẾT Ý TƯỞNG

### Mô tả sản phẩm

**TaxAI Vietnam** là ứng dụng web/mobile tích hợp AI, cho phép bất kỳ người dùng nào **hỏi câu hỏi về thuế TNCN bằng ngôn ngữ tự nhiên** và nhận được câu trả lời chính xác, có căn cứ pháp lý, tức thì — giống như đang hỏi một chuyên gia thuế riêng.

### 4 Tính năng cốt lõi

#### Tính năng 1: Chatbot AI Hỏi-Đáp Thuế
- Người dùng gõ câu hỏi bằng tiếng Việt thông thường:  
  *"Tôi lương 30 triệu, có 2 con nhỏ, phải đóng thuế bao nhiêu?"*  
  *"Tôi bán Shopee 900 triệu năm nay có cần nộp thuế không?"*
- AI phân tích, tra cứu đúng file pháp lý, trả lời từng bước rõ ràng
- Mỗi câu trả lời **bắt buộc kèm căn cứ pháp lý** (Luật/Nghị định/Thông tư)
- Tích hợp **Anti-Hallucination System** (8 luật cứng) — không bao giờ bịa số liệu

#### Tính năng 2: Máy Tính Thuế Tương Tác
- User nhập: Lương gross, số người phụ thuộc, vùng lao động, loại thu nhập
- AI tự chạy **8-bước Calculation Checklist** đã được kiểm toán
- Xuất ra bảng tính từng bậc thuế lũy tiến, BHXH/BHYT/BHTN riêng biệt
- So sánh: "Bạn tiết kiệm X triệu so với quy định cũ 2025"

#### Tính năng 3: Lịch Nhắc Thuế Cá Nhân
- Dựa vào hồ sơ người dùng → tự tạo lịch kê khai/nộp thuế phù hợp
- Push notification nhắc trước deadline 7 ngày, 1 ngày
- Cover toàn bộ: quyết toán năm, kê khai quý, hạn đăng ký NPT

#### Tính năng 4: Cập Nhật Luật Tự Động (AI-Assisted)
- Hệ thống theo dõi văn bản pháp luật mới từ gdt.gov.vn, chinhphu.vn
- AI đọc, tóm tắt thay đổi → human review → cập nhật knowledge base
- Người dùng **luôn có thông tin thuế mới nhất**, không lo đọc nhầm luật cũ

### Nền tảng kỹ thuật

```
User Interface (Web/Mobile)
        │
        ▼
AI Chatbot Engine (LLM + Knowledge Base)
        │
        ├── Knowledge Base: 12 file reference thuế TNCN (đã có sẵn)
        ├── Anti-Hallucination: 8 rules + 3 Verification Gates
        ├── Calculator Engine: Logic tính thuế 8 bước
        └── Update Pipeline: Theo dõi văn bản pháp luật mới
```

---

## 5. KHÁCH HÀNG MỤC TIÊU

### Phân khúc chính (Primary)

| Nhóm | Quy mô ước tính | Nhu cầu chính |
|------|----------------|---------------|
| **Freelancer / KOL / Người bán online** | ~8-11 triệu người | Biết mình có phải nộp thuế không, nộp bao nhiêu |
| **Người đi làm lương từ 15-50 triệu/tháng** | ~5 triệu người | Tính thuế đúng, quyết toán đúng |
| **Người vừa nghỉ việc / rút BHXH** | ~1-2 triệu/năm | Điều kiện rút, tính tiền BHXH/BHTN |

### Phân khúc phụ (Secondary)
- **Sinh viên / Người đi làm lần đầu** — chưa hiểu hệ thống thuế
- **HR / Kế toán SME** — cần công cụ tra cứu nhanh, không sai
- **Người nước ngoài (Expat)** làm việc tại Việt Nam

---

## 6. ĐIỂM KHÁC BIỆT SO VỚI CÁC ỨNG DỤNG KHÁC

### So sánh cạnh tranh

| Tiêu chí | TaxAI Vietnam | eTax Mobile (Nhà nước) | Google / ChatGPT | Kế toán tư nhân |
|----------|:---:|:---:|:---:|:---:|
| Hỏi bằng ngôn ngữ tự nhiên | ✅ | ❌ | ⚠️ (có thể sai) | ✅ |
| Cập nhật luật 2026 chính xác | ✅ | ✅ | ❌ (thường lỗi thời) | ✅ |
| Có căn cứ pháp lý mỗi câu trả lời | ✅ | ❌ | ❌ | ✅ |
| Anti-Hallucination (không bịa số) | ✅ | N/A | ❌ | ✅ |
| Miễn phí | ✅ | ✅ | ⚠️ (giới hạn) | ❌ (300-500k/giờ) |
| Tính thuế từng bước tương tác | ✅ | ⚠️ (cơ bản) | ❌ | ✅ |
| Nhắc lịch nộp thuế cá nhân hóa | ✅ | ⚠️ | ❌ | ❌ |
| Cover BHXH + BHTN | ✅ | ❌ | ❌ | ✅ |
| Cập nhật tự động khi luật mới | ✅ | ⚠️ (chậm) | ❌ | Tùy người |
| Khả năng mở rộng scale | ✅ (AI) | ❌ | N/A | ❌ |

### 3 Lợi thế cạnh tranh cốt lõi (USP)

1. **"Chuyên gia thuế trong túi, miễn phí"** — eTax Mobile chỉ làm được khai nộp, không giải thích. ChatGPT giải thích nhưng hay sai. TaxAI vừa giải thích đúng, vừa có nguồn pháp lý.

2. **Hệ thống chống sai sót AI độc quyền** — 8 Anti-Hallucination Rules + 3 Verification Gates + Calculation Checklist 8 bước — là "hộp an toàn" mà các AI tổng quát không có.

3. **Knowledge base thuế VN chuyên sâu nhất** — đã qua 4 vòng kiểm toán, đạt 9.2/10, cover từ lương đến freelancer, KOL, expat, BHXH, BHTN — không sản phẩm nào trên thị trường làm được trọn vẹn như vậy.

---

## 7. MÔ HÌNH KINH DOANH (Business Model)

### Giai đoạn 1 — Freemium (Năm 1)

| Tier | Giá | Tính năng |
|------|-----|-----------|
| **Free** | 0đ | 10 câu hỏi/tháng, tính thuế cơ bản, lịch nhắc |
| **Pro** | 49.000đ/tháng | Không giới hạn câu hỏi, xuất PDF báo cáo thuế, ưu tiên cập nhật |
| **Business** | 299.000đ/tháng | Dành cho HR/kế toán, quản lý nhiều nhân viên, API access |

### Giai đoạn 2 — B2B (Năm 2-3)

- **Bán API** cho phần mềm kế toán (MISA, Fast, Bravo) tích hợp chatbot thuế
- **White-label** cho ngân hàng, fintech (VPBank, Techcombank...) tích hợp tư vấn thuế vào app
- **Đối tác Tổng cục Thuế** — cung cấp giải pháp hỗ trợ người nộp thuế

### Ước tính doanh thu (năm 1)

```
Mục tiêu: 50.000 user Free + 2.000 user Pro + 50 tài khoản Business
Doanh thu ước tính:
  Pro:      2.000 × 49.000đ × 12 tháng = ~1.17 tỷ đồng/năm
  Business: 50 × 299.000đ × 12 tháng  = ~180 triệu đồng/năm
  Tổng:     ~1.35 tỷ đồng/năm
```

---

## 8. LỘ TRÌNH PHÁT TRIỂN (Roadmap)

```
Tháng 1-2  │ MVP: Web chatbot + Calculator + 12 reference files (ĐÃ CÓ)
Tháng 3-4  │ Beta testing: 500 người dùng, thu thập feedback
Tháng 5-6  │ Ra mắt chính thức, chiến dịch content marketing
Tháng 7-9  │ Mobile app (iOS/Android), tính năng lịch nhắc
Tháng 10-12│ B2B API, đàm phán đối tác kế toán/ngân hàng
Năm 2       │ Mở rộng sang BHXH Calculator đầy đủ, mở rộng thị trường
```

---

## 9. RỦI RO & GIẢI PHÁP

| Rủi ro | Mức độ | Giải pháp |
|--------|--------|-----------|
| Luật thuế thay đổi liên tục | 🔴 Cao | AI-assisted update pipeline, human review trước khi publish |
| AI đưa ra câu trả lời sai | 🔴 Cao | 8 Anti-Hallucination Rules + bắt buộc disclaimer + luôn dẫn nguồn |
| Cạnh tranh từ ChatGPT/Gemini | 🟡 Trung bình | Chuyên sâu hóa — họ generalist, ta specialist thuế VN |
| Người dùng không tin AI về thuế | 🟡 Trung bình | Luôn kèm nguồn pháp lý, cảnh báo "không thay thế tư vấn chuyên nghiệp" |
| Chi phí LLM API cao | 🟡 Trung bình | Optimize prompt, cache câu hỏi phổ biến, dùng model nhỏ cho câu đơn giản |

---

## 10. ĐỘI NGŨ (Team Canvas)

| Vai trò | Kỹ năng cần thiết |
|---------|-----------------|
| **Founder / Product** | Hiểu luật thuế VN, quản lý sản phẩm |
| **AI Engineer** | LLM integration, RAG, prompt engineering |
| **Frontend Developer** | React/Next.js, UX design |
| **Tax Advisor (part-time)** | Kiểm toán nội dung, xác nhận pháp lý |

> 💡 **Lợi thế hiện tại:** Knowledge base (12 files, 9.2/10 audit score) đã sẵn có — MVP có thể build trong **2 tháng** với team 2-3 người.

---

## 11. PHÂN TÍCH SWOT

| | Điểm mạnh (S) | Điểm yếu (W) |
|---|---|---|
| **Nội bộ** | Knowledge base chuyên sâu đã có; Anti-hallucination system; Không có đối thủ direct | Cần cập nhật khi luật thay đổi; Phụ thuộc LLM API bên ngoài |

| | Cơ hội (O) | Thách thức (T) |
|---|---|---|
| **Bên ngoài** | Luật thuế mới 2026 tạo nhu cầu khổng lồ; Xu hướng số hóa thuế của Nhà nước; Thị trường AI chatbot tăng trưởng nhanh | Rủi ro pháp lý nếu AI tư vấn sai; Tâm lý người VN thích hỏi người thật |

---

## 12. CHỈ SỐ THÀNH CÔNG (KPIs)

| KPI | Mục tiêu Tháng 6 | Mục tiêu Năm 1 |
|-----|-----------------|---------------|
| Người dùng đăng ký | 5.000 | 50.000 |
| Câu hỏi được trả lời/ngày | 500 | 5.000 |
| Tỷ lệ hài lòng (CSAT) | ≥ 4.0/5 | ≥ 4.2/5 |
| Tỷ lệ chuyển đổi Free → Pro | 3% | 5% |
| Độ chính xác câu trả lời (audit) | ≥ 90% | ≥ 95% |

---

## 13. TẦM NHÌN DÀI HẠN

> **"Trở thành nền tảng tư vấn tài chính cá nhân AI hàng đầu Đông Nam Á, bắt đầu từ thuế TNCN Việt Nam."**

Sau thuế TNCN → mở rộng sang:
- Bảo hiểm xã hội toàn diện (BHXH, BHYT, BHTN)
- Thuế cho doanh nghiệp nhỏ (SME)
- Lập kế hoạch tài chính cá nhân (PFM)
- Thị trường: Thái Lan, Indonesia, Philippines (luật thuế tương đồng)

---

## 14. 📎 TÀI LIỆU ĐÍNH KÈM (Proof of Concept)

Dự án đã có **sẵn MVP Data Layer** — không phải ý tưởng trên giấy:

| Tài liệu | Mô tả | Trạng thái |
|----------|-------|-----------|
| `SKILL.md` | Master AI prompt + workflow 7 bước + 8 Anti-Hallucination Rules | ✅ Hoàn chỉnh |
| `references/tong-quan-thue.md` | Biểu thuế 5 bậc, giảm trừ gia cảnh, trần BHXH/BHTN | ✅ Hoàn chỉnh |
| `references/vi-du-tinh-thue.md` | 7 case study tính thuế kiểm toán | ✅ Hoàn chỉnh |
| `references/freelancer-guide.md` | Hướng dẫn Freelancer/KOL/Seller | ✅ Hoàn chỉnh |
| `references/sop-quyet-toan.md` | SOP quyết toán 9 bước eTax Mobile | ✅ Hoàn chỉnh |
| `references/nguoi-nuoc-ngoai-guide.md` | Expat, DTA, flat 20% | ✅ Hoàn chỉnh |
| `references/bhxh-rut-mot-lan-guide.md` | BHXH rút 1 lần: 2 nhóm, 4 case study | ✅ Hoàn chỉnh |
| `references/bhtn-tro-cap-guide.md` | Trợ cấp thất nghiệp: công thức, quy trình | ✅ Hoàn chỉnh |
| `pending-review/` | 5 văn bản pháp luật mới nhất 2026 đang tích hợp | 🔄 Đang xử lý |

> **Audit Score: 9.2/10** — đã qua 4 vòng kiểm toán độc lập.

---

*Báo cáo chuẩn bị cho môn EXE — Entrepreneurship Execution | 05/2026*
*Dữ liệu căn cứ: Luật 109/2025/QH15 | NĐ 141/2026/NĐ-CP | NĐ 68/2026/NĐ-CP | NQ 198/2025/QH15*
