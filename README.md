# Standalone Frappe CRM (Yalnız CRM)

Azərbaycan və regional tələblərə uyğunlaşdırılmış, müstəqil **Frappe CRM** konteynerləşdirilmiş mühiti.

> [!NOTE]
> Bu layihədə ERPNext-in ağır və mürəkkəb modulları (mühasibatlıq, istehsalat, anbar və s.) **yoxdur**. Sırf müasir **Frappe CRM (Vue 3)** və onun ehtiyac duyduğu təmiz **Frappe Framework** istifadə olunur.

---

## ✨ Xüsusiyyətlər

1. **Setup Wizard avtomatik tamamlanıb:** İlk girişdə heç bir ilkin konfiqurasiya / setup sualı tələb olunmur, birbaşa işə başlamaq mümkündür.
2. **AZN (₼) Valyutası:** Frappe-nin rəsmi bazasında olmayan Azərbaycan Manatı (`AZN`, simvol `₼`, qəpik `100`) avtomatik əlavə olunub və standart sistem valyutası kimi təyin edilib.
3. **Standart Dil:** Sistem və Administrator üçün standart olaraq **Türk dili (tr)** təyin edilib.
4. **Regional Ayarlar:** Ölkə: `Azerbaijan`, Saat qurşağı: `Asia/Baku`, Tarix formatı: `dd-mm-yyyy`.
5. **1 Komanda ilə işə düşmə:** Docker və Docker Compose vasitəsilə dərhal qalxır.

---

## 🚀 1 Komanda ilə Başlamaq

```bash
./start.sh
# və ya
make up
```

Sistem qalxdıqdan sonra brauzerdə açın:
- **URL:** [http://localhost:8080](http://localhost:8080) (CRM üçün: [http://localhost:8080/crm](http://localhost:8080/crm))
- **İstifadəçi adı:** `Administrator`
- **Şifrə:** `admin`

---

## 🛠 İdarəetmə Əmrləri

- **İşə salmaq:** `./start.sh` və ya `make up`
- **Dayandırmaq:** `./stop.sh` və ya `make stop`
- **Məlumatları yenidən idxal etmək:** `make import`
- **Loqlara baxmaq:** `make logs`
- **Statusu yoxlamaq:** `make status`
- **Tam sıfırlamaq (bütün məlumatları silmək):** `make clean`

---

## 📊 İdxal Edilmiş Məlumatlar və Fərdiləşdirmələr

1. **Ərazi İyerarxiyası (CRM Territory):**
   - 254 vahiddən ibarət tam iyerarxiya (`All Territories` -> `Azerbaijan` -> `Baku`, rayonlar, şəhərlər və Ağdərə daxil olmaqla).
   - Rayon adlarının fərqləri (`Absheron` vs `Absheron District`, `Sumgait` vs `Sumgayit City`, `Guba` vs `Quba District` və s.) heç bir join xətası olmadan avtomatik xəritələndirilib.
2. **Azərbaycan Sənaye Sahələri (CRM Industry):**
   - 38 yerli sənaye sahəsi (Qida, Tikinti, Logistika, İT və s.) sistemə əlavə edilib.
3. **Şirkətlər (CRM Organization - 20,000+):**
   - VÖEN, Telefon, Telefon 2, E-poçt, Rəhbər/Direktor, Poçt İndeksi, Tam Ünvan və Fəaliyyət qeydləri üçün xüsusi sahələr (Custom Fields) yaradılıb.
   - Siyahı və detal panellərində (UI Side Panel & List View) bütün bu sahələr aktivdir.
4. **Canlı Pipeline Nümunələri:**
   - Real sövdələşmələr (CRM Deal - AZN ilə mərhələlər: Won, Negotiation, Proposal, Demo) və Əlaqəli Şəxslər (Contacts) yaradılıb.

---

## 🏗 Arxitektura Stack-i

- **Frappe CRM App:** `ghcr.io/frappe/crm:latest`
- **Database:** `MariaDB 10.8` (utf8mb4_unicode_ci)
- **Cache & Queue:** `Redis 6.2`
- **Reverse Proxy:** `Nginx` (Port `8080`)
- **Auto-Config Script:** `scripts/setup_crm.py`
- **Data Import Script:** `scripts/import_crm_data.py`

