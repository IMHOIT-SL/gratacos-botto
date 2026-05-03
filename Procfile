web: gunicorn --chdir dashboard --bind 0.0.0.0:${PORT:-8082} --workers 2 --timeout 120 app:app.server
