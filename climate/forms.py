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
    | ModelForm for creating or updating Site
    | fields = ('title', 'comment', 'narrowArea', 'wideArea', 'lat', 'lon', 'isActive', \
                  'isPublic', 'primaryImage')
    """
    class Meta:
        model = Site
        fields = ('title', 'comment', 'narrowArea', 'wideArea', 'lat', 'lon', 'isActive',
                  'isPublic', 'primaryImage')


class ObservationForm(forms.ModelForm):
    """
    | ModelForm for creating Observation
    | fields = ('siteId', 'windSpeed', 'comment') + MultipleChoiceField from Weather.WEATHER_CODE
    """
    weatherCode = forms.MultipleChoiceField(choices=Weather.WEATHER_CODE,
                                            widget=forms.CheckboxSelectMultiple(),
                                            required=False)

    class Meta:
        model = RawObservation
        fields = ('siteId', 'windSpeed', 'comment')


class DiaryForm(forms.ModelForm):
    """
    | ModelForm for creating RawManualData
    | fields = {'tMin', 'tMax', 'precAmount', 'day'}
    """
    class Meta:
        model = RawManualData
        fields = {'tMin', 'tMax', 'precAmount', 'day'}


class RegistrationForm(UserCreationForm):
    """
    | UserCreationForm for user registration
    | fields = ('username', 'email', 'password1', 'password2') + ReCaptchaField
    """
    captcha = ReCaptchaField(attrs={
        'theme': 'white',
    })
    email = forms.EmailField(max_length=200, help_text='Kötelező')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.Form):
    """
    | Form for editing user permissions
    | Fields: isAdmin, isActive, canUpload
    """
    isAdmin = forms.BooleanField(required=False, label='Admin')
    isActive = forms.BooleanField(required=False, label='Aktív')
    canUpload = forms.BooleanField(required=False, label='Tölthet fel adatfájlokat')


class InstrumentForm(forms.ModelForm):
    """
    | ModelForm for creating and updating Instrument
    | fields = ('title', 'comment', 'siteId', 'type', 'isActive', 'primaryImage')
    """
    class Meta:
        model = Instrument
        fields = ('title', 'comment', 'siteId', 'type', 'isActive', 'primaryImage')
