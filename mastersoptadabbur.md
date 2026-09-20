# TADABBURLIFE — MASTER SOP

**Version:** 1.1  
**Status:** FROZEN GOVERNANCE BASELINE  
**Scope:** TadabburLife Platform  
**Long-term scale:** 1,000+ sessions × bilingual/multiple languages

---

## 1. PURPOSE & AUTHORITY

MASTER-SOP adalah pedoman kerja utama pengembangan TadabburLife.

Setiap sesi kerja baru wajib membaca:

1. MASTER-SOP
2. CURRENT-STATUS

sebelum melakukan perubahan pada repository atau website.

MASTER-SOP mengatur cara bekerja dan prinsip yang tidak boleh dilanggar.

### Hierarki acuan

ABSOLUTE SACRED LOCK  
↓  
MASTER-SOP  
↓  
CURRENT-STATUS  
↓  
ACTIVE TASK / CONVERSATION

Jika terjadi konflik, acuan yang lebih tinggi harus dipertahankan.

Detail implementasi yang cepat berubah ditempatkan pada CURRENT-STATUS, technical documentation, SEO documentation, product specification, atau CHANGELOG.

---

## 2. CONTENT INTEGRITY

### 2.1 Absolute Sacred Lock

TadabburLife membedakan dengan tegas antara sumber wahyu/dalil dan lapisan penjelasan.

Bagian berikut merupakan **ABSOLUTE SACRED LOCK** dan tidak boleh diubah untuk kepentingan SEO, SERP, keyword, readability, engagement, layout, monetisasi, translation optimization, maupun kebutuhan teknis:

- teks ayat Al-Qur'an yang digunakan;
- identitas dan referensi surah/ayat;
- terjemahan Al-Qur'an yang telah ditetapkan untuk sesi;
- teks hadis yang dikutip;
- identitas/rujukan hadis dan atribusi sumber yang telah diverifikasi.

Ayat Al-Qur'an dan hadis tidak boleh diparafrasekan seolah-olah menjadi teks sumber asli. SEO harus menyesuaikan diri kepada sumber, bukan sumber yang diubah agar sesuai dengan SEO.

Jika ditemukan kesalahan penyalinan, referensi, atribusi, atau masalah akurasi pada bagian sacred lock, jangan melakukan perubahan diam-diam. Verifikasi sumber terlebih dahulu dan perlakukan koreksi sebagai **religious-source correction**, bukan SEO rewrite.

### 2.2 SEO-Adaptive Explanatory Layer

Di luar Absolute Sacred Lock, lapisan penjelasan dapat dikembangkan, disusun ulang, diperjelas, diperluas, atau disesuaikan berdasarkan keyword target, search intent, bilingual SERP evidence, kebutuhan pembaca, dan peluang search territory.

Lapisan adaptif dapat mencakup:

- contextual introduction;
- penjelasan/tadabbur pendukung;
- struktur pembahasan;
- heading dan subheading;
- answer block;
- FAQ;
- refleksi;
- contoh penerapan;
- konteks kehidupan;
- practical explanation;
- transition/copy;
- internal-link context;
- summary/key takeaway;
- Journey Mission/practical action apabila penyesuaian tetap konsisten dengan petunjuk sesi.

Penyesuaian diperbolehkan hanya apabila:

1. tetap relevan dengan ayat/hadis dan tema sesi;
2. tidak mengubah, memelintir, atau memaksakan makna ayat/hadis;
3. tidak membuat klaim agama tanpa dasar yang memadai;
4. tidak menempatkan keyword sebagai otoritas atas sumber agama;
5. membantu kebutuhan pembaca nyata;
6. tidak melakukan keyword stuffing;
7. tidak menciptakan cannibalization yang tidak disengaja;
8. mempertahankan journey dan kualitas tadabbur.

**Prinsip:** WAHYU/DALIL ADALAH ANCHOR YANG TETAP. EXPLANATORY LAYER BOLEH SEARCH-ADAPTIVE.

---

## 3. SCALABILITY PRINCIPLE

TadabburLife dirancang sebagai platform jangka panjang dengan target sekurang-kurangnya **1,000+ sessions × bilingual/multiple languages**.

Jumlah sesi aktif saat ini bukan batas arsitektur. Content structure, routing, bilingual architecture, internal linking, sitemap, schema, metadata, progress tracking, search architecture, sharing, dan QC harus mampu berkembang tanpa membutuhkan redesign fundamental.

**BUILD FOR THE ACTIVE CORPUS. ARCHITECT FOR 1,000+.**

Hindari hard-coded logic yang bergantung pada jumlah sesi saat ini apabila sistem dapat dibuat data-driven.

---

## 4. PRODUCT EXPERIENCE

TadabburLife bukan kumpulan artikel SEO yang berdiri sendiri. TadabburLife adalah **CONNECTED TADABBUR JOURNEY**.

AYAT → MEMAHAMI PETUNJUK → REFLEKSI → JOURNEY MISSION / PRACTICAL ACTION → PROGRESS → NEXT SESSION

Search landing membawa pembaca masuk ke journey, bukan mengubah journey menjadi kumpulan artikel terpisah.

SEO-adaptive explanation boleh memperkuat entry point dari search, tetapi tidak boleh merusak session progression, continuity, progress, next-session navigation, atau pengalaman tadabbur.

---

## 5. READER FIRST + SEARCH INTENT ALIGNED

TadabburLife dibuat untuk manusia, bukan crawler. Kebutuhan manusia yang datang melalui search dipahami melalui search intent dan SERP evidence.

SEARCH NEED → USEFUL ANSWER → COMFORTABLE READING → DEEPER TADABBUR → CLEAR NEXT STEP

Prioritas:

**Sacred-source integrity → Reader usefulness → Religious/contextual accuracy → Reading comfort → Journey continuity → Search-intent alignment → Technical optimization.**

SEO harus membantu pembaca menemukan jawaban yang relevan tanpa membuat pembahasan terasa dibuat untuk mesin pencari.

---

## 6. BILINGUAL & MULTILINGUAL ARCHITECTURE

### 6.1 Each Language Is an Independent Search Ecosystem

Versi Indonesia dan English merupakan pasangan tadabbur, tetapi bukan satu keyword ecosystem.

Deep SERP dilakukan secara independen untuk setiap bahasa/market. Keyword English tidak boleh ditentukan hanya dengan menerjemahkan keyword Indonesia.

Untuk masing-masing ecosystem evaluasi:

- search intent;
- query language;
- long-tail opportunity;
- competition;
- adjacent intent;
- SERP composition;
- cannibalization risk;
- relevance to the session's Quran/hadith anchor.

Search territory dan explanatory presentation antarbahasa dapat berbeda selama tetap berakar pada sumber agama dan tema sesi yang sama.

### 6.2 Functional Parity

Tidak ada bahasa yang boleh menjadi versi sekunder TadabburLife.

Setiap versi bahasa harus mempertahankan functional parity pada navigation, CTA, journey state, session progression, alerts/status, cards, badges, layout, spacing, icon hierarchy, information density, sharing, dan fungsi utama lainnya.

Perbedaan editorial diperbolehkan jika diperlukan oleh bahasa, reader behavior, atau independently validated search intent.

### 6.3 Language Signals

Setiap pasangan/kelompok halaman bahasa harus memiliki konfigurasi yang benar untuk canonical, hreflang, x-default, metadata, language switching, dan internal linking antarbahasa.

---

## 7. SEARCH ARCHITECTURE

### 7.1 Evidence Before Optimization

SERP EVIDENCE → SEARCH INTENT → SEARCH TERRITORY → KEYWORD MAPPING → IMPLEMENTATION

Keyword tidak boleh dipaksakan jika SERP evidence atau relevansi sesi tidak mendukung target tersebut.

### 7.2 Opportunity Gate

SERP yang lemah atau kompetisinya rendah bukan alasan yang cukup untuk menarget keyword.

Target harus memenuhi seluruh prinsip berikut:

**SEARCH OPPORTUNITY + SESSION RELEVANCE + INTENT FIT + CONTENT VALUE + CANNIBALIZATION SAFETY**

Keyword/search territory hanya layak ditarget jika dapat dijawab secara substantif oleh sesi tanpa memaksakan makna ayat/hadis.

### 7.3 One Intent Territory → One Canonical Landing

Setiap primary search intent / keyword territory harus memiliki satu canonical landing utama.

Sebelum menetapkan target baru wajib dilakukan cannibalization check terhadap active corpus.

### 7.4 SEO Workflow

DEEP SERP  
→ INTENT CLASSIFICATION  
→ LONG-TAIL / WEAK-SERP OPPORTUNITY  
→ SEARCH TERRITORY  
→ KEYWORD MAPPING  
→ QURAN / HADITH RELEVANCE CHECK  
→ CANNIBALIZATION CHECK  
→ BILINGUAL EXPLANATORY ADAPTATION  
→ TITLE / H1 / META  
→ ANSWER LAYER / SUPPORTING CONTENT  
→ INTERNAL LINKING  
→ SCHEMA  
→ READER QC  
→ RELIGIOUS-INTEGRITY QC  
→ TECHNICAL SEO  
→ LIVE / CRAWLER QC

Keyword density bukan target. **Search usefulness adalah target.**

---

## 8. CONTENT ENHANCEMENT & SEO ADAPTATION

SEO enhancement tidak dibatasi hanya pada metadata atau elemen di luar artikel.

Explanatory layer boleh diperkuat secara substantif untuk menjawab target search intent dan bersaing pada SERP yang relevan, termasuk melalui penjelasan tambahan, answer blocks, useful FAQ, examples, contextual sections, clearer structure, headings, summaries, dan internal linking.

Namun:

**SEO BOLEH MENGUBAH CARA PENJELASAN DISAJIKAN. SEO TIDAK BOLEH MENGUBAH WAHYU/DALIL AGAR COCOK DENGAN KEYWORD.**

Setiap pengembangan harus:

- relevan terhadap sacred anchor sesi;
- memberikan nilai informasi nyata;
- natural untuk pembaca;
- akurat;
- tidak membuat klaim agama yang melampaui dasar;
- tidak sekadar meniru kompetitor;
- tidak mengisi halaman dengan teks demi panjang konten;
- menjaga search territory;
- menjaga connected journey.

---

## 9. INDEXABILITY

Tidak semua URL yang dapat dibuka harus diindeks.

URL dibedakan menjadi **PUBLIC / SEARCH LANDING** dan **INTERNAL / OWNER / UTILITY**.

Sitemap hanya memuat canonical URL yang memang ditujukan untuk indexing. Robots, noindex, canonical, sitemap, dan internal linking harus konsisten dengan keputusan indexability.

---

## 10. SHARE EXPERIENCE

Sharing merupakan bagian dari product experience TadabburLife.

Share output harus merepresentasikan sesi yang benar, bahasa yang benar, title/copy yang benar, URL publik yang benar, dan visual yang sesuai.

---

## 11. WORKING FEATURE PRESERVATION

Fitur yang sudah terbukti bekerja dianggap sebagai **KNOWN-GOOD BEHAVIOR**.

**FIX THE TARGET WITHOUT BREAKING THE NEIGHBOR.**

Perubahan explanatory content atau SEO tidak boleh digunakan sebagai alasan merusak fitur yang sudah bekerja.

---

## 12. CONTROLLED IMPROVEMENT

Perubahan dapat berupa small fix, batch update, content/SEO adaptation, atau major system update.

Major update harus memiliki scope yang jelas, baseline/known-good behavior, implementation check, regression check, deploy verification, dan live QC.

---

## 13. QC FRAMEWORK

### 13.1 Sacred Source Integrity QC

Verifikasi bahwa:

- teks ayat tidak berubah;
- referensi surah/ayat tidak berubah secara tidak sah;
- terjemahan yang ditetapkan tidak berubah;
- teks/rujukan hadis tidak berubah secara tidak sah;
- explanatory adaptation tidak bertentangan dengan sacred anchor.

Untuk perubahan global, sacred-source integrity harus dapat diverifikasi corpus-wide sebanyak mungkin secara otomatis.

### 13.2 Explanatory Content QC

Periksa:

- relevansi terhadap keyword/search intent;
- usefulness;
- factual/contextual accuracy;
- naturalness;
- tidak ada keyword stuffing;
- tidak ada unsupported religious claim;
- tidak ada forced interpretation;
- konsistensi dengan tema sesi.

### 13.3 Reader QC

Periksa clarity, usefulness, hierarchy, mobile comfort, navigation, next-step clarity, dan apakah perjalanan tadabbur tetap natural.

### 13.4 SEO QC

Periksa SERP intent, search territory, keyword mapping, relevance gate, title, H1, meta description, canonical, hreflang, internal linking, schema, sitemap, indexability, cannibalization, dan crawler-visible HTML.

Setiap bahasa dievaluasi berdasarkan search ecosystem masing-masing.

### 13.5 Technical / Regression QC

Periksa mobile, desktop, layout, spacing/padding, broken links, language switching, journey state, next-session behavior, sharing, OG metadata, crawler-visible HTML, dan regression terhadap halaman/sesi lain.

### 13.6 Active Corpus QC

QC mengikuti **ACTIVE CORPUS**, bukan jumlah sesi permanen.

Untuk perubahan global pada shared template, generator, routing, metadata engine, translation layer, content engine, atau shared component, wajib dilakukan corpus-wide verification. Sampling saja tidak cukup jika perubahan dapat memengaruhi seluruh corpus.

---

## 14. REPOSITORY WORKFLOW

### BEFORE WORK

READ MASTER-SOP → READ CURRENT-STATUS → DEFINE SCOPE → IDENTIFY SACRED SOURCE → IDENTIFY TARGET SEARCH TERRITORY → IDENTIFY AFFECTED FILES → IDENTIFY KNOWN-GOOD BEHAVIOR

### IMPLEMENT

MAKE CHANGE → SACRED SOURCE CHECK → EXPLANATORY CONTENT QC → SEO QC → REGRESSION CHECK

### AFTER DEPLOY

LIVE QC → READER QC → RELIGIOUS-INTEGRITY QC → SEO / TECHNICAL QC → UPDATE CURRENT-STATUS → RECORD SIGNIFICANT DECISION IN CHANGELOG

---

## 15. DEFINITION OF DONE

Pekerjaan belum dianggap selesai hanya karena code selesai, commit berhasil, build berhasil, atau deploy berhasil.

**DONE berarti:**

IMPLEMENTED  
+ LIVE VERIFIED  
+ SACRED SOURCE INTEGRITY VERIFIED  
+ EXPLANATORY CONTENT VERIFIED  
+ NO MATERIAL REGRESSION  
+ READER EXPERIENCE VERIFIED  
+ SEO / TECHNICAL VERIFIED WHEN RELEVANT  
+ CURRENT-STATUS UPDATED.

Untuk perubahan global, DONE juga membutuhkan active-corpus integrity verification.

---

## 16. GUARDRAILS

JANGAN:

- mengubah teks ayat Al-Qur'an untuk SEO atau alasan editorial;
- mengubah referensi ayat tanpa proses koreksi sumber yang terverifikasi;
- mengubah terjemahan Al-Qur'an yang telah ditetapkan hanya agar cocok dengan keyword;
- mengubah teks/rujukan hadis untuk SEO;
- memparafrase ayat/hadis lalu menyajikannya seolah-olah teks sumber;
- memaksakan keyword yang tidak relevan dengan ayat/hadis atau tema sesi;
- mengejar weak SERP hanya karena kompetisinya rendah;
- membuat unsupported religious claim;
- melakukan keyword stuffing;
- menerjemahkan keyword satu bahasa secara otomatis menjadi target bahasa lain;
- membuat target keyword tanpa SERP evidence;
- membuat dua canonical landing sengaja mengejar intent utama yang sama;
- memperbaiki satu fitur dengan merusak fitur lain;
- merusak journey demi landing-page SEO;
- memperlakukan salah satu bahasa sebagai versi sekunder;
- memasukkan owner/internal page ke index tanpa tujuan;
- menganggap build/deploy sukses sebagai bukti website benar;
- meninggalkan major update tanpa regression QC;
- mengubah known-good behavior di luar scope;
- membuat arsitektur yang bergantung pada jumlah sesi saat ini jika dapat dibuat data-driven.

---

## 17. WHAT DOES NOT BELONG IN MASTER-SOP

MASTER-SOP tidak digunakan untuk menyimpan informasi yang cepat berubah, seperti jumlah active session terkini, sesi terakhir yang dikerjakan, keyword target individual, hasil SERP terbaru, angka padding spesifik, nama file implementasi, bug aktif, eksperimen monetisasi, harga akses, campaign, atau pekerjaan berikutnya.

Informasi tersebut ditempatkan pada CURRENT-STATUS, TECHNICAL DOCUMENTATION, SEO DOCUMENTATION, PRODUCT SPECIFICATION, atau CHANGELOG.

---

## 18. MASTER-SOP CHANGE CONTROL

MASTER-SOP adalah dokumen stabil.

MASTER-SOP hanya direvisi apabila terjadi perubahan fundamental pada content integrity, product philosophy, architecture principle, search principle, QC principle, atau governance proyek.

Perubahan fundamental harus menaikkan versi dokumen dan dicatat dalam CHANGELOG.

---

# FINAL PRINCIPLES

**PROTECT THE QURAN AND HADITH SOURCE.**

**LET THE EXPLANATION ADAPT — NEVER THE REVELATION.**

**SERVE THE READER.**

**UNDERSTAND THE SEARCH INTENT.**

**TARGET OPPORTUNITY ONLY WHEN RELEVANCE IS REAL.**

**PRESERVE THE JOURNEY.**

**FIX THE TARGET WITHOUT BREAKING THE NEIGHBOR.**

**BUILD FOR THE ACTIVE CORPUS.**

**ARCHITECT FOR 1,000+.**

**DEPLOY IS NOT DONE. VERIFIED IS DONE.**

---

**END OF MASTER-SOP v1.1**
