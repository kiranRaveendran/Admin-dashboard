from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Specialisation
from .forms import specialization_Form
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .forms import *
from .models import Doctors, Patients, Review
from datetime import date
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'username': user.username})
            else:
                return JsonResponse({'success': False}, status=401)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = LoginForm()

    return render(request, 'authorization/login.html', {'form': form})


def dashboard(request):
    return render(request, 'dashboard.html')


# ////////////////////// Doctor module


def doctor_Dashboard(request):
    doctors = Doctors.objects.all

    return render(request, "doctor/doctor_Dashboard.html", {'doctors': doctors})


def add_doctors(request):
    form = Doctor_Form()
    if request.method == 'POST':
        form = Doctor_Form(request.POST, request.FILES)
        if form.is_valid():
            # Mobile number validation using view logic (optional)
            mobile = form.cleaned_data['mobile']
            if Doctors.objects.filter(mobile=mobile).exists():
                # Add error to specific field
                JsonResponse({'msg': 'Mobile numebr already exist'})
            else:
                form.save()
                return JsonResponse({'msg': 'Success'})
        else:
            error_message = form.errors.as_text()
    else:
        form = Doctor_Form()
        error_message = ''  # No errors initially
    return render(request, "doctor/add_doctors.html", {'form': form, 'error_message': error_message})


def delete_doctors(request, pk):
    doctor = Doctors.objects.get(id=pk)
    doctor.delete()
    return redirect("view_doctors")


def view_doctors(request):
    doctors = Doctors.objects.all()
    return render(request, 'doctor/view_doctor.html', {'doctors': doctors})


def block(request, pk):
    if request.method == 'POST':
        doctor = Doctors.objects.get(id=pk)
        doctor.isblocked = True
        doctor.save()
        return redirect(reverse('blocked_doctors'))


def blocked_doctors(request):
    blocked_doctors = Doctors.objects.filter(isblocked=True)
    return render(request, 'doctor/blocked_doctors.html', {'blocked_doctors': blocked_doctors})


def unblock(request, pk):
    if request.method == 'POST':
        doctor = Doctors.objects.get(id=pk)
        doctor.isblocked = False
        doctor.save()
        return redirect(reverse('approved_doctors'))


def approved(request, pk):
    doctor = Doctors.objects.get(id=pk)
    doctor.status = True
    doctor.save()

    return redirect('approved_doctors')


def approved_doctors(request):
    doctors = Doctors.objects.all()
    return render(request, 'doctor/approved_doctors.html', {'doctors': doctors})


# ////////////////////// Patient module


def patient_Dashboard(request):
    patients = Patients.objects.all()
    return render(request, 'patient_Dashboard.html', {'patients': patients})


def view_patients(request):
    patients = Patients.objects.all()
    return render(request, 'patient/view_patients.html', {'patients': patients})


def block_p(request, patient_id):
    if request.method == 'POST':
        patient = Patients.objects.get(id=patient_id)
        patient.is_blocked = True
        patient.save()
        return redirect('blocked_patients')


def blocked_patients(request):

    blocked_patients = Patients.objects.filter(is_blocked=True)
    return render(request, 'patient/blocked_patients.html', {'patients': blocked_patients})


def unblock_patients(request, patient_id):
    if request.method == 'POST':
        patient = Patients.objects.get(id=patient_id)
        patient.is_blocked = False
        patient.save()
        return redirect(reverse('view_patients'))


def delete_patients(request, patient_id):
    patient = Patients.objects.get(id=patient_id)
    patient.delete()
    return redirect("view_patients")

# ------------------------- doctor's feedback


def patients_Feedback(request):
    doctors = Doctors.objects.all

    return render(request, 'patients_Feedback.html', {'doctors': doctors})


def view_reviews(request, doctor_id):
    doctor = Doctors.objects.get(id=doctor_id)
    reviews = Review.objects.filter(doctors_name=doctor)
    return render(request, 'view_reviews.html', {'reviews': reviews})


def delete_reviews(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    doctor = review.doctors_name
    review.delete()
    doctor.update_feedback_count()
    return redirect("patients_Feedback")


# ////////////////////// Ongoin , Upcoming consultation section


@login_required(login_url='login_page')
def ongoing_consulations(request):
    today = date.today()
    ongoing = Appointment.objects.filter(
        date=today).order_by('doctor_name', 'time')
    unique_ongoing = []
    seen_doctors = set()
    for consultation in ongoing:
        doctor_name = consultation.doctor_name
        time = consultation.time
        if (doctor_name, time) not in seen_doctors:
            unique_ongoing.append(consultation)
            seen_doctors.add((doctor_name, time))
    return render(request, "ongoing.html", {'ongoing':  unique_ongoing})


@login_required(login_url='login_page')
def upcoming_consultations(request):
    today = date.today()
    upcoming = Appointment.objects.filter(
        date__gt=today).order_by('doctor_name', 'time')
    unique_upcoming = []
    seen_doctors = set()
    for consultation in upcoming:
        doctor_name = consultation.doctor_name
        time = consultation.time
        if (doctor_name, time) not in seen_doctors:
            unique_upcoming.append(consultation)
            seen_doctors.add((doctor_name, time))

    return render(request, 'upcoming.html', {'upcoming': unique_upcoming})

# ////////////////////// Specialization section


def specialization(request):
    specialization_data = Specialisation.objects.all()
    form = specialization_Form()
    return render(request, 'add_Specialization.html', {'form': form, 'specialization_data': specialization_data})


def add_specialization(request):
    specialization_data = Specialisation.objects.all()
    form = specialization_Form()
    if request.method == 'POST':
        form = specialization_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('add_specialization'))
    else:
        return render(request, 'add_Specialization.html', {'form': form, 'specialization_data': specialization_data})


def updateSpecialization(request, pk):
    data = get_object_or_404(Specialisation, pk=pk)
    form_data = specialization_Form(
        request.POST or None, instance=get_object_or_404(Specialisation, pk=pk))
    if request.method == 'POST':
        form_data = specialization_Form(
            request.POST or None, instance=get_object_or_404(Specialisation, pk=pk))
        if form_data.is_valid():
            form_data.save()
            return JsonResponse({'msg': 'Success'})
        else:
            return JsonResponse({'msg': 'Error', 'errors': form_data.errors})
    elif request.method == 'GET':
        form = specialization_Form(instance=data)
        response_data = {
            'name': form['name'].value()
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'msg': 'Invalid request'}, status=400)


def load_specialization(request):
    specialization_data = Specialisation.objects.all()
    condition = True
    return render(request, 'specialization_load.html', {'specialization_data': specialization_data, 'condition': condition})


def specialization_edit_button(request, pk):
    data = get_object_or_404(Specialisation, pk=pk)
    form_data = specialization_Form(instance=data)
    return render(request, 'specialization_edit_button.html', {'form_data': form_data, 'data': data})

def deleteSpecialization(request, pk):
    if request.method == "GET":  # Make sure it's a GET request
        name = get_object_or_404(Specialisation, id=pk)
        name.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# ////////////////////// Amount module

@login_required(login_url='login_page')
def amount_dashboard(request):
    return render(request, 'amount/amount_dashboard.html')


@login_required(login_url='login_page')
def patient_paymentdetails(request):
    patients = Patients.objects.all()
    payments = Payments.objects.select_related(
        'patient_name', 'doctor_name')

# filtering the doctors name by doctors fees
    doctors_data = Doctors.objects.all()
    doctor_names_by_fee = {}
    for doctor in doctors_data:
        if doctor.doctor_fees in doctor_names_by_fee:
            doctor_names_by_fee[doctor.doctor_fees].append(doctor.first_name)
        else:
            doctor_names_by_fee[doctor.doctor_fees] = [doctor.first_name]

# Filter the queryset based on the search query
    if request.method == 'GET':
        search_query = request.GET.get('query', '')
        if search_query:
            payments = Payments.objects.filter(Q(patient_name__first_name__icontains=search_query) | Q(
                patient_name__last_name__icontains=search_query))

    appointment_dates = {}
    appointment_data = Appointment.objects.all()
    for payment in payments:
        appointments = Appointment.objects.filter(
            doctor_name=payment.doctor_name)
        appointment_dates[payment.patient_name.id] = [
            appointment.date.strftime('%Y-%m-%d') for appointment in appointments]
    return render(request, 'amount/patient_paymentdetails.html', {'appointment_data': appointment_data, 'doctor_names_by_fee': doctor_names_by_fee, 'payments': payments, 'appointment_dates': appointment_dates, 'patients': patients})


def payments_tobedone(request):
    appointments = Appointment.objects.all()
    # filtering the doctors name by doctors fees
    doctors_data = Doctors.objects.all()
    doctor_names_by_fee = {}
    for doctor in doctors_data:
        if doctor.doctor_fees in doctor_names_by_fee:
            doctor_names_by_fee[doctor.doctor_fees].append(doctor.first_name)
        else:
            doctor_names_by_fee[doctor.doctor_fees] = [doctor.first_name]
    return render(request, 'amount/payments_tobedone.html', {'appointments': appointments, 'doctor_names_by_fee': doctor_names_by_fee})


def debited_payment(request):
    payments = 0
    return render(request, 'amount/debited_payment.html', {'payments': payments})


def offlineDebitPayments(request):
    consultations = OfflineConsultation.objects.all()
    # Assuming there's only one SetCommission entry and it's for offline consultations
    commission_entry = SetCommission.objects.latest('current_date')
    commission_percentage = int(commission_entry.OfflineSetCommission)

    # final amount after commission deduction
    modified_data = []
    for consultation in consultations:
        offline_fee = float(consultation.offline_fee)
        commission_amount = (commission_percentage / 100) * offline_fee
        final_amount = offline_fee - commission_amount
        modified_data.append({
            'doctor_name': consultation.doctor_name,
            'no_of_questions': consultation.no_of_questions,
            'patient_name': consultation.patient_name,
            'original_offline_fee': offline_fee,
            'final_amount': final_amount,
        })

    return render(request, 'amount/offline_debit_payment.html', {'data': modified_data})


def onlineDebitPayments(request):
    consultations = Payments.objects.all()
    # Assuming there's only one SetCommission entry and it's for offline consultations
    commission_entry = SetCommission.objects.latest('current_date')
    commission_percentage = int(commission_entry.OnlineSetCommission)

    dr_list = Doctors.objects.all()
    dr_name_fee = {d.first_name: d.doctor_fees for d in dr_list}

    modified_data = []
    for consultation in consultations:
        doctor_name = str(consultation.doctor_name)
        online_fee = dr_name_fee.get(doctor_name, 0)
        commission_amount = (commission_percentage / 100) * online_fee
        final_amount = online_fee - commission_amount
        modified_data.append({
            'doctor_name': consultation.doctor_name,
            'patient_name': consultation.patient_name,
            'original_offline_fee': online_fee,
            'final_amount': final_amount,
        })
    return render(request, 'amount/online_debit_payment.html', {'data': modified_data})


def set_commission(request):
    f = SetCommission.objects.all().order_by('current_date')
    if request.method == 'POST':
        form = SetCommissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('set_commission')
    else:
        form = SetCommissionForm()
    return render(request, 'amount/set_commission.html', {'form': form, 'f': f})


def SetOnline_ChartbotPayment_function(request):
    form = SetOnline_ChartbotPayment_Form()
    if request.method == 'POST':
        form = SetOnline_ChartbotPayment_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chatbot_payment')
    return render(request, 'amount/setchatbot_payment.html', {'form': form})


def chatbot_paiddetails(request):
    data = SetOnline_ChartbotPayment.objects.all()
    return render(request, 'amount/chatbot_paiddetails.html', {'data': data})


def setoffline_chat(request):
    form = SetOffline_ChartPayment_Form()
    if request.method == 'POST':
        form = SetOffline_ChartPayment_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('setoffline_chat')
    return render(request, 'amount/Setoffline_chat_payment.html', {'form': form})


def offline_patient_payment_details(request):
    form = OfflineConsultation.objects.all()
    return render(request, 'amount/offline_paymentDetails.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True, 'message': 'Your password was successfully updated!'})
        else:
            form_html = render_to_string('your_template_with_form.html', {
                                         'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = CustomPasswordChangeForm(request.user)
        form_html = render_to_string('your_template_with_form.html', {
                                     'form': form}, request=request)
        return JsonResponse({'form_html': form_html})

# /////////////////////////////////////////


def logout(request):
    auth.logout(request)
    return redirect("login_page")
