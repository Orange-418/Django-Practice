from django.db import models


class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    date_of_birth = models.DateField()

class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Property(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    property_number = models.CharField(max_length=50)
    unit_number = models.CharField(max_length=50, blank=True)
    property_street_name = models.CharField(max_length=100)
    property_city = models.CharField(max_length=50)
    property_state = models.CharField(max_length=50)
    property_zip = models.CharField(max_length=50)


class TenantLease(models.Model):
    file = models.FileField()
    assign_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    assign_tenant = models.ManyToManyField(Tenant)
    assign_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    lease_term = models.IntegerField()
