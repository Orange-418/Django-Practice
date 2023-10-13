#forms.py
from django import forms
from .models import Owner, Property, Tenant, TenantLease
from magic import Magic
from django.forms import ModelChoiceField, Form, ModelMultipleChoiceField, formset_factory


class RegisterForm(forms.Form):
    # Email field with a class of 'form-control' for styling
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    # Text field for the username with a class of 'form-control' for styling
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # Password field with a class of 'form-control' for styling
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # Password field for password confirmation with a class of 'form-control' for styling
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # Text field for the first name with a class of 'form-control' for styling
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # Text field for the last name with a class of 'form-control' for styling
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class UploadFileForm(forms.Form):
    property_management_agreement = forms.FileField()

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class RentalForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_number', 'unit_number', 'property_street_name', 'property_city', 'property_state', 'property_zip', 'owner']
    owner = forms.ModelChoiceField(queryset=Owner.objects.all())

# First, define your form for a single tenant selection
class TenantSelectionForm(Form):
    tenant = ModelChoiceField(queryset=Tenant.objects.all())

# Then, create a formset using the form above
TenantSelectionFormSet = formset_factory(TenantSelectionForm, extra=1)

# Next, define your main form
class NewTenantLeaseForm(forms.ModelForm):
    class Meta:
        model = TenantLease
        fields = ['file', 'assign_property', 'assign_owner', 'rent_amount', 'lease_term']


    def clean_file(self):
        file = self.cleaned_data['file']
        # check file size
        if file.size > 5000000:
            raise forms.ValidationError('File size must be under 5mb')
        # check file type using python magic library
        mime = Magic(mime=True)
        file_type = mime.from_buffer(file.read())
        if file_type != 'application/pdf':
            raise forms.ValidationError('File must be a PDF')
        return