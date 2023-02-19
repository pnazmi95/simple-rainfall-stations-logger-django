from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from .models import Rainfall


class RainfallForm(forms.ModelForm):
    class Meta:
        model = Rainfall
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RainfallForm, self).__init__(*args, **kwargs)
        self.fields['submit_date'] = JalaliDateField(label=('تاریخ'), widget=AdminJalaliDateWidget)
