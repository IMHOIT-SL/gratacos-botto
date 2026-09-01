web: gunicorn --chdir dashboard --bind 0.0.0.0:${PORT:-8082} --workers 1 --threads 4 --timeout 120 app:server
