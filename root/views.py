import os
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.backends import UserModel
from django.contrib.auth import get_user_model
from django.contrib import messages 
from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse
from django.conf import settings
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import resolve, reverse
from django.contrib.auth.backends import ModelBackend
import logging

from .models import UploadFileForm, FileUpload, Task, ShoppingItem


# Create your views here.
# @login_required
def index(request):
    return render(request, 'root/index.html')


def documents(request):
    context = {}
    context['form'] = UploadFileForm()
    context['FileUploads'] = FileUpload.objects.all()
    return render(request, 'root/documents.html', context)


def handle_uploaded_file(app, f):
    target = os.path.join(settings.BASE_DIR, app, "uploads", f.name)
    # print(target)
    with open(target, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def sanitizeFilename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def upload_file(request):
    # https://www.geeksforgeeks.org/filefield-django-forms/
    context = {}
    context['form'] = UploadFileForm()
    context['FileUploads'] = FileUpload.objects.all()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            fu = FileUpload(title=request.POST.get("title", ""), orig_filename=f.name)
            fu.save()
            f.name = str(fu.id) + "-" + sanitizeFilename(f.name)
            fu.filename = f.name
            fu.save()
            handle_uploaded_file(resolve(request.path).app_name, f)

            return HttpResponseRedirect(reverse('root:documents'))
        # else: # fix
        #    messages.error(request, 'Received form was invalid!')  # fix
        #    return HttpResponseRedirect(reverse('root:documents')) # fix
    else:
        return HttpResponseRedirect(reverse('root:documents'))


def download_file(request):
    f_name = request.GET.get("file");
    appname = resolve(request.path).app_name
    target = os.path.join(settings.BASE_DIR, appname, "uploads", f_name)
    # f_id =  int(request.GET.get("file_id")) # fix
    # fu = FileUpload.objects.get(id=f_id)    # fix 
    # target = os.path.join(settings.BASE_DIR, appname, "uploads", fu.orig_filename) # fix
    f = open(target, 'rb')
    return FileResponse(f, as_attachment=True)


def invalid_call(request):
    return render(request, 'root/invalid_call.html')


def getUser(request):
	username = request.user
	return User.objects.get(username=username)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class TasksView(generic.ListView):
    model = Task
    template_name = 'root/tasks.html'
    context_object_name = 'tasks'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(TasksView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = getUser(self.request)
        return Task.objects.filter(owner=user.id)
    

@login_required
def add_task(request):
    username = request.user
    user = User.objects.get(username=username)
    todo = request.POST.get('todo', '')
    due_date = request.POST.get('due_date')
    task = Task(todo=todo, due_date = due_date, owner = user)
    task.save()
    return HttpResponseRedirect(reverse('root:tasks'))


@login_required
def delete_task(request):
    user = getUser(request)
    id = request.POST.get('id', '-1')
    num = Task.objects.filter(id=id).delete()
    # num = Task.objects.filter(id=id, owner=user.id).delete() # fix
    if num[0] != 1:
        messages.error(request, 'Task could not be found for deletion.')
    else:
         messages.success(request, 'Task successfully deleted!')

    return HttpResponseRedirect(reverse('root:tasks'))


@login_required
def high_security_page(request):
    logger = logging.getLogger(__name__)
    user = getUser(request)
    # logger.info("{} User {} with id {} entered the high security page".format(get_client_ip(request), user.username, user.id)); # fix
    return render(request, 'root/high_security_page.html')


@login_required
def download_secrets(request):
    logger = logging.getLogger(__name__)
    user = getUser(request)
    # logger.info("{} User {} with id {} downloaded all secrets".format(get_client_ip(request), user.username, user.id)); # fix
    messages.success(request, 'You successfully downloaded all secrets!')
    return HttpResponseRedirect(reverse('root:high_security_page'))


# taken from the django sources and modified for logging
class RootBackend(ModelBackend):
    UserModel = get_user_model()
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger = logging.getLogger(__name__)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
            # logger.info("{} User {} failed to log in".format(get_client_ip(request), username)); # fix  
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                # logger.info("{} User {} with id {} logged in successfully".format(get_client_ip(request), user.username, user.id)); # fix
                return user


class ShoppinglistView(generic.ListView):
    model = ShoppingItem
    template_name = 'root/shoppinglist.html'
    context_object_name = 'items'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(ShoppinglistView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = getUser(self.request)
        return ShoppingItem.objects.filter(owner=user.id)
    

@login_required
def add_item(request):
    username = request.user
    user = User.objects.get(username=username)
    name = request.POST.get('item', '')
    amount = request.POST.get('amount')
    item = ShoppingItem(item=name, amount=amount, owner = user)
    item.save()
    return HttpResponseRedirect(reverse('root:shoppinglist'))

@csrf_exempt    # remove this line to fix issue
@login_required
def delete_item(request):
    user = getUser(request)
    id = request.POST.get('id', '-1')
    num = ShoppingItem.objects.filter(id=id, owner=user.id).delete()
    if num[0] != 1:
        messages.error(request, 'Item could not be found for deletion.')
    else:
         messages.success(request, 'Item successfully deleted!')

    return HttpResponseRedirect(reverse('root:shoppinglist'))