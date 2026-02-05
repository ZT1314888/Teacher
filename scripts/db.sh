#!/bin/bash
# 数据库管理脚本

case "$1" in
  migrate)
    echo "Creating migrations..."
    .venv/bin/python backend/manage.py makemigrations
    echo "Applying migrations..."
    .venv/bin/python backend/manage.py migrate
    echo "Migrations completed!"
    ;;
  collectstatic)
    echo "Collecting static files..."
    .venv/bin/python backend/manage.py collectstatic --noinput
    echo "Static files collected!"
    ;;
  createsuperuser)
    echo "Creating superuser..."
    .venv/bin/python backend/manage.py createsuperuser
    ;;
  reset)
    echo "WARNING: This will delete all data!"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
      rm -f backend/db.sqlite3
      .venv/bin/python backend/manage.py migrate
      echo "Database reset completed!"
    else
      echo "Operation cancelled."
    fi
    ;;
  *)
    echo "Usage: $0 {migrate|collectstatic|createsuperuser|reset}"
    echo ""
    echo "Commands:"
    echo "  migrate        - Create and apply migrations"
    echo "  collectstatic  - Collect static files"
    echo "  createsuperuser - Create admin superuser"
    echo "  reset          - Reset database (WARNING: deletes all data)"
    exit 1
    ;;
esac
