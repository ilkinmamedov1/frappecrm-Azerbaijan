#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "Frappe CRM dayandırılır..."
docker compose stop
echo "Frappe CRM dayandırıldı. Yenidən işə salmaq üçün: ./start.sh"
