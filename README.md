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
- **Loqlara baxmaq:** `make logs`
- **Statusu yoxlamaq:** `make status`
- **Tam sıfırlamaq (bütün məlumatları silmək):** `make clean`

---

## 🏗 Arxitektura Stack-i

- **Frappe CRM App:** `ghcr.io/frappe/crm:latest`
- **Database:** `MariaDB 10.8` (utf8mb4_unicode_ci)
- **Cache & Queue:** `Redis 6.2`
- **Reverse Proxy:** `Nginx` (Port `8080`)
- **Auto-Config Script:** `scripts/setup_crm.py`
