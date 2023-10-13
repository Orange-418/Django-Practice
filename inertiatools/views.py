#views.py
import re
import magic
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.core.files.storage import default_storage

from .models import Tenant, Owner, Property
from .forms import OwnerForm, RentalForm, RegisterForm, TenantForm, NewTenantLeaseForm, TenantSelectionFormSet


def register(request):
    # If the user is already authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('home')

    template = 'register.html'
    error_message = None

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Validate the username
            if len(form.cleaned_data['username']) < 5:
                error_message = 'Username must be at least 5 characters long.'
            # Validate the first and last name
            elif (
                    len(form.cleaned_data['first_name']) < 1 or
                    len(form.cleaned_data['last_name']) < 1
            ):
                error_message = 'First and last name must be at least 1 character long.'
            # Validate that the username is unique
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                error_message = 'Username already exists.'
            # Validate that the passwords match
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                error_message = 'Passwords do not match.'
            # Validate the password strength
            elif not re.match(
                    r'^(?=.*[!@#$%^&*])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[!@#$%^&*A-Za-z\d]{12,64}$',
                    form.cleaned_data['password']
            ):
                error_message = 'Password must be between 12 and 64 characters long, and contain one special character (! @ # $ % ^ & *), one uppercase letter, one lowercase letter, and one number.'
            else:
                # Save the user to the database
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'])
                user.save()
                # Login the user
                dj_login(request, user)

                # Redirect to the account page
                return HttpResponseRedirect('/account/')

        else:
            error_message = "Please enter all details."
    else:
        form = RegisterForm()

    return render(request, template, {'form': form, 'error_message': error_message})

def home(request):
    """
    Home page view. Renders the 'home.html' template.
    """
    return render(request, 'home.html')

def login(request):
    """
    Handle user login.
    """
    # If the user is already authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('home')

    template = 'login.html'
    if request.method == 'POST':
        # Collect form data
        username = request.POST['username']
        password = request.POST['user_password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            dj_login(request, user)

            # Redirect to the account page
            return HttpResponseRedirect('/account/')
        else:
            return render(
                request,
                template,
                {
                    'error_message': 'Invalid login credentials.'
                }
            )

    return render(request, template)

def logout(request):
    """
    Handle user logout.
    """
    dj_logout(request)
    # Redirect to the home page
    return HttpResponseRedirect('/')

def account(request):
    """
    Display the user's account information.
    """
    # If the user is not authenticated, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email
    }
    return render(request, 'account.html', context)



def create_rental(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rentals')  # redirect to the rentals page
    else:
        form = RentalForm()
    return render(request, 'create-rental.html', {'form': form})



def new_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            # access the form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            date_of_birth = form.cleaned_data['date_of_birth']

            # store the data using a database query or other method
            Tenant.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, date_of_birth=date_of_birth)

            return redirect('home')  # redirect to the home page
        else:
            return render(request, 'new-tenant.html', {'form': form})  # render the template with the invalid form
    else:
        form = TenantForm()  # initialize the form
        return render(request, 'new-tenant.html', {'form': form})  # render the template with the empty form

def tenants(request):
    # get the list of tenants from the database
    tenants = Tenant.objects.all()

    return render(request, 'tenants.html', {'tenants': tenants})

def tenant_edit(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)  # get the tenant object from the database

    form = TenantForm(request.POST or None, instance=tenant)  # create a form instance with the tenant data

    if request.method == 'POST':
        if form.is_valid():
            form.save()  # save the form data to the database
            return redirect('tenants')  # redirect to the tenants page

    return render(request, 'tenant-edit.html', {'form': form, 'tenant': tenant})  # render the tenant-edit template


def owners(request):
    """
    View function for the owners page.
    """

    owners = Owner.objects.all()  # get all owners from the database

    return render(request, 'owners.html', {'owners': owners})  # render the owners template

def owner_create(request):
    """
    View function for the owner create page.
    """
    if request.method == 'POST':
        form = OwnerForm(request.POST)  # create a form instance with the POST data
        if form.is_valid():
            form.save()  # save the form data to the database
            return redirect('owners')  # redirect to the owners page
    else:
        form = OwnerForm()  # create a blank form
    return render(request, 'owner-create.html', {'form': form})  # render the owner-create template

def owner_edit(request, owner_id):
    """
    View function for the owner edit page.
    """
    owner = get_object_or_404(Owner, pk=owner_id)  # get the owner object from the database
    print(1)
    form = OwnerForm(request.POST or None, instance=owner)  # create a form instance with the owner data
    print(2)

    if request.method == 'POST':
        if form.is_valid():
            form.save()  # save the form data to the database
            return redirect('owners')  # redirect to the owners page

    return render(request, 'owner-edit.html', {'form': form, 'owner': owner})  # render the owner-edit template

def owner_delete(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)  # get the owner object from the database
    owner.delete()  # delete the owner from the database
    return redirect('owners')  # redirect to the owners page

def rentals(request):
    properties = Property.objects.all()
    return render(request, 'rentals.html', {'properties': properties})

def new_tenant_leases(request):
    tenant_selection_formset = TenantSelectionFormSet()
    if request.method == 'POST':
        form = NewTenantLeaseForm(request.POST, request.FILES)
        tenant_selection_formset = TenantSelectionFormSet(request.POST)
        if form.is_valid() and tenant_selection_formset.is_valid():
            # process the form data here
            tenant_leases = []
            for form in tenant_selection_formset:
                tenant = form.cleaned_data.get('tenant')
                if tenant:
                    tenant_leases.append(tenant)
            form.cleaned_data['assign_tenant'] = tenant_leases
            form.save()
            return redirect('/tenant-leases/')
    else:
        form = NewTenantLeaseForm()
    return render(request, 'new_tenant_leases.html', {'form': form, 'tenant_selection_formset': tenant_selection_formset})







