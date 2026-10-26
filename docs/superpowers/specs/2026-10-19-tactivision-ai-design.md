# Alcyone AI — Spesifikasi Desain Sistem & UI Map Bola

**Tanggal:** 2026-10-19  
**Versi:** 1.0.0  
**Baseline Data:** Alcyone Synthetic Dataset 1.1.0 (`SYN_001`–`SYN_010`, `CLUB_A`–`CLUB_E`)

## 1. Intent & Why
Penggemar taktik, analis amatir, dan kreator konten membutuhkan alat visual yang menghubungkan pola spasial di lapangan 2D dengan bukti event kanonis dan metrik deterministik, tanpa halusinasi angka dari LLM.

## 2. Goals, Non-Goals, & Anti-Goals
- **Goals:**
  - Visualisasi lapangan 2D (105m × 68m) dengan poligon Voronoi (`d3-delaunay`), jalur umpan & cover shadow (radius 3.4m), Zone 14, passing network, dan heatmap (21×14 grid).
  - Filter taktik bahasa alami (ID/EN) yang diubah ke JSON schema allowlist lalu dieksekusi secara deterministik terhadap `events.jsonl` (100/100 golden query lulus).
  - Simulator What-If berbasis aturan dengan seed berpasangan (`alcyone-rule-sim-0.1`) untuk membandingkan konfigurasi baseline vs kandidat.
  - Penjelasan berbasis bukti dan trace 3-agen menggunakan Gemini API (`gemini-3.8-flash` melalui `google-genai` / `@google/genai` `interactions.create`).
- **Non-Goals:**
  - Prediksi hasil pertandingan Premier League nyata atau ekstraksi computer vision dari video siaran.
  - Menyajikan `shot_quality_proxy` sebagai xG resmi.
- **Anti-Goals (Hal yang membuat sistem gagal meski berjalan teknis):**
  - LLM mengarang event ID, menghitung metrik sendiri, atau mengeksekusi SQL/Python bebas.
  - Mengklaim pergeseran pin pemain di browser saja sebagai simulasi kausal nyata tanpa label `simulated_estimate` dan provenance sintetis.

## 3. Constraints
- Lapangan standar 105m × 68m; waktu pertandingan 0–5.400 detik (2 babak × 2.700 detik).
- Semua perhitungan statistik dan filter event dilakukan oleh kode deterministik; LLM (`gemini-3.8-flash`) dibatasi pada parsing bahasa alami ke schema JSON dan perangkuman hasil terhitung.

## 4. Keputusan Arsitektur (User vs Pilihan Builder)
- **Dari Dokumen & Prompt Pengguna:**
  - Komponen UI `AlcyoneBoard.vue` dengan HTML5 `<canvas>` 2D (`840×544 px`, skala `8 px/m`), `d3-delaunay` Voronoi, deteksi jalur umpan (cover shadow), kalkulasi Zone 14, drag-and-drop pemain, serta 3 persona (`Fan`, `Analyst`, `Broadcaster`).
  - Kontrak REST API `/api/v1` dengan FastAPI + Pydantic dan arsitektur data kanonis `SYN_001`–`SYN_010` (`CLUB_A`–`CLUB_E`).
- **Pilihan Builder (Ditandai Eksplisit):**
  - **Integrasi Dataset Kanonis + Preset Sandbox:** UI mendukung peralihan langsung antara 10 pertandingan liga sintetis (`SYN_001` s/d `SYN_010`, 5 klub `CLUB_A`–`CLUB_E`, 55 pemain) dan preset taktik interaktif (`3-2-4-1 Inverted Box`, `4-3-3 Wide Overload`, `2-3-5 High Press`).
  - **Adapter LLM Gemini API (`gemini-3.8-flash`):** Mengimplementasikan adapter LLM menggunakan SDK terbaru `google-genai >= 2.30.1` (Python) dan `@google/genai >= 2.29.1` (TypeScript) dengan endpoint `client.interactions.create(model="gemini-3.8-flash", ...)` dan properti `interaction.output_text`, menggantikan placeholder provider lama.
  - **Grafik 2 (Interactive SVG Multi-Agent & System Architecture):** Disertakan langsung sebagai tab interaktif dengan animasi aliran paket data `stroke-dasharray` / `stroke-dashoffset`.
