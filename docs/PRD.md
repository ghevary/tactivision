# Product Requirements Document (PRD) — Alcyone AI

**Versi dokumen:** 1.0.0  
**Status:** Draf untuk perencanaan MVP  
**Baseline dataset:** Alcyone Synthetic Dataset 1.1.0  
**Platform utama:** Aplikasi web responsif

## 1. Ringkasan produk

Alcyone AI adalah ruang kerja analisis taktik berbasis web untuk pertandingan sepak bola fiktif. Sistem mengubah event pertandingan terstruktur dan posisi pemain tersinkronisasi menjadi visualisasi yang bisa diperiksa. Pengguna dapat menelusuri hubungan operan, heatmap event/okupansi, wilayah Voronoi, mencari rangkaian taktik dengan bahasa alami, dan membandingkan intervensi taktik yang didukung menggunakan simulator sintetis.

Produk ini bukan pengganti layanan skor langsung dan tidak mengklaim membuat prediksi akurat tentang pertandingan Premier League nyata. Nilai pembeda utamanya adalah hubungan antara **bukti visual, analitik deterministik, dan penjelasan AI yang berlandaskan bukti tersebut**.

## 2. Pernyataan masalah

Penggemar yang ingin memahami taktik sering menemui dua kondisi ekstrem: aplikasi skor/statistik yang terlalu sederhana dan tidak menjelaskan pola, atau alat analitik spesialis yang membutuhkan pengetahuan teknis dan proses filtering manual. Pembelajar taktik dan kreator konten membutuhkan cara untuk mengubah pertanyaan seperti “mengapa pressing membuka ruang tengah?” menjadi bukti yang dapat diperiksa di lapangan.

Masalah kedua adalah kepercayaan. AI bahasa alami dapat memberi jawaban yang terdengar meyakinkan tetapi mengarang angka atau interpretasi. Alcyone harus memisahkan hasil perhitungan dari teks generatif dan menunjukkan event sumber serta batasan model.

## 3. Target pengguna

### Persona utama — Pembelajar taktik / analis amatir

- Menonton sepak bola dan ingin memahami pressing, jarak antarlini, build-up, counterattack, serta blok pertahanan.
- Mengenal konsep sepak bola umum, tetapi belum tentu mampu menulis query data atau skrip.
- Membutuhkan penjelasan visual dan kemampuan untuk memeriksa bukti di balik suatu temuan.

### Persona sekunder — Kreator konten sepak bola

- Membuat ulasan pertandingan, video edukasi, atau utas taktik.
- Perlu menemukan rangkaian kejadian menarik dan menyusun statistik pendukung menjadi penjelasan yang mudah dipahami.
- Harus dapat memverifikasi hasil sebelum memublikasikannya; teks generatif hanya draf, bukan analisis otoritatif.

### Persona tersier — Developer / evaluator hackathon

- Membutuhkan contoh yang bisa direproduksi, provenance data sintetis, API terdokumentasi, dan pemisahan yang jelas antara perhitungan deterministik dan bahasa hasil generasi LLM.

## 4. Tujuan produk

- **G1 — Menjelaskan:** pengguna dapat menghubungkan klaim taktik dengan metrik, posisi, dan rangkaian event yang terhitung.
- **G2 — Mengeksplorasi ruang:** pengguna dapat memeriksa passing network, heatmap, dan wilayah Voronoi pada lapangan 2D.
- **G3 — Mencari dengan bahasa alami:** pengguna dapat menanyakan pola taktik dalam Bahasa Indonesia atau Inggris dan mendapatkan hasil yang difilter secara deterministik.
- **G4 — Membandingkan intervensi:** pengguna dapat mengubah parameter taktik yang didukung lalu melihat metrik simulasi baseline dan kandidat.
- **G5 — Menjaga kepercayaan:** provenance data sintetis, metode kalkulasi, referensi event, dan keterbatasan model ditampilkan secara eksplisit.

## 5. Di luar cakupan (non-goals)

MVP tidak akan:

- menyediakan hasil resmi/real-time Premier League, tracking pemain nyata, statistik klub nyata, atau analisis video;
- memperkirakan tracking dari rekaman siaran atau computer vision;
- menjanjikan prediksi hasil pertandingan nyata atau taktik yang optimal;
- menyajikan `shot_quality_proxy` sebagai xG resmi;
- melatih model ML khusus sebelum simulator dan proses evaluasinya dipahami;
- menyediakan akun, langganan, kolaborasi tim, atau berbagi publik kecuali ditambahkan setelah evaluasi MVP;
- menerima SQL atau kode bebas dari pengguna melalui antarmuka bahasa alami.

## 6. Cakupan dan prioritas

### P0 — Wajib untuk MVP

1. **Browser pertandingan:** daftar 10 fixture sintetis, klub home/away, skor, durasi, dan provenance data.
2. **Ringkasan pertandingan:** statistik tim/pemain, key moments, serta jendela waktu lima menit.
3. **Lapangan 2D interaktif:** posisi pemain pada timestamp tracking, filter tim, dan timeline event.
4. **Passing network:** node pemain dan edge passer/receiver berbobot; attempts dan completions dapat dibedakan.
5. **Heatmap:** pilih surface event density, progression destination, dan player occupancy yang disediakan dataset.
6. **Voronoi:** tampilkan wilayah spasial pada snapshot yang tersedia; kalkulasi on-demand hanya jika diimplementasikan dan diuji.
7. **Filter taktik bahasa alami:** ubah bahasa pengguna menjadi query terstruktur yang divalidasi dan tampilkan event yang benar-benar cocok beserta jumlah/ID-nya.
8. **Perbandingan What-If:** dukung parameter taktik yang terdaftar; tampilkan baseline, kandidat, delta, ringkasan run berpasangan, ketidakpastian jika tersedia, dan peringatan sintetik.
9. **Penjelasan berbasis bukti:** rangkum hanya metrik/event yang dikembalikan backend dan tampilkan referensi pertandingan, waktu, atau event bila memungkinkan.
10. **Provenance dan batasan:** beri tahu pengguna bahwa data bersifat sintetis dan What-If adalah simulator berbasis aturan.

### P1 — Setelah MVP

- Voronoi pada timestamp arbitrer berdasarkan tracking.
- Simpan/ekspor perbandingan What-If sebagai JSON atau gambar.
- Template query bahasa alami tambahan dan konteks pertanyaan lanjutan.
- Preset skenario buatan pengguna dan riwayat perbandingan.
- Metrik taktik tambahan setelah ditinjau secara domain.
- Cache untuk visualisasi dan filter yang sering diakses.

### P2 — Riset / pengembangan mendatang

- Kalibrasi simulator dengan dataset dunia nyata yang sesuai jika aturan dan lisensi mengizinkan.
- Evaluasi model hasil berbasis ML pada dataset uji terpisah yang didefinisikan jelas.
- Impor video atau tracking hanya jika hak penggunaan, format data, dan ruang lingkupnya sesuai.

## 7. Alur utama pengguna

### Alur A — Mengeksplorasi pertandingan

1. Pengguna membuka daftar pertandingan.
2. Pengguna memilih fixture sintetis.
3. Aplikasi memuat metadata dan ringkasan yang sudah dihitung.
4. Pengguna memilih tim, fase, rentang waktu, atau lapisan visualisasi.
5. Aplikasi menampilkan lapangan dan analitik terkait.
6. Pengguna dapat memeriksa event/nilai sumber dari suatu temuan visual.

### Alur B — Bertanya tentang taktik

1. Pengguna memasukkan pertanyaan, misalnya “Tampilkan counterattack yang berujung tembakan setelah menit 75.”
2. Query parser menghasilkan filter terstruktur (urutan event, interval waktu, tim, outcome).
3. Backend memvalidasi field, operator, rentang, dan ID entitas.
4. Query executor deterministik memfilter event pertandingan kanonis.
5. UI menampilkan jumlah hasil, timeline, dan detail event yang cocok.
6. Jika diminta, model penjelasan merangkum hasil event dan statistik yang ditemukan saja.

### Alur C — Menguji intervensi What-If

1. Pengguna memilih pertandingan baseline dan tim.
2. Pengguna mengubah kontrol taktik yang didukung, misalnya intensitas pressing atau tinggi garis pertahanan.
3. Backend memvalidasi batas parameter dan membentuk permintaan intervensi.
4. Simulator mengevaluasi baseline dan kandidat menggunakan seed/repetisi berpasangan.
5. Lapisan analitik menghitung delta metrik dan ringkasan ketidakpastian.
6. UI menampilkan kedua kondisi secara berdampingan, termasuk trade-off positif dan negatif.
7. Lapisan penjelasan membuat ringkasan hati-hati beserta disclaimer simulasi sintetis.

## 8. Kebutuhan fungsional dan kriteria penerimaan

### FR-001 — Pemilihan pertandingan dan tim

- Aplikasi harus menampilkan seluruh pertandingan di `data/fixtures.csv` / folder pertandingan kanonis.
- Setiap pertandingan harus menunjukkan tepat dua klub peserta dan sisi home/away.
- **Kriteria:** seluruh 10 fixture dapat dibuka tanpa ID tim atau pemain yang tidak ditemukan.

### FR-002 — Provenance dan notifikasi data sintetis

- Aplikasi harus menampilkan bahwa pertandingan dan hasilnya sintetis.
- **Kriteria:** notifikasi terlihat di halaman pertandingan dan hasil What-If, bukan hanya di dokumentasi.

### FR-003 — Ringkasan pertandingan

- Aplikasi harus memuat analytics yang sudah dihitung jika tersedia.
- **Kriteria:** skor, statistik tim, dan key moments sesuai `analytics.json` kanonis.

### FR-004 — Passing network

- Aplikasi harus memfilter event operan berdasarkan tim dan rentang waktu opsional.
- Metrik edge dihitung dari event passer/receiver atau dicocokkan dengan edge hasil perhitungan sebelumnya.
- **Kriteria:** jumlah attempts/completions pada network cocok dengan event hasil filter.

### FR-005 — Heatmap

- Aplikasi harus menampilkan surface heatmap yang didukung beserta legenda dan satuan.
- **Kriteria:** pilihan tim/surface cocok dengan lapisan `heatmaps.json`; filter yang tidak diwakili data precomputed harus dihitung ulang atau ditolak secara jelas.

### FR-006 — Voronoi

- Aplikasi harus menampilkan timestamp dengan tracking tersinkronisasi.
- Wilayah harus dibatasi pada lapangan 105 × 68 meter.
- **Kriteria:** terdapat tepat 22 sel untuk setiap snapshot lengkap dan total luas hasil clipping berada dalam toleransi pengujian.
- **Batasan:** labeli sebagai pembagian geometris berdasarkan pemain terdekat, bukan model definitif penguasaan ruang.

### FR-007 — Query bahasa alami

- LLM (atau fallback berbasis aturan yang terbatas) harus menghasilkan objek JSON sesuai schema query allowlist.
- Backend, bukan LLM, yang menjalankan filter terhadap event sumber.
- **Kriteria:** fixture query mengembalikan jumlah/ID event yang diharapkan; field/operator tidak valid ditolak; query tidak pernah membuat event baru.

### FR-008 — Simulasi What-If

- Hanya intervensi yang terdokumentasi dan berada dalam rentang parameter yang diizinkan yang boleh dijalankan.
- Simulator harus mengembalikan metrik baseline/kandidat, delta, ID run, seed/repetisi, dan batasan.
- **Kriteria:** `delta = candidate - baseline`; hasil dapat direproduksi untuk permintaan/seed yang sama; intervensi tak didukung menghasilkan error validasi yang jelas.
- UI tidak boleh menyebut hasil sebagai prediksi pertandingan nyata yang sudah terverifikasi.

### FR-009 — Penjelasan AI

- Prompt penjelasan menerima hasil backend terstruktur dan referensi bukti, bukan seluruh dataset tanpa alasan.
- **Kriteria:** setiap klaim angka dapat dilacak ke field hasil; nilai yang tidak tersedia dinyatakan sebagai tidak tersedia, bukan ditebak.

### FR-010 — Penanganan error

- Aplikasi harus menangani ID pertandingan tidak ditemukan, ID tim salah, timestamp tidak tersedia, kegagalan provider LLM, rate limit, dan parameter What-If yang tidak didukung.
- **Kriteria:** pengguna menerima pesan yang dapat ditindaklanjuti; log backend menyertakan request/correlation ID tanpa membocorkan secret.

## 9. Kontrak data

Sumber kanonis:

- `data/clubs.csv` — registri klub fiktif yang stabil.
- `data/player_registry.csv` — identitas pemain dan atribut dasar yang stabil.
- `data/fixtures.csv` — relasi pertandingan dan klub.
- `data/matches/{match_id}/match.json` — metadata/konfigurasi pertandingan.
- `events.jsonl` — sumber event kanonis.
- `tracking.jsonl` — keadaan pemain dan bola yang tersinkronisasi.
- `analytics.json`, `passing_network.json`, `heatmaps.json`, `spatial_analytics.json` — data turunan.
- `what_if_scenarios.jsonl`, `what_if_runs.jsonl` — contoh/hasil skenario sintetis.
- `flat/` — ekspor praktis, bukan jalur tulis kanonis.

Jangan mengedit file analitik turunan secara terpisah dari event/tracking. Setelah sumber kanonis berubah, bangun ulang data turunan dan jalankan validator.

## 10. Kebutuhan nonfungsional

- **Kebenaran:** referensi event/pemain/tim dan agregat lolos uji otomatis.
- **Reproduksibilitas:** generator/simulator memakai seed eksplisit; skenario menyimpan versi engine dan seed.
- **Keterlacakan:** sertakan `match_id`, event ID atau jendela sumber, metode kalkulasi, dan versi simulator jika sesuai.
- **Target performa awal (usulan):** p95 API ringkasan/network/heatmap precomputed ≤ 1,5 detik pada pengembangan lokal; query taktik deterministik p95 ≤ 2 detik tanpa menghitung latensi LLM; What-If MVP ≤ 5 detik untuk jumlah repetisi yang dibatasi. Ukur kembali setelah profiling.
- **Ketahanan:** validasi payload API dan jangan percaya JSON dari model sebelum lolos validasi schema.
- **Keamanan:** secret provider hanya di environment server; field/operator query harus allowlist; batasi rate request LLM; larang eksekusi kode, path file arbitrer, dan SQL pengguna.
- **Aksesibilitas:** kontrol dapat dioperasikan dengan keyboard, label terlihat, legenda terbaca, dan informasi tidak hanya dibedakan dengan warna.
- **Kemudahan pemeliharaan:** frontend, API, domain service, simulator, dan kontrak data mempunyai interface serta pengujian jelas.

## 11. Kebijakan AI dan simulasi

AI digunakan untuk memahami bahasa dan menjelaskan hasil, bukan sebagai sumber kebenaran statistik.

- Query parser menghasilkan filter terstruktur; backend yang melakukan penyaringan.
- Perhitungan analytics deterministik dan diuji tanpa bergantung pada keluaran LLM.
- Model penjelasan hanya menerima event/meterik relevan yang telah diambil.
- Output harus menyatakan bila hasil berasal dari simulasi sintetis.
- Perbandingan paired-seed membantu mengontrol randomness simulator, tetapi tidak membuktikan kausalitas dunia nyata.
- Fuzzy logic atau ML dapat dipertimbangkan kemudian, setelah baseline dan evaluasi stabil.

## 12. Rencana evaluasi dan metrik keberhasilan yang diusulkan

Angka berikut adalah **target evaluasi prototipe**, bukan hasil pengukuran yang sudah tercapai.

- **Kebenaran dataset:** seluruh pemeriksaan schema dan lintas file pada validator lulus.
- **Akurasi fixture query:** 100% fixture query deterministik mengembalikan jumlah/ID event yang diharapkan. Ini menguji executor pada kasus yang sudah diketahui, bukan pemahaman bahasa umum.
- **Validitas parser LLM:** ≥95% dari set uji yang ditinjau manual menghasilkan schema valid; keluaran tidak valid di-retry atau ditolak dengan aman.
- **Penjelasan grounded:** 0 event ID palsu dan 0 klaim numerik tanpa bukti pada set uji penerimaan.
- **Konsistensi visualisasi:** jumlah network, input heatmap, dan geometri Voronoi melewati uji konsistensi otomatis.
- **Integritas What-If:** delta cocok dengan agregasi run; hasil dengan seed/config sama dapat diulang ketika mode deterministik digunakan.
- **Kemudahan penggunaan:** minimal 4 dari 5 pengguna uji dapat menyelesaikan eksplorasi pertandingan dan query taktik tanpa bantuan (uji formatif kecil, bukan validasi statistik).

## 13. Risiko dan mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Pola sintetis dianggap sebagai kesimpulan sepak bola nyata | UX menyesatkan | Label permanen, provenance, batasan eksplisit, bahasa yang hati-hati |
| LLM mengarang event/statistik | Hilangnya kepercayaan | Eksekusi deterministik, validasi schema, penjelasan berdasar hasil, uji klaim |
| Simulator What-If terlalu sederhana | Saran taktik menyesatkan | Sebut sebagai surrogate sintetis; tampilkan metrik/parameter; jangan klaim prediksi nyata |
| File tracking/CSV besar memperlambat aplikasi | Performa buruk | Muat per pertandingan, gunakan data turunan, stream JSONL atau indeks/cache |
| Data turunan tidak konsisten setelah edit | Visualisasi tidak cocok | Pipeline regenerasi tunggal dan validator lintas file |
| Provider LLM tidak tersedia atau mahal | Query/penjelasan terganggu | Adapter provider, rate limit, fallback filter deterministik |

## 14. Milestone yang disarankan

1. **M0 — Kontrak dan validasi data:** dataset dapat dibaca; validator lulus; fixture menjadi tes.
2. **M1 — API read-only:** daftar/detail pertandingan, ringkasan, event, timestamp tracking, analytics turunan.
3. **M2 — MVP visualisasi:** pitch, timeline event, network, heatmap, Voronoi.
4. **M3 — Query taktik:** parser sesuai schema, executor deterministik, evaluasi berbasis fixture.
5. **M4 — What-If MVP:** satu atau dua intervensi, paired simulation, perbandingan hasil.
6. **M5 — Penjelasan grounded dan demo:** penanganan error, provenance, tampilan responsif, alur demo.

## 15. Keputusan terbuka

- Pilih provider dan model LLM setelah memastikan aturan hackathon, ketersediaan, dan biaya.
- Tentukan apakah runtime What-If menjalankan simulasi penuh atau surrogate dengan ruang lingkup terbatas untuk tiap parameter.
- Tetapkan metrik taktik MVP dan dokumentasikan rumusnya.
- Pilih renderer lapangan SVG atau Canvas setelah prototipe interaksi dibuat.
- Konfirmasi hosting dan pengelolaan secret sebelum deployment.
