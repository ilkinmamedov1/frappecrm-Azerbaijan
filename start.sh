#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Əgər .env faylı yoxdursa, .env.example-dan avtomatik yaradılır
if [ ! -f .env ]; then
  echo "--> .env faylı yaradılır (.env.example əsasında)..."
  cp .env.example .env
fi

# .env-dən portu oxuyuruq
PORT=$(grep -E "^CRM_PORT=" .env | cut -d '=' -f2 | tr -d ' ' || echo "8080")
PORT=${PORT:-8080}

# Lokal şəbəkə IP-sini tapırıq
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")

echo "=========================================================="
echo "      Frappe CRM Azerbaijan - 1 Komanda ilə Başlama       "
echo "=========================================================="

docker compose up -d

echo "Sistemin hazır olması yoxlanılır (Port: $PORT)..."
MAX_RETRIES=60
COUNT=0
until curl -sI "http://127.0.0.1:$PORT" | grep -qE "200 OK|403 FORBIDDEN"; do
  sleep 3
  COUNT=$((COUNT+1))
  if [ $COUNT -ge $MAX_RETRIES ]; then
    echo "Gözləmə müddəti bitdi. Loqlara baxmaq üçün: make logs"
    exit 1
  fi
done

echo ""
echo "=========================================================="
echo "✓ Frappe CRM Azerbaijan uğurla işə salındı!"
echo "✓ Valyuta: AZN (₼)"
echo "✓ Dil: Türkçe (tr)"
echo "✓ Məlumatlar: 20,000+ Şirkət, 254 Ərazi, 89 Sənaye Sahəsi"
echo "✓ Lokal Giriş (Bu kompüterdən):"
echo "    http://localhost:$PORT (və ya http://localhost:$PORT/crm)"
echo "✓ Şəbəkə Girişi (Lokal şəbəkədəki digər cihazlardan):"
echo "    http://$LOCAL_IP:$PORT"
echo "✓ İstifadəçi: Administrator"
echo "✓ Şifrə: admin (və ya .env-də təyin etdiyiniz şifrə)"
echo "=========================================================="
