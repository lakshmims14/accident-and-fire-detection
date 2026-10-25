from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login,logout as logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Exists, OuterRef


def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def logout_views(request):
    logout(request)
    return redirect('login')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name='rescue').exists():
                try:
                    rescue = RescueTeam.objects.get(user=user)
                    if rescue.status != 'approved':
                        messages.error(request, "Your account is pending approval.")
                        return redirect('login')
                except RescueTeam.DoesNotExist:
                    messages.error(request, "Rescue account not found.")
                    return redirect('login')

            elif user.groups.filter(name='user').exists():
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile.status != 'approved':
                        messages.error(request, "Your account is pending approval.")
                        return redirect('login')
                except UserProfile.DoesNotExist:
                    messages.error(request, "User profile not found.")
                    return redirect('login')

            auth_login(request, user)
            request.session['userid'] = user.id

            if user.is_superuser:
                return redirect('admin_home')
            elif user.groups.filter(name='rescue').exists():
                return redirect('rescue_home')
            elif user.groups.filter(name='user').exists():
                return redirect('user_home')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

#FORGOT PASSWORD
def forgot_password(request):
    context = {}
    if request.method == 'POST':
        if 'check_user' in request.POST:
            username = request.POST.get('username')
            try:
                user = User.objects.get(username=username)
                context['user_found'] = True
                context['username'] = username
            except User.DoesNotExist:
                messages.error(request, "User does not exist. Please check your username.")

        elif 'change_password' in request.POST:
            username = request.POST.get('username')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
            else:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully! Please login again.")
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, "Unexpected error: user not found.")

    return render(request, 'forgot_password.html', context)

#/////////ADMIN/////////////////////////////////////////////////////////////////////////////////////////////////////////
@login_required(login_url='login')
def admin_home(request):
    return render(request,"admin_home.html")


# ------------------ VIEW USERS ------------------
@login_required(login_url='login')
def admin_view_users(request):
    users = UserProfile.objects.all().order_by('id')
    return render(request, 'admin_view_users.html', {'users': users})

# ------------------ APPROVE USER ------------------
@login_required(login_url='login')
def admin_approve_user(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    profile.status = 'approved'
    profile.save()
    messages.success(request, " approved successfully!")
    return redirect('admin_view_users')

# ------------------ REJECT USER ------------------
@login_required(login_url='login')
def admin_reject_user(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    profile.status = 'rejected'
    profile.save()
    messages.success(request, " rejected successfully!")
    return redirect('admin_view_users')

# ------------------ DELETE USER ------------------
@login_required(login_url='login')
def admin_delete_user(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    user_name = profile.name
    profile.user.delete()
    messages.success(request, " deleted successfully!")
    return redirect('admin_view_users')

# ------------------ VIEW RESCUE TEAM ------------------
@login_required(login_url='login')
def admin_view_rescue_team(request):
    teams = RescueTeam.objects.all().order_by('id')
    return render(request, 'admin_view_rescue_team.html', {'teams': teams})

# ------------------ APPROVE RESCUE TEAM ------------------
@login_required(login_url='login')
def admin_approve_rescue(request, team_id):
    team = get_object_or_404(RescueTeam, id=team_id)
    team.status = 'approved'
    team.save()
    messages.success(request, team.name + " approved successfully!")
    return redirect('admin_view_rescue_team')

# ------------------ REJECT RESCUE TEAM ------------------
@login_required(login_url='login')
def admin_reject_rescue(request, team_id):
    team = get_object_or_404(RescueTeam, id=team_id)
    team.status = 'rejected'
    team.save()
    messages.success(request, team.name + " rejected successfully!")
    return redirect('admin_view_rescue_team')

# ------------------ DELETE RESCUE TEAM ------------------
@login_required(login_url='login')
def admin_delete_rescue(request, team_id):
    team = get_object_or_404(RescueTeam, id=team_id)
    team_name = team.name
    team.user.delete()
    messages.success(request, team_name + " deleted successfully!")
    return redirect('admin_view_rescue_team')

# ------------------ ADMIN COMPLAINTS ------------------
@login_required(login_url='login')
def admin_complaints(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        reply_text = request.POST.get('reply')
        complaint = get_object_or_404(Complaint, id=complaint_id)

        if reply_text:
            complaint.reply = reply_text
            complaint.save()
            messages.success(request, "Reply sent successfully.")
        else:
            messages.error(request, "Reply cannot be empty.")
        return redirect('admin_complaints')

    complaints = Complaint.objects.filter(reply__isnull=True).order_by('-date')
    return render(request, 'admin_complaints.html', {'complaints': complaints})


#ADMIN VIEW FEEDBACKS
@login_required(login_url='login')
def admin_feedbacks(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    feedbacks = Feedback.objects.all().order_by('-date')

    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'admin_feedbacks.html', context)

# ---------- VIEW ACCIDENT RECORDS ----------
@login_required
def view_accident_records(request):
    records = AccidentRecord.objects.select_related('camera').annotate(
        unassigned_first=Case(
            When(status='unassigned', then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('unassigned_first', '-detected_at')
    return render(request, 'admin_view_accident_records.html', {'records': records})

# ---------- VIEW FIRE RECORDS ----------
@login_required
def view_fire_records(request):
    records = FireRecord.objects.select_related('camera').annotate(
        unassigned_first=Case(
            When(status='unassigned', then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('unassigned_first', '-detected_at')
    return render(request, 'admin_view_fire_records.html', {'records': records})


# ---------- ADMIN ASSIGN ALERT ACCIDENT ----------

# @login_required(login_url='login')
# def admin_assign_accident(request, record_id):
#     record = get_object_or_404(AccidentRecord, id=record_id)
#     rescue_teams = RescueTeam.objects.filter(status='approved')
#
#     if request.method == 'POST':
#         rescue_id = request.POST.get('rescue_team')
#         status = request.POST.get('status')
#         rescue_team = get_object_or_404(RescueTeam, id=rescue_id)
#
#         Alert.objects.create(
#             camera=record.camera,
#             rescue_team=rescue_team,
#             record_type='accident',
#             status=status
#         )
#
#
#         record.status = 'assigned'
#         record.save()
#
#         messages.success(request, 'Accident record assigned to ' + rescue_team.name + ' with status ' + status.capitalize() + '!')
#         return redirect('view_accident_records')
#
#     return render(request, 'admin_assign_alert.html', {
#         'record': record,
#         'record_type': 'accident',
#         'rescue_teams': rescue_teams,
#     })


@login_required(login_url='login')
def admin_assign_accident(request, record_id):

    record = get_object_or_404(AccidentRecord, id=record_id)
    rescue_teams = RescueTeam.objects.filter(status='approved')

    if request.method == 'POST':
        rescue_id = request.POST.get('rescue_team')
        rescue_team = get_object_or_404(RescueTeam, id=rescue_id)

        # AUTOMATIC PRIORITY
        status = 'important'  # Accident = always high priority

        Alert.objects.create(
            camera=record.camera,
            rescue_team=rescue_team,
            record_type='accident',
            status=status
        )

        record.status = 'assigned'
        record.save()

        messages.success(
            request,
            f'Accident record assigned to {rescue_team.name} with HIGH priority!'
        )

        return redirect('view_accident_records')

    return render(request, 'admin_assign_alert.html', {
        'record': record,
        'record_type': 'accident',
        'rescue_teams': rescue_teams,
        'auto_priority': 'important'
    })


# ---------- ADMIN ASSIGN ALERT FIRE ----------
# @login_required(login_url='login')
# def admin_assign_fire(request, record_id):
#     record = get_object_or_404(FireRecord, id=record_id)
#     rescue_teams = RescueTeam.objects.filter(status='approved')
#
#     if request.method == 'POST':
#         rescue_id = request.POST.get('rescue_team')
#         status = request.POST.get('status')
#         rescue_team = get_object_or_404(RescueTeam, id=rescue_id)
#
#         Alert.objects.create(
#             camera=record.camera,
#             rescue_team=rescue_team,
#             record_type='fire',
#             status=status
#         )
#
#         record.status = 'assigned'
#         record.save()
#
#         messages.success(request, 'Fire record assigned to ' + rescue_team.name + ' with status ' + status.capitalize() + '!')
#         return redirect('view_fire_records')
#
#     return render(request, 'admin_assign_alert.html', {
#         'record': record,
#         'record_type': 'fire',
#         'rescue_teams': rescue_teams,
#     })

@login_required(login_url='login')
def admin_assign_fire(request, record_id):

    record = get_object_or_404(FireRecord, id=record_id)
    rescue_teams = RescueTeam.objects.filter(status='approved')

    # -------- AUTOMATIC PRIORITY LOGIC --------
    if record.confidence is None:
        auto_status = 'Low'
    elif record.confidence >= 0.80:
        auto_status = 'important'
    elif record.confidence >= 0.50:
        auto_status = 'Medium'
    else:
        auto_status = 'Low'
    # -----------------------------------------

    if request.method == 'POST':
        rescue_id = request.POST.get('rescue_team')
        rescue_team = get_object_or_404(RescueTeam, id=rescue_id)

        Alert.objects.create(
            camera=record.camera,
            rescue_team=rescue_team,
            record_type='fire',
            status=auto_status
        )

        record.status = 'assigned'
        record.save()

        messages.success(
            request,
            f'Fire record assigned to {rescue_team.name} with {auto_status.upper()} priority!'
        )

        return redirect('view_fire_records')

    return render(request, 'admin_assign_alert.html', {
        'record': record,
        'record_type': 'fire',
        'rescue_teams': rescue_teams,
        'auto_priority': auto_status
    })


# ---------- DELETE ACCIDENT RECORD ----------
@login_required(login_url='login')
def delete_accident_record(request, record_id):
    record = get_object_or_404(AccidentRecord, id=record_id)
    record.delete()
    messages.success(request, 'Accident record deleted successfully!')
    return redirect('view_accident_records')

# ---------- DELETE FIRE RECORD ----------
@login_required(login_url='login')
def delete_fire_record(request, record_id):
    record = get_object_or_404(FireRecord, id=record_id)
    record.delete()
    messages.success(request, 'Fire record deleted successfully!')
    return redirect('view_fire_records')


# ---------- ADMIN MANAGE AWARENESS ----------
@login_required(login_url='login')
def admin_manage_awareness(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if not title or not description:
            messages.error(request, "Title and Description are required!")
        else:
            Awareness.objects.create(title=title, description=description)
            messages.success(request, "Awareness added successfully!")
            return redirect('admin_manage_awareness')

    awareness_list = Awareness.objects.all().order_by('-date')
    return render(request, 'admin_manage_awareness.html', {'awareness_list': awareness_list})


# ---------- DELETE AWARENESS ----------
@login_required(login_url='login')
def admin_delete_awareness(request, id):
    awareness = get_object_or_404(Awareness, id=id)
    awareness.delete()
    messages.success(request, "Awareness deleted successfully!")
    return redirect('admin_manage_awareness')


#/////////////USER//////////////////////////////////////////////////////////////////////////////////////////////////////
@login_required(login_url='login')
def user_home(request):
    return render(request,'userhome.html')

def user_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        place = request.POST.get('place')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadhar_proof = request.FILES.get('aadhar_proof')
        profile_picture = request.FILES.get('profile_picture')

        if not all([name, email, phone, place, address, username, password]):
            messages.error(request, "All fields are required!")
            return redirect('user_registration')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('user_registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('user_registration')

        user = User.objects.create_user(username=username, password=password, email=email)
        user_group, _ = Group.objects.get_or_create(name='user')
        user.groups.add(user_group)

        UserProfile.objects.create(
            user=user, name=name, email=email, phone=phone, place=place,
            address=address, aadhar_proof=aadhar_proof, profile_picture=profile_picture
        )

        messages.success(request, "✅ Registration successful")
        return redirect('login')

    return render(request, 'user_registration.html')



#PROFILE VIEW
@login_required(login_url='login')
def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile})


#REPORT ACCIDENT
@login_required(login_url='login')
def report_accident(request):
    from django.utils import timezone
    from django.contrib import messages
    from django.shortcuts import render, redirect
    from .models import Report

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        file = request.FILES.get('file')

        if not title or not description or not latitude or not longitude:
            messages.error(request, "Please fill in all required fields.")
            return redirect('report_accident')

        Report.objects.create(
            user=request.user,
            title=title,
            description=description,
            latitude=latitude,
            longitude=longitude,
            file=file,
            date=timezone.now().date(),
            time=timezone.now().time(),
            status='pending'
        )

        messages.success(request, "Accident reported successfully! Rescue team will respond soon.")
        return redirect('report_accident')

    reports = Report.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'report_accident.html', {'reports': reports})

# User complaints view
@login_required(login_url='login')
def user_complaints(request):
    user_id = request.session.get('userid')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        complaint_text = request.POST.get('complaint')
        if complaint_text:
            Complaint.objects.create(sender=user, complaint=complaint_text)
            messages.success(request, "Complaint submitted successfully.")
            return redirect('user_complaints')
        else:
            messages.error(request, "Please enter a complaint.")

    complaints = Complaint.objects.filter(sender=user).order_by('-date')

    context = {
        'complaints': complaints
    }
    return render(request, 'user_complaints.html', context)

#USER FEEDBACKS
@login_required(login_url='login')
def user_feedback(request):
    user_id = request.session.get('userid')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        if feedback_text:
            Feedback.objects.create(sender=user, feedback=feedback_text)
            messages.success(request, "Feedback submitted successfully.")
            return redirect('user_feedback')
        else:
            messages.error(request, "Feedback cannot be empty.")

    feedbacks = Feedback.objects.filter(sender=user).order_by('-date')
    return render(request, 'user_feedback.html', {'feedbacks': feedbacks})

#USER VIEW AWARENESS
def user_view_awareness(request):
    awareness_list = Awareness.objects.all().order_by('-id')
    if not awareness_list:
        messages.info(request, "No awareness posts available at the moment.")
    return render(request, 'user_view_awareness.html', {'awareness_list': awareness_list})



#///////////////RESCUE TEAM/////////////////////////////////////////////////////////////////////////////////////////////

@login_required(login_url='login')
def rescue_home(request):
    return render(request,'rescue_home.html')

def register_rescue(request):
    CATEGORIES = ['Fire', 'Accident']

    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        place = request.POST.get('place')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        license_proof = request.FILES.get('license_proof')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect('register_rescue')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_rescue')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        group, created = Group.objects.get_or_create(name='rescue')
        user.groups.add(group)

        RescueTeam.objects.create(
            user=user,
            category=category,
            name=name,
            email=email,
            phone=phone,
            place=place,
            address=address,
            license_proof=license_proof,
        )

        messages.success(request, "Rescue Team registered successfully!")
        return redirect('register_rescue')

    return render(request, 'register_rescueteam.html', {'categories': CATEGORIES})


#RESCUE PROFILE VIEW
@login_required(login_url='login')
def rescue_profile(request):
    profile = RescueTeam.objects.get(user=request.user)
    return render(request, 'rescue_profile.html', {'profile': profile})


#VIEW REPORT
@login_required(login_url='login')
def view_reports(request):
    user_id = request.session.get('userid')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        rescue_team = RescueTeam.objects.get(user=user)
    except (User.DoesNotExist, RescueTeam.DoesNotExist):
        messages.error(request, "Rescue account not found.")
        return redirect('login')

    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_status = request.POST.get('status')
        report = get_object_or_404(Report, id=report_id)
        if new_status in ['in_progress', 'resolved']:
            report.rescue_team = rescue_team
        else:
            report.rescue_team = None

        report.status = new_status
        report.save()
        messages.success(request, "Report '" + report.title + "' status updated to '" + new_status + "'.")
        return redirect('view_reports')

    pending_reports = Report.objects.filter(status='pending').order_by('-date', '-time')

    my_reports = Report.objects.filter(rescue_team=rescue_team).exclude(status='pending') \
        .annotate(
            status_order=Case(
                When(status='in_progress', then=Value(1)),
                When(status='resolved', then=Value(2)),
                default=Value(3),
                output_field=IntegerField()
            )
        ).order_by('status_order', '-date', '-time')

    context = {
        'pending_reports': pending_reports,
        'my_reports': my_reports,
    }

    return render(request, 'rescue_team_reports.html', context)


#RESCUE COMPLAINTS
@login_required(login_url='login')
def rescue_complaints(request):
    user_id = request.session.get('userid')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        rescue_team = RescueTeam.objects.get(user=user)
    except (User.DoesNotExist, RescueTeam.DoesNotExist):
        messages.error(request, "Rescue account not found.")
        return redirect('login')

    if request.method == 'POST':
        complaint_text = request.POST.get('complaint')
        if complaint_text:
            Complaint.objects.create(sender=user, complaint=complaint_text)
            messages.success(request, "Complaint submitted successfully.")
            return redirect('rescue_complaints')
        else:
            messages.error(request, "Please enter a complaint.")

    complaints = Complaint.objects.filter(sender=user).order_by('-date')

    context = {
        'complaints': complaints
    }
    return render(request, 'rescue_complaints.html', context)



#RESCUE FEEDBACK
@login_required(login_url='login')
def rescue_feedback(request):
    user_id = request.session.get('userid')
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        if feedback_text:
            Feedback.objects.create(sender=user, feedback=feedback_text)
            messages.success(request, "Feedback submitted successfully.")
            return redirect('rescue_feedback')
        else:
            messages.error(request, "Feedback cannot be empty.")

    feedbacks = Feedback.objects.filter(sender=user).order_by('-date')
    return render(request, 'rescue_feedback.html', {'feedbacks': feedbacks})

#RESCUE TEAM VIEW ALERTS
@login_required
def rescue_team_alerts(request):
    try:
        team = request.user.rescueteam
    except RescueTeam.DoesNotExist:
        team = None

    alerts_by_status = {'important': [], 'medium': [], 'low': []}

    if team:
        alerts = Alert.objects.filter(rescue_team=team).order_by('-time')
        for alert in alerts:

            video_url = None
            if alert.record_type == 'accident':
                record = alert.camera.accidentrecord_set.filter(status='assigned').last()
                if record and record.result_video:
                    video_url = record.result_video.url
            elif alert.record_type == 'fire':
                record = alert.camera.firerecord_set.filter(status='assigned').last()
                if record and record.result_video:
                    video_url = record.result_video.url
            alert.video_url = video_url

            status_key = alert.status.lower()
            if status_key in alerts_by_status:
                alerts_by_status[status_key].append(alert)

    return render(request, 'rescue_team_alerts.html', {'alerts_by_status': alerts_by_status})


#//////////ACCIDENT DETECTION///////////////////////////////////////////////////////////////////////////////////////////

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ultralytics import YOLO
import os, threading, platform, subprocess
from .models import Camera, AccidentRecord
from django.utils import timezone

progress_data = {
    "status": "Waiting...",
    "result_video": None,
    "completed": False,
    "accident_detected": False
}

ACCIDENT_MODEL_PATH = r"D:\Fire and accident detection web\Accident\runs\detect\accident_detector\weights\best.pt"


# views.py

@login_required
def add_camera(request):
    # Superuser-only access
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        camera_type = request.POST.get('type')

        # Basic validation
        if not name or not latitude or not longitude or not camera_type:
            messages.error(request, "All fields are required.")
            return redirect('add_camera')

        try:
            Camera.objects.create(
                name=name.strip(),
                latitude=latitude,
                longitude=longitude,
                type=camera_type
            )
            messages.success(request, "Camera added successfully.")

        except Exception as e:
            messages.error(request, f"Failed to add camera: {str(e)}")

        return redirect('add_camera')

    cameras = Camera.objects.all().order_by('-date')
    return render(request, 'admin_add_camera.html', {'cameras': cameras})


# ADMIN: DELETE CAMERA
@login_required
def delete_camera(request, camera_id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    camera = get_object_or_404(Camera, id=camera_id)
    camera.delete()
    messages.success(request, 'Camera deleted successfully.')
    return redirect('add_camera')

# DETECT CAMERA
@login_required
def detect_camera(request, camera_id):
    try:
        camera = Camera.objects.get(id=camera_id)
    except Camera.DoesNotExist:
        messages.error(request, "Camera not found.")
        return redirect('add_camera')

    if camera.type == 'fire':
        template = 'fire_detect.html'
    elif camera.type == 'accident':
        template = 'accident_detect.html'
    else:
        messages.error(request, "Unknown camera type.")
        return redirect('add_camera')

    cameras = Camera.objects.filter(type='accident')
    return render(request, template, {'camera': camera, 'cameras': cameras})

# ACCIDENT DETECTION PAGE
def accident_detect(request):
    cameras = Camera.objects.filter(type='accident')
    return render(request, "accident_detect.html", {"processing": False, "cameras": cameras})

# BACKGROUND THREAD FUNCTION
def detect_accident_background(upload_path, camera_id):
    global progress_data
    progress_data = {"status": "Initializing...", "result_video": None, "completed": False, "accident_detected": None}

    try:
        output_dir = os.path.join(settings.MEDIA_ROOT, "results", "predictions")
        os.makedirs(output_dir, exist_ok=True)

        progress_data["status"] = "Loading YOLO model..."
        model = YOLO(ACCIDENT_MODEL_PATH)

        progress_data["status"] = "Running accident detection..."
        results = model.predict(
            source=upload_path,
            save=True,
            project=os.path.join(settings.MEDIA_ROOT, "results"),
            name="predictions",
            exist_ok=True,
            conf=0.3,
            imgsz=640
        )

        accident_found = False
        for result in results:
            names = result.names
            for box in result.boxes:
                cls = int(box.cls)
                label = names[cls].lower()
                if "accident" in label:
                    accident_found = True
                    break
            if accident_found:
                break

        temp_files = [f for f in os.listdir(output_dir) if f.lower().endswith((".mp4", ".avi"))]
        if not temp_files:
            progress_data["status"] = "⚠️ No result video found!"
            progress_data["completed"] = True
            return

        latest_file = max(temp_files, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)))
        latest_path = os.path.join(output_dir, latest_file)

        progress_data["result_video"] = latest_path
        progress_data["accident_detected"] = accident_found

        if accident_found:
            progress_data["status"] = "🚨 Accident detected!"
            camera = Camera.objects.get(id=camera_id)

            AccidentRecord.objects.create(
                camera=camera,
                result_video=os.path.relpath(latest_path, settings.MEDIA_ROOT),
                detected_at=timezone.localtime())
        else:
            progress_data["status"] = "✅ No accident detected."

        progress_data["completed"] = True

    except Exception as e:
        progress_data["status"] = "❌ Error: " + str(e)
        progress_data["completed"] = True

# PROCESS VIDEO
def process_video(request):
    global progress_data
    progress_data = {"status": "Waiting...", "result_video": None, "completed": False}

    if request.method == "POST":
        video_file = request.FILES.get("video")
        camera_id = request.POST.get("camera")

        if not camera_id:
            messages.error(request, "Please select a camera.")
            return redirect("accident_detect")

        if video_file:
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = os.path.join(upload_dir, video_file.name)

            with open(upload_path, "wb+") as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            thread = threading.Thread(target=detect_accident_background, args=(upload_path, camera_id))
            thread.start()

            cameras = Camera.objects.filter(type='accident')
            selected_camera = Camera.objects.get(id=camera_id)
            return render(request, "accident_detect.html", {"processing": True, "camera": selected_camera, "cameras": cameras})

    cameras = Camera.objects.filter(type='accident')
    return render(request, "accident_detect.html", {"processing": False, "cameras": cameras})

# GET PROGRESS
def get_progress(request):
    return JsonResponse(progress_data)

# OPEN RESULT VIDEO
def open_video_system(request):
    try:
        video_path = progress_data.get("result_video")
        if video_path and os.path.exists(video_path):
            if platform.system() == "Windows":
                os.startfile(video_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", video_path])
            else:
                subprocess.run(["xdg-open", video_path])
    except Exception as e:
        print("⚠️ Failed to open video: " + str(e))
    return redirect("accident_detect")



#//////////FIRE DETECTION///////////////////////////////////////////////////////////////////////////////////////////////

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ultralytics import YOLO
import os, threading, platform, subprocess
from .models import Camera, FireRecord
from django.utils import timezone

progress_data_fire = {
    "status": "Waiting...",
    "result_video": None,
    "completed": False,
    "fire_detected": False
}

FIRE_MODEL_PATH = r"D:\Fire and accident detection web\fire-smoke-detection.v2-v2.yolov8\runs\detect\fire_smoke_model3\weights\best.pt"


# FIRE DETECTION PAGE
@login_required
def fire_detect(request):
    cameras = Camera.objects.filter(type='fire')
    return render(request, "fire_detect.html", {"processing": False, "cameras": cameras})


# BACKGROUND THREAD FUNCTION
from django.db import close_old_connections
from django.utils import timezone
import os
import time
import torch

def detect_fire_background(upload_path, camera_id):
    global progress_data_fire
    progress_data_fire = {
        "status": "Initializing...",
        "result_video": None,
        "completed": False,
        "fire_detected": None,
        "confidence": None
    }

    try:
        # ✅ Thread-safe DB handling
        close_old_connections()

        output_dir = os.path.join(settings.MEDIA_ROOT, "results", "fire_predictions")
        os.makedirs(output_dir, exist_ok=True)

        progress_data_fire["status"] = "Loading Fire model..."
        model = YOLO(FIRE_MODEL_PATH)

        progress_data_fire["status"] = "Running fire detection..."
        results = model.predict(
            source=upload_path,
            save=True,
            project=output_dir,
            name="predictions",
            exist_ok=True,
            conf=0.3,
            imgsz=640
        )

        fire_found = False
        max_confidence = 0.0

        # 🔍 Parse YOLO results
        for result in results:
            for box in result.boxes:
                label = result.names[int(box.cls)].lower()
                conf = float(box.conf.item())  # tensor → float

                if "fire" in label:
                    fire_found = True
                    max_confidence = max(max_confidence, conf)

        pred_dir = os.path.join(output_dir, "predictions")

        # ⏳ Wait for output video
        temp_files = []
        for _ in range(10):
            temp_files = [
                f for f in os.listdir(pred_dir)
                if f.lower().endswith((".mp4", ".avi"))
            ]
            if temp_files:
                break
            time.sleep(0.5)

        if not temp_files:
            progress_data_fire["status"] = "⚠️ No result video found."
            progress_data_fire["completed"] = True
            return

        latest_file = max(
            temp_files,
            key=lambda f: os.path.getmtime(os.path.join(pred_dir, f))
        )

        latest_path = os.path.join(pred_dir, latest_file)

        progress_data_fire["result_video"] = latest_path
        progress_data_fire["fire_detected"] = fire_found
        progress_data_fire["confidence"] = round(max_confidence, 3)

        if fire_found:
            progress_data_fire["status"] = "🚨 Fire detected!"

            camera = Camera.objects.get(id=camera_id)

            FireRecord.objects.create(
                camera=camera,
                result_video=os.path.relpath(latest_path, settings.MEDIA_ROOT),
                detected_at=timezone.now(),
                confidence=max_confidence,  # ✅ STORED
                status="unassigned"
            )

        else:
            progress_data_fire["status"] = "✅ No fire detected."

        progress_data_fire["completed"] = True

    except Exception as e:
        import traceback
        traceback.print_exc()
        progress_data_fire["status"] = f"❌ Error: {e}"
        progress_data_fire["completed"] = True



# PROCESS VIDEO (handles POST)
@login_required
def process_fire_video(request):
    global progress_data_fire
    progress_data_fire = {"status": "Waiting...", "result_video": None, "completed": False}

    if request.method == "POST":
        video_file = request.FILES.get("video")
        camera_id = request.POST.get("camera")

        if not camera_id:
            messages.error(request, "Please select a camera.")
            return redirect("fire_detect")

        if video_file:
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = os.path.join(upload_dir, video_file.name)

            with open(upload_path, "wb+") as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            thread = threading.Thread(target=detect_fire_background, args=(upload_path, camera_id))
            thread.start()

            cameras = Camera.objects.filter(type='fire')
            selected_camera = Camera.objects.get(id=camera_id)
            return render(request, "fire_detect.html", {"processing": True, "camera": selected_camera, "cameras": cameras})

    cameras = Camera.objects.filter(type='fire')
    return render(request, "fire_detect.html", {"processing": False, "cameras": cameras})


# GET PROGRESS
@login_required
def get_fire_progress(request):
    return JsonResponse(progress_data_fire)


# OPEN RESULT VIDEO
@login_required
def open_fire_video_system(request):
    try:
        video_path = progress_data_fire.get("result_video")
        if video_path and os.path.exists(video_path):
            if platform.system() == "Windows":
                os.startfile(video_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", video_path])
            else:
                subprocess.run(["xdg-open", video_path])
    except Exception as e:
        print("⚠️ Failed to open video: " + str(e))
    return redirect("fire_detect")
