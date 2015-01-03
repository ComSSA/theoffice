from django.shortcuts import render, redirect
from forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from textwrap import dedent
from django.contrib import messages
from django.core.exceptions import ValidationError
from pytidyclub import pytidyclub
from django.conf import settings
from django.core.urlresolvers import reverse

def login(request):
    # check if user has logged in
    if request.user.is_authenticated():
        return redirect('home:index')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            messages.success(request, "You have been logged in successfully, %s" % form.user.first_name)
            return redirect("home:index")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {
        'form': form
        })

@login_required
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('home:index')
    return render(request, 'accounts/logout.html')

def admin(request):
    change_password_form = AdminChangePasswordForm()
    reset_password_form = UserSelectionForm()
    add_admin_form = NonAdminSelectionForm()
    remove_admin_form = AdminSelectionForm()
    create_user_form = CreateUserForm()
    return render(request, 'accounts/admin.html', {
        'password_form': change_password_form,
        'add_admin_form': add_admin_form,
        'remove_admin_form': remove_admin_form,
        'reset_password_form': reset_password_form,
        'create_user_form': create_user_form
        })

def sync(request):
    sync = [
    ]
    

    for s in sync:
        group = Group.objects.get_or_create(name = s['group'])[0]
        group.permissions.clear()
        for permission in s['permissions']:
            perm = Permission.objects.get(codename = permission)
            group.permissions.add(perm)
            print "Added %s to %s" % (perm, group)
        group.save()

    messages.success(request, "Permissions have been synced successfully.")
    return redirect('accounts:admin')
    
def change_password_admin(request):
    if request.method == 'POST':
        form = AdminChangePasswordForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['user']
            u.set_password(form.cleaned_data['password'])
            u.save()
            messages.success(request, "%s's password has been changed." % form.cleaned_data['user'])
            return redirect('accounts:admin')
    else:
        return redirect('accounts:admin')

def admin_reset_password(request):
    if request.method == 'POST':
        form = UserSelectionForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['user']
            pw = get_user_model().objects.make_random_password()
            u.set_password(pw)
            u.save()

            message = """Dear %s,

                      Your theoffice password has been reset by %s.

                      Your password has been set to: '%s'.

                      --
                      theoffice
                      http://theoffice.comssa.org.au/
                      """ % (u.first_name, request.user.first_name, pw)

            send_mail(
                subject = 'theoffice Password Reset',
                message = dedent(message),
                from_email = 'keydist@comssa.org.au',
                recipient_list = (u.email,),
            )

            messages.success(request, "%s's password has been reset successfully, and an email has been sent to them." % u.first_name)

            return redirect('accounts:admin')
    else:
        return redirect('accounts:admin')

def admin_create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                u = get_user_model().objects.create_user(
                    form.cleaned_data['curtin_id'],
                    form.cleaned_data['first_name'], 
                    form.cleaned_data['last_name']
                )
                u.save()
                messages.success(request, 'User created.')
            except ValidationError as e:
                messages.error(request, 'Error creating user: %s' % e)
                return redirect('accounts:admin')
        else:
            messages.error(request, "Error.")
    
    return redirect('accounts:admin')

def admin_add_admin(request):
    if request.method == 'POST':
        form = NonAdminSelectionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user.is_superuser = True
            pw = get_user_model().objects.make_random_password()
            user.set_password(pw)
            user.save()

            message = """\
                    Dear %s,

                    %s has made you an administrator on theoffice.

                    Your password has been set to: '%s'.

                    --
                    theoffice
                    http://theoffice.comssa.org.au/
                    """ % (user.first_name, request.user.first_name, pw)

            send_mail(
                subject = 'Welcome to theoffice',
                message = dedent(message),
                from_email = 'keydist@comssa.org.au',
                recipient_list = (user.email,),
            )
            messages.success(request, 'The user has been created and a password has been emailed to them.')
        else:
            messages.error(request, "Error.")
    
    return redirect('accounts:admin')

def admin_remove_admin(request):
    if request.method == 'POST':
        form = AdminSelectionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user.is_superuser = False
            pw = get_user_model().objects.make_random_password()
            user.set_password(pw)
            user.save()

            message = """\
                    Dear %s,

                    %s has removed you as an administrator on theoffice.

                    --
                    theoffice
                    http://theoffice.comssa.org.au/
                    """ % (user.first_name, request.user.first_name)

            send_mail(
                subject = 'theoffice privilege removal',
                message = dedent(message),
                from_email = 'keydist@comssa.org.au',
                recipient_list = (user.email,),
            )
            messages.success(request, 'The user has been removed as an admin.')
        else:
            messages.error(request, "Error.")
    
    return redirect('accounts:admin')


def cp(request):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
        proxy = True
    except KeyError:
        ip = request.META['REMOTE_ADDR']
        proxy = False

    return render(request, 'accounts/cp.html', {
        'change_password_form': ChangePasswordForm(),
        'ip': ip,
        'proxy': proxy,
        'tidyclub': request.user.tidyclub_api_token
    })

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, "Your password has been changed successfully.")
    
    return redirect('accounts:cp')
    
def tidyclub(request):
    if request.method == "GET":
        a = pytidyclub.Club(
            slug = "ComSSA",
            client_id = settings.TIDYCLUB_API_ID,
            client_secret = settings.TIDYCLUB_API_SECRET
        )
        
        if 'code' in request.GET:
            a.auth_authcode_exchange_code(request.GET['code'], request.build_absolute_uri(reverse('accounts:tidyclub')))
            request.user.tidyclub_api_token = a.token
            request.user.save()
        else:
            return redirect(a.auth_authcode_get_url(request.build_absolute_uri(reverse('accounts:tidyclub'))))
    
    return redirect('accounts:cp')   

