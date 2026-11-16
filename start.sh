#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "=========================================="
echo "   Frappe CRM (Yalnız CRM) Başladılır    "
echo "=========================================="

docker compose up -d

echo "Sistemin hazır olması yoxlanılır..."
until curl -sI http://localhost:8080 | grep -q "200 OK"; do
  sleep 2
done

echo ""
echo "=========================================="
echo "✓ Frappe CRM uğurla işə salındı!"
echo "✓ Standart Valyuta: AZN (₼)"
echo "✓ Standart Dil: Türkçe (tr)"
echo "✓ URL: http://localhost:8080 (və ya http://localhost:8080/crm)"
echo "✓ İstifadəçi adı: Administrator"
echo "✓ Şifrə: admin"
echo "=========================================="
