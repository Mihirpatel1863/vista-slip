from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return self.user.username

class Block(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Resident(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='residents')
    name = models.CharField(max_length=100)
    flat_no = models.CharField(max_length=20)

    class Meta:
        unique_together = ('block', 'flat_no')  # Ensures flat numbers are unique per block
        ordering = ['flat_no']  # Default ordering by flat number

    def __str__(self):
        return f"{self.name} ({self.flat_no})"

PAYMENT_CHOICES = [
    ('cash','Cash'),
    ('cheque','Cheque'),
    ('online','Online'),
]

class MaintenanceSlip(models.Model):
    slip_no = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.localdate)
    block = models.ForeignKey(Block, on_delete=models.PROTECT)
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT)
    maintenance_charge_date = models.DateField()
    amount_text = models.CharField(max_length=200)
    amount_number = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    cheque_details = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.slip_no} - {self.resident}"

    def get_absolute_url(self):
        return reverse('slip_detail', args=[self.pk])
