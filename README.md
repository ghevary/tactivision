# TactiVision AI

**Platform Analisis Taktik Sepak Bola Berbantuan AI (AI-Assisted Football Tactical Analytics Platform).**  
Versi: **1.1.0** · Dukungan Bahasa: **Bahasa Indonesia (ID) & English (EN)**

TactiVision AI dirancang untuk membantu analis taktik, pelatih, akademisi, dan kreator konten memahami *mengapa* dan *bagaimana* suatu pola permainan sepak bola terjadi. Platform menggabungkan analitik event deterministik, visualisasi spasial 2D (Voronoi & Passing Lanes), engine evaluasi offside simetris dua arah (Hukum XI IFAB), pencarian taktik dengan bahasa alami (Natural Language Query), serta simulator What-If berpasangan (*paired-seed tactical sandbox*).

---

## Fitur Utama

- **Opsi Multi-Bahasa (Bilingual ID / EN):** Switcher bahasa interaktif di bagian navigasi atas dengan persistensi otomatis (`localStorage`). Seluruh label UI, evaluasi offside, metrik, serta penjelasan persona tersedia dalam Bahasa Indonesia dan English.
- **Symmetric 2D Dual-Pitch Board:** Lapangan simetris sisi kiri dan kanan dengan rendering Voronoi 22 sel, vektor operan, heatmap spasial, dan evaluasi garis batas offside/onside interaktif (drag-and-drop pemain dan bola).
- **Rule-Based IFAB Law 11 Offside Engine:** Pengecekan status offside presisi dengan dukungan aturan pengecualian set-piece (Goal Kick, Throw-In, Corner Kick), pemain di paruh lapangan sendiri, dan referensi garis bola.
- **Multi-Persona Narrative Generator:** Persona *Analyst*, *Broadcaster*, dan *Fan* dengan dukungan grounded AI explanation (Gemini 3.8 Flash) dan fallback deterministik berbasis metrik riil.
- **What-If Tactical Sandbox:** Pengujian intervensi intensitas pressing dan ketinggian garis pertahanan dengan *paired seed* (20 repetisi) untuk membandingkan baseline vs skenario kandidat.
- **Natural Language Query Engine:** Penerjemahan pertanyaan bahasa alami menjadi query filter allowlist deterministik yang diaudit langsung terhadap berkas event pertandingan.

---

## Struktur Repositori

```text
.
├── apps/
│   └── web/                     # Frontend Vite + Vue 3 + Tailwind CSS + d3-delaunay
│       ├── index.html           # Single Page Application interaktif (Bilingual ID/EN)
│       ├── package.json
│       ├── vite.config.js       # Vite config dengan proxy otomatis /api -> :8000
│       └── src/
├── services/
│   └── api/                     # Backend FastAPI REST API (/api/v1)
│       ├── main.py              # Endpoint health, matches, analytics, what-if & query
│       ├── llm_adapter.py       # Adapter Gemini 3.8 Flash & fallback deterministik
│       ├── query_service.py     # Filter allowlist event deterministik
│       ├── what_if_service.py   # Paired-seed simulation engine
│       └── requirements.txt
├── data/                        # Dataset sintetis kanonis (5 klub, 10 fixtures, event & tracking)
│   ├── clubs.csv
│   ├── fixtures.csv
│   ├── player_registry.csv
│   ├── dataset_manifest.json
│   ├── matches/                 # SYN_001 s.d. SYN_010
│   └── flat/                    # Ekspor flat tabular CSV
├── docs/                        # Spesifikasi produk & arsitektur sistem
│   ├── PRD.md
│   └── SYSTEM_ARCHITECTURE.md
├── index_standalone_preview.html # Versi pratinjau mandiri langsung tanpa server build
├── .env.example
├── .gitignore
└── LICENSE                      # MIT License
```

---

## Panduan Menjalankan Aplikasi

### 1. Prasyarat
- **Node.js** (v18+) & **npm**
- **Python** (3.10+) atau package manager [`uv`](https://github.com/astral-sh/uv)

### 2. Konfigurasi Environment (Opsional)
Salin `.env.example` ke `.env`:
```bash
cp .env.example .env
```
Isi `GEMINI_API_KEY` jika ingin mengaktifkan narasi LLM langsung dari Google GenAI. Jika tidak diisi, sistem otomatis beralih ke engine deterministik lokal.

### 3. Menjalankan Backend (FastAPI REST API)
```bash
# Membuat venv dan menginstal dependensi
uv venv .venv
source .venv/bin/activate
uv pip install -r services/api/requirements.txt

# Menjalankan server API pada port 8000
cd services/api
uvicorn main:app --host 0.0.0.0 --port 8000
```
- API Healthcheck: `http://127.0.0.1:8000/api/v1/health`
- Swagger Documentation: `http://127.0.0.1:8000/docs`

### 4. Menjalankan Frontend (Vite + Vue 3)
Di terminal baru:
```bash
cd apps/web
npm install
npm run dev
```
Buka browser ke [**http://localhost:5173**](http://localhost:5173).

### 5. Menjalankan Versi Standalone Langsung
Anda juga dapat membuka berkas [`index_standalone_preview.html`](index_standalone_preview.html) langsung di peramban web modern tanpa perlu menjalankan node/build server.

---

## Penggantian Bahasa (Language Toggle)
Klik tombol switcher di kanan atas header:
- **🇮🇩 ID**: Bahasa Indonesia (Default)
- **🇬🇧 EN**: English

Pilihan bahasa Anda akan disimpan di peramban dan langsung memperbarui seluruh antarmuka secara instan.

---

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
Copyright (c) 2026 Ghevary Suprapto.
