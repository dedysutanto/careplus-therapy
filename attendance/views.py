import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from student.models import Students
from schedule.models import Schedules
from therapist.models import Therapists
from data_support.models import Activities


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def construct_name(obj):
    return '{}. {} ({})'.format(obj.id, obj.name, obj.call_name)

def get_student(request):
    if is_ajax(request=request):
        query = request.GET.get("term", "")
        print(query)
        students = Students.objects.filter(
            name__icontains=query,
            call_name__icontains=query,
            session_scheduled__gt=0
        )
        results = []
        place_json = {}
        for student in students:
            place_json = construct_name(student)
            results.append(place_json)
        data = json.dumps(results)

    mimetype = "application/json"
    return HttpResponse(data, mimetype)

def get_student_detail(request):
    if is_ajax(request=request):
        query = request.GET.get("term", "")
        print(query)
        try:
            student = Students.objects.get(
                id=query
            )
            today = datetime.date.today()
            schedules = Schedules.objects.filter(
                student=student,
                date=today,
                is_done=False,
            )
            schedules_next = Schedules.objects.filter(
                student=student,
                date__gt=today,
                is_done=False,
            ).order_by('date')
        except ObjectDoesNotExist:
            student = None
        place_json = {}
        if student:
            place_json['status'] = True

            schedules_array = []
            if schedules:
                for schedule in schedules:
                    schedule_list = {}
                    therapist = Therapists.objects.get(id=schedule.therapist.id)
                    activity = Activities.objects.get(id=schedule.activity.id)
                    schedule_list['id'] = schedule.id
                    schedule_list['date'] = schedule.date
                    schedule_list['start'] = schedule.start
                    schedule_list['end'] = schedule.end
                    schedule_list['therapist'] = therapist.name
                    schedule_list['activity'] = activity.name
                    schedules_array.append(schedule_list)

                place_json['schedules'] = schedules_array
            else:
                place_json['schedules'] = None

            schedules_array = []
            if schedules_next:
                for schedule in schedules_next:
                    schedule_list = {}
                    therapist = Therapists.objects.get(id=schedule.therapist.id)
                    activity = Activities.objects.get(id=schedule.activity.id)
                    schedule_list['id'] = schedule.id
                    schedule_list['date'] = schedule.date
                    schedule_list['start'] = schedule.start
                    schedule_list['end'] = schedule.end
                    schedule_list['therapist'] = therapist.name
                    schedule_list['activity'] = activity.name
                    schedules_array.append(schedule_list)

                place_json['schedules_next'] = schedules_array
            else:
                place_json['schedules_next'] = None
        else:
            place_json['status'] = False
            #place_json['nia'] = anggota.nia
            #place_json['nama'] = anggota.nama
            #place_json['wilayah'] = anggota.wilayah.pk

        data = json.dumps(place_json, indent=4, sort_keys=True, default=str)

    mimetype = "application/json"
    return HttpResponse(data, mimetype)

def index(request):
    return render(request, template_name='attendance/index.html')

def scanner(request):
    return render(request, 'attendance/scanner.html')


def qr_scan(request):
    pass

