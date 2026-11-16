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

clean:
	@echo "Bütün konteyner və verilənlər bazası silinir..."
	@docker compose down -v
