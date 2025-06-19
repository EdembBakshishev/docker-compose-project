#!/usr/bin/bash
timestamp=$(date +"%Y%m%d-%H%M%S")
backup_file="edem-$timestamp.sql"
mkdir -p backups
docker exec docker-compose-project-db-1 pg_dump -U user smmhub > "backups/$backup_file"
echo "Backup created: backups/$backup_file"
ls backups/edem-*.sql 2>/dev/null | sort -r | tail -n +3 | xargs -r rm -v
