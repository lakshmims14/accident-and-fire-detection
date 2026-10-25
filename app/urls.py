
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('logout/', views.logout_views, name='logout'),
    path('login/',views.login,name="login"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

#////////////////ADMIN//////////////////////////////////////////////////////////////////////////////////////////////////

    path('admin_home/', views.admin_home, name="admin_home"),
    path('admin_view_users/', views.admin_view_users, name='admin_view_users'),
    path('admin_approve_user/<int:user_id>/', views.admin_approve_user, name='admin_approve_user'),
    path('admin_reject_user/<int:user_id>/', views.admin_reject_user, name='admin_reject_user'),
    path('admin_delete_user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),

    path('admin_rescue_team/', views.admin_view_rescue_team, name='admin_view_rescue_team'),
    path('admin_rescue_team/approve/<int:team_id>/', views.admin_approve_rescue, name='admin_approve_rescue'),
    path('admin_rescue-team_reject/<int:team_id>/', views.admin_reject_rescue, name='admin_reject_rescue'),
    path('admin_rescue_team_delete/<int:team_id>/', views.admin_delete_rescue, name='admin_delete_rescue'),

    path('admin_complaints/', views.admin_complaints, name='admin_complaints'),
    path('admin_feedbacks/', views.admin_feedbacks, name='admin_feedbacks'),

    path('view_fire_records/', views.view_fire_records, name='view_fire_records'),
    path('view_accident_records/', views.view_accident_records, name='view_accident_records'),

    path('add_camera/', views.add_camera, name='add_camera'),
    path('delete_camera/<int:camera_id>/', views.delete_camera, name='delete_camera'),
    path('detect_camera/<int:camera_id>/', views.detect_camera, name='detect_camera'),

    path("detect_accident/", views.accident_detect, name="accident_detect"),
    path("process_video/", views.process_video, name="process_video"),
    path("get_progress/", views.get_progress, name="get_progress"),
    path("open_video_system/", views.open_video_system, name="open_video_system"),

    path('fire_detect/', views.fire_detect, name='fire_detect'),
    path('process_fire_video/', views.process_fire_video, name='process_fire_video'),
    path('get_fire_progress/', views.get_fire_progress, name='get_fire_progress'),
    path('open_fire_video_system/', views.open_fire_video_system, name='open_fire_video_system'),


    path('admin_assign_accident/<int:record_id>/', views.admin_assign_accident, name='admin_assign_accident'),
    path('admin_assign_fire/<int:record_id>/', views.admin_assign_fire, name='admin_assign_fire'),
    path('accidents_delete/<int:record_id>/', views.delete_accident_record, name='delete_accident_record'),
    path('fires_delete/<int:record_id>/', views.delete_fire_record, name='delete_fire_record'),
    path('admin_manage_awareness/', views.admin_manage_awareness, name='admin_manage_awareness'),
    path('admin_delete_awareness/<int:id>/', views.admin_delete_awareness, name='admin_delete_awareness'),



#//////////USER/////////////////////////////////////////////////////////////////////////////////////////////////////////

    path('user_home/', views.user_home, name="user_home"),
    path('user_registration/',views.user_registration,name="user_registration"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('report_accident/', views.report_accident, name='report_accident'),
    path('user_complaints/', views.user_complaints, name='user_complaints'),
    path('user_feedback/', views.user_feedback, name='user_feedback'),
    path('view_awareness/', views.user_view_awareness, name='user_view_awareness'),




#///////////RESCUE//////////////////////////////////////////////////////////////////////////////////////////////////////

    path('rescue_home/', views.rescue_home, name="rescue_home"),
    path('register_rescue/', views.register_rescue, name='register_rescue'),
    path('rescue_profile/', views.rescue_profile, name='rescue_profile'),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('rescue_complaints/', views.rescue_complaints, name='rescue_complaints'),
    path('rescue_feedback/', views.rescue_feedback, name='rescue_feedback'),
    path('rescue_alerts/', views.rescue_team_alerts, name='rescue_team_alerts'),






]
