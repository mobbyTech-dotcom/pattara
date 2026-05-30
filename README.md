# ภัทรา Homemade - Django

## รันบนเครื่อง (Local)
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deploy บน Render
1. Push โค้ดขึ้น GitHub
2. ไป render.com → New Web Service → เชื่อม repo
3. ตั้งค่า:
   - Build Command: `bash build.sh`
   - Start Command: `gunicorn patthara.wsgi:application`
4. ใส่ Environment Variable: `DEBUG=False`
5. Deploy

## Login แอดมิน
- URL: `/login/`
- Username: `admin`
- Password: `patthara2024`
- **เปลี่ยนรหัสผ่านหลัง deploy ด้วยนะครับ!**
