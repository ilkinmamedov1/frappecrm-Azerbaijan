#!/usr/bin/env python3
"""
Frappe CRM avtomatik ilkin sazlama skripti:
1. AZN (₼ - Azərbaycan Manatı) valyutasını sistemə əlavə edir.
2. Setup Wizard-ı avtomatik keçir (istifadəçidən əlavə sual soruşulmur).
3. Ölkə: Azerbaijan, Saat qurşağı: Asia/Baku, Valyuta: AZN təyin edir.
4. Standart dili Türk dili (tr) edir.
5. Administrator profilini Türkçe dilinə keçirir.
"""

import os
import sys

# İş qovluğunu Frappe Bench sites qovluğuna keçiririk
bench_sites = "/home/frappe/frappe-bench/sites"
if os.path.exists(bench_sites):
    os.chdir(bench_sites)

# Loq qovluğunun mövcudluğunu təmin edirik
os.makedirs("/home/frappe/logs", exist_ok=True)
os.makedirs("/home/frappe/frappe-bench/logs", exist_ok=True)

import frappe
from frappe.desk.page.setup_wizard import setup_wizard

def setup():
    frappe.init(site="frontend", sites_path=bench_sites)
    frappe.connect()

    # 1. AZN Valyutasını əlavə et
    if not frappe.db.exists("Currency", "AZN"):
        azn = frappe.get_doc({
            "doctype": "Currency",
            "currency_name": "AZN",
            "symbol": "₼",
            "fraction": "Qəpik",
            "fraction_units": 100,
            "smallest_currency_fraction_value": 0.01,
            "number_format": "#,###.##",
            "enabled": 1,
        })
        azn.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ AZN (₼) valyutası uğurla əlavə edildi.")
    else:
        print("✓ AZN valyutası artıq mövcuddur.")

    # 2. Setup Wizard-ı tamamla
    if not frappe.is_setup_complete():
        args = {
            "language": "Turkish",
            "lang": "tr",
            "country": "Azerbaijan",
            "timezone": "Asia/Baku",
            "currency": "AZN",
            "company_name": "My Company",
            "first_name": "Administrator",
            "full_name": "Administrator",
        }
        setup_wizard.setup_complete(args)
        print("✓ Frappe Setup Wizard avtomatik tamamlandı.")
    else:
        print("✓ Setup Wizard artıq tamamlanıb.")

    # 3. Sistem parametrlərini sazla (Türk dili, AZN, Asia/Baku)
    settings = frappe.get_doc("System Settings")
    settings.setup_complete = 1
    settings.language = "tr"
    settings.country = "Azerbaijan"
    settings.time_zone = "Asia/Baku"
    settings.currency = "AZN"
    settings.number_format = "#,###.##"
    settings.date_format = "dd-mm-yyyy"
    settings.time_format = "HH:mm:ss"
    settings.save(ignore_permissions=True)

    # 4. Administrator istifadəçisinin dilini Türk dili et
    admin = frappe.get_doc("User", "Administrator")
    admin.language = "tr"
    admin.save(ignore_permissions=True)

    # 5. Keşi təmizlə və yadda saxla
    frappe.db.commit()
    frappe.clear_cache()
    print("✓ Frappe CRM ilkin sazlama (AZN + Türk dili + Setup Wizard bypass) uğurla yekunlaşdı!")

if __name__ == "__main__":
    setup()
