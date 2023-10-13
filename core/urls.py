#urls.py
from django.contrib import admin
from django.urls import path, include
from inertiatools import views

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Include URLs from the inertiatools application
    path('', include('inertiatools.urls')),

    # Home page URL
    path('home', views.home, name='home'),

    # Register page URL
    path('register/', views.register, name='register'),

    # Account page URL
    path('account/', views.account, name='account'),

    # Login page URL
    path('login/', views.login, name='login'),

    # Logout page URL
    path('logout/', views.logout, name='logout'),

    #create-rental page URL
    path('create-rental/', views.create_rental, name='create-rental'),

    # new-tenant page URL
    path('new-tenant/', views.new_tenant, name='new-tenant'),

    # URL pattern for the tenants page
    path('tenants/', views.tenants, name='tenants'),

    # URL pattern for the tenant edit page
    path('tenant/<int:tenant_id>/edit/', views.tenant_edit, name='tenant_edit'),

    # URL pattern for the owners page
    path('owners/', views.owners, name='owners'),

    # URL pattern for the owner create page
    path('owner/create/', views.owner_create, name='owner_create'),

    # URL pattern for the owner edit page
    path('owner/<int:owner_id>/edit/', views.owner_edit, name='owner_edit'),

    # URL pattern for the owner delete page
    path('owner/<int:owner_id>/delete/', views.owner_delete, name='owner_delete'),

    path('rentals/', views.rentals, name='rentals'),

    path('new-tenant-leases/', views.new_tenant_leases, name='new-tenant-leases'),


]
