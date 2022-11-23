from django.urls import path
from .views import index, scanner, qr_scan, get_student, get_student_detail, pin_input


urlpatterns = [
    path('', index, name="attendance_index"),
    path('pin/', pin_input, name="attendance_pin"),
    #path('get_pin/', get_pin, name="attendance_get-pin"),
    path('scanner/', scanner, name="attendance_scanner"),
    path('scanner/', scanner, name="attendance_scanner"),
    path('qr_scan/', qr_scan, name="attendance_qr-scan"),
    path('get_student/', get_student, name="attendance_get-student"),
    path('get_student_detail/', get_student_detail, name="attendance_get-student-detail"),
]
