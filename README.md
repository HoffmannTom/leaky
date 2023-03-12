# leaky
A sample project with Django to show common mistakes


Creating user via python shell:  
python manage.py shell   
from django.contrib.auth.models import User  
user = User.objects.create_user('Alice', None,'Alice')  
user = User.objects.create_user('Bob', None,'Bob')  
user.save()  
exit()  

# Background
This project was created for the course "Cyber Security Base 2023" of the university of Helsinki.  
For details, see https://cybersecuritybase.mooc.fi/module-3.1  

The app demonstrates five common mistakes:
- Injection
- Security Misconfiguration
- Broken access control
- Security Logging and Monitoring Failures
- CSRF
