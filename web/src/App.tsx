import { useState, useEffect } from 'react'
import './index.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

type Page = 'home' | 'chat' | 'calculator' | 'calendar' | 'updates'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface CalcResult {
  calculation_steps?: { step: number; label: string; value: number | null; formula: string }[]
  total_tax?: number
  effective_rate?: number
  net_salary?: number
  comparison_2025?: { tax_2025: number; tax_2026: number; saved: number; saved_year: number }
  answer?: string
  disclaimer?: string
}

interface Deadline {
  description: string
  deadline_formatted: string
  days_left: number
  urgency: string
  user_type: string
}

function App() {
  const [page, setPage] = useState<Page>('home')

  return (
    <div className="app">
      <nav className="navbar">
        <div className="container">
          <a className="logo" onClick={() => setPage('home')} style={{ cursor: 'pointer' }}>
            <span className="logo-icon">🇻🇳</span>
            <span className="logo-text">TaxAI Vietnam</span>
          </a>
          <ul className="nav-links">
            <li><a className={page === 'chat' ? 'active' : ''} onClick={() => setPage('chat')}>🤖 Hỏi đáp</a></li>
            <li><a className={page === 'calculator' ? 'active' : ''} onClick={() => setPage('calculator')}>🧮 Tính thuế</a></li>
            <li><a className={page === 'calendar' ? 'active' : ''} onClick={() => setPage('calendar')}>📅 Lịch thuế</a></li>
            <li><a className={page === 'updates' ? 'active' : ''} onClick={() => setPage('updates')}>🔄 Cập nhật</a></li>
          </ul>
        </div>
      </nav>

      {page === 'home' && <HomePage onNavigate={setPage} />}
      {page === 'chat' && <ChatPage />}
      {page === 'calculator' && <CalculatorPage />}
      {page === 'calendar' && <CalendarPage />}
      {page === 'updates' && <UpdatesPage />}
    </div>
  )
}

/* ═══ HOME PAGE ═══ */
function HomePage({ onNavigate }: { onNavigate: (p: Page) => void }) {
  return (
    <main>
      <section className="hero">
        <div className="container">
          <h1>Trợ lý thuế <span>AI thông minh</span></h1>
          <p>Tra cứu thuế TNCN 2026, tính thuế tự động, nhắc deadline — Đúng luật, Tức thì, Miễn phí</p>
        </div>
      </section>
      <div className="container">
        <div className="features-grid">
          <a className="feature-card" onClick={() => onNavigate('chat')}>
            <div className="icon">🤖</div>
            <h3>Hỏi Đáp AI</h3>
            <p>Hỏi bất kỳ câu hỏi nào về thuế TNCN, BHXH, BHTN — AI trả lời có căn cứ pháp lý, không bịa số liệu.</p>
          </a>
          <a className="feature-card" onClick={() => onNavigate('calculator')}>
            <div className="icon">🧮</div>
            <h3>Tính Thuế Tự Động</h3>
            <p>Nhập lương, số NPT, vùng — nhận kết quả thuế 5 bậc lũy tiến chi tiết từng bước + so sánh 2025.</p>
          </a>
          <a className="feature-card" onClick={() => onNavigate('calendar')}>
            <div className="icon">📅</div>
            <h3>Lịch Thuế Cá Nhân</h3>
            <p>Xem deadline sắp tới, SOP quyết toán eTax Mobile 9 bước, checklist hồ sơ cần chuẩn bị.</p>
          </a>
          <a className="feature-card" onClick={() => onNavigate('updates')}>
            <div className="icon">🔄</div>
            <h3>Cập Nhật Luật Mới</h3>
            <p>AI tự động crawl 4 cổng chính thống, phân tích tác động văn bản mới lên thuế TNCN.</p>
          </a>
        </div>
      </div>
    </main>
  )
}

/* ═══ CHAT PAGE ═══ */
function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Xin chào! Tôi là TaxAI — trợ lý thuế TNCN Vietnam 2026. Bạn muốn hỏi gì?\n\n💡 Ví dụ:\n• "Lương 30 triệu, 2 con nhỏ, đóng thuế bao nhiêu?"\n• "Bán Shopee 800 triệu có phải nộp thuế không?"\n• "Điều kiện rút BHXH 1 lần?"' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg }),
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer || 'Xin lỗi, có lỗi xảy ra.' }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: '❌ Không thể kết nối server. Vui lòng kiểm tra lại.' }])
    }
    setLoading(false)
  }

  return (
    <div className="chat-container">
      <div className="page-header">
        <h2>🤖 Hỏi Đáp Thuế AI</h2>
        <p>Hỏi bằng ngôn ngữ tự nhiên — AI trả lời có căn cứ pháp lý</p>
      </div>
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <div className="message-avatar">{m.role === 'user' ? '👤' : '🤖'}</div>
            <div className="message-content">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="loading-dots"><span /><span /><span /></div>
            </div>
          </div>
        )}
      </div>
      <div className="chat-input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Nhập câu hỏi về thuế TNCN, BHXH, BHTN..."
          disabled={loading}
        />
        <button className="btn-send" onClick={sendMessage} disabled={loading}>Gửi</button>
      </div>
    </div>
  )
}

/* ═══ CALCULATOR PAGE ═══ */
function CalculatorPage() {
  const [salary, setSalary] = useState('')
  const [npt, setNpt] = useState('0')
  const [region, setRegion] = useState('I')
  const [result, setResult] = useState<CalcResult | null>(null)
  const [loading, setLoading] = useState(false)

  const calculate = async () => {
    if (!salary) return
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/api/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          gross_salary: parseFloat(salary) * 1000000,
          num_dependents: parseInt(npt),
          region,
          income_type: 'salary',
        }),
      })
      setResult(await res.json())
    } catch {
      setResult({ answer: '❌ Không thể kết nối server.' })
    }
    setLoading(false)
  }

  const fmt = (n: number) => n.toLocaleString('vi-VN')

  return (
    <div className="calc-container">
      <div className="page-header">
        <h2>🧮 Máy Tính Thuế TNCN 2026</h2>
        <p>Biểu thuế 5 bậc lũy tiến — Luật 109/2025/QH15</p>
      </div>
      <div className="calc-form">
        <div className="form-group">
          <label>Lương Gross (triệu/tháng)</label>
          <input type="number" value={salary} onChange={e => setSalary(e.target.value)} placeholder="25" />
        </div>
        <div className="form-group">
          <label>Số Người Phụ Thuộc</label>
          <input type="number" value={npt} onChange={e => setNpt(e.target.value)} min="0" />
        </div>
        <div className="form-group">
          <label>Vùng Lương Tối Thiểu</label>
          <select value={region} onChange={e => setRegion(e.target.value)}>
            <option value="I">Vùng I (HCM, Hà Nội...)</option>
            <option value="II">Vùng II</option>
            <option value="III">Vùng III</option>
            <option value="IV">Vùng IV</option>
          </select>
        </div>
        <div className="form-group">
          <label>Loại Thu Nhập</label>
          <select><option value="salary">Tiền lương, tiền công</option></select>
        </div>
        <button className="btn-calculate" onClick={calculate} disabled={loading}>
          {loading ? 'Đang tính...' : '⚡ Tính Thuế Ngay'}
        </button>
      </div>

      {result && result.calculation_steps && (
        <div className="result-card">
          <h3>📊 Kết Quả Tính Thuế</h3>
          <table className="result-table">
            <thead><tr><th>Bước</th><th>Mục</th><th>Số tiền (VNĐ)</th><th>Công thức</th></tr></thead>
            <tbody>
              {result.calculation_steps.map((s, i) => (
                <tr key={i}>
                  <td>{s.step}</td>
                  <td>{s.label}</td>
                  <td style={{ color: s.value && s.value < 0 ? '#ef4444' : s.value && s.value > 0 ? '#10b981' : 'inherit', fontWeight: 600 }}>
                    {s.value !== null ? fmt(s.value) : '—'}
                  </td>
                  <td style={{ color: '#94a3b8', fontSize: 13 }}>{s.formula}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="result-total">
            Thuế TNCN: {fmt(result.total_tax || 0)} VNĐ/tháng
          </div>
          <p style={{ color: '#94a3b8', fontSize: 13 }}>
            Thuế suất hiệu dụng: {result.effective_rate}% | Lương NET: {fmt(result.net_salary || 0)} VNĐ
          </p>

          {result.comparison_2025 && result.comparison_2025.saved > 0 && (
            <div className="comparison-box">
              <p className="saved">🎉 Tiết kiệm {fmt(result.comparison_2025.saved)} VNĐ/tháng so với 2025</p>
              <p style={{ color: '#94a3b8', fontSize: 13 }}>
                ({fmt(result.comparison_2025.saved_year)} VNĐ/năm | Thuế 2025: {fmt(result.comparison_2025.tax_2025)} → 2026: {fmt(result.comparison_2025.tax_2026)})
              </p>
            </div>
          )}

          <p style={{ color: '#f59e0b', fontSize: 12, marginTop: 16 }}>{result.disclaimer}</p>
        </div>
      )}

      {result && result.answer && !result.calculation_steps && (
        <div className="result-card">
          <p style={{ whiteSpace: 'pre-wrap' }}>{result.answer}</p>
        </div>
      )}
    </div>
  )
}

/* ═══ CALENDAR PAGE ═══ */
function CalendarPage() {
  const [deadlines, setDeadlines] = useState<Deadline[]>([])
  const [loading, setLoading] = useState(false)
  const [loaded, setLoaded] = useState(false)

  const loadDeadlines = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/api/calendar`)
      const data = await res.json()
      setDeadlines(data.deadlines || [])
    } catch {
      setDeadlines([])
    }
    setLoading(false)
    setLoaded(true)
  }

  useEffect(() => { if (!loaded) loadDeadlines() }, [loaded])

  return (
    <div className="calendar-container">
      <div className="page-header">
        <h2>📅 Lịch Nộp Thuế 2026</h2>
        <p>Deadline sắp tới — không bỏ lỡ hạn nộp</p>
      </div>
      {loading ? (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <div className="loading-dots"><span /><span /><span /></div>
        </div>
      ) : (
        <div className="deadline-list">
          {deadlines.length === 0 && <p style={{ color: '#94a3b8', textAlign: 'center' }}>Không có deadline nào sắp tới.</p>}
          {deadlines.map((d, i) => (
            <div key={i} className="deadline-item">
              <div className="deadline-urgency">
                {d.days_left <= 7 ? '🔴' : d.days_left <= 30 ? '🟡' : '🟢'}
              </div>
              <div className="deadline-info">
                <h4>{d.description}</h4>
                <p>{d.deadline_formatted} • {d.user_type}</p>
              </div>
              <div className="deadline-countdown" style={{ color: d.days_left <= 7 ? '#ef4444' : d.days_left <= 30 ? '#f59e0b' : '#10b981' }}>
                {d.days_left} ngày
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/* ═══ UPDATES PAGE ═══ */
function UpdatesPage() {
  const [updates, setUpdates] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [loaded, setLoaded] = useState(false)

  const loadUpdates = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/api/updates`)
      const data = await res.json()
      setUpdates(data.updates || [])
    } catch {
      setUpdates([])
    }
    setLoading(false)
    setLoaded(true)
  }

  const triggerCrawl = async () => {
    setLoading(true)
    try {
      await fetch(`${API_URL}/api/update/crawl`, { method: 'POST' })
      await loadUpdates()
    } catch { setLoading(false) }
  }

  useEffect(() => { if (!loaded) loadUpdates() }, [loaded])

  return (
    <div className="updates-container">
      <div className="page-header">
        <h2>🔄 Cập Nhật Luật Mới</h2>
        <p>AI tự động theo dõi văn bản pháp luật từ 4 cổng chính thống</p>
      </div>
      <div style={{ textAlign: 'center', marginBottom: 24 }}>
        <button className="btn-send" onClick={triggerCrawl} disabled={loading}>
          {loading ? 'Đang crawl...' : '🔍 Crawl Ngay'}
        </button>
      </div>
      {updates.map((u, i) => (
        <div key={i} className="update-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <strong>{u.document_name}</strong>
            <span className={`impact-badge ${(u.impact_level || 'low').toLowerCase()}`}>{u.impact_level}</span>
          </div>
          <p style={{ color: '#94a3b8', fontSize: 14 }}>{u.summary}</p>
          <p style={{ color: '#64748b', fontSize: 12, marginTop: 8 }}>
            Nguồn: {u.source_site} • {new Date(u.crawled_at).toLocaleDateString('vi-VN')}
          </p>
        </div>
      ))}
      {!loading && updates.length === 0 && (
        <p style={{ color: '#94a3b8', textAlign: 'center', padding: 40 }}>
          Chưa có dữ liệu. Nhấn "Crawl Ngay" để bắt đầu.
        </p>
      )}
    </div>
  )
}

export default App
