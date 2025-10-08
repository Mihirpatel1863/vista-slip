from django import forms
from .models import MaintenanceSlip, Resident, Block

class LoginWithPinForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    pin = forms.CharField(max_length=6, min_length=6)

class MaintenanceSlipForm(forms.ModelForm):
    class Meta:
        model = MaintenanceSlip
        fields = ['date','resident', 'block',  'maintenance_charge_date',
                  'amount_number','amount_text', 'payment_method', 'cheque_details']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'maintenance_charge_date': forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cheque_details'].required = False


class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['name', 'flat_no']  # block will be set in the view
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resident Name'}),
            'flat_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Flat No'}),
        }

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Block Name'}),
        }
