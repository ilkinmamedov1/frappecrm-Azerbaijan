# Frappe CRM Azerbaijan - Modullar və Funksionallıq İzahı

Bu sənəddə **Frappe CRM Azerbaijan** layihəsinə daxil olan bütün əsas modullar, tətbiq edilmiş yerli fərdiləşdirmələr və verilənlər strukturu ətraflı izah edilmişdir.

---

## 1. 🏢 Organizations (Şirkətlər və Təşkilatlar)

Bu modul sistemin əsas onurğa sütunudur və Azərbaycan üzrə **20,000-dən çox** real müəssisə və şirkəti əhatə edir.

### Xüsusi Sahələr (Custom Fields):
Frappe CRM-in standart modelinə Azərbaycan biznes mühitinin tələblərinə uyğun aşağıdakı rəsmi sahələr əlavə edilmişdir:
- **VÖEN (`voen`):** Şirkətin Vahid Ödəyici Eyniləşdirmə Nömrəsi (Vergi ID). Cədvəl axtarışında və filtrində dərhal çıxır.
- **Telefon (`phone`):** Əsas korporativ əlaqə nömrəsi.
- **Telefon 2 (`phone_2`):** Əlavə və ya qısa nömrə (məsələn: `*6600`, `*2114`).
- **E-poçt (`email`):** Rəsmi korporativ elektron poçt ünvanı.
- **Rəhbər / Direktor (`director`):** Müəssisənin direktoru və ya rəhbər şəxsi.
- **Poçt İndeksi (`post_code`):** Poçt indeksi (məs: `AZ1000`, `AZ1145`).
- **Tam Ünvan (`full_address`):** Rayon, qəsəbə, küçə, bina və məhəlləni əks etdirən ətraflı ünvan mətni.
- **Fəaliyyət Sahəsi / Qeyd (`notes`):** Şirkətin dəqiq ixtisaslaşdığı xidmət və ya məhsul növü.

### Sürətli Filtrlər (Quick Filters):
Siyahının ən yuxarı panelində 1 kliklə filtrasiya imkanı:
- **Bölge:** Azərbaycanın 254 ərazi vahidindən birini seçərək şirkətləri filtr etmək.
- **Endüstri:** Sənaye növünə görə filtr.
- **VÖEN:** Nömrəyə görə anında axtarış.
- **Telefon & E-poçt:** Əlaqə məlumatlarına görə axtarış.

---

## 2. 🗺 Territories (Ərazi İyerarxiyası)

Sistemdə **254 ərazi vahidindən** ibarət dəqiq ağac iyerarxiyası qurulmuşdur:
- `All Territories` (Kök)
  - `Azerbaijan` (Ölkə)
    - `Baku` (Paytaxt - Qrup)
      - *Yasamal, Nəsimi, Nərimanov, Xətai, Binəqədi, Səbail, Sabunçu, Suraxanı, Xəzər, Qaradağ, Pirallahı, Nizami rayonları.*
    - `Nakhchivan Autonomous Republic`
      - *Naxçıvan şəhəri, Babək, Culfa, Ordubad, Sədərək, Şahbuz, Şərur, Kəngərli rayonları.*
    - Bütün digər şəhər və rayonlar: *Gəncə, Sumqayıt, Mingəçevir, Şirvan, Abşeron, Quba, Qusar, Lənkəran, Şəki, Ağdam, Ağdərə, Şuşa, Füzuli, Zəngilan, Kəlbəcər və s.*

> **Qeyd:** Excel-dəki qısa adlar (`Absheron`, `Guba`, `Sumgait`) ilə standart adlar (`Absheron District`, `Quba District`, `Sumgayit City`) arasında 100%-lik xəritələndirmə aparılıb və heç bir join/xarici açar xətası yoxdur.

---

## 3. 🏭 Industries (Sənaye Sahələri)

Sistemdə cəmi **89 sənaye sahəsi** mövcuddur. Bunun 38-i sırf Azərbaycan bazarının yerli sektorlarını təşkil edir:
- *Logistika, Anbar və Nəqliyyat*
- *Tikinti, Təmir və Tikinti Materialları*
- *Qida və İçki*
- *İT və Proqram Təminatı*
- *Bank, Maliyyə və Sığorta*
- *Ticarət və Distribusiya*
- *Tibb, Əczaçılıq və Laboratoriya*
- *Kənd Təsərrüfatı və Baytarlıq*
- *Neft, Qaz və Kimya*
- *Turizm, Otel və İaşə* və s.

---

## 4. 👥 Contacts (Kişilər / Əlaqəli Şəxslər)

Təşkilatlarla əlaqəli şəxslərin (direktorlar, menecerlər, satınalma rəhbərləri) reyestri.

### Cədvəl Sütunları:
- **Adı (`full_name`):** Şəxsin tam adı və rəngli avatarı.
- **Vəzifə (`designation`):** Şəxsin tutduğu vəzifə (məs: `Direktor`).
- **Telefon (`mobile_no`):** Mobil və ya birbaşa nömrə (kliklədikdə zəng funksiyası).
- **E-poçt (`email_id`):** Şəxsi və ya korporativ e-poçt.
- **Təşkilat (`company_name`):** Təmsil etdiyi şirkətin adı və loqosu.
- **Son Yenilənmə (`modified`):** Qeydin son dəyişdirilmə tarixi.

---

## 5. 💼 Deals (Sövdələşmələr / Satış Boru Kəməri)

Satış prosesini mərhələ-mərhələ idarə etmək üçün müasir **Vue 3 Kanban** və Siyahı lövhəsi.

### Mərhələlər (Stages):
1. **Qualification (İlkin Uyğunlaşdırma)**
2. **Demo/Making (Təqdimat və Nümayiş)**
3. **Proposal/Quotation (Qiymət Təklifi)**
4. **Negotiation (Danışıqlar və Razılaşma)**
5. **Ready to Close (Bağlanmağa Hazır)**
6. **Won (Uğurla Qazanıldı 🏆)**
7. **Lost (İtirildi)**

Bütün məbləğlər və hesablamalar standart olaraq **AZN (₼)** valyutası ilə aparılır.

---

## 6. 🎯 Leads (Müştəri Namizədləri / Adaylar)

Soyuq zənglər, sərgilər, vebsayt və reklam kampaniyalarından daxil olan potensial müştərilərin idarə edilməsi.
- Namizəd təsdiqləndikdə tək kliklə **Organization (Şirkət)**, **Contact (Əlaqə)** və ya **Deal (Sövdələşmə)** sənədinə çevrilir.

---

## 7. ✅ Tasks (Görevlər və Tapşırıqlar)

Satış komandası üçün gündəlik icra ediləcək tapşırıqlar:
- **Prioritetlər:** `High` (Yüksək), `Medium` (Orta), `Low` (Aşağı)
- **Statuslar:** `Todo` (Görüləcək), `In Progress` (İcrada), `Done` (Tamamlandı), `Backlog` (Gözləmədə)
- Hər bir tapşırıq birbaşa əlaqəli şirkətə və ya sövdələşməyə bağlanır.

---

## 8. 📅 Calendar (Takvim / Təqvim)

Görüşlər, zəng vaxtları, demo təqdimatları və müqavilə imzalanma tarixlərini əks etdirən interaktiv təqvim.
- Həftəlik, günlük və aylıq baxış rejimləri.
- Rəngli təsnifatlaşdırma (Yaşıl: Uğurlu, Mavi: Görüş, Narıncı: Təqdimat, Bənövşəyi: Demo).

---

## 9. 📞 Call Logs (Zəng Qeydləri)

Müştərilərlə aparılan telefon danışıqlarının qeydiyyatı:
- Zəng növü: Daxil olan (`Incoming`) və ya Çıxan (`Outgoing`).
- Status: `Completed`, `In Progress`, `Busy`, `No Answer`.
- Danışıq müddəti (dəqiqə və saniyə).
- Nömrə üzrə şirkət və kontaktın sistem tərəfindən avtomatik tanınması.
