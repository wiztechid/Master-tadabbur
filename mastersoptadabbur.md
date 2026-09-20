# TADABBURLIFE — MASTER SOP

**Version:** 1.0  
**Status:** FROZEN  
**Scope:** TadabburLife Platform  
**Long-term scale:** 1,000+ sessions × bilingual/multiple languages

---

## 1. PURPOSE & AUTHORITY

MASTER-SOP adalah pedoman kerja utama pengembangan TadabburLife.

Setiap sesi kerja baru wajib membaca:

1. MASTER-SOP
2. CURRENT-STATUS

sebelum melakukan perubahan pada repository atau website.

MASTER-SOP mengatur **cara bekerja dan prinsip yang tidak boleh dilanggar**.

MASTER-SOP tidak memberikan kewenangan untuk mengubah substansi tadabbur yang telah dikunci.

### Hierarki acuan

LOCKED CONTENT  
↓  
MASTER-SOP  
↓  
CURRENT-STATUS  
↓  
ACTIVE TASK / CONVERSATION

Jika terjadi konflik, acuan yang lebih tinggi harus dipertahankan.

Detail implementasi yang cepat berubah tidak disimpan di MASTER-SOP. Detail tersebut ditempatkan pada CURRENT-STATUS, technical documentation, SEO documentation, product specification, atau CHANGELOG.

---

## 2. CONTENT INTEGRITY

### 2.1 Locked Content

Setiap sesi tadabbur yang telah disetujui dan dinyatakan selesai menjadi **LOCKED CONTENT**.

Locked content dapat mencakup ayat dan referensinya, terjemahan yang telah disetujui, tafsir/penjelasan, hadis atau dalil pendukung, refleksi, batas pemaknaan, pesan utama, practical action / Journey Mission, serta hubungan makna antarelemen dalam satu sesi.

Locked content tidak boleh diubah hanya untuk SEO, keyword, readability score, engagement, layout, monetisasi, translation optimization, atau kebutuhan teknis.

Tanpa instruksi eksplisit, locked content tidak boleh ditulis ulang, diparafrase, diringkas, diperluas, direinterpretasi, dikurangi, atau diubah maknanya.

**Prinsip:** SEO, UI, translation engineering, dan technical optimization bekerja mengelilingi locked content, bukan menulis ulang locked content.

---

## 3. SCALABILITY PRINCIPLE

TadabburLife dirancang sebagai platform jangka panjang dengan target sekurang-kurangnya **1,000+ sessions × bilingual/multiple languages**.

Jumlah sesi aktif saat ini bukan batas arsitektur. Content structure, routing, bilingual architecture, internal linking, sitemap, schema, metadata, progress tracking, search architecture, sharing, dan QC harus mampu berkembang tanpa membutuhkan redesign fundamental.

**BUILD FOR THE ACTIVE CORPUS. ARCHITECT FOR 1,000+.**

Hindari hard-coded logic yang bergantung pada jumlah sesi saat ini apabila sistem dapat dibuat data-driven. Penambahan sesi baru tidak boleh membutuhkan perubahan fundamental terhadap arsitektur website.

---

## 4. PRODUCT EXPERIENCE

TadabburLife bukan kumpulan artikel SEO yang berdiri sendiri. TadabburLife adalah **CONNECTED TADABBUR JOURNEY**.

AYAT → MEMAHAMI PETUNJUK → REFLEKSI → JOURNEY MISSION / PRACTICAL ACTION → PROGRESS → NEXT SESSION

Perubahan SEO, UI, maupun technical architecture tidak boleh merusak urutan perjalanan, session progression, completion state, unread/read state, next-session navigation, recovery posisi pembaca, atau kontinuitas pengalaman tadabbur.

Search landing membawa pembaca **masuk ke journey**, bukan mengubah journey menjadi kumpulan artikel terpisah.

---

## 5. READER FIRST + SEARCH INTENT ALIGNED

TadabburLife dibuat untuk manusia, bukan crawler. Namun kebutuhan manusia yang datang melalui search harus dipahami melalui search intent dan SERP evidence.

SEARCH NEED → USEFUL ANSWER → COMFORTABLE READING → DEEPER TADABBUR → CLEAR NEXT STEP

Prioritas: Content integrity → Reader usefulness → Reading comfort → Journey continuity → Search-intent alignment → Technical optimization.

SEO harus membantu pembaca menemukan halaman yang tepat dan tidak boleh membuat pengalaman membaca terasa dibuat untuk mesin pencari.

---

## 6. BILINGUAL & MULTILINGUAL ARCHITECTURE

### 6.1 Setiap Bahasa adalah Search Ecosystem

Versi Indonesia dan English merupakan pasangan konten, tetapi bukan satu keyword ecosystem. Jika bahasa baru ditambahkan di masa depan, prinsip yang sama berlaku.

Deep SERP dilakukan secara independen untuk setiap bahasa/market. Keyword English tidak boleh ditentukan hanya dengan menerjemahkan keyword Indonesia.

Untuk masing-masing ecosystem evaluasi search intent, query language, long-tail opportunity, competition, adjacent intent, SERP composition, dan cannibalization risk.

Search territory antarbahasa dapat berbeda. Namun substansi dan makna inti harus tetap ekuivalen.

### 6.2 Functional Parity

Tidak ada bahasa yang boleh menjadi versi sekunder TadabburLife.

Setiap versi bahasa harus mempertahankan functional parity pada content structure, navigation, CTA, journey state, session progression, alerts/status, cards, badges, layout, spacing, icon hierarchy, information density, sharing, dan fungsi utama lainnya.

Perbedaan diperbolehkan jika diperlukan oleh bahasa, reader behavior, atau search intent.

### 6.3 Language Signals

Setiap pasangan/kelompok halaman bahasa harus memiliki konfigurasi yang benar untuk canonical, hreflang, x-default, metadata, language switching, dan internal linking antarbahasa.

---

## 7. SEARCH ARCHITECTURE

### 7.1 Evidence Before Optimization

SERP EVIDENCE → SEARCH INTENT → SEARCH TERRITORY → KEYWORD MAPPING → IMPLEMENTATION

Keyword tidak boleh dipaksakan jika SERP evidence tidak mendukung target tersebut.

### 7.2 One Intent Territory → One Canonical Landing

Setiap primary search intent / keyword territory harus memiliki satu canonical landing utama. Dua halaman tidak boleh sengaja mengejar primary intent yang sama tanpa alasan arsitektural yang jelas. Sebelum menetapkan target baru wajib dilakukan cannibalization check terhadap active corpus.

### 7.3 SEO Workflow

DEEP SERP → INTENT CLASSIFICATION → LONG-TAIL OPPORTUNITY → KEYWORD MAPPING → CANNIBALIZATION CHECK → TITLE / H1 / META → ANSWER LAYER → INTERNAL LINKING → SCHEMA → TECHNICAL SEO → LIVE / CRAWLER QC

Keyword density bukan target. **Search usefulness adalah target.**

---

## 8. CONTENT ENHANCEMENT BOUNDARY

Konten utama tidak boleh diubah hanya untuk memasukkan keyword, memperpanjang halaman, meningkatkan keyword density, menaikkan SEO score, atau meniru kompetitor.

SEO enhancement dapat ditempatkan di luar locked content jika akurat, relevan, membantu pembaca, tidak mengubah substansi, tidak menciptakan cannibalization, dan tidak mengganggu journey.

Contoh enhancement: contextual introduction, answer block, FAQ yang benar-benar berguna, navigational context, structured data, dan internal linking.

---

## 9. INDEXABILITY

Tidak semua URL yang dapat dibuka harus diindeks.

URL dibedakan menjadi **PUBLIC / SEARCH LANDING** dan **INTERNAL / OWNER / UTILITY**.

Public search landing dapat masuk index apabila memenuhi standar kualitas dan canonical architecture. Internal, owner, administrative, atau utility page tidak boleh masuk search index jika tidak ditujukan untuk search discovery.

Sitemap hanya memuat canonical URL yang memang ditujukan untuk indexing. Robots, noindex, canonical, sitemap, dan internal linking harus konsisten dengan keputusan indexability.

---

## 10. SHARE EXPERIENCE

Sharing merupakan bagian dari product experience TadabburLife, bukan sekadar dekorasi.

Share output harus merepresentasikan sesi yang benar, bahasa yang benar, title/copy yang benar, URL publik yang benar, dan visual yang sesuai.

Share card, OG image, generated image, native share, atau fallback sharing harus diuji pada pengalaman pengguna nyata.

---

## 11. WORKING FEATURE PRESERVATION

Fitur yang sudah terbukti bekerja dianggap sebagai **KNOWN-GOOD BEHAVIOR**.

Jangan rewrite, remove, atau mengubah known-good behavior hanya karena sedang memperbaiki bagian lain, kecuali perubahan tersebut memang berada dalam scope.

**FIX THE TARGET WITHOUT BREAKING THE NEIGHBOR.**

---

## 12. CONTROLLED IMPROVEMENT

Perubahan dapat berupa small fix, batch update, atau major system update.

Major update harus memiliki scope yang jelas, baseline/known-good behavior, implementation check, regression check, deploy verification, dan live QC.

---

## 13. QC FRAMEWORK

### 13.1 Content Integrity QC

Pastikan tidak terjadi perubahan tidak disengaja terhadap locked content, meaning, session structure, dan semantic parity antarbahasa.

Content Integrity QC mengikuti **ACTIVE CORPUS**, bukan jumlah sesi permanen.

Contoh:
- 47 sessions × 2 languages = 94 targets
- 100 sessions × 2 languages = 200 targets
- 1,000 sessions × 2 languages = 2,000 targets

Untuk perubahan GLOBAL yang menyentuh shared template, content generator, routing, metadata engine, translation layer, shared component, atau sistem lain yang digunakan seluruh sesi, wajib dilakukan **corpus-wide integrity verification**.

Sampling saja tidak cukup untuk perubahan yang secara sistemik dapat memengaruhi seluruh corpus. Sistem QC harus dirancang scalable sehingga validasi active corpus dapat dilakukan secara otomatis sebanyak mungkin.

### 13.2 Reader QC

Periksa clarity, usefulness, hierarchy, mobile comfort, navigation, next-step clarity, dan apakah perjalanan tadabbur tetap natural. Reader QC dilakukan sebagai pengguna, bukan sebagai developer website.

### 13.3 SEO QC

Periksa SERP intent, search territory, keyword mapping, title, H1, meta description, canonical, hreflang, internal linking, schema, sitemap, indexability, cannibalization, dan crawler-visible HTML.

Setiap bahasa dievaluasi berdasarkan search ecosystem masing-masing.

### 13.4 Technical / Regression QC

Periksa mobile, desktop, layout, spacing/padding, broken links, language switching, journey state, next-session behavior, sharing, OG metadata, crawler-visible HTML, dan regression terhadap halaman/sesi lain.

---

## 14. REPOSITORY WORKFLOW

### BEFORE WORK
READ MASTER-SOP → READ CURRENT-STATUS → DEFINE SCOPE → IDENTIFY AFFECTED FILES → IDENTIFY KNOWN-GOOD BEHAVIOR

### IMPLEMENT
MAKE CHANGE → SOURCE QC → CONTENT INTEGRITY CHECK → REGRESSION CHECK

### AFTER DEPLOY
LIVE QC → READER QC → SEO / TECHNICAL QC AS REQUIRED → UPDATE CURRENT-STATUS → RECORD SIGNIFICANT DECISION IN CHANGELOG

---

## 15. DEFINITION OF DONE

Pekerjaan belum dianggap selesai hanya karena code selesai, commit berhasil, build berhasil, atau deploy berhasil.

**DONE berarti:** IMPLEMENTED + LIVE VERIFIED + CONTENT INTEGRITY VERIFIED + NO MATERIAL REGRESSION + READER EXPERIENCE VERIFIED + SEO / TECHNICAL VERIFIED WHEN RELEVANT + CURRENT-STATUS UPDATED.

Untuk perubahan global terhadap seluruh sistem, DONE juga membutuhkan **active-corpus integrity verification**.

---

## 16. GUARDRAILS

JANGAN:

- mengubah locked content tanpa instruksi eksplisit,
- menggunakan SEO sebagai alasan rewrite substansi,
- menerjemahkan keyword satu bahasa secara otomatis menjadi target bahasa lain,
- membuat target keyword tanpa SERP evidence,
- membuat dua canonical landing sengaja mengejar intent utama yang sama,
- memperbaiki satu fitur dengan merusak fitur lain,
- merusak journey demi landing-page SEO,
- memperlakukan salah satu bahasa sebagai versi sekunder,
- memasukkan owner/internal page ke index tanpa tujuan,
- menganggap build/deploy sukses sebagai bukti website benar,
- meninggalkan major update tanpa regression QC,
- mengubah known-good behavior di luar scope,
- membuat arsitektur yang bergantung pada jumlah sesi saat ini jika dapat dibuat data-driven.

---

## 17. WHAT DOES NOT BELONG IN MASTER-SOP

MASTER-SOP tidak digunakan untuk menyimpan informasi yang cepat berubah, seperti jumlah active session terkini, sesi terakhir yang dikerjakan, keyword target individual, hasil SERP terbaru, angka padding spesifik, nama file implementasi, bug aktif, eksperimen monetisasi, harga akses, campaign, atau pekerjaan berikutnya.

Informasi tersebut ditempatkan pada CURRENT-STATUS, TECHNICAL DOCUMENTATION, SEO DOCUMENTATION, PRODUCT SPECIFICATION, atau CHANGELOG.

---

## 18. MASTER-SOP CHANGE CONTROL

MASTER-SOP adalah dokumen stabil. Perubahan pekerjaan sehari-hari tidak otomatis mengubah MASTER-SOP.

MASTER-SOP hanya direvisi apabila terjadi perubahan fundamental pada content integrity, product philosophy, architecture principle, search principle, QC principle, atau governance proyek.

Perubahan fundamental harus menaikkan versi dokumen.

---

# FINAL PRINCIPLES

**PROTECT THE SUBSTANCE.**

**SERVE THE READER.**

**UNDERSTAND THE SEARCH INTENT.**

**PRESERVE THE JOURNEY.**

**FIX THE TARGET WITHOUT BREAKING THE NEIGHBOR.**

**BUILD FOR THE ACTIVE CORPUS.**

**ARCHITECT FOR 1,000+.**

**DEPLOY IS NOT DONE. VERIFIED IS DONE.**

---

**END OF MASTER-SOP v1.0**
