from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    address = models.TextField()
    aadhar_proof = models.FileField(upload_to='aadhar_proofs/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')


# Rescue Team Model
class RescueTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    address = models.TextField()
    license_proof = models.FileField(upload_to='license_proofs/')
    status = models.CharField(max_length=20, default='pending')


# Report Model
class Report(models.Model):
    rescue_team = models.ForeignKey(RescueTeam, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('in_progress','In Progress'),('resolved','Resolved')], default='pending')


# Camera Model
class Camera(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=[('fire','Fire'),('accident','Accident')])


# Alert Model
class Alert(models.Model):
    RECORD_TYPE_CHOICES = (
        ('accident', 'Accident'),
        ('fire', 'Fire'),
    )
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    rescue_team = models.ForeignKey(RescueTeam, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('important','Important'),('medium','Medium'),('low','Low')])
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)

# Awareness Model
class Awareness(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

# Complaint Model
class Complaint(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.TextField()
    reply = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

# Feedback Model
class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)

#ACCIDENT
class AccidentRecord(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    result_video = models.FileField(upload_to='accident_results/')
    detected_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('unassigned', 'Unassigned'), ('assigned', 'Assigned')], default='unassigned')

#FIRE
class FireRecord(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    result_video = models.FileField(upload_to='results/fire_predictions/',max_length=1000)
    detected_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('unassigned', 'Unassigned'), ('assigned', 'Assigned')], default='unassigned')
    confidence = models.FloatField(null=True,blank=True,max_length=1000,help_text="Highest fire detection confidence (0–1)")


