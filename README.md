# Frappe CRM Azerbaijan 🇦🇿

Azərbaycan və regional biznes tələblərinə tam uyğunlaşdırılmış, müstəqil, yüksək performanslı və konteynerləşdirilmiş **Frappe CRM** mühiti.

> [!NOTE]
> Bu layihədə ERPNext-in ağır və artıq modulları (mühasibatlıq, istehsalat, anbar və s.) **yoxdur**. Sırf müasir **Frappe CRM (Vue 3 / Tailwind CSS)** və onun ehtiyac duyduğu təmiz **Frappe Framework v16** istifadə olunur.

---

## ✨ Əsas Xüsusiyyətlər

1. **20,000+ Azərbaycan Şirkəti (CRM Organization):**
   - VÖEN, əsas və ikinci telefon, e-poçt, rəhbər/direktor adı, poçt indeksi, tam ünvan və fəaliyyət qeydləri ilə tam inteqrasiya.
   - Siyahıda VÖEN və nömrə ilə sürətli axtarış və dinamik yan panel (Side Panel).
2. **254 Vahidlik Ərazi İyerarxiyası (CRM Territory):**
   - Bütün Bakı rayonları, Naxçıvan Muxtar Respublikası, Ağdərə rayonu daxil olmaqla bütün Azərbaycan rayon və şəhərləri iyerarxik strukturda qurulub. Heç bir join xətası yoxdur.
3. **89 Sənaye Sahəsi (CRM Industry):**
   - Azərbaycan bazarına xas 38 yerli sənaye sahəsi (Logistika, Tikinti, Qida, İT, Ticarət və s.) əlavə edilib.
4. **Sürətli Filtrlər (Quick Filters):**
   - Cədvəlin yuxarısında **Bölge** (Territory combobox), **Endüstri**, **VÖEN**, **Telefon** və **E-poçt** üzrə anında axtarış və filtrasiya.
5. **Canlı Satış Boru Kəməri (Deals & Pipeline):**
   - AZN valyutası ilə real sövdələşmələr (Won, Negotiation, Proposal, Demo).
6. **Zəng Qeydləri (Call Logs) & Təqvim (Calendar) & Tapşırıqlar (Tasks):**
   - Rəhbərlərlə aparılan danışıqlar, həftəlik rəngli təqvim tədbirləri və Kanban tipli tapşırıqlar aktivləşdirilib.
7. **Bütün Konfiqurasiya `.env` Faylı ilə İdarə Olunur:**
   - Portlar, parollar, valyuta, dil və sayt parametrləri `.env` vasitəsilə asanlıqla dəyişdirilə bilər.
8. **Lokal Şəbəkəyə Tam Açıqdır:**
   - Eyni Wi-Fi və ya LAN şəbəkəsində olan istənilən kompüter və ya telefondan birbaşa daxil olmaq mümkündür.
9. **Nginx Hazır Konfiqurasiyası:**
   - Öz domeniniz və Let's Encrypt SSL (HTTPS) sertifikatı üçün hazır Nginx şablonu təqdim olunur.
10. **1 Komanda ilə Başlamaq:**
    - Heç bir manual konfiqurasiya tələb olunmur; Setup Wizard avtomatik tamamlanır.

---

## 🚀 1 Komanda ilə İşə Salmaq (Zero-Config)

Terminalda layihə qovluğuna keçin və icra edin:

```bash
./start.sh
# və ya
make up
```

Skript avtomatik olaraq:
1. `.env` faylını yaradır (əgər yoxdursa).
2. MariaDB, Redis, WSGI Backend, Nginx və Socket.IO konteynerlərini qaldırır.
3. AZN valyutasını, Türk dilini və Azərbaycan regional sazlamalarını tətbiq edir.
4. Bütün əraziləri, sənaye sahələrini, 20 min şirkəti, zəngləri və tapşırıqları bazaya idxal edir.

Sistem hazır olduqdan sonra brauzerdə açın:
- **Lokal Giriş (Bu kompüterdən):** [http://localhost:8080/crm](http://localhost:8080/crm) (və ya [http://localhost:8080](http://localhost:8080))
- **Şəbəkə Girişi (Digər cihazlardan):** `http://<KOMPÜTERİN_IP_ÜNVANI>:8080` (məsələn: `http://192.168.1.77:8080`)
- **İstifadəçi adı:** `Administrator`
- **Şifrə:** `admin`

---

## ⚙️ `.env` Konfiqurasiya Faylı

Layihədəki bütün parametrlər `.env` faylı vasitəsilə idarə olunur. İstədiyiniz dəyəri dəyişə bilərsiniz:

```bash
# Host portu (Lokal şəbəkədə hər kəsə açıqdır)
CRM_PORT=8080

# Frappe Sayt Adı
FRAPPE_SITE_NAME=frontend

# Administrator Şifrəsi
ADMIN_PASSWORD=admin

# MariaDB Baza Şifrəsi
MYSQL_ROOT_PASSWORD=admin
MARIADB_ROOT_PASSWORD=admin

# Regional Parametrlər
DEFAULT_COUNTRY=Azerbaijan
DEFAULT_TIMEZONE=Asia/Baku
DEFAULT_CURRENCY=AZN
DEFAULT_LANGUAGE=tr
```

> **Qeyd:** Əgər `.env` faylında heç bir dəyişiklik etməsəniz, sistem standart etibarlı parametrlərlə 1 komanda ilə açılacaq.

---

## 🌐 Nginx ilə Domen və SSL (HTTPS) Quraşdırılması

Layihə daxilində hazır [nginx/frappecrm.conf](file:///home/ilkin/Desktop/opencode/frappe-crm/nginx/frappecrm.conf) şablonu yerləşdirilmişdir. Əgər sisteminizi real domendə (məs: `crm.sirketiniz.az`) və SSL ilə işlətmək istəyirsinizsə:

```bash
# 1. Konfiqurasiya faylını Nginx qovluğuna kopyalayın
sudo cp nginx/frappecrm.conf /etc/nginx/sites-available/frappecrm.conf

# 2. Domen adınızı qeyd edin
sudo nano /etc/nginx/sites-available/frappecrm.conf
# server_name crm.sirketiniz.az;

# 3. Saytı aktiv edin və Nginx-i yenidən başladın
sudo ln -s /etc/nginx/sites-available/frappecrm.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 4. Pulsuz Let's Encrypt SSL sertifikatı alın
sudo certbot --nginx -d crm.sirketiniz.az
```

---

## 🛠 İdarəetmə Əmrləri (`Makefile`)

Layihəni rahat idarə etmək üçün qısa əmrlər mövcuddur:

| Əmr | Təyinatı |
| :--- | :--- |
| `make up` və ya `./start.sh` | Bütün servisləri və CRM-i işə salır |
| `make stop` və ya `./stop.sh` | Servisləri dayandırır (məlumatlar qorunur) |
| `make restart` | Bütün konteynerləri yenidən başladır |
| `make logs` | Canlı sistem loqlarını izləyir (`docker compose logs -f`) |
| `make status` | Konteynerlərin vəziyyətini yoxlayır |
| `make import` | Şirkətləri və əraziləri təkrar bazaya idxal edir |
| `make clean` | Bütün konteynerləri və verilənlər bazasını sıfırlayır |

---

## 📖 Ətraflı Modul Sənədləri

Bütün modulların (Organizations, Contacts, Deals, Leads, Tasks, Calendar, Call Logs) daxili strukturu, xüsusi sahələri və funksionallığı barədə geniş məlumat üçün [MODULES.md](file:///home/ilkin/Desktop/opencode/frappe-crm/MODULES.md) faylına baxın.

---

## 🏗 Arxitektura və Texnologiyalar

- **Frontend:** Vue 3, Tailwind CSS, Frappe UI
- **Backend:** Frappe Framework v16, Python 3.11, Gunicorn WSGI
- **Real-time:** Node.js, Socket.IO (Port `9000`)
- **Database:** MariaDB 10.8 (`utf8mb4_unicode_ci`)
- **Cache & Queue:** Redis 6.2 (Cache & Background Worker)
- **Konteynerləşdirmə:** Docker & Docker Compose
- **İlkin Sazlama:** `scripts/setup_crm.py`
- **Məlumat İdxalı:** `scripts/import_crm_data.py`
