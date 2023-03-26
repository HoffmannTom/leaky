# leaky
A sample project with Django to show common programming mistakes in web applications.  
The application gets automatically deployed at https://leaky.onrender.com.

# Background
This project was created for the course "Cyber Security Base 2023" of the university of Helsinki.  
For details, see https://cybersecuritybase.mooc.fi/module-3.1  

The app demonstrates five common mistakes:
1) Injection
2) Security Misconfiguration
3) Broken access control
4) Security Logging and Monitoring Failures
5) CSRF

# Creation of app users
Creating user can be accomplished via a Python shell: 
```
python manage.py shell   
from django.contrib.auth.models import User  
user = User.objects.create_user('Alice', None,'Alice')  
user = User.objects.create_user('Bob', None,'Bob')  
user.save()  
exit()  
```
