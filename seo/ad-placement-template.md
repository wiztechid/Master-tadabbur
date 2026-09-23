# TadabburLife — Ad Placement Template

**Version:** 1.0  
**Date:** 2026-09-23  
**Status:** APPROVED BLUEPRINT — NO LIVE AD CODE YET

## Prinsip

TadabburLife adalah produk tadabbur terlebih dahulu, baru kemudian permukaan monetisasi. Iklan tidak boleh memecah blok ayat/terjemahan, tafsir, hadis, atau berada dekat tombol navigasi/aksi yang berisiko memicu klik tidak sengaja.

Baseline saat launch: **maksimal 2 unit manual per landing sesi**, **1 unit homepage**, **1 unit hub ID/EN**, dan **0 iklan pada legal/trust pages**. Auto Ads agresif, anchor, dan vignette tetap OFF pada fase awal sampai mobile reader QC lulus.

## Landing sesi — posisi resmi

### S1 — Primary mid-content

Letakkan **setelah bagian “Fakta Nash • Pelajaran • Batas”** dan sebelum bagian penerapan/kehidupan.

Urutan:

Fakta Nash • Pelajaran • Batas
→ **ADS-S1**
→ Kehidupan / Penerapan

Alasan: pembaca sudah memperoleh ayat, konteks, tafsir/hadis, dan inti penjelasan; slot juga jauh dari tombol Previous/Next, share, dan Complete Reflection.

**Priority: HIGH — default launch slot.**

### S2 — Secondary late-content

Letakkan **setelah bagian Kehidupan/Penerapan dan sebelum Hikmah Utama atau Muhasabah**, menyesuaikan struktur sesi.

Urutan:

Kehidupan / Penerapan
→ **ADS-S2**
→ Hikmah Utama / Muhasabah

Gunakan hanya pada landing yang cukup panjang. Jika halaman pendek atau terasa padat di mobile, **S2 wajib dimatikan**.

**Priority: MEDIUM — optional setelah mobile QC.**

## Zona tanpa iklan

Jangan menaruh iklan:

- di dalam atau di antara Arabic Qur’an, transliterasi, dan terjemahan;
- di dalam Deep-SERP direct-answer block;
- di dalam kartu Tafsir atau Hadis;
- di dalam Reflection Card;
- tepat sebelum/sesudah Tandai Selesai Tadabbur / Complete Reflection;
- dekat Share, Previous, Next, language switcher, menu, CTA, dropdown, atau kontrol interaktif;
- di antara heading dan isi yang diterangkannya;
- dengan visual yang menyerupai session card, navigasi, tombol, atau rekomendasi TadabburLife.

## Homepage

Gunakan **HOME-01** setelah pembaca melewati hero dan minimal satu blok konten/produk yang substantif.

Urutan:

Hero / brand promise
→ Journey/current-session/content block
→ **ADS-HOME-01**
→ discovery/supporting section

Jangan menaruh iklan di atas fold sebelum pengunjung memahami apa itu TadabburLife. **Maksimal 1 unit saat launch.**

## Hub /tadabbur/ dan /en/tadabbur/

Gunakan **HUB-01** setelah intro dan sekitar **6–8 kartu sesi pertama**. Untuk corpus 47 sesi saat ini, satu unit sudah cukup. HUB-02 baru dipertimbangkan jika corpus jauh lebih panjang.

## Halaman tanpa iklan

Selalu ad-free:

- About
- Contact
- Privacy Policy
- Cookie Policy
- Terms
- Disclaimer
- owner/internal pages
- modal, share UI, progress UI, dan utility overlays.

## Interactive Journey

Pada fase awal, **jangan pasang manual ads di interactive reader**. Monetisasi Journey harus menjadi eksperimen terpisah setelah landing SEO stabil dan accidental-click QC lulus.

## Styling dasar ad container

Gunakan container netral, bukan kartu yang menyerupai konten:

    .ad-zone {
      width: 100%;
      margin: 32px auto;
      padding: 12px 0;
      text-align: center;
      clear: both;
    }

Label hanya netral seperti **Advertisement** / **Iklan**, tanpa panah, animasi, atau ajakan mengklik. Setelah ukuran unit nyata diketahui, reserve ruang yang cukup untuk mengurangi layout shift.

## Mobile QC wajib

Sebelum sebuah slot diaktifkan:

- tidak ada overlap/horizontal overflow;
- iklan tidak berdesakan dengan link atau button;
- Arabic/translation tetap satu blok utuh;
- konten tetap dominan;
- spacing nyaman;
- tidak ada sticky UI yang bertabrakan.

## Affiliate coexistence

AdSense dan affiliate banner jangan ditumpuk berdekatan. Sisakan minimal satu bagian konten substantif di antara dua blok komersial. Jika halaman menggunakan affiliate module, pertimbangkan menonaktifkan S2.

## Guard privasi agama

Jangan membuat first-party audience, remarketing list, atau personalization logic dari sesi Qur’an yang dibaca, progress tadabbur, refleksi, atau inferensi keyakinan agama. Progress tetap menjadi fitur pengalaman produk, bukan sinyal penargetan iklan.

## Launch matrix

| Surface | Slot | Launch |
|---|---|---|
| Session landing | S1 setelah Fakta Nash/Pelajaran/Batas | YES |
| Session landing | S2 setelah application section | OPTIONAL setelah mobile QC |
| Homepage | HOME-01 setelah blok substantif pertama | YES |
| ID hub | HUB-01 setelah 6–8 sesi | YES |
| EN hub | HUB-01 setelah 6–8 sesi | YES |
| Legal/trust pages | none | NO ADS |
| Interactive controls/modals | none | NO ADS |
| Ayat/translation/tafsir/hadith | none | NO ADS |

## Activation checklist

1. Site sudah approved/connected ke AdSense.
2. Publisher ID asli tersedia; jangan pernah commit placeholder pub-ID ke production.
3. ads.txt dipublikasikan menggunakan publisher ID resmi.
4. Privacy/Cookie disclosure tetap current.
5. Consent platform dikonfigurasi jika diwajibkan.
6. S1/S2 lulus mobile + desktop reader QC.
7. Navigation/completion controls jelas terpisah dari iklan.
8. Data minat agama tidak digunakan untuk ad personalization.
9. Total iklan/promo berbayar tetap lebih sedikit daripada publisher-content.
10. Jalankan live regression QC setelah aktivasi.

## Decision

**TadabburLife ad-placement baseline = READER-FIRST / CONSERVATIVE.**

Mulai dengan satu atau dua in-page unit pada sesi panjang; jangan langsung mengejar maximum-density Auto Ads.