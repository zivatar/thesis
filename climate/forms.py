from django import forms

from climate.classes.Weather import Weather
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User

from climate.models.Instrument import Instrument
from climate.models.RawManualData import RawManualData
from climate.models.RawObservation import RawObservation
from climate.models.Site import Site


class SiteForm(forms.ModelForm):
    """
    siteform
    """
    class Meta:
        model = Site
        fields = ('title', 'comment', 'narrowArea', 'wideArea', 'lat', 'lon', 'isActive', 'isPublic', 'primaryImage')


class ObservationForm(forms.ModelForm):
    weatherCode = forms.MultipleChoiceField(choices=Weather.WEATHER_CODE, widget=forms.CheckboxSelectMultiple(),
                                            required=False)

    class Meta:
        model = RawObservation
        fields = ('siteId', 'windSpeed', 'comment')


# my_field = forms.MultipleChoiceField(choices=Weather.WEATHER_CODE, widget=forms.CheckboxSelectMultiple())

class DiaryForm(forms.ModelForm):
    class Meta:
        model = RawManualData
        fields = {'tMin', 'tMax', 'precAmount', 'day'}


class RegistrationForm(UserCreationForm):
    captcha = ReCaptchaField(attrs={
        'theme': 'white',
    })
    email = forms.EmailField(max_length=200, help_text='Kötelező')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.Form):
    isAdmin = forms.BooleanField(required=False, label='Admin')
    isActive = forms.BooleanField(required=False, label='Aktív')
    canUpload = forms.BooleanField(required=False, label='Tölthet fel adatfájlokat')


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ('title', 'comment', 'siteId', 'type', 'isActive', 'primaryImage')
