from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone
from datetime import date
from datetime import datetime

# Create your models here.


class Specialisation(models.Model):
    name = models.CharField(max_length=200, null=False,
                            blank=False)

    def __str__(self):
        return self.name


class Doctors(models.Model):

    first_name = models.CharField(
        max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    mobile = models.CharField(
        max_length=20, null=False, blank=False, unique=True)
    date_of_birth = models.DateField()
    country_code = models.CharField(max_length=20, default='US')
    GENDER_CHOICES = [
        ('CHOOSE', '--Choose--'),
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default=0)
    email = models.EmailField(null=False, blank=False)
    specialisation = models.ForeignKey(
        Specialisation, on_delete=models.CASCADE)
    doctor_fees = models.IntegerField()
    address = models.TextField(max_length=300, null=False, blank=False)
    experience = models.FloatField()
    qualification = models.CharField(max_length=20, default='MBBS')
    image = models.ImageField(null=False, blank=False)
    isblocked = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    feedback_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip()
        # Strip whitespace from other fields if necessary
        super(Doctors, self).save(*args, **kwargs)

    def update_feedback_count(self):
        self.feedback_count = self.review_set.count()
        self.save()

    class Meta:
        verbose_name = 'Add Doctor'

    def __str__(self):
        return self.first_name


class Patients(models.Model):

    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    mobile = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    age = models.IntegerField()
    GENDER_CHOICES = [

        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(max_length=300, null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    status = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Add Patient'

    def __str__(self):
        return self.first_name


class Review(models.Model):
    doctors_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patients_name = models.ForeignKey(Patients, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200)
    doctor_reply = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.doctors_name.update_feedback_count()

    def delete(self, *args, **kwargs):
        doctor = self.doctors_name
        super().delete(*args, **kwargs)
        doctor.update_feedback_count()

    def __str__(self):
        return str(self.patients_name)


class Appointment(models.Model):
    doctor_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient_name = models.ForeignKey(Patients, on_delete=models.CASCADE)
    time = models.TimeField(default=timezone.now().strftime('%H:%M:%S'))
    date = models.DateField(default=date.today().strftime('%Y-%m-%d'))
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.patient_name)


class Payments(models.Model):
    patient_name = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    paid_amount = models.CharField(max_length=100)
    p_date = models.DateField(default=date.today().strftime('%Y-%m-%d'))
    payment_status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.patient_name)


class SetCommission(models.Model):
    percentage_choice = [
        ('10', '10%'),
        ('20', '20%'),
        ('30', '30%'),
        ('40', '40%'),
        ('50', '50%'),
        ('60', '60%'),
    ]
    OfflineSetCommission = models.CharField(
        max_length=10, choices=percentage_choice)
    OnlineSetCommission = models.CharField(
        max_length=10, choices=percentage_choice)
    current_date = models.DateField(default=date.today)

    def __str__(self):
        return f" 'Offline commision amount is ::' {self.OfflineSetCommission}  'Online commission amount is' {self.OnlineSetCommission} 'and date is  {self.current_date}"


# # gender = models.CharField(max_length=10, choices=percentage_choice)

# After offline consulation its detailes will come to this table, now its just for a test try.

class SetOnline_ChartbotPayment(models.Model):
    Current_date = models.DateField(default=date.today)
    No_of_questions = models.CharField(max_length=20)
    online_fee = models.CharField(max_length=100)

    def __str__(self):
        return f'On "{self.Current_date}" Online chatbot payment and no of question is "{self.No_of_questions}"'


class SetOffline_ChartPayment(models.Model):
    Current_date = models.DateField(default=date.today)
    No_of_questions = models.CharField(max_length=20)
    online_fee = models.CharField(max_length=100)
    doctor_name = models.ForeignKey(
        Doctors, on_delete=models.CASCADE)

    def __str__(self):
        return f'Dr name "{self.doctor_name}" and fee is {self.online_fee}'


class OfflineConsultation(models.Model):
    doctor_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    no_of_questions = models.CharField(max_length=20)
    patient_name = models.ForeignKey(Patients, on_delete=models.CASCADE)
    offline_fee = models.CharField(max_length=100)

    def __str__(self):
        return f'Patient name "{self.patient_name}" and the no of offline question is {self.no_of_questions}'
