Socialty - Django project scaffold (No WeasyPrint)

Instructions:
1. Create a Python virtualenv and activate it.
2. Install requirements: pip install -r requirements.txt
3. Update SECRET_KEY in socialty/settings.py and DATABASES with your PostgreSQL (pgAdmin) credentials.
4. Run:
     python manage.py makemigrations
     python manage.py migrate
     python manage.py createsuperuser
5. Place chairman signature image at media/chairman_signature.png
6. Run server:
     python manage.py runserver

The project contains the 'society' app with models: Profile, Block, Resident, MaintenanceSlip.
Slip printing is handled by browser's Print dialog (no external PDF libs).
