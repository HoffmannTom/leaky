from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}), required=True)


class FileUpload(models.Model):
    title = models.CharField(max_length=50, null=False)
    filename = models.CharField(max_length=50, null=False)
    orig_filename = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.title + "(" + self.filename + ")"
    
    
class Task(models.Model):
    todo = models.CharField(max_length=50, null=False)
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.todo + " till " + self.due_date
    

class ShoppingItem(models.Model):
    item = models.CharField(max_length=50, null=False)
    amount = models.IntegerField(default=1, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item + " (" + self.amount + ")"    