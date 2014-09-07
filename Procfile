web: gunicorn -w $AILTDOU_WORKNUM -b 127.0.0.1:$PORT wsgi:app
mail: python manage.py inbox -p $PORT
