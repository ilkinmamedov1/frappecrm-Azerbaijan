#!/usr/bin/env python3
"""
Frappe CRM Məlumat İdxalı və Fərdiləşdirmə Skripti:
1. Ərazi iyerarxiyasını (CRM Territory) idxal edir və Ağdərə rayonunu əlavə edir.
2. Excel-dəki 74 rayonu tam xəritələndirir (mapping) - heç bir join/link xətası olmur.
3. 38 Azərbaycan sənaye sahəsini (CRM Industry) əlavə edir.
4. CRM Organization üçün xüsusi sahələri (VÖEN, telefon, direktor, tam ünvan və s.) yaradır.
5. CRM Fields Layout və CRM View Settings-i yeniləyərək UI-da zəngin görünüş təmin edir.
6. 20,000+ şirkəti sürətli batch rejimində bazaya idxal edir.
7. UI-da canlı hərəkət üçün nümunəvi Əlaqəli Şəxslər (Contacts), Sövdələşmələr (Deals) və Liderlər (Leads) yaradır.
"""

import os
import sys
import openpyxl
from datetime import datetime

# Frappe mühitini təyin edirik
bench_sites = "/home/frappe/frappe-bench/sites"
if os.path.exists(bench_sites):
    os.chdir(bench_sites)

import frappe
from frappe.utils import now_datetime

def get_excel_path(filename):
    paths = [
        f"/tmp/frappecrm/{filename}",
        f"/home/frappe/frappe-bench/sites/../data/{filename}",
        f"/opt/data/{filename}",
        f"/home/ilkin/Desktop/frappecrm/{filename}"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def setup_custom_fields():
    print("--> 1. Xüsusi sahələr (Custom Fields) yoxlanılır və yaradılır...")
    
    # Cədvəlin uzunluğunu tənzimləyirik ki, 140 simvoldan uzun adlarda SQL xətası olmasın
    try:
        frappe.db.sql("ALTER TABLE `tabCRM Organization` MODIFY name VARCHAR(255), MODIFY organization_name VARCHAR(255);")
    except Exception as e:
        pass

    custom_fields = [
        {'fieldname': 'voen', 'label': 'VÖEN', 'fieldtype': 'Data', 'insert_after': 'organization_name', 'in_list_view': 1, 'in_standard_filter': 1},
        {'fieldname': 'phone', 'label': 'Telefon', 'fieldtype': 'Data', 'insert_after': 'website', 'in_list_view': 1, 'in_standard_filter': 1},
        {'fieldname': 'phone_2', 'label': 'Telefon 2', 'fieldtype': 'Data', 'insert_after': 'phone'},
        {'fieldname': 'email', 'label': 'E-poçt', 'fieldtype': 'Data', 'insert_after': 'phone_2', 'in_standard_filter': 1},
        {'fieldname': 'director', 'label': 'Rəhbər / Direktor', 'fieldtype': 'Data', 'insert_after': 'email'},
        {'fieldname': 'post_code', 'label': 'Poçt İndeksi', 'fieldtype': 'Data', 'insert_after': 'territory'},
        {'fieldname': 'full_address', 'label': 'Tam Ünvan', 'fieldtype': 'Small Text', 'insert_after': 'post_code'},
        {'fieldname': 'notes', 'label': 'Fəaliyyət Sahəsi / Qeyd', 'fieldtype': 'Small Text', 'insert_after': 'full_address'}
    ]

    for cf_data in custom_fields:
        if not frappe.db.exists('Custom Field', {'dt': 'CRM Organization', 'fieldname': cf_data['fieldname']}):
            cf = frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': 'CRM Organization',
                **cf_data
            })
            cf.insert(ignore_permissions=True)
            print(f"  + Custom Field əlavə edildi: {cf_data['fieldname']}")

    frappe.db.commit()
    frappe.clear_cache(doctype='CRM Organization')

    # FCRM Settings valyutasını AZN edirik
    try:
        fcrm = frappe.get_single('FCRM Settings')
        fcrm.currency = 'AZN'
        fcrm.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        pass

    # UI Side Panel layout-u yeniləyirik
    import json
    side_panel = frappe.get_doc('CRM Fields Layout', 'CRM Organization-Side Panel')
    layout = [
        {
            'label': 'Əsas Məlumatlar',
            'name': 'details_section',
            'opened': True,
            'columns': [
                {
                    'name': 'col_main',
                    'fields': [
                        'organization_name',
                        'voen',
                        'phone',
                        'phone_2',
                        'email',
                        'website',
                        'director',
                        'territory',
                        'industry',
                        'no_of_employees',
                        'full_address',
                        'post_code',
                        'notes'
                    ]
                }
            ]
        }
    ]
    side_panel.layout = json.dumps(layout)
    side_panel.save(ignore_permissions=True)

    if frappe.db.exists('CRM Fields Layout', 'CRM Organization-Quick Entry'):
        qe = frappe.get_doc('CRM Fields Layout', 'CRM Organization-Quick Entry')
        qe.layout = json.dumps(layout)
        qe.save(ignore_permissions=True)

    # CRM View Settings list sütunlarını tənzimləyirik
    columns = [
        {'label': 'Şirkət Adı', 'type': 'Data', 'key': 'organization_name', 'width': '18rem'},
        {'label': 'VÖEN', 'type': 'Data', 'key': 'voen', 'width': '10rem'},
        {'label': 'Telefon', 'type': 'Data', 'key': 'phone', 'width': '12rem'},
        {'label': 'Bölge', 'type': 'Link', 'key': 'territory', 'options': 'CRM Territory', 'width': '12rem'},
        {'label': 'Endüstri', 'type': 'Link', 'key': 'industry', 'options': 'CRM Industry', 'width': '14rem'},
        {'label': 'Website', 'type': 'Data', 'key': 'website', 'width': '12rem'},
        {'label': 'Ünvan', 'type': 'Small Text', 'key': 'full_address', 'width': '18rem'},
        {'label': 'Son Yenilənmə', 'type': 'Datetime', 'key': 'modified', 'width': '8rem'}
    ]
    rows = ['name', 'organization_name', 'voen', 'phone', 'territory', 'industry', 'website', 'full_address', 'modified']

    view_name = 'CRM Organization-default-list'
    if not frappe.db.exists('CRM View Settings', view_name):
        view = frappe.get_doc({
            'doctype': 'CRM View Settings',
            'name': view_name,
            'label': 'Bütün Şirkətlər',
            'dt': 'CRM Organization',
            'type': 'list',
            'is_default': 1,
            'is_standard': 1,
            'public': 1,
            'columns': json.dumps(columns),
            'rows': json.dumps(rows)
        })
        view.insert(ignore_permissions=True)
    else:
        view = frappe.get_doc('CRM View Settings', view_name)
        view.columns = json.dumps(columns)
        view.rows = json.dumps(rows)
        view.is_default = 1
        view.save(ignore_permissions=True)

    # Quick Filters (Bölge, Endüstri, VÖEN, Telefon, E-poçt) qlobal sazlaması
    quick_filters = ['territory', 'industry', 'voen', 'phone', 'email']
    if gs := frappe.db.exists('CRM Global Settings', {'dt': 'CRM Organization', 'type': 'Quick Filters'}):
        frappe.db.set_value('CRM Global Settings', gs, 'json', json.dumps(quick_filters))
    else:
        doc = frappe.new_doc('CRM Global Settings')
        doc.dt = 'CRM Organization'
        doc.type = 'Quick Filters'
        doc.json = json.dumps(quick_filters)
        doc.insert(ignore_permissions=True)

    from frappe.custom.doctype.property_setter.property_setter import make_property_setter
    for f in ['territory', 'industry']:
        make_property_setter('CRM Organization', f, 'in_standard_filter', '1', 'Check', validate_fields_for_doctype=False)

    frappe.db.commit()
    print("✓ Xüsusi sahələr və UI interfeysi hazırlandı.")

def setup_territories():
    print("--> 2. Ərazi iyerarxiyası (CRM Territory) yoxlanılır və idxal edilir...")
    
    if not frappe.db.exists('CRM Territory', 'All Territories'):
        frappe.get_doc({
            'doctype': 'CRM Territory',
            'territory_name': 'All Territories',
            'is_group': 1
        }).insert(ignore_permissions=True)

    t_file = get_excel_path("territory_import_staged_all.xlsx") or get_excel_path("territories_staged.xlsx")
    if t_file:
        wb = openpyxl.load_workbook(t_file, read_only=True)
        for sheetname in ['01 Import First', '02 Import Second', '03 Import Third']:
            if sheetname in wb.sheetnames:
                ws = wb[sheetname]
                rows = list(ws.iter_rows(values_only=True))[1:]
                for r in rows:
                    name, parent, is_group = r[0], r[1], int(r[2] or 0)
                    if name and not frappe.db.exists('CRM Territory', name):
                        frappe.get_doc({
                            'doctype': 'CRM Territory',
                            'territory_name': name,
                            'parent_crm_territory': parent,
                            'is_group': is_group
                        }).insert(ignore_permissions=True)

    # Ağdərə rayonunu əlavə edirik
    if not frappe.db.exists('CRM Territory', 'Aghdara District'):
        frappe.get_doc({
            'doctype': 'CRM Territory',
            'territory_name': 'Aghdara District',
            'parent_crm_territory': 'Azerbaijan',
            'is_group': 0
        }).insert(ignore_permissions=True)

    frappe.db.commit()
    print(f"✓ Ərazi iyerarxiyası hazır! Cəmi ərazi sayı: {frappe.db.count('CRM Territory')}")

def build_territory_mapping():
    existing_territories = set(frappe.get_all('CRM Territory', pluck='name'))
    special = {
        'Aghdara': 'Aghdara District',
        'Aghjabadi': 'Agjabadi District',
        'Agstafa': 'Aghstafa District',
        'Gabala': 'Qabala District',
        'Gakh': 'Qakh District',
        'Gazakh': 'Qazakh District',
        'Gobustan': 'Qobustan District',
        'Guba': 'Quba District',
        'Gubadli': 'Qubadli District',
        'Gusar': 'Qusar District',
        'Masalli': 'Masally District',
        'Nakhchivan': 'Nakhchivan City',
        'Saatli': 'Saatly District',
        'Sumgait': 'Sumgayit City',
        'Zagatala': 'Zaqatala District',
    }
    
    def mapper(reg_name):
        if not reg_name:
            return 'Azerbaijan'
        reg_name = str(reg_name).strip()
        if reg_name in existing_territories:
            return reg_name
        if reg_name in special and special[reg_name] in existing_territories:
            return special[reg_name]
        if f"{reg_name} District" in existing_territories:
            return f"{reg_name} District"
        if f"{reg_name} City" in existing_territories:
            return f"{reg_name} City"
        return 'Azerbaijan'

    return mapper

def setup_industries(org_file):
    print("--> 3. Azərbaycan Sənaye Sahələri (CRM Industry) yoxlanılır...")
    wb = openpyxl.load_workbook(org_file, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c).strip() if c is not None else '' for c in rows[0]]
    ind_idx = header.index('Endüstri') if 'Endüstri' in header else -1

    if ind_idx != -1:
        industries = set(str(r[ind_idx]).strip() for r in rows[1:] if r[ind_idx])
        created = 0
        for ind in sorted(industries):
            if not frappe.db.exists('CRM Industry', ind):
                frappe.get_doc({
                    'doctype': 'CRM Industry',
                    'industry': ind
                }).insert(ignore_permissions=True)
                created += 1
        frappe.db.commit()
        print(f"✓ Sənaye sahələri hazır! Əlavə edildi: {created}, Cəmi: {frappe.db.count('CRM Industry')}")

def import_organizations(org_file):
    print(f"--> 4. Şirkətlər faylı oxunur: {org_file}...")
    wb = openpyxl.load_workbook(org_file, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c).strip() if c is not None else '' for c in rows[0]]
    
    col_idx = {name: header.index(name) for name in header if name}
    print(f"  Toplam şirkət sətri: {len(rows)-1}")

    territory_map = build_territory_mapping()
    existing_orgs = set(frappe.get_all('CRM Organization', pluck='name'))
    seen_names = set(existing_orgs)

    now_str = str(now_datetime())
    records = []
    skipped = 0
    directors_for_contacts = []

    for i, r in enumerate(rows[1:]):
        name_val = r[col_idx['Şirket Adı']] if 'Şirket Adı' in col_idx and col_idx['Şirket Adı'] < len(r) else None
        if not name_val:
            skipped += 1
            continue

        raw_name = str(name_val).strip()
        # Max length 250
        if len(raw_name) > 250:
            raw_name = raw_name[:250]

        # Duplicate handle
        org_name = raw_name
        if org_name in seen_names:
            suffix = 2
            cand = f"{raw_name} ({suffix})"
            while cand in seen_names:
                suffix += 1
                cand = f"{raw_name} ({suffix})"
            org_name = cand
        seen_names.add(org_name)

        # Field extractions
        emp = str(r[col_idx['Personel Sayısı']]).strip() if 'Personel Sayısı' in col_idx and r[col_idx['Personel Sayısı']] else '1-10'
        website = str(r[col_idx['Website']]).strip() if 'Website' in col_idx and r[col_idx['Website']] else None
        phone = str(r[col_idx['Telefon']]).strip() if 'Telefon' in col_idx and r[col_idx['Telefon']] else None
        voen = str(r[col_idx['VOEN']]).strip() if 'VOEN' in col_idx and r[col_idx['VOEN']] else None
        phone2 = str(r[col_idx['Sirket Telefonu 2']]).strip() if 'Sirket Telefonu 2' in col_idx and r[col_idx['Sirket Telefonu 2']] else None
        raw_reg = r[col_idx['Bölge']] if 'Bölge' in col_idx and col_idx['Bölge'] < len(r) else None
        territory = territory_map(raw_reg)
        ind = str(r[col_idx['Endüstri']]).strip() if 'Endüstri' in col_idx and r[col_idx['Endüstri']] else None
        pcode = str(r[col_idx['Post Code']]).strip() if 'Post Code' in col_idx and r[col_idx['Post Code']] else None
        director = str(r[col_idx['Director']]).strip() if 'Director' in col_idx and r[col_idx['Director']] else None
        email = str(r[col_idx['E-posta']]).strip() if 'E-posta' in col_idx and r[col_idx['E-posta']] else None
        notes = str(r[col_idx['Qeyd/Not']]).strip() if 'Qeyd/Not' in col_idx and r[col_idx['Qeyd/Not']] else None
        addr = str(r[col_idx['Adres']]).strip() if 'Adres' in col_idx and r[col_idx['Adres']] else None

        if director and director != '0':
            # Remove trailing semicolon
            director_clean = director.rstrip(';').strip()
            if len(directors_for_contacts) < 20:
                directors_for_contacts.append({
                    'org': org_name,
                    'director': director_clean,
                    'phone': phone,
                    'email': email
                })

        records.append((
            org_name, now_str, now_str, 'Administrator', 'Administrator', 0, 0,
            org_name, emp, 'AZN', 1.0, 0.0,
            website, territory, ind,
            voen, phone, phone2, email, director, pcode, addr, notes
        ))

    print(f"  Hazırlanmış unikal qeyd sayı: {len(records)} (Keçilən: {skipped})")
    print("--> 5. MariaDB üzərindən sürətli batch idxalı başlayır...")

    fields = [
        'name', 'creation', 'modified', 'modified_by', 'owner', 'docstatus', 'idx',
        'organization_name', 'no_of_employees', 'currency', 'exchange_rate', 'annual_revenue',
        'website', 'territory', 'industry',
        'voen', 'phone', 'phone_2', 'email', 'director', 'post_code', 'full_address', 'notes'
    ]

    frappe.db.bulk_insert('CRM Organization', fields, records, ignore_duplicates=True, chunk_size=1000)
    frappe.db.commit()
    print("✓ Bütün şirkətlər uğurla idxal olundu!")
    return directors_for_contacts

def setup_sample_pipeline(directors):
    print("--> 6. UI üçün nümunəvi Sövdələşmələr (Deals) və Əlaqələr (Contacts) yaradılır...")
    
    # Contact yaratmaq
    contact_count = 0
    for d in directors[:15]:
        full_name = d['director']
        # remove suffixes like -direktor
        if '-' in full_name:
            full_name = full_name.split('-')[0].strip()
        first_name = full_name.split()[0]
        last_name = " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else ""

        if not frappe.db.exists('Contact', {'first_name': first_name, 'company_name': d['org']}):
            contact = frappe.get_doc({
                'doctype': 'Contact',
                'first_name': first_name,
                'last_name': last_name,
                'company_name': d['org'],
                'mobile_no': d['phone'],
                'email_id': d['email'] if d['email'] and d['email'] != '0' else None,
                'links': [
                    {'link_doctype': 'CRM Organization', 'link_name': d['org']}
                ]
            })
            try:
                contact.insert(ignore_permissions=True)
                contact_count += 1
            except Exception:
                pass

    frappe.db.commit()
    print(f"✓ Əlaqəli şəxslər (Contacts) yaradıldı: {contact_count}")

    # Deals yaratmaq
    deals_data = [
        {'title': 'İllik Logistika və Daşıma Müqaviləsi', 'org': 'YOM Logistics', 'status': 'Won', 'amount': 25000},
        {'title': 'Tikinti Materialları Təchizatı Tenderi', 'org': 'Solida Xırdalan (SOLİDA MMC)', 'status': 'Negotiation', 'amount': 48500},
        {'title': 'Supermarket Şəbəkəsi Korporativ Tərəfdaşlıq', 'org': 'OBA MARKET - 69', 'status': 'Proposal/Quotation', 'amount': 72000},
        {'title': 'Qida və Restoran Şəbəkəsi Təchizatı', 'org': 'Domino’s Pizza Azerbaijan (Xırdalan filialı)', 'status': 'Qualified', 'amount': 18000},
        {'title': 'Sənaye Avadanlığı və Ehtiyat Hissələri Alqısı', 'org': 'AZTEXNİKA MMC', 'status': 'Demo/Making', 'amount': 95000},
    ]

    deals_created = 0
    for deal_info in deals_data:
        # Check if org exists
        if frappe.db.exists('CRM Organization', deal_info['org']):
            org_doc = frappe.get_doc('CRM Organization', deal_info['org'])
            deal = frappe.get_doc({
                'doctype': 'CRM Deal',
                'organization': org_doc.name,
                'currency': 'AZN',
                'annual_revenue': deal_info['amount'],
                'status': deal_info['status'],
                'deal_owner': 'Administrator',
                'email': org_doc.email,
                'mobile_no': org_doc.phone
            })
            try:
                deal.insert(ignore_permissions=True)
                deals_created += 1
            except Exception as e:
                pass

    frappe.db.commit()
    print(f"✓ Pipeline Sövdələşmələri (Deals) yaradıldı: {deals_created}")

    # Leads yaratmaq
    sample_leads = [
        {'first_name': 'Elşən', 'last_name': 'Əliyev', 'organization': 'ProAV', 'status': 'Qualified', 'email': 'elshen@proav.az', 'mobile_no': '+994125254272', 'source': 'Exhibition', 'territory': 'Baku', 'industry': 'İT və Proqram Təminatı', 'lead_owner': 'Administrator'},
        {'first_name': 'Səbinə', 'last_name': 'Qurbanova', 'organization': 'BATEEL', 'status': 'Contacted', 'email': 'info@bateel.az', 'mobile_no': '+994125116934', 'source': 'Campaign', 'territory': 'Baku', 'industry': 'Qida və İçki', 'lead_owner': 'Administrator'},
        {'first_name': 'Elçin', 'last_name': 'Vəliyev', 'organization': 'VM MMC', 'status': 'New', 'email': 'elchin@vmc.az', 'mobile_no': '+994124906086', 'source': 'Cold Calling', 'territory': 'Baku', 'industry': 'Poliqrafiya, Çap və Nəşriyyat', 'lead_owner': 'Administrator'},
        {'first_name': 'Loğman', 'last_name': 'Həsənov', 'organization': 'YOM Logistics', 'status': 'Nurture', 'email': 'logman@yomlogistics.az', 'mobile_no': '+994124482401', 'source': 'Reference', 'territory': 'Absheron District', 'industry': 'Logistika, Anbar və Nəqliyyat', 'lead_owner': 'Administrator'}
    ]
    leads_created = 0
    for l in sample_leads:
        if not frappe.db.exists('CRM Lead', {'email': l['email']}):
            lead = frappe.get_doc({'doctype': 'CRM Lead', **l})
            lead.insert(ignore_permissions=True)
            leads_created += 1
    frappe.db.commit()
    print(f"✓ Müştəri namizədləri (Leads) yaradıldı: {leads_created}")

    # Call Logs (Zəng Qeydləri) yaratmaq
    call_logs = [
        {
            'id': 'CALL-2026-00001', 'from': '+994124482401', 'to': '+994502345678',
            'type': 'Incoming', 'status': 'Completed', 'telephony_medium': 'Manual',
            'duration': 185, 'start_time': '2026-11-16 11:30:00', 'end_time': '2026-11-16 11:33:05',
            'receiver': 'Administrator', 'reference_doctype': 'CRM Organization', 'reference_docname': 'YOM Logistics',
            'links': [{'link_doctype': 'CRM Organization', 'link_name': 'YOM Logistics'}]
        },
        {
            'id': 'CALL-2026-00002', 'from': '+994502345678', 'to': '+994773223146',
            'type': 'Outgoing', 'status': 'Completed', 'telephony_medium': 'Manual',
            'duration': 240, 'start_time': '2026-11-16 14:15:00', 'end_time': '2026-11-16 14:19:00',
            'caller': 'Administrator', 'reference_doctype': 'CRM Organization', 'reference_docname': 'Solida Xırdalan (SOLİDA MMC)',
            'links': [{'link_doctype': 'CRM Organization', 'link_name': 'Solida Xırdalan (SOLİDA MMC)'}]
        },
        {
            'id': 'CALL-2026-00003', 'from': '+994554007839', 'to': '+994502345678',
            'type': 'Incoming', 'status': 'Completed', 'telephony_medium': 'Manual',
            'duration': 120, 'start_time': '2026-11-16 16:00:00', 'end_time': '2026-11-16 16:02:00',
            'receiver': 'Administrator', 'reference_doctype': 'CRM Organization', 'reference_docname': 'OBA MARKET - 69',
            'links': [{'link_doctype': 'CRM Organization', 'link_name': 'OBA MARKET - 69'}]
        }
    ]
    calls_created = 0
    for cl in call_logs:
        if not frappe.db.exists('CRM Call Log', cl['id']):
            doc = frappe.get_doc({'doctype': 'CRM Call Log', **cl})
            doc.insert(ignore_permissions=True)
            calls_created += 1
    frappe.db.commit()
    print(f"✓ Zəng qeydləri (Call Logs) yaradıldı: {calls_created}")

    # Calendar Events (Təqvim Tədbirləri) yaratmaq
    events_data = [
        {
            'subject': 'YOM Logistics — İllik Daşıma Şərtlərinin Təsdiqi',
            'starts_on': '2026-11-16 20:00:00', 'ends_on': '2026-11-16 21:00:00',
            'color': '#10b981', 'event_type': 'Private', 'status': 'Open',
            'description': 'YOM Logistics rəhbəri ilə illik logistika müqaviləsinin yekun təsdiqi və imzalanması.',
            'reference_doctype': 'CRM Organization', 'reference_docname': 'YOM Logistics'
        },
        {
            'subject': 'Solida Xırdalan MMC — Tikinti Tender Görüşü',
            'starts_on': '2026-11-17 11:00:00', 'ends_on': '2026-11-17 12:30:00',
            'color': '#3b82f6', 'event_type': 'Private', 'status': 'Open',
            'description': 'Solida Xırdalan ilə material təchizatı üzrə qiymət danışıqları.',
            'reference_doctype': 'CRM Organization', 'reference_docname': 'Solida Xırdalan (SOLİDA MMC)'
        },
        {
            'subject': 'OBA MARKET — Satınalma Şöbəsi ilə Təqdimat',
            'starts_on': '2026-11-18 15:00:00', 'ends_on': '2026-11-18 16:00:00',
            'color': '#f59e0b', 'event_type': 'Private', 'status': 'Open',
            'description': 'OBA Market şəbəkəsi ilə korporativ təchizat təqdimatı.',
            'reference_doctype': 'CRM Organization', 'reference_docname': 'OBA MARKET - 69'
        },
        {
            'subject': 'AZTEXNİKA MMC — Texnika Demo Nümayişi',
            'starts_on': '2026-11-19 10:00:00', 'ends_on': '2026-11-19 11:00:00',
            'color': '#8b5cf6', 'event_type': 'Private', 'status': 'Open',
            'description': 'Sənaye avadanlıqlarının əyani nümayişi və sınaq işləri.',
            'reference_doctype': 'CRM Organization', 'reference_docname': 'AZTEXNİKA MMC'
        }
    ]
    events_created = 0
    for ev in events_data:
        if not frappe.db.exists('Event', {'subject': ev['subject']}):
            doc = frappe.get_doc({'doctype': 'Event', 'owner': 'Administrator', **ev})
            doc.insert(ignore_permissions=True)
            events_created += 1
    frappe.db.commit()
    print(f"✓ Təqvim tədbirləri (Calendar Events) yaradıldı: {events_created}")

    # Tasks (Görevler) yaratmaq
    tasks_data = [
        {
            'title': 'YOM Logistics üçün yeni qiymət təklifi hazırlamaq',
            'priority': 'High', 'status': 'Todo', 'assigned_to': 'Administrator',
            'due_date': '2026-11-17 18:00:00', 'reference_doctype': 'CRM Organization', 'reference_docname': 'YOM Logistics',
            'description': 'Bakı-Gəncə marşrutu üzrə endirimli tarif cədvəlini tərtib edib müştəriyə göndərmək.'
        },
        {
            'title': 'Solida Xırdalan ilə müqavilə bəndlərini razılaşdırmaq',
            'priority': 'High', 'status': 'In Progress', 'assigned_to': 'Administrator',
            'due_date': '2026-11-18 15:00:00', 'reference_doctype': 'CRM Organization', 'reference_docname': 'Solida Xırdalan (SOLİDA MMC)',
            'description': 'Ödəniş müddəti və çatdırılma qrafiki üzrə hüquq şöbəsi ilə birgə razılaşdırma aparmaq.'
        },
        {
            'title': 'OBA Market filialının sifariş sorğusunu cavablandırmaq',
            'priority': 'Medium', 'status': 'Todo', 'assigned_to': 'Administrator',
            'due_date': '2026-11-19 12:00:00', 'reference_doctype': 'CRM Organization', 'reference_docname': 'OBA MARKET - 69',
            'description': 'Filial üçün tələb olunan məhsulların mövcudluğunu anbarla dəqiqləşdirmək.'
        },
        {
            'title': 'AZTEXNİKA MMC ilə ilkin görüş keçirildi və akt imzalandı',
            'priority': 'Medium', 'status': 'Done', 'assigned_to': 'Administrator',
            'due_date': '2026-11-16 16:00:00', 'reference_doctype': 'CRM Organization', 'reference_docname': 'AZTEXNİKA MMC',
            'description': 'İlkin təqdimat uğurla yekunlaşdı, tender komissiyasına sənədlər təqdim edildi.'
        }
    ]
    tasks_created = 0
    for t in tasks_data:
        if not frappe.db.exists('CRM Task', {'title': t['title']}):
            doc = frappe.get_doc({'doctype': 'CRM Task', **t})
            doc.insert(ignore_permissions=True)
            tasks_created += 1
    frappe.db.commit()
    frappe.clear_cache()
    print(f"✓ Görevlər (CRM Tasks) yaradıldı: {tasks_created}")

def main():
    frappe.init(site="frontend", sites_path=bench_sites)
    frappe.connect()

    setup_custom_fields()
    setup_territories()

    org_file = get_excel_path("organizations (copy).xlsx") or get_excel_path("organizations.xlsx")
    if not org_file:
        print("XƏTA: Şirkətlər faylı (organizations.xlsx) tapılmadı!")
        sys.exit(1)

    setup_industries(org_file)
    directors = import_organizations(org_file)
    setup_sample_pipeline(directors)

    print("\n=======================================================")
    print("✓ FRAPPE CRM BÜTÜN İDXAL VƏ SAZLAMA TAMAMLANDI!")
    print(f"  - Cəmi Şirkət (CRM Organization): {frappe.db.count('CRM Organization')}")
    print(f"  - Cəmi Ərazi (CRM Territory): {frappe.db.count('CRM Territory')}")
    print(f"  - Cəmi Sənaye (CRM Industry): {frappe.db.count('CRM Industry')}")
    print(f"  - Cəmi Sövdələşmə (CRM Deal): {frappe.db.count('CRM Deal')}")
    print(f"  - Cəmi Əlaqə (Contact): {frappe.db.count('Contact')}")
    print(f"  - Cəmi Zəng Qeydi (CRM Call Log): {frappe.db.count('CRM Call Log')}")
    print(f"  - Cəmi Təqvim Tədbiri (Event): {frappe.db.count('Event')}")
    print(f"  - Cəmi Görev (CRM Task): {frappe.db.count('CRM Task')}")
    print("=======================================================")

if __name__ == "__main__":
    main()
