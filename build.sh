#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# Run migrations
echo "Applying migrations..................."
python manage.py migrate

# echo "Collecting static files...................."
# python manage.py collectstatic --noinput

echo "Populating countries......................."
python manage.py prepopulate_cbe

echo "Starting application..............."
exec daphne -b 0.0.0.0 -p 8000 cbe_res_hub.asgi:application
