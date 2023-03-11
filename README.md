# leaky
leaky app with django for excercise purposes.


Creating user via python shell:  
python manage.py shell   
from django.contrib.auth.models import User  
user = User.objects.create_user('Alice', None,'Alice')  
user = User.objects.create_user('Bob', None,'Bob')  
user.save()  
exit()  
