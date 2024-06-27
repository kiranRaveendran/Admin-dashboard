from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Specialisation)
admin.site.register(Doctors)
admin.site.register(Patients)
admin.site.register(Review)
admin.site.register(Appointment)
admin.site.register(Payments)
admin.site.register(SetCommission)
admin.site.register(OfflineConsultation)
admin.site.register(SetOnline_ChartbotPayment)
admin.site.register(SetOffline_ChartPayment)
