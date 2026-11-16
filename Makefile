.PHONY: up down restart logs status clean

up:
	@./start.sh

down:
	@docker compose down

stop:
	@./stop.sh

restart:
	@docker compose restart

logs:
	@docker compose logs -f

status:
	@docker compose ps

import:
	@echo "Şirkətlər və ərazilər bazaya idxal edilir..."
	@docker exec -w /home/frappe/frappe-bench/sites frappe-crm-backend-1 /home/frappe/frappe-bench/env/bin/python /opt/scripts/import_crm_data.py

clean:
	@echo "Bütün konteyner və verilənlər bazası silinir..."
	@docker compose down -v
