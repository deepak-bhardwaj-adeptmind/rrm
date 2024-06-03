from django import forms
from django.forms import DateInput

from rrm_app.models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate


class RoomRateForm(forms.ModelForm):
    class Meta:
        model = RoomRate
        fields = ['room_id', 'room_name', 'default_rate']


class OverriddenRoomRateForm(forms.ModelForm):
    class Meta:
        model = OverriddenRoomRate
        fields = ['room_rate', 'overridden_rate', 'stay_date']
        widgets = {
            'stay_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['discount_id', 'discount_name', 'discount_type', 'discount_value']


class DiscountRoomRateForm(forms.ModelForm):
    class Meta:
        model = DiscountRoomRate
        fields = ['room_rate', 'discount']


class RoomRateFilterForm(forms.Form):
    room_id = forms.CharField(label='Room ID')
    start_date = forms.DateField(label='Start Date', widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=DateInput(attrs={'type': 'date'}))

    def clean_room_id(self):
        room_id = self.cleaned_data['room_id']
        try:
            return int(room_id)
        except ValueError:
            raise forms.ValidationError("Invalid room ID.")
