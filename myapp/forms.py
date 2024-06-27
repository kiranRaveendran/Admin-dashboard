from django.contrib.auth.forms import PasswordChangeForm
import re
from django import forms
from .models import *
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your username', 'id': 'username', 'class': 'px-5 py-2  focus:outline-none'}))
    password = forms.CharField(widget=forms.PasswordInput(
        # ,'id':'passw'
        # ,'id':'passw'
        attrs={'placeholder': 'Enter your password', 'id': 'password', 'class': 'px-5 py-2 focus:outline-none'}))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')

    #     if not username or not password:
    #         raise ValidationError('Please enter both username and password.')

    #     username_pattern = r'^[a-zA-Z0-9_]{3,16}$'
    #     password_pattern = r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'

    #     if not re.match(username_pattern, username):
    #         raise ValidationError(
    #             'Invalid username. Use only letters, numbers, and underscores (3-16 characters).')

    #     if not re.match(password_pattern, password):
    #         raise ValidationError(
    #             'Invalid password. Password must be at least 8 characters long and contain at least one letter and one digit.')

    #     user = authenticate(username=username, password=password)
    #     if user is None or not user.is_active:
    #         raise ValidationError('Invalid username or password.')

    #     return cleaned_data


class Doctor_Form(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['first_name', 'last_name', 'mobile', 'gender', 'email',
                  'specialisation', 'doctor_fees', 'address', 'experience', 'image', 'date_of_birth', 'country_code', 'qualification']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md '}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md '}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Enter Mobile Number', 'id': 'number', 'pattern': '[6-9]\d{9,12}', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md ', 'id': 'mobile_num'}),
            'gender': forms.Select(attrs={'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 px-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email', 'id': 'email', 'pattern': '[^\s@]+@[^\s@]+\.[^\s@]+', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md'}),
            'specialisation': forms.Select(choices=[('', 'Choose')], attrs={'placeholder': 'Specialisation', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md'}),
            'doctor_fees': forms.TextInput(attrs={'placeholder': 'Doctor fees', 'class': 'form-control block w-[60vw]  sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Address', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Experience', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md'}),
            'image': forms.FileInput(attrs={'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200'
                                            }),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs  border border-gray-300 rounded-md', 'type': 'date', 'id': 'id_date_of_birth'}),
            'country_code': forms.TextInput(attrs={'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs border border-gray-300 rounded-md'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'Qualification', 'class': 'form-control block w-[60vw] sm:w-[20vw] py-2 lg:py-3 pl-4 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs border border-gray-300 rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super(Doctor_Form, self).__init__(*args, **kwargs)
        self.fields['specialisation'].choices = [("", "--Choose--")] + [
            (spec.id, spec.name) for spec in Specialisation.objects.all()
        ]


def clean_mobile(self):
    mobile = self.cleaned_data['mobile']
    # Check if mobile already exists in the database (excluding the current object if editing)
    if self.instance.pk is None or Doctors.objects.filter(mobile=mobile).exclude(pk=self.instance.pk).exists():
        raise forms.ValidationError('Mobile number already exists.')
    return mobile


class specialization_Form(forms.ModelForm):
    class Meta:
        model = Specialisation
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'edit_button', 'placeholder': 'Enter specialization', 'class': 'form-control text-center block w-[20vw] sm:w-[20vw] py-1 sm:py-3 lg:py-2 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-xs border border-gray-300 rounded-md '}),
        }


class SetCommissionForm(forms.ModelForm):
    class Meta:
        model = SetCommission
        fields = ['OfflineSetCommission',
                  'OnlineSetCommission', 'current_date']
        labels = {
            'OfflineSetCommission': 'Offline Set Commission',
            'OnlineSetCommission': 'Online Set Commission',
        }
        widgets = {
            # Ensure the input is displayed as a date input
            'current_date': forms.DateInput(attrs={'class': 'form-control text-center w-[60vw] sm:w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md', 'type': 'date'})
        }
    OfflineSetCommission = forms.ChoiceField(
        choices=[('', 'Select Offline Commission')] +
        SetCommission.percentage_choice,
        label="Offline Set Commission",
        widget=forms.Select(attrs={
                            'class': 'form-control text-center block w-[60vw] sm:w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md'})
    )
    OnlineSetCommission = forms.ChoiceField(
        choices=[('', 'Select Online Commission')] +
        SetCommission.percentage_choice,
        label="Online Set Commission",
        widget=forms.Select(attrs={
                            'class': 'form-control text-center block w-[60vw] sm:w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md'})
    )


class SetOnline_ChartbotPayment_Form(forms.ModelForm):
    class Meta:
        model = SetOnline_ChartbotPayment
        fields = ['Current_date',
                  'No_of_questions', 'online_fee']
        labels = {
            'No_of_questions': 'Set no of question',
            'online_fee': 'online chatbot fee',
            'doctor_name': 'Doctor name'
        }
        widgets = {
            'Current_date': forms.DateInput(
                attrs={
                    'class': 'form-control text-center w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md',
                    'type': 'date'
                }
            ),
            'No_of_questions': forms.TextInput(
                attrs={
                    'class': 'form-control text-center  w-[20vw] py-2 lg:py-3 custom-height lg:custom-height text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md',
                    'placeholder': 'Enter the number of questions'
                }
            ),
            'online_fee': forms.TextInput(
                attrs={
                    'class':  'form-control text-center w-[20vw] py-2 lg:py-3 custom-height lg:custom-height text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md', 'placeholder': 'Enter the online chatbot fee'
                }
            ),
            # 'doctor_name': forms.Select(
            #     attrs={
            #         'class': 'form-control text-center w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md'
            #     }
            # ),
        }


class SetOffline_ChartPayment_Form(forms.ModelForm):
    class Meta:
        model = SetOffline_ChartPayment
        fields = ['doctor_name', 'Current_date',
                  'No_of_questions', 'online_fee']
        labels = {
            'No_of_questions': 'Set no of question',
            'online_fee': 'online chatbot fee',
            'doctor_name': 'Doctor name'
        }
        widgets = {
            'Current_date': forms.DateInput(
                attrs={
                    'class': 'form-control text-center w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md',
                    'type': 'date'
                }
            ),
            'No_of_questions': forms.TextInput(
                attrs={
                    'class': 'form-control text-center  w-[20vw] py-2 lg:py-3 custom-height lg:custom-height text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md',
                    'placeholder': 'Enter the number of questions'
                }
            ),
            'online_fee': forms.TextInput(
                attrs={
                    'class':  'form-control text-center w-[20vw] py-2 lg:py-3 custom-height lg:custom-height text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md', 'placeholder': 'Enter the offline chat fee'
                }
            ),
            'doctor_name': forms.Select(
                attrs={
                    'class': 'form-control text-center w-[20vw] py-2 lg:py-3 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-xs lg:text-sm border border-gray-300 rounded-md'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SetOffline_ChartPayment_Form, self).__init__(*args, **kwargs)
        self.fields['doctor_name'].choices = [("", "--Choose--")] + [
            (doctor.id, doctor.first_name) for doctor in Doctors.objects.all()
        ]


# class OfflineConsultationForm(forms.ModelForm):
#     class Meta:
#         model = OfflineConsultation
#         fields = ['doctor_name', 'no_of_questions',
#                   'patient_name', 'offline_fee']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-controlpy-2 px-4 border rounded-md w-2/3 focus:outline-none focus:border-none ', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-controlpy-2 px-4 border rounded-md w-2/3 focus:outline-none focus:border-none', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-controlpy-2 px-4 border rounded-md w-2/3 focus:outline-none focus:border-none', 'placeholder': 'Confirm New Password'})
