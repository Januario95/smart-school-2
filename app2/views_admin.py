from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.contrib.auth.decorators import (
    login_required
)
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth import (
    authenticate, login as auth_login, logout
)

from app2.models import (
    SubjectName, SubjectMark, Turma, Classe, 
    Student, Teacher, Parent, Semester, 
)
from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel, 
    StudentNameNewModel, SubjectNewModel,
    SubjectTestsNewModel, TeacherSchoolAttended,
    SubjectNameNewModel, Year, SemesterModel, TeacherNameNewModel,
    StudentMessageAdmin, ParentToAdminMessage, AdminToParentsMessage, 
    AdminToTeacherMessage, Attendance, ParentNameNewModel,
    TimeTable, SubjectTimetable, TeacherClassAttendance,
    TeacherClassAttendance, TimeTableTurma, TimeTableDay,
)
from app2.forms import (
    CheckMarks, CheckMarksForTests, CheckTeacherForm,
    SearchStudentForm, LoginForm, UserForm,
    StudentStatisticsForms, StudentSchoolDetailsForm,
    SendMessageForm, SendMessageFormFather, SendMessageFormMother,
    SearchMessageForm, RegisterTeacherForm, TimeTableForm,
    TeacherAttendanceForm, RegisterTeacherSubjectForm,
    RegisterStudentForm, YearSemesterClasseTurmForm,
)

import json
import time
import datetime as dt
from datetime import datetime, timedelta


def navbar_view(request):
    return render(request,
                     'pages/admin/navbar_view.html')

def logout_page(request):
    logout(request)
    try:
        previous_path = request.META.get('HTTP_REFERER')
        return redirect(previous_path)
    except Exception as e:
        return redirect('/entrar/')


def login_page(request):
    message = None
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data['username']
                password = data['password']
                user = User.objects.filter(
                    username=username
                )
                # print(user)
                if user.exists():
                    # print('USER EXISTS')
                    user = user.first()
                    first_name = user.first_name
                    last_name = user.last_name
                    user = authenticate(
                        request,
                        username=username,
                        password=password
                    )
                    if user is not None:
                        auth_login(request, user)
                        # response = redirect('/')
                        previous_path = request.META.get('HTTP_REFERER')
                        return redirect(previous_path)
                        # print(response['Location'])
                        return response
                else:
                    print('USER DOES NOT EXIST')
                    message = 'Wrong username or password'
        else:
            form = LoginForm()

        return render(request,
                    'pages/auth/login.html',
                    {'form': form,
                    'message': message})


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/entrar/')
    else:
        user_exists = ''
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username, first_name, last_name, email, password, confirm_password, phone_number, location = data.values()
                user = User.objects.filter(
                    username=username,
                    email=email
                )
                print('PASSWORD=', confirm_password)
                if user.exists():
                    user_exists = 'Ja existe um usuario com este email. Cadastre-se com email diferente'
                else:
                    # user = User.objects.create(
                    # 	username=username,
                    # 	email=email,
                    # 	first_name=first_name,
                    # 	last_name=last_name
                    # )
                    # user.set_password(confirm_password)
                    # user.save()
                    # client = Client.objects.create(
                    # 	first_name=first_name,
                    # 	last_name=last_name,
                    # 	user=user,
                    # 	email=email,
                    # 	phone_number=phone_number,
                    # 	location=location
                    # )
                    # client.save()
                    return redirect('/')
            else:
                print(form.errors)
        else:
            form = UserForm()

    return render(request,
                  'pages/auth/register.html',
                  {'form': form,
                   'user_exists': user_exists})


@login_required
def profile_view(request):
    return render(request,
                    'pages/admin/profile.html')

@login_required
def home(request):
    if request.user.is_superuser:
        return redirect('/professores/')
    
    if request.user.is_staff:
        user = request.user
        teacher = user.teachernamenewmodel_set.first()
        print(teacher)
        return redirect(f'/professor-perfil/{ teacher.pk }/')
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

        return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})


@login_required
def get_subject_tests_api(request, pk, subject_name):
    test_names = []
    test_marks = []
    subject_names = []
    subject_avg_marks = []
    tests_avg = None
    average = None
    try:
        student = Student.objects.get(pk=pk)
        subject = SubjectName.objects.filter(name=subject_name)
        if subject.exists():
            try:
                subject = subject.first()
                subject = student.get_subject_tests(subject)
                subjects_test_marks = student.get_subjects_test_marks()
                average = student.get_average()
                vals = []
                # print(json.dumps(subjects_test_marks, indent=4, default=str))
                for row in subjects_test_marks:
                    # subject_names.append(row['subject']['name'])
                    # subject_avg_marks.append(row['tests_avg'])
                    vals.append((row['subject']['name'], row['tests_avg']))

                vals = sorted(vals, key=lambda x: x[1])
                for val in vals:
                    subject_names.append(val[0])
                    subject_avg_marks.append(val[1])

                tests = subject['tests']
                tests_avg = subject['tests_avg']
                for row in tests:
                    test_names.append(row.get('name').title())
                    test_marks.append(row.get('mark'))
            except Exception as e:
                print(e)
        else:
            subject = None
    except Student.DoesNotExist:
        subject = None

    return JsonResponse({
        'test_names': test_names,
        'test_marks': test_marks,
        'tests_avg': tests_avg,
        'subject_names': subject_names,
        'subject_avg_marks': subject_avg_marks,
        'average': average
    }) 


def get_test_marks_pos_neg(student_tests, subject_name):
    # print(student_tests)
    subj_test_1_pos = 0
    subj_test_1_neg = 0
    subj_test_2_pos = 0
    subj_test_2_neg = 0
    subj_test_3_pos = 0
    subj_test_3_neg = 0
    for tests in student_tests:
        row_data = []
        for row in tests:
            if row['name'] == 'test1':
                if row['mark'] >= 10:
                    subj_test_1_pos += 1
                else:
                    subj_test_1_neg += 1
            if row['name'] == 'test2':
                if row['mark'] >= 10:
                    subj_test_2_pos += 1
                else:
                    subj_test_2_neg += 1
            if row['name'] == 'test3':
                if row['mark'] >= 10:
                    subj_test_3_pos += 1
                else:
                    subj_test_3_neg += 1

    total_test_1 = (subj_test_1_pos + subj_test_1_neg)
    total_test_2 = (subj_test_2_pos + subj_test_2_neg)
    total_test_3 = (subj_test_3_pos + subj_test_3_neg)
    return {
        'subj_test_1_pos': (subj_test_1_pos * 100) / total_test_1,
        'subj_test_1_neg': (subj_test_1_neg * 100) / total_test_1,
        'subj_test_2_pos': (subj_test_2_pos * 100) / total_test_2,
        'subj_test_2_neg': (subj_test_2_neg * 100) / total_test_2,
        'subj_test_3_pos': (subj_test_3_pos * 100) / total_test_3,
        'subj_test_3_neg': (subj_test_3_neg * 100) / total_test_3,
        'subject_name': subject_name
    }
    # return {
    # 	'subj_test_1_pos': subj_test_1_pos,
    # 	'subj_test_1_neg': subj_test_1_neg,
    # 	'subj_test_2_pos': subj_test_2_pos,
    # 	'subj_test_2_neg': subj_test_2_neg,
    # 	'subj_test_3_pos': subj_test_3_pos,
    # 	'subj_test_3_neg': subj_test_3_neg,
    # 	'subject_name': subject_name
    # }


@login_required
def get_student_pass_fail_stats(request, semester, classe, turma):
    if not request.user.is_superuser:
        return JsonResponse({
            'message': 'Access denided'
        })
    else:
        passed_students = None
        failed_students = None
        passed_students_perc = None
        failed_students_perc = None
        student_pos_neg = None
        subject_tests_pos_neg = []
        try:
            turma = Turma.objects.get(name=turma)
            classe = Classe.objects.get(name=classe, turma=turma)
            students = Student.objects.filter(classe=classe)
            print(students.count())
            passed_students = 0
            failed_students = 0
            math_tests = []
            physics_tests = []
            chemistry_tests = []
            biology_tests = []
            biology_tests = []
            portuguese_tests = []
            geography_tests = []
            english_tests = []
            history_tests = []
            french_tests = []
            for student in students:
                # print(student)
                # print(json.dumps(student.serialize(), indent=4, default=str))
                maths = SubjectName.objects.get(name='Matematica')
                physics = SubjectName.objects.get(name='Fisica')
                chemistry = SubjectName.objects.get(name='Quimica')
                biology = SubjectName.objects.get(name='Biologia')
                portuguese = SubjectName.objects.get(name='Portugues')
                portuguese = SubjectName.objects.get(name='Portugues')

                geography = SubjectName.objects.get(name='Geografia')
                english = SubjectName.objects.get(name='Ingles')
                history = SubjectName.objects.get(name='Historia')
                french = SubjectName.objects.get(name='Frances')

                maths_pos_neg = student.get_subject_tests_pos_neg(maths)
                math_tests.append(maths_pos_neg)

                physics_pos_neg = student.get_subject_tests_pos_neg(physics)
                physics_tests.append(physics_pos_neg)

                chemistry_pos_neg = student.get_subject_tests_pos_neg(chemistry)
                chemistry_tests.append(chemistry_pos_neg)

                biology_pos_neg = student.get_subject_tests_pos_neg(biology)
                biology_tests.append(biology_pos_neg)

                portuguese_pos_neg = student.get_subject_tests_pos_neg(portuguese)
                portuguese_tests.append(portuguese_pos_neg)

                geography_pos_neg = student.get_subject_tests_pos_neg(geography)
                geography_tests.append(geography_pos_neg)

                english_pos_neg = student.get_subject_tests_pos_neg(english)
                english_tests.append(english_pos_neg)

                history_pos_neg = student.get_subject_tests_pos_neg(history)
                history_tests.append(history_pos_neg)

                french_pos_neg = student.get_subject_tests_pos_neg(french)
                french_tests.append(french_pos_neg)

                avg = student.get_average()
                if avg >= 10:
                    passed_students += 1
                else:
                    failed_students += 1
            total = passed_students + failed_students
            passed_students_perc = (passed_students * 100) / total
            failed_students_perc = (failed_students * 100) / total
            # print(json.dumps(math_tests, indent=4, default=str))

            math_tests_marks = get_test_marks_pos_neg(math_tests, 'Matematica')
            physics_tests_marks = get_test_marks_pos_neg(physics_tests, 'Fisica')
            chemistry_tests_marks = get_test_marks_pos_neg(chemistry_tests, 'Quimica')
            biology_tests_marks = get_test_marks_pos_neg(biology_tests, 'Biologia')
            portuguese_tests_marks = get_test_marks_pos_neg(portuguese_tests, 'Portugues')
            geography_tests_marks = get_test_marks_pos_neg(geography_tests, 'Geografia')
            english_tests_marks = get_test_marks_pos_neg(english_tests, 'Ingles')
            history_tests_marks = get_test_marks_pos_neg(history_tests, 'Historia')
            french_tests_marks = get_test_marks_pos_neg(french_tests, 'Frances')
            subject_tests_pos_neg = [
                math_tests_marks, physics_tests_marks,
                chemistry_tests_marks, biology_tests_marks, portuguese_tests_marks,
                geography_tests_marks, english_tests_marks, history_tests_marks,
                french_tests_marks
            ]

        except Exception as e:
            print(e.args)
            pass

        return JsonResponse({
            'passed_students': passed_students,
            'failed_students': failed_students,
            'passed_students_perc': passed_students_perc,
            'failed_students_perc': failed_students_perc,
            'subject_tests_pos_neg': subject_tests_pos_neg
        })


def get_daily_timetable_data(data, index):
    return [row[index] for row in data]

def get_slots(start_times, end_times, index):
    return [slot[index] for slot in [start_times, end_times]]

def create_day_timetable(timetable, day, subject, start_slot, end_slot):
    timetable_day = TimeTableDay.objects.create(
        class_start_time=start_slot,
        class_end_time=end_slot,
        day=day,
        subject=subject
    )
    timetable_day.save()
    timetable.days.add(timetable_day)
    timetable.save()

@require_POST
@login_required
def add_timetable_api(request):
    post_data = json.loads(request.body)
    # print(post_data)
    data = post_data.get('data')
    school_data = post_data.get('schoolData')
    
    year = Year.objects.get(year=school_data.get('year'))
    new_semester = SemesterNewModel.objects.get(
        name=school_data.get('semester'))
    classe = ClasseNewModel.objects.get(
        name=school_data.get('classe')
    )
    turma = TurmaNewModel.objects.get(
        name=school_data.get('turma')
    )
    semester = SemesterModel.objects.create(
        year=year,
        name=new_semester,
        classe=classe,
        turma=turma
    )
    semester.save()
    timetable = TimeTableTurma.objects.create(
        semester=semester
    )
    timetable.save()

    class_start_time_slotes = get_daily_timetable_data(data, 0)
    class_end_time_slotes = get_daily_timetable_data(data, 1)
    monday_data = get_daily_timetable_data(data, 2)
    tuesday_data = get_daily_timetable_data(data, 3)
    wednesday_data = get_daily_timetable_data(data, 4)
    thurday_data = get_daily_timetable_data(data, 5)
    friday_data = get_daily_timetable_data(data, 6)
    all_days = [monday_data, tuesday_data, wednesday_data,
                thurday_data, friday_data]
    slot1 = get_slots(class_start_time_slotes, class_end_time_slotes, 0)
    slot2 = get_slots(class_start_time_slotes, class_end_time_slotes, 1)
    slot3 = get_slots(class_start_time_slotes, class_end_time_slotes, 2)
    slot4 = get_slots(class_start_time_slotes, class_end_time_slotes, 3)
    slot5 = get_slots(class_start_time_slotes, class_end_time_slotes, 4)
    slot6 = get_slots(class_start_time_slotes, class_end_time_slotes, 5)
    
    for day, day_data in zip(['2ª Feira', '3ª Feira', '4ª Feira',
                               '5ª Feira', '6ª Feira'], all_days):
        print(day, len(day_data))
        for index, subject in enumerate(day_data):
            slot = get_slots(class_start_time_slotes, class_end_time_slotes, index)
            subject = SubjectNameNewModel.objects.get(name=subject)
            create_day_timetable(timetable, day, subject, slot[0], slot[1])

    return JsonResponse({
        'class_start_time_slotes': class_start_time_slotes,
        'class_end_time_slotes': class_end_time_slotes,
        'monday_data': monday_data,
        'tuesday_data': tuesday_data,
        'wednesday_data': wednesday_data,
        'thurday_data': thurday_data,
        'friday_data': friday_data
    })


@login_required
def timetable_view(request):
    if request.user.is_superuser:
        subjects = []
        timetable_data = []
        timetable_data_exists = False
        if request.method == 'POST':
            form = YearSemesterClasseTurmForm(request.POST)
            if form.is_valid():  
                inner_data = form.cleaned_data
                # print(inner_data)
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                ) 
                # print(new_semester)
                for semester in new_semester:
                    # new_semester = new_semester.first()
                    timetable = TimeTableTurma.objects.filter(
                        semester=semester
                    )
                    subjects = SubjectNameNewModel.objects.all()
                    subjects = [subj.name for subj in subjects]
                    if timetable.exists():
                        timetable = timetable.first()
                        days = timetable.days.all()
                        days = days.order_by('class_end_time')
                        index = 0
                        for _ in range(6):
                            day_data = days[index:index+5]
                            row_data = {}
                            first_row = day_data[0]
                            row_data['class_start_time'] = first_row.class_start_time
                            row_data['class_end_time'] = first_row.class_end_time
                            for row in day_data:
                                row = row.serialize()
                                day = row.get('day').replace('ª', '').replace(' ', '_')
                                row_data[day] = row.get('subject')

                            timetable_data.append(row_data)
                            timetable_data_exists = True
                            index += 5
            else: 
                print(form.errors)
        else:
            form = YearSemesterClasseTurmForm()
      
        return render(request,
                      'pages/admin/timetable_view.html',
                      {'form': form, 'subjects': subjects, 'timetable_data': timetable_data,
                       'timetable_data_exists': timetable_data_exists})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})



@login_required
def timetable_view_2(request):
    if request.user.is_superuser:
        subjects = []
        timetable_data = []
        timetable_data_exists = False
        if request.method == 'POST':
            form = YearSemesterClasseTurmForm(request.POST)
            if form.is_valid():  
                inner_data = form.cleaned_data
                # print(inner_data)
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                ) 
                # print(new_semester)
                for semester in new_semester:
                    # new_semester = new_semester.first()
                    timetable = TimeTableTurma.objects.filter(
                        semester=semester
                    )
                    subjects = SubjectNameNewModel.objects.all()
                    subjects = [subj.name for subj in subjects]
                    if timetable.exists():
                        timetable = timetable.first()
                        days = timetable.days.all()
                        days = days.order_by('class_end_time')
                        index = 0
                        for _ in range(6):
                            day_data = days[index:index+5]
                            row_data = {}
                            first_row = day_data[0]
                            row_data['class_start_time'] = first_row.class_start_time
                            row_data['class_end_time'] = first_row.class_end_time
                            for row in day_data:
                                row = row.serialize()
                                day = row.get('day').replace('ª', '').replace(' ', '_')
                                row_data[day] = row.get('subject')

                            timetable_data.append(row_data)
                            timetable_data_exists = True
                            index += 5
            else: 
                print(form.errors)
        else:
            form = YearSemesterClasseTurmForm()
      
        return render(request,
                      'pages/admin/timetable_view.html',
                      {'form': form, 'subjects': subjects, 'timetable_data': timetable_data,
                       'timetable_data_exists': timetable_data_exists})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def timetable_add(request):
    if request.user.is_superuser:
        class_length = list(range(1, 7))
        subjects = SubjectNameNewModel.objects.all()
        if request.method == 'POST':
            form = YearSemesterClasseTurmForm(request.POST)
            if form.is_valid(): 
                inner_data = form.cleaned_data
                print(inner_data)
            else: 
                print(form.errors)
        else:
            form = YearSemesterClasseTurmForm()
 
        return render(request,
                      'pages/admin/timetable_add.html',
                      {'form': form, 'class_length': class_length, 'subjects': subjects})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def get_semester_marks_api(request, semester_name, student_pk, year, classe, turma):
    student = StudentNameNewModel.objects.get(pk=student_pk)
    
    year = Year.objects.get(year=year)
    semester_name = SemesterNewModel.objects.get(name=semester_name)
    classe = ClasseNewModel.objects.get(name=classe)
    turma = TurmaNewModel.objects.get(name=turma)
    new_semester = SemesterModel.objects.filter(
        name=semester_name,
        year=year,
        classe=classe,
        turma=turma
    )
    new_semester = new_semester.first()
    # print(new_semester)

    stud_semesters = student.new_semester.all()
    data = []
    test_names = []
    data_exists = False
    media_values = []
    subjects_ = []
    for sem in stud_semesters:
        if sem.name == new_semester.name:
            subjects = sem.subjects.all()
            for subj in subjects:
                row = {'subject_name': subj.name.name}
                i = 1
                medias = []
                for test in subj.tests.all():
                    test_name = test.name.replace(' ', '_')
                    row[f'test_name_{i}'] = test.name
                    row[f'test_mark_{i}'] = test.mark
                    medias.append(test.mark)
                    if test.name not in test_names:
                        test_names.append(test.name)
                    i += 1
                media = round(sum(medias) / len(medias), 1)
                row['media'] = media
                media_values.append(float(media))
                subjects_.append(subj.name.name)
                data.append(row)
                data_exists = True
    
    subj_marks = []
    for subj, media in zip(subjects_, media_values):
        row = [subj, media]
        subj_marks.append(row)
    subj_marks = sorted(subj_marks, key=lambda val: val[1])
    subjects_for_bar_chart = []
    marks_for_bar_chart = []
    for subj, mark in subj_marks:
        subjects_for_bar_chart.append(subj)
        marks_for_bar_chart.append(mark)

    media_final = 0
    if media_values:
        media_final = round(sum(media_values) / len(media_values), 1)

    return JsonResponse({
        'data': data,
        'data_exists': data_exists,
        'test_names': test_names,
        'media_values': media_values,
        'subjects': subjects_,
        'media_final': media_final,
        'subjects_for_bar_chart': subjects_for_bar_chart,
        'marks_for_bar_chart': marks_for_bar_chart
    })

@login_required
def student_academic_performance(request, pk):
    try:
        student = StudentNameNewModel.objects.get(pk=pk)
        # print(json.dumps(student.serialize(), default=str, indent=4))
    except Student.DoesNotExist:
        student = None

    semesters_ = []
    year_ = None
    if request.method == 'POST':
        form = StudentSchoolDetailsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            year_ = year
            year = Year.objects.filter(year=year)
            
            if year.exists():
                year = year.first()
                semesters = SemesterModel.objects.filter(
                    year=year
                )
                
                stud_semesters = student.new_semester.all()
                for semest in stud_semesters:
                    if semest in semesters:
                        semesters_.append(semest)
                    else:
                        pass
        else:
            print(form.errors)
    else:
        form = StudentSchoolDetailsForm()
        
    return render(request,
                  'pages/admin/student_academic_performance.html',
                  {'student': student, 'form': form, 'semesters': semesters_,
                      'year': year_})

@login_required
def student_school_details(request, pk):
    semesters = []
    semesters_ = []
    try:
        student = StudentNameNewModel.objects.get(pk=pk)
        # print(student.order_by('year'))
        # student = student.order_by('year')
        # teachers = Teacher.objects.filter(classe=student.classe)
        # subject_teachers = []
        semesters = student.new_semester.all()
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        form = StudentSchoolDetailsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            year = Year.objects.filter(year=year)
            
            if year.exists():
                year = year.first()
                # print(year)
                semesters = SemesterModel.objects.filter(
                    year=year
                )
                
                # print(len(semesters))
                stud_semesters = student.new_semester.all()
                semesters_ = []
                for semest in stud_semesters:
                    if semest in semesters:
                        # print(semest.pk)
                        semesters_.append(semest)

                # print([sem.pk for sem in semesters_])
        else:
            print(form.errors)
    else:
        form = StudentSchoolDetailsForm()
        
    return render(request,
                  'pages/admin/student_school_details.html',
                  {'form': form, 'student': student, 'semesters': semesters_})


def get_semester_attendance(data):
    subjects = SubjectNameNewModel.objects.all()
    subjects = [subj.name for subj in subjects]
    values = {}
    # values['subjects'] = subjects
    is_present_vals = []
    is_not_present_vals = []
    subjects_ = []
    for subj in subjects:
        subj_data = [val for val in data if val[0] == subj]
        is_present = 0
        is_not_present = 0
        for val in subj_data:
            if val[1] == True:
                is_present += 1
            else:
                is_not_present += 1
        subjects_.append(subj)
        is_present_vals.append(is_present)
        is_not_present_vals.append(is_not_present)

        values['subjects'] = subjects_
        values['is_present_vals'] = is_present_vals
        values['is_not_present_vals'] = is_not_present_vals
    return values




@login_required
def get_semester_attendance_api(request, semester_name, student_pk, year, classe, turma):
    student = StudentNameNewModel.objects.get(pk=student_pk)

    year = Year.objects.get(year=year)
    semester_name = SemesterNewModel.objects.get(name=semester_name)
    classe = ClasseNewModel.objects.get(name=classe)
    turma = TurmaNewModel.objects.get(name=turma)
    new_semester = SemesterModel.objects.filter(
        name=semester_name,
        year=year,
        classe=classe,
        turma=turma
    )
    new_semester = new_semester.first()
    # print(new_semester)

    attendances = Attendance.objects.filter(
        student=student,
        semester=new_semester,
    )
    # print(attendances)
    data = []
    data_exists = False
    for attendance in attendances:
        data.append([attendance.subject.name, attendance.is_present])
        data_exists = True
    # print(data)
    data_ = get_semester_attendance(data)

    return JsonResponse({
        'data': data_,
        'data_exists': data_exists
    })


@login_required
def get_attendance(request, semester_pk, teacher_pk, student_pk, subject_pk,
                      semester_year, semester_classe, semester_turma):
    data = []
    days_attended = 0
    days_missed = 0
    try:
        year = Year.objects.get(year=semester_year)
        classe = ClasseNewModel.objects.get(name=semester_classe)
        turma = TurmaNewModel.objects.get(name=semester_turma)
        semester = SemesterModel.objects.filter(
            year=year,
            classe=classe,
            turma=turma
        )
        semester = semester.first()
        teacher = TeacherNameNewModel.objects.get(pk=teacher_pk)
        student = StudentNameNewModel.objects.get(pk=student_pk)
        subject = SubjectNameNewModel.objects.get(pk=subject_pk)
        subject_name = subject.name
        attendances = Attendance.objects.filter(
            teacher=teacher,
            student=student,
            subject=subject,
            semester=semester,
        )
        print(attendances)
        for att in attendances:
            if att.is_present:
                days_attended += 1
            if not att.is_present:
                days_missed += 1
            data.append(att.serialize())
        
        print(attendances)
    except Exception as e:
        print(e.args)
        attendance = None
        subject_name = ''

    return JsonResponse({
        'data': data,
        'days_attended': days_attended,
        'days_missed': days_missed,
        'subject_name': subject_name
    })


@login_required
def get_semester(request, pk):
    data = []
    try:
        current_semester = SemesterModel.objects.get(pk=pk)
        new_semester = SemesterModel.objects.filter(
            name=current_semester.name, 
            year=current_semester.year, 
            turma=current_semester.turma, 
            classe=current_semester.classe
        )
        teachers = TeacherNameNewModel.objects.filter(new_semester__in=new_semester)
        # print(teachers)
        new_semester = new_semester.first()
        for teacher in teachers:
            row = {
                'teacher_pk': teacher.pk,
                'teacher_first_name': teacher.first_name,
                'teacher_last_name': teacher.last_name
            }
            teacher_current_sem = [sem for sem in teacher.new_semester.all() if 
              sem.name == current_semester.name]
            # print(teacher_current_sem)
            for sem in teacher_current_sem:
                teacher_subjects = sem.subjects.all()
                print(teacher_subjects)
                for index, subj in enumerate(teacher_subjects, start=1):
                    row[f'subject'] = f'{subj.name}'
                    sub = SubjectNameNewModel.objects.get(name=subj.name.name)
                    row['subject_pk'] = sub.pk
                print(row)
            data.append(row)

    except Exception as e:
        print(e.args)
        current_semester = None

    return JsonResponse({
        'data': data
    })



@login_required
def student_parents_details(request, pk):
    try:
        student = StudentNameNewModel.objects.get(pk=pk)
        parents = student.parents.all()
        father = parents[0]
        mother = parents[1]
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':		
        if 'form1' in request.POST:
            father_phone_number = request.POST['father_phone_number']
            father_message = request.POST['father_message']
            print(f'father_phone_number = {father_phone_number}, father_message = {father_message}')
            parent = ParentNameNewModel.objects.filter(phone_number=father_phone_number)
            print(parent)
            if parent.exists():
                parent = parent.first()

                sender = request.user
                receiver = parent
                message = AdminToParentsMessage.objects.create(
                    sender=sender,
                    receiver=receiver,
                    message=father_message
                )
                message.save()
                print(message)
    
        if 'form2' in request.POST:
            mother_phone_number = request.POST['mother_phone_number']
            mother_message = request.POST['mother_message']
            print(f'mother_phone_number = {mother_phone_number}, mother_message = {mother_message}')
            parent = ParentNameNewModel.objects.filter(phone_number=mother_phone_number)
            if parent.exists():
                parent = parent.first()

                sender = request.user
                receiver = parent
                message = AdminToParentsMessage.objects.create(
                    sender=sender,
                    receiver=receiver,
                    message=mother_message
                )
                message.save()
                print(message)

        form = SendMessageFormFather(initial={
            'father_phone_number': father.phone_number
        })
        form2 = SendMessageFormMother(initial={
            'mother_phone_number': mother.phone_number
        })
    else:
        form = SendMessageFormFather(initial={
            'father_phone_number': father.phone_number
        })
        form2 = SendMessageFormMother(initial={
            'mother_phone_number': mother.phone_number
        })

    return render(request,
                  'pages/admin/student_parents_details.html',
                  {'student': student, 'form': form, 'form2': form2})


@login_required
def student_details_api(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        student = None

    if student is not None:
        student = student.serialize()

    return JsonResponse({
        'student': student
    })


@login_required
def teacher_details(request, pk):
    try:
        teacher = TeacherNameNewModel.objects.get(pk=pk)
    except Teacher.DoesNotExist:
        teacher = None

    # if teacher is not None:
    # 	teacher = teacher.serialize()

    return render(request,
                  'pages/admin/teacher_details.html',
                  {'teacher': teacher})

@login_required
def teacher_details_api(request, pk):
    try:
        teacher = Teacher.objects.get(pk=pk)
    except Teacher.DoesNotExist:
        teacher = None

    if teacher is not None:
        teacher = teacher.serialize()

    return JsonResponse({
        'teacher': teacher
    })

@login_required
def pesquisar_estudante(request):
    students_ = []
    student = None
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SearchStudentForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                # classe = data.get('classe')
                students = Student.objects.filter(
                    first_name=first_name
                )
                if students.exists():
                    if last_name != '':
                        students = students.filter(
                            last_name=last_name)
                else:
                    students = Student.objects.filter(
                        last_name=last_name
                    )

                # students = Student.objects.filter(
                # 	(Q(first_name=first_name) |
                # 	Q(last_name=first_name))
                # 	# & Q(grade=grade)
                # )
                for stud in students:
                    student = stud.serialize()
                    students_.append(student)
                print(json.dumps(student, indent=4, default=str))
            else:
                print(form.errors)
        else:
            form = SearchStudentForm()

        return render(request,
                      'pages/admin/pesquisar_estudante.html',
                      {'form': form, 'students': students_})

    message = 'Acesso negado. Nao tem permissao para ver essa pagina'
    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def student_list_details(request):
    data = []
    is_student_list = False
    turma = None
    classe = None
    year_name = None
    semester_name = None
    turma_name = None
    classe_name = None
    gender_name = None
    if request.user.is_superuser:
        students_ = []
        student = None
        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                gender_name = gender
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                # print(new_semester.count())
                students = StudentNameNewModel.objects.filter(
                        new_semester__in=new_semester
                )
                if gender == 'masculino':
                    students = students.filter(
                        gender='male'
                    )
                elif gender == 'feminino':
                    students = students.filter(
                        gender='female'
                    )
                students = students.order_by('first_name')
                # print([stud.gender for stud in students])
                students_ = []
                # print(students.count())
                for stud in students:
                    students_.append(stud.serialize_basic_info())
            else:
                print(form.errors)	
        else:
            form = CheckTeacherForm()
  
        return render(request,
                    'pages/admin/student_list_details.html',
                    {'form': form, 'students': students_,
                    'student': student, 'is_student_list': is_student_list,
                    'turma': turma, 'classe': classe, 'year_name': year_name,
                    'classe_name': classe_name, 'gender_name': gender_name,
                    'semester_name': semester_name, 'turma_name': turma_name})

    print('Non-superuser trying to access student-list-details')
    message = 'Acesso negado. Nao tem permissao para ver essa pagina'
    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def student_details(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        student = None
    return render(request,
                  'pages/admin/student_details.html',
                  {'student': student})

@login_required
def student_personal_details(request, pk):
    try:
        student = StudentNameNewModel.objects.get(pk=pk)
        messages = StudentMessageAdmin.objects.filter(
            sender=request.user,
            receiver=student
        )
        messages = messages.order_by('-sent_at')
    except Student.DoesNotExist:
        student = None
        messages = []

    today = None

    if request.method == 'POST':
        if 'search-message' in request.POST:
            date = request.POST['date']
            year, month, day = date.split('-')
            today = dt.date(int(year), int(month), int(day))
            tomorow = today + timedelta(days=1)
            messages = messages.filter(Q(sent_at__gte=today) & Q(sent_at__lte=tomorow))
            today = today.strftime('%d de %m de %Y')
        if 'send-message' in request.POST:
            text_message = request.POST['message']

            sender = request.user
            receiver = student
            message = StudentMessageAdmin.objects.create(
                sender=sender,
                receiver=receiver,
                message=text_message
            )
            message.save()
            
    form = SendMessageForm(initial={
        'phone_number': student.phone_number
    })
    form2 = SearchMessageForm()
        
    return render(request,
                  'pages/admin/student_personal_details.html',
                  {'student': student, 'messages': messages, 'form': form, 'form2': form2,
                      'today': today})

@login_required
def presenca_de_estudantes(request):
    if request.user.is_superuser:
        students_ = []
        student = None
        subject = None
        student_data = []
        subject_names = []
        subject_names_ = []
        nr_of_subjects = 0
        year_name = None
        semester_name = None
        turma_name = None
        classe_name = None
        gender_name = None

        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                gender_name = gender
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                # print(year, semester, classe, turma)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                # print(new_semester)
                students = StudentNameNewModel.objects.filter(new_semester__in=new_semester)
                # print(students)
                semester = new_semester.first()
                # print(semester.year, semester.name, semester.classe, semester.turma)
                # print(semester, end=' ')
                subject_names = [subj.name.name for subj in semester.subjects.all()]
                for subject_name in subject_names:
                    nr_of_subjects += 1

                students = students.order_by('first_name')
                if gender == 'masculino':
                    students = students.filter(
                        gender='male'
                    )
                elif gender == 'feminino':
                    students = students.filter(
                        gender='female'
                    )
                for student in students:
                    # print(student.attendance_set.count())
                    semester_attendance = Attendance.objects.filter(
                        semester=semester
                    )
                    # print(semester_attendance)
                    attendances = Attendance.objects.filter(
                        student=student,
                        semester=semester
                    )
                    # print(semester, end=' ')
                    # print(attendances)
                    # print()
                    # subject_names = [subj.name.name for subj in semester.subjects.all()]
                    row = {'student_name': student.fullname()}
                    row['student_pk'] = student.pk
                    for subject_name in subject_names:
                        row[f'{subject_name}'] = {'is_present': 0, 'is_not_present': 0}

                    is_present = 0
                    is_not_present = 0
                    for attendance in attendances:
                        if attendance.is_present:
                            is_present += 1
                            row[f'{attendance.subject.name}']['is_present'] += 1
                        else:
                            is_not_present += 1
                            row[f'{attendance.subject.name}']['is_not_present'] += 1
                    row['is_present'] = is_present
                    row['is_not_present'] = is_not_present
                    # print(row)
                    # print('')
                    student_data.append(row)

                for subject_name in subject_names:
                    row = {'subject': subject_name}
                    subject_names_.append(row)
                nr_of_subjects *= 2
                nr_of_subjects += 2
            else:
                print(form.errors)
        else:
            form = CheckTeacherForm()
    
        return render(request,
                    'pages/admin/presenca_de_estudantes.html',
                    {'form': form, 'student_data': student_data, 'subject_names': subject_names,
                       'nr_of_subjects': nr_of_subjects, 'subject_names_': subject_names_,
                     'year_name': year_name, 'classe_name': classe_name, 'gender_name': gender_name,
                     'semester_name': semester_name, 'turma_name': turma_name})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def notas_de_estudantes_tests(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                print(inner_data)
                gender = inner_data.get('gender')
                gender_name = gender
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                # print(year, semester, classe, turma)
                new_semester = SemesterModel.objects.filter(
                    year=year,
                    name=semester,
                    classe=classe,
                    turma=turma,
                )  
                # print(new_semester)
                students = StudentNameNewModel.objects.filter(
                    new_semester__in=new_semester
                )
                print(students)
            else:
                print(form.errors)
        else:
            form = CheckTeacherForm()

        return render(request,
                      'pages/admin/notas_de_estudantes_tests.html',
                      {'form': form})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})

  
@login_required
def notas_de_estudantes_page(request):
    if request.user.is_superuser:
        students = []
        students_ = []
        subject_names = SubjectNameNewModel.objects.all()
        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                gender_name = gender
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                # print(year, semester, classe, turma)
                new_semester = SemesterModel.objects.filter(
                    year=year,
                    name=semester,
                    classe=classe,
                    turma=turma,
                )
                # print(new_semester)
                students = StudentNameNewModel.objects.filter(
                    new_semester__in=new_semester
                )
                if new_semester.exists(): 
                    new_semester = new_semester.first()
                
                for student in students:
                    row = {
                        'fullname': student.fullname()
                    }
                    student_semesters = student.new_semester.all()
                    for stud_sem in student_semesters:
                        if (stud_sem.year == new_semester.year and 
                            stud_sem.name == new_semester.name and
                            stud_sem.classe == new_semester.classe and
                            stud_sem.turma == new_semester.turma):
                            subjects = stud_sem.subjects.all()
                            tests_marks = {}
                            for subj in subjects:
                                tests = subj.tests.all()
                                row_ = {
                                    'ACS_1': 0,
                                    'ACS_2': 0,
                                    'ACS_3': 0
                                }
                                for test in tests:
                                    row_[test.name.replace(' ', '_')] = test.mark
                                row[f'{subj}'] = row_
                                # row[f'{subj}'] = [dict(test.name=test.mark) ]
                                # print(subj, ':', [dict(name=test.name.replace(' ', '_'), mark=test.mark) for test in tests])
                    print(row)
                    students_.append(row)
            else:
                print(form.errors)
        else: 
            form = CheckTeacherForm()

        tests = ['1', '2', '3']
        nr_of_subjects = subject_names.count() * len(tests)
  
        return render(request,
                      'pages/admin/notas_de_estudantes_page.html',
                      {'form': form, 'students': students_, 'tests': tests,
                       'subject_names': subject_names, 'nr_of_subjects': nr_of_subjects})
    else: 
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,   
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
# @cache_page(60*15)
def notas_de_estudantes(request):
    student = 'Yes'
    students_ = None
    subjects_names = []
    nr_of_subjects = 0
    new_semester = []
    semester_data = []
    year_name = None
    turma_name = None
    gender_name = None
    classe_name = None
    semester_name = None
    if request.user.is_superuser:
        students_ = []
        student = None
        subject = None

        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                gender_name = gender
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                # print(year, semester, classe, turma)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                # print(new_semester.count())
                for sem in new_semester:
                    sem_stud = sem.studentnamenewmodel_set.all()
                    # print(sem_stud.count())
                    if sem_stud.count():
                        semester_stud = sem_stud.first()
                        nr_of_subjects = sem.get_nr_of_subjects()
                        subjects_names = sem.get_subjects_names()
                        media_values = sem.get_semester_averages()
                        media_values.update({'student_name': semester_stud.fullname()})
                        media_values.update({'student_id': semester_stud.pk})
                        media_values.update({'student_fullname': semester_stud.fullname()})
                        media_values.update({'student_final_avg': sem.get_semester_final_avg()})
                        semester_data.append(media_values)
                    else:
                        pass

                students = StudentNameNewModel.objects.filter(
                        new_semester__in=new_semester
                )
                if gender == 'masculino':
                    students = students.filter(
                        gender='male'
                    )
                elif gender == 'feminino':
                    students = students.filter(
                        gender='female'
                    )
                students = students.order_by('first_name')
                students_ = []
                for stud in students:
                    students_.append(stud.serialize_basic_info())
            else:
                print(form.errors)	
        else:
            form = CheckTeacherForm()

        semester_data = sorted(semester_data, key=lambda val: val['student_fullname'])
        
        return render(request,
                      'pages/admin/notas_de_estudantes.html',
                      {'form': form, 'student': student,
                       'students': students_, 'subject': subject,
                       'subjects_names': subjects_names, 'nr_of_subjects': nr_of_subjects,
                       'new_semester': new_semester, 'semester_data': semester_data,
                       'year_name': year_name, 'turma_name': turma_name,
                       'gender_name': gender_name, 'classe_name': classe_name,
                       'semester_name': semester_name})

    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def ver_notas_de_tests(request):
    student = 'Yes'
    students_ = None
    if request.user.is_superuser:
        students_ = []
        student = None
        subject = None
        if request.method == 'POST':
            form = CheckMarksForTests(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                print(inner_data)
                turma = inner_data.get('turma')
                subject = inner_data.get('subject')
                classe = Classe.objects.filter(
                    name=inner_data.get('classe'),
                    turma=turma)
                if classe.exists():
                    classe = classe.first()
                    students = Student.objects.filter(
                        classe=classe
                    )
                    for stud in students:
                        # subject_tests = student.get_subject_tests(subject)
                        # student = student.serialize()
                        # student['subject_tests'] = subject_tests
                        student = stud.serialize_tests(subject)
                        students_.append(student)
                    print(json.dumps(student, indent=4, default=str))
        else:
            form = CheckMarksForTests()

        return render(request,
                      'pages/admin/ver_notas_de_tests.html',
                      {'form': form, 'student': student,
                       'students': students_, 'subject': subject})

    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})



def student_self_registration(request):
    student_exists = False
    student = None
    message = None
    same_password = None
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            inner_data = form.cleaned_data
            # print(inner_data)
            username= inner_data.get('username')
            password = inner_data.get('password')
            confirm_password = inner_data.get('confirm_password')
            email = inner_data.get('email')
            first_name = inner_data.get('first_name')
            last_name = inner_data.get('last_name')
            numero_de_bi = inner_data.get('ic_number')
            gender = inner_data.get('gender')
            # print(gender)
            birth_date = inner_data.get('birth_date')
            phone_number = inner_data.get('phone_number')
            province = inner_data.get('province')
            city = inner_data.get('city')
            bairro = inner_data.get('bairro')
            
            if password != confirm_password:
                message = 'Passwords nao sao iguais.'
                same_password = True
            else:
                student = StudentNameNewModel.objects.filter(email=email)
                if student.exists():
                    student_exists = True
                    student = student.first()
                    message = 'Estudante com esse email ja existe. Use outro email.'
                else:
                    if gender == 'masculino':
                        student_gender = 'male'
                    else:
                        student_gender = 'female'
                    student = StudentNameNewModel.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        numero_de_bi=numero_de_bi,
                        gender=student_gender,
                        birth_date=birth_date,
                        phone_number=phone_number,
                        email=email,
                        province=province,
                        city=city,
                        bairro=bairro,
                    )
                    student.save()

                    user = User.objects.create(username=username)
                    user.set_password(password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.is_staff = False
                    user.save()
                    # print(user)
                    student.user = user
                    student.save()

                    year = inner_data.get('year')
                    year = Year.objects.get(year=year)
                    turma = inner_data.get('turma')
                    turma = TurmaNewModel.objects.get(name=turma)
                    classe = inner_data.get('classe')
                    classe = ClasseNewModel.objects.get(name=classe)
                    semester = inner_data.get('semester')
                    semester = SemesterNewModel.objects.get(name=semester)
                    subjects = inner_data.get('subjects')

                    new_semester = SemesterModel.objects.create(
                        name=semester,
                        turma=turma,
                        classe=classe,
                        year=year
                    )
                    student.new_semester.add(new_semester)
                    student.save()

                    for subj in subjects:
                        subj = SubjectNameNewModel.objects.get(name=subj)
                        subject = SubjectTestsNewModel.objects.create(
                            name=subj
                        ) 
                        subject.save()
                        new_semester.subjects.add(subject)
                        new_semester.save()

                    father = ParentNameNewModel.objects.create(
                        email = inner_data.get('father_email'),
                        first_name = inner_data.get('father_first_name'),
                        last_name = inner_data.get('father_last_name'),
                        numero_de_bi = inner_data.get('father_ic_number'),
                        # gender = 'Male',
                        phone_number = inner_data.get('father_phone_number'),
                        job_title=inner_data.get('father_profession'),
                        province = inner_data.get('father_province'),
                        city = inner_data.get('father_city'),
                        bairro = inner_data.get('father_bairro')
                    )
                    father.gender = 'male'
                    father.save()
                    student.parents.add(father)
                    student.save()


                    mother = ParentNameNewModel.objects.create(
                        email = inner_data.get('mother_email'),
                        first_name = inner_data.get('mother_first_name'),
                        last_name = inner_data.get('mother_last_name'),
                        numero_de_bi = inner_data.get('mother_ic_number'),
                        # gender = 'Female',
                        phone_number = inner_data.get('mother_phone_number'),
                        job_title=inner_data.get('mother_profession'),
                        province = inner_data.get('mother_province'),
                        city = inner_data.get('mother_city'),
                        bairro = inner_data.get('mother_bairro')
                    )
                    mother.gender = 'female'
                    mother.save()
                    student.parents.add(mother)
                    student.save()
                    message = f'A conta para {student.fullname()} foi criada com sucesso.'
        else:
            print(form.errors)
    else:
        form = RegisterStudentForm()

    return render(request,
                'pages/admin/student_self_registration.html',
                {'form': form, 'student_exists': student_exists, 'student': student,
                'message': message, 'same_password': same_password})


@login_required
def register_student(request):
    if request.user.is_superuser:
        message = None
        same_password = False
        student_exists = False
        student = None
        if request.method == 'POST':
            form = RegisterStudentForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                username= inner_data.get('username')
                password = inner_data.get('password')
                confirm_password = inner_data.get('confirm_password')
                email = inner_data.get('email')
                first_name = inner_data.get('first_name')
                last_name = inner_data.get('last_name')
                numero_de_bi = inner_data.get('ic_number')
                gender = inner_data.get('gender')
                # print(gender)
                birth_date = inner_data.get('birth_date')
                phone_number = inner_data.get('phone_number')
                province = inner_data.get('province')
                city = inner_data.get('city')
                bairro = inner_data.get('bairro')
                
                if password != confirm_password:
                    message = 'Passwords nao sao iguais.'
                    same_password = True
                else:
                    student = StudentNameNewModel.objects.filter(email=email)
                    if student.exists():
                        student_exists = True
                        student = student.first()
                        message = 'Estudante com esse email ja existe. Use outro email.'
                    else:
                        if gender == 'masculino':
                            student_gender = 'male'
                        else:
                            student_gender = 'female'
                        user = User.objects.create(username=username)
                        user.set_password(password)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email
                        user.save()
  
                        student = StudentNameNewModel.objects.create(
                            user=user,
                            first_name=first_name,
                            last_name=last_name,
                            numero_de_bi=numero_de_bi,
                            gender=student_gender,
                            birth_date=birth_date,
                            phone_number=phone_number,
                            email=email,
                            province=province,
                            city=city,
                            bairro=bairro,
                        )
                        student.save()

                        year = inner_data.get('year')
                        year = Year.objects.get(year=year)
                        turma = inner_data.get('turma')
                        turma = TurmaNewModel.objects.get(name=turma)
                        classe = inner_data.get('classe')
                        classe = ClasseNewModel.objects.get(name=classe)
                        semester = inner_data.get('semester')
                        semester = SemesterNewModel.objects.get(name=semester)
                        new_semester = SemesterModel.objects.filter(
                            name=semester,
                            turma=turma,
                            classe=classe,
                            year=year
                        )
                        if new_semester.exists():
                            new_semester = new_semester.first()
                        else:
                            new_semester = SemesterModel.objects.create(
                                name=semester,
                                turma=turma,
                                classe=classe,
                                year=year
                            )
                        student.new_semester.add(new_semester)
                        student.save()

                        father = ParentNameNewModel.objects.create(
                            email = inner_data.get('father_email'),
                            first_name = inner_data.get('father_first_name'),
                            last_name = inner_data.get('father_last_name'),
                            numero_de_bi = inner_data.get('father_ic_number'),
                            # gender = 'Male',
                            phone_number = inner_data.get('father_phone_number'),
                            job_title=inner_data.get('father_profession'),
                            province = inner_data.get('father_province'),
                            city = inner_data.get('father_city'),
                            bairro = inner_data.get('father_bairro')
                        )
                        father.gender = 'male'
                        father.save()
                        student.parents.add(father)
                        student.save()


                        mother = ParentNameNewModel.objects.create(
                            email = inner_data.get('mother_email'),
                            first_name = inner_data.get('mother_first_name'),
                            last_name = inner_data.get('mother_last_name'),
                            numero_de_bi = inner_data.get('mother_ic_number'),
                            # gender = 'Female',
                            phone_number = inner_data.get('mother_phone_number'),
                            job_title=inner_data.get('mother_profession'),
                            province = inner_data.get('mother_province'),
                            city = inner_data.get('mother_city'),
                            bairro = inner_data.get('mother_bairro')
                        )
                        mother.gender = 'female'
                        mother.save()
                        student.parents.add(mother)
                        student.save()
                        message = f'A conta para {student.fullname()} foi criada com sucesso. <a href="#">Ver detalhes</a>'
            else:
                print(form.errors)
        else:
            form = RegisterStudentForm()

        return render(request,
                    'pages/admin/register_student.html',
                    {'form': form, 'student_exists': student_exists, 'student': student,
                    'message': message, 'same_password': same_password})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})




@login_required
def get_all_students_in_a_year(request, year_name):
    classes = ClasseNewModel.objects.all()
    year = Year.objects.filter(year=year_name)
    try:
        first_year = year.first()
        classe_names = [classe.name for classe in classes]
        # print(classe_names)

        total_male = 0
        total_female = 0
        all_males = []
        all_females = []
        data = []
        for classe in classes:
            row = {}
            row['classe'] = classe.name
            new_semester = SemesterModel.objects.filter(
                year=first_year, classe=classe)
            if new_semester.exists():
                new_semester_ = new_semester.first()

            students = StudentNameNewModel.objects.filter(
                new_semester__in=new_semester
            )
            row['classe'] = classe.name
            total_students = 0
            male_count = 0
            female_count = 0
            for student in students:
                total_students += 1
                if student.gender == 'male':
                    male_count += 1
                if student.gender == 'female':
                    female_count += 1
            row['male_count'] = male_count
            row['female_count'] = female_count
            all_males.append(male_count)
            all_females.append(female_count)
            row['total_male_female'] = male_count + female_count
            total_male += male_count
            total_female += female_count
            data.append(row)
        total = total_male + total_female
    except Exception as e:
        print(e.args)
 
    return JsonResponse({
        'data': data,
        'total_male': total_male,
        'total_female': total_female,
        'all_males': all_males,
        'all_females': all_females,
        'total': total,
        'classe_names': classe_names
    })



@login_required
def all_students(request):
    form = CheckTeacherForm()
    students = StudentNameNewModel.objects.all()
    # print(students.count())

    return render(request,
                     'pages/admin/all_students.html',
                  {'students': students, 'form': form})

@login_required
def lista_de_estudantes(request):
    # if request.user.is_authenticated:
    # 	user = request.user
    # 	stud = Student.objects.filter(
    # 		first_name=user.first_name,
    # 		last_name=user.last_name)
    # 	if stud.exists():
    # 		return redirect(f'/perfil/{user.username}/notas/')
    # 	else:
    # 		teacher = Teacher.objects.filter(
    # 			first_name=user.first_name,
    # 			last_name=user.last_name)
    # 		if teacher.exists():
    # 			pass

    student = None
    data = []
    is_student_list = False
    turma = None
    classe = None
    students_ = []
    semester_name = None
    turma_name = None
    classe_name = None
    year_name = None
    gender_name = None
    is_authenticated = request.user.is_authenticated
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                # print(new_semester.count())
                students = StudentNameNewModel.objects.filter(
                        new_semester__in=new_semester
                )
                if gender == 'masculino':
                    students = students.filter(
                        gender='male'
                    )
                    gender_name = 'Homens'
                elif gender == 'feminino':
                    students = students.filter(
                        gender='female'
                    )
                    gender_name = 'Mulheres'
                students = students.order_by('first_name')
                # print([stud.gender for stud in students])
                students_ = []
                # print(students.count())
                for stud in students:
                    students_.append(stud.serialize_basic_info())
                    # print(json.dumps(stud.serialize_basic_info(), indent=4))
            else:
                print(form.errors)
        else:
            form = CheckTeacherForm()

        return render(request,
                      'pages/admin/lista_de_estudantes.html',
                      {'form': form, 'students': data,
                       'student': student, 'is_student_list': is_student_list,
                       'turma': turma, 'classe': classe, 'new_students': students_,
                       'semester_name': semester_name, 'turma_name': turma_name,
                       'classe_name': classe_name, 'year_name': year_name,
                       'gender_name': gender_name})

    message = 'Acesso negado. Nao tem permissao para ver essa pagina'
    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})

@login_required
def teacher_add_subject(request, pk):
    try:
        teacher = TeacherNameNewModel.objects.get(pk=pk)
        semesters =  teacher.new_semester.all()
        # print(semesters)
    except TeacherNameNewModel.DoesNotExist:
        teacher = None
        semesters = None

    subject_added = False
    semester_exists = None

    if request.method == 'POST':
        form = RegisterTeacherSubjectForm(request.POST)
        if form.is_valid():
            inner_data = form.cleaned_data
            # print(inner_data)
            academic_year = inner_data.get('academic_year')
            year_name = academic_year
            year = Year.objects.get(year=academic_year)
            turma = inner_data.get('turma')
            turma_name = turma
            turma = TurmaNewModel.objects.get(name=turma)
            subject_name = inner_data.get('subject')
            subject = SubjectNameNewModel.objects.get(name=subject_name)
            classe = inner_data.get('classe')
            classe_name = classe
            classe = ClasseNewModel.objects.get(name=classe)
            semester = inner_data.get('semester')
            semester_name = semester
            semester = SemesterNewModel.objects.get(name=semester)
            new_semester = SemesterModel.objects.filter(
                name=semester,
                turma=turma,
                classe=classe,
                year=year
            )
            # print(new_semester.count())
            if new_semester.exists():
                new_semester = new_semester.first()
            else:
                new_semester = SemesterModel.objects.create(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                new_semester.save()

            teacher_sem = teacher.new_semester.all()
            print(teacher_sem)
            semester_exists_ = False
            if teacher_sem:
                for sem in teacher_sem:
                    if (sem.year == new_semester.year and sem.name == new_semester.name and 
                        sem.classe == new_semester.classe and sem.turma == new_semester.turma):
                        subjects = sem.subjects.all()
                        subjects = [subj.name for subj in subjects]
                        semester_exists_ = True
                        if subject not in subjects:
                            subject_test = SubjectTestsNewModel.objects.create(name=subject)
                            subject_test.save()

                            sem.subjects.add(subject_test)
                            sem.save()
                            teacher.new_semester.add(sem)
                            teacher.save()
                            print(f'ADDING SUBJECT {subject!r} TO EXISTING SEMESTER')
                            semester_exists = f'Professor {teacher.fullname().upper()} foi registado para lecionar {subject_name} na {classe_name} turma {turma_name}, do {semester_name} semestre de {year_name}'
                    teacher_sem = teacher.new_semester.all()
                if not semester_exists_:
                    subject_test = SubjectTestsNewModel.objects.create(name=subject)
                    subject_test.save()

                    new_semester = SemesterModel.objects.create(
                        name=semester,
                        turma=turma,
                        classe=classe,
                        year=year
                    ) 
                    new_semester.save()

                    new_semester.subjects.add(subject_test)
                    new_semester.save()
                    teacher.new_semester.add(new_semester)
                    teacher.save()
                    print(f'CREATING SUBJECT {subject!r} TO NEW SEMESTER')  
            else:
                subject_test = SubjectTestsNewModel.objects.create(name=subject)
                subject_test.save()

                new_semester.subjects.add(subject_test)
                new_semester.save()
                teacher.new_semester.add(new_semester)
                teacher.save()
                print(f'CREATING SUBJECT {subject!r} - NEW SEMESTER')
                semester_exists = f'Professor {teacher.fullname().upper()} foi registado para lecionar {subject_name} na {classe_name} turma {turma_name}, do {semester_name} semestre de {year_name}'
            semesters = teacher.new_semester.all()
        else:
            print(form.errors)
    else:
        form = RegisterTeacherSubjectForm()

    return render(request,
                     'pages/admin/teacher_add_subject.html',
                  {'teacher': teacher, 'semesters': semesters, 'form': form,
                     'semester_exists': semester_exists})


@login_required
def register_teacher_subject(request, teacher_pk):
    try:
        teacher = TeacherNameNewModel.objects.get(pk=teacher_pk)

        if request.method == 'POST':
            form = RegisterTeacherSubjectForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                print(inner_data)
            else:
                print(form.errors)
        else:
            form = RegisterTeacherSubjectForm()

        return render(request,
                'pages/admin/register_teacher_subject.html',
                {'form': form, 'teacher': teacher})
    except Exception as e:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'
        return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})

@login_required
def admin_regiser_student_subject(request):
    message = None
    if request.user.is_superuser:
        if request.method == 'POST':
            form = RegisterTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                print(inner_data)
            else:
                print(form.errors)
        else:
            form = RegisterTeacherForm()

            return render(request,
                        'pages/admin/admin_regiser_student_subject.html',
                    {'form': form})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def register_teacher(request):
    message = None
    same_password = False
    teacher_exists = False
    start_date_is_after_end_date = False
    if request.user.is_superuser:
        if request.method == 'POST':
            form = RegisterTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                print(inner_data)
                username= inner_data.get('username')
                password = inner_data.get('password')
                confirm_password = inner_data.get('confirm_password')
                email = inner_data.get('email')
                first_name = inner_data.get('first_name')
                last_name = inner_data.get('last_name')
                numero_de_bi = inner_data.get('ic_number')
                gender = inner_data.get('gender')
                birth_date = inner_data.get('birth_date')
                phone_number = inner_data.get('phone_number')
                province = inner_data.get('province')
                city = inner_data.get('city')
                bairro = inner_data.get('bairro')

                university = inner_data.get('university')
                degree = inner_data.get('degree')
                curso = inner_data.get('curso')
                country_of_study = inner_data.get('country_of_study')
                city_of_study = inner_data.get('city_of_study')
                study_start_date = inner_data.get('study_start_date')
                study_end_date = inner_data.get('study_end_date')

                year = inner_data.get('year')
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = SemesterNewModel.objects.get(name=semester)
                semester = SemesterModel.objects.create(
                    name=semester_name,
                    year=year,
                    classe=classe,
                    turma=turma,
                )
                semester.save()

                school = TeacherSchoolAttended.objects.create(
                    name=university,
                    degree=degree,
                    major=curso,
                    city=city_of_study,
                    country=country_of_study,
                    start_date=study_start_date,
                    end_date=study_end_date
                )
                school.save()

                has_errors = False
                study_start_date = inner_data.get('study_start_date')
                study_end_date = inner_data.get('study_end_date')
                if study_start_date > study_end_date:
                    start_date_is_after_end_date = True
                    has_errors = True
                    message = 'Data de inicio do curso deve ser antes da data de termino do curso'

                elif password != confirm_password:
                    message = 'Passwords nao sao iguais.'
                    same_password = True
                    has_errors = True

                if not has_errors:
                    teacher = TeacherNameNewModel.objects.filter(email=email)
                    if teacher.exists():
                        teacher_exists = True
                        teacher = teacher.first()
                        message = 'Professor com esse email ja existe. Use outro email.'
                    else:
                        user = User.objects.create(username=username)
                        user.set_password(password)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = email
                        user.is_staff = True
                        user.save()
                        print(user)

                        if gender == 'masculino':
                            student_gender = 'male'
                        else:
                            student_gender = 'female'
                        teacher = TeacherNameNewModel.objects.create(
                            user=user,
                            first_name=first_name,
                            last_name=last_name,
                            numero_de_bi=numero_de_bi,
                            gender=student_gender,
                            birth_date=birth_date,
                            phone_number=phone_number,
                            email=email,
                            province=province,
                            city=city,
                            bairro=bairro
                        )
                        teacher.new_semester.add(semester)
                        teacher.school_attended.add(school)
                        teacher.save()
                        print(teacher)
                        return redirect(f'/professores-adicionar-disciplina/{ teacher.pk }/')
            else:
                print(form.errors)
        else:
            form = RegisterTeacherForm()

        return render(request,
                    'pages/admin/register_teacher.html',
                    {'form': form, 'teacher_exists': teacher_exists,
                    'message': message, 'same_password': same_password,
                    'start_date_is_after_end_date': start_date_is_after_end_date})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def ver_list_de_professores(request):
    message = None
    teachers_ = []
    semester_name = None
    turma_name = None
    classe_name = None
    year_name = None
    gender_name = None
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name = semester
                semester = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                # print(new_semester.count())
                teachers = TeacherNameNewModel.objects.filter(
                        new_semester__in=new_semester
                )
                if gender == 'masculino':
                    teachers = teachers.filter(
                        gender='male'
                    )
                    gender_name = 'Homens'
                elif gender == 'feminino':
                    teachers = teachers.filter(
                        gender='female'
                    )
                    gender_name = 'Mulheres'
                teachers = teachers.order_by('first_name')
                # print([stud.gender for stud in teachers])
                teachers_ = []
                # print(teachers.count())
                for stud in teachers:
                    stud_info = stud.serialize_basic_info()
                    if stud_info not in teachers_:
                        teachers_.append(stud_info)
            else:
                print(form.errors)
        else:
            form = CheckTeacherForm()

        return render(request,
                      'pages/admin/lista_de_professores.html',
                      {'teachers': teachers_,
                       'form': form, 'semester_name': semester_name, 'turma_name': turma_name,
                        'classe_name': classe_name, 'year_name': year_name,
                        'gender_name': gender_name})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def teacher_personal_details(request, pk):
    try:
        teacher = TeacherNameNewModel.objects.get(pk=pk)
        messages = AdminToTeacherMessage.objects.filter(
            sender=request.user,
            receiver=teacher
        )
        messages = messages.order_by('-sent_at')
    except Student.DoesNotExist:
        teacher = None
        messages = []

    today = None

    if request.method == 'POST':
        if 'search-message' in request.POST:
            date = request.POST['date']
            year, month, day = date.split('-')
            today = dt.date(int(year), int(month), int(day))
            tomorow = today + timedelta(days=1)
            messages = messages.filter(Q(sent_at__gte=today) & Q(sent_at__lte=tomorow))
            today = today.strftime('%d de %m de %Y')
        if 'send-message' in request.POST:
            text_message = request.POST['message']

            sender = request.user
            receiver = teacher
            message = AdminToTeacherMessage.objects.create(
                sender=sender,
                receiver=receiver,
                message=text_message
            )
            message.save()
            
    form = SendMessageForm(initial={
        'phone_number': teacher.phone_number
    })
    form2 = SearchMessageForm()
        
    return render(request,
                  'pages/admin/teacher_personal_details.html',
                  {'teacher': teacher, 'messages': messages, 'form': form, 'form2': form2,
                      'today': today})


@login_required
def teacher_list_details(request):
    data = []
    is_student_list = False
    turma = None
    classe = None
    teachers_ = []
    if request.user.is_superuser:
        students_ = []
        student = None
        if request.method == 'POST':
            form = CheckTeacherForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                gender = inner_data.get('gender')
                year = inner_data.get('year')
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                # print(new_semester.count())
                teachers = TeacherNameNewModel.objects.filter(
                        new_semester__in=new_semester
                )
                if gender == 'masculino':
                    teachers = teachers.filter(
                        gender='male'
                    )
                elif gender == 'feminino':
                    teachers = teachers.filter(
                        gender='female'
                    )
                teachers = teachers.order_by('first_name')
                # print([stud.gender for stud in students])
                # print(students.count())
                teachers_ = []
                for stud in teachers:
                    teacher_info = stud.serialize_basic_info()
                    if teacher_info not in teachers_:
                        teachers_.append(teacher_info)
            else:
                print(form.errors)	
        else:
            form = CheckTeacherForm()

        return render(request,
                    'pages/admin/teacher_list_details.html',
                    {'form': form, 'teachers': teachers_,
                    'is_student_list': is_student_list,
                    'turma': turma, 'classe': classe})

    message = 'Acesso negado. Nao tem permissao para ver essa pagina'
    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})


@login_required
def get_teacher_semester_info(request, semester_name, year, classe, turma):	
    year = Year.objects.get(year=year)
    semester_name = SemesterNewModel.objects.get(name=semester_name)
    classe = ClasseNewModel.objects.get(name=classe)
    turma = TurmaNewModel.objects.get(name=turma)
    new_semester = SemesterModel.objects.filter(
        name=semester_name,
        year=year,
        classe=classe,
        turma=turma
    )
    students = StudentNameNewModel.objects.filter(
        new_semester__in=new_semester
    )
    # print(students.count())
    new_semester = new_semester.first()
    # print(new_semester)

    students_ = []
    for student in students:
        students_.append(student.serialize_basic_info())

    return JsonResponse({
        'students': students_
    })


@login_required
def teacher_timetables(request):
    timetable = []
    year_name = None
    semester_name = None
    turma_name = None
    classe_name = None
    all_classes = []
    if request.method == 'POST':
        form = TimeTableForm(request.POST)
        if form.is_valid():
            inner_data = form.cleaned_data
            # print(inner_data)
            year = inner_data.get('year')
            year_name = year
            year = Year.objects.get(year=year)
            turma = inner_data.get('turma')
            turma_name = turma
            turma = TurmaNewModel.objects.get(name=turma)
            classe = inner_data.get('classe')
            classe_name = classe
            classe = ClasseNewModel.objects.get(name=classe)
            semester = inner_data.get('semester')
            semester_name = semester
            semester = SemesterNewModel.objects.get(name=semester)
            timetable = TimeTable.objects.filter(
                turma=turma,
                classe=classe,
                semester=semester,
                year=year
            )
            if timetable.exists():
                timetable = timetable.first()
                subjects = timetable.subjects.all()
                monday_classes = []
                tuesday_classes = []
                wednesday_classes = []
                thursday_classes = []
                friday_classes = []
                for subject in subjects:
                    if subject.class_day == '2ª Feira':
                        monday_classes.append(subject)
                    if subject.class_day == '3ª Feira':
                        tuesday_classes.append(subject)
                    if subject.class_day == '4ª Feira':
                        wednesday_classes.append(subject)
                    if subject.class_day == '5ª Feira':
                        thursday_classes.append(subject)
                    if subject.class_day == '6ª Feira':
                        friday_classes.append(subject)
                
                all_classes = [monday_classes, tuesday_classes, wednesday_classes,
                                  thursday_classes, friday_classes]
                # print(all_classes)
            else:
                timetable = []
    else:
        form = TimeTableForm()

    return render(request,
                     'pages/admin/teacher_timetables.html',
                  {'form': form, 'timetable': timetable, 'year_name': year_name,
                    'classe_name': classe_name,  'semester_name': semester_name,
                    'turma_name': turma_name, 'all_classes': all_classes})


@login_required
def capture_teacher_attendance_api(request, teacher_pk, class_date, class_time, attended,
                                      classe_name, turma_name, subject_name):
    attendance_exists = False
    teacher_name = None
    try:
        teacher = TeacherNameNewModel.objects.get(pk=teacher_pk)
        teacher_name = teacher.fullname()
        classe = ClasseNewModel.objects.get(name=classe_name)
        turma = TurmaNewModel.objects.get(name=turma_name)
        subject = SubjectNameNewModel.objects.get(name=subject_name)
        attendance = TeacherClassAttendance.objects.filter(
            teacher=teacher,
            classe=classe,
            turma=turma,
            subject=subject,
            class_date=class_date,
            class_time=class_time
        )
        # print(attendance)
        attended = int(attended)
        if attended == 1:
            attended = True
        if attended == 0:
            attended = False

        if attendance.exists():
            attendance_exists = True
            attendance = attendance.first()
            # if attended == 1:
            # 	attendance.attended = True
            # if attended == 0:
            attendance.attended = attended
            # attendance.class_time = class_time
            attendance.save()
        else:
            attendance = TeacherClassAttendance.objects.create(
                teacher=teacher,
                classe=classe,
                turma=turma,
                subject=subject,
                class_date=class_date,
                class_time=class_time,
                attended=attended
            )
            attendance.save()
            # print(attendance)
    except Exception as e:
        print(e.args)

    return JsonResponse({
        'attendance_exists': attendance_exists,
        'teacher_name': teacher_name
    })



@login_required
def teacher_attendance_take(request):
    if request.user.is_superuser:
        teachers_ = []
        turma_name = None
        classe_name = None
        semester_name_ = None
        year_name = None
        if request.method == 'POST':
            form = TimeTableForm(request.POST)
            if form.is_valid():
                inner_data = form.cleaned_data
                # print(inner_data)
                year = inner_data.get('year')
                year_name = year
                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name_ = semester
                semester_name = SemesterNewModel.objects.get(name=semester)
                new_semester = SemesterModel.objects.filter(
                    name=semester_name,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                teachers = TeacherNameNewModel.objects.filter(
                    new_semester__in=new_semester
                )

                new_semester = new_semester.first()
                for teacher in teachers:
                    row = {
                        'pk': teacher.pk,
                        'fullname': teacher.fullname()
                    }
                    sems = teacher.new_semester.all()
                    for sem in sems:
                        if sem.name ==new_semester.name:
                            subjects = [subj.name.name for subj in sem.subjects.all()]
                            row['subjects'] = subjects

                    attendances = teacher.teacherclassattendance_set.all()
                    today = dt.datetime.today()
                    for attendance in attendances:
                        if attendance.class_date == today:
                            print(attendance)
                    teachers_.append(row)
                # print(teachers_)
            else:
                print(form.errors)
        else:
            form = TimeTableForm()

        return render(request,
                    'pages/admin/teacher_attendance_take.html',
                    {'form': form, 'teachers': teachers_, 'turma_name': turma_name,
                       'classe_name': classe_name, 'semester_name': semester_name_,
                     'year_name': year_name})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})

@login_required
def teacher_attendance_check(request):
    if request.user.is_superuser:
        teachers_ = []
        turma_name = None
        classe_name = None
        semester_name_ = None
        year_name = None
        attendances = []
        attendances_exists = False
        if request.method == 'POST':
            form = TeacherAttendanceForm(request.POST)
            if form.is_valid(): 
                inner_data = form.cleaned_data
                print(inner_data)
                year = inner_data.get('year')
                year_name = year
                month = inner_data.get('month')
                # print(month)
                dates = []
                if month != '0':
                    for day in range(1, 32):
                        try:
                            date = dt.date(year=int(year), month=int(month), day=day)
                            dates.append(date)
                        except Exception as e:
                            pass

                year = Year.objects.get(year=year)
                turma = inner_data.get('turma')
                turma_name = turma
                turma = TurmaNewModel.objects.get(name=turma)
                classe = inner_data.get('classe')
                classe_name = classe
                classe = ClasseNewModel.objects.get(name=classe)
                semester = inner_data.get('semester')
                semester_name_ = semester
                semester_name = SemesterNewModel.objects.get(name=semester)
                from_ = inner_data.get('from_')
                to_ = inner_data.get('to_')
                new_semester = SemesterModel.objects.filter(
                    name=semester_name,
                    turma=turma,
                    classe=classe,
                    year=year
                )
                teachers = TeacherNameNewModel.objects.filter(
                    new_semester__in=new_semester
                )
                # print(teachers)
                for teacher in teachers:
                    attendance = TeacherClassAttendance.objects.filter(
                        teacher=teacher,
                        turma=turma,
                        classe=classe
                    )  
                    attendance = attendance.filter(
                        Q(class_date__gte=from_) & Q(class_date__lte=to_)
                    )
                    # attendance = teacher.teacherclassattendance_set.all()
                    # print(attendance.count())
                    # if dates: 
                    #     attendance = attendance.filter(class_date__in=dates)
                    attendances.append(attendance)
                     
                if len(attendance) > 0: 
                    attendances_exists = True
            else: 
                print(form.errors)
        else:
            form = TeacherAttendanceForm()
        return render(request,
                    'pages/admin/teacher_attendance_check.html',
                    {'form': form, 'attendances': attendances,
                     'attendances_exists': attendances_exists})

    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})

@login_required
def teacher_attedances_page(request):
    if request.user.is_superuser:
        return render(request,
                      'pages/admin/teacher_attedances_page.html')
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})

@login_required
def teacher_subject_info_api(request, semesterPk, teacherPk, semesterYear, 
                              semesterName, semesterClasse, semesterTurma):
    try:
        semester = SemesterModel.objects.get(pk=semesterPk)
        teacher = TeacherNameNewModel.objects.get(pk=teacherPk)
        teacher_semeters = teacher.new_semester.all()
        subjects = []
        for sem in teacher_semeters:
            if sem.name == semester.name:
                # print(f'{sem.name} - EQUAL')
                subjects = [subj.name.name for subj in sem.subjects.all()]
            else:
                pass
                # print(f'{sem.name} - DIFFERENT')

        year = Year.objects.get(year=semesterYear)
        semester_name = SemesterNewModel.objects.get(name=semesterName)
        classe = ClasseNewModel.objects.get(name=semesterClasse)
        turma = TurmaNewModel.objects.get(name=semesterTurma)
        new_semester = SemesterModel.objects.filter(
            name=semester_name,
            turma=turma,
            classe=classe,
            year=year
        )
        # print(new_semester)
        students = StudentNameNewModel.objects.filter(
            new_semester__in=new_semester
        )
        nr_male = 0
        nr_female = 0
        for student in students:
            if student.gender == 'male':
                nr_male += 1
            elif student.gender == 'female':
                nr_female += 1
        total_students = nr_male + nr_female
        print(total_students)
        
    except SemesterModel.DoesNotExist:
        semester = []
        subjects = []
        nr_male = 0
        nr_female = 0
        total_students = 0

    return JsonResponse({
        'subjects': subjects,
        'nr_male': nr_male,
        'nr_female': nr_female,
        'total_students': total_students
    })


@login_required
def teacher_subject_details(request, pk):
    semesters = []
    semesters_ = []
    year_name = None
    try:
        teacher = TeacherNameNewModel.objects.get(pk=pk)
        semesters =  teacher.new_semester.all()
        # print(semesters)
    except TeacherNameNewModel.DoesNotExist:
        teacher = None
        semesters = None

    if request.method == 'POST':
        form = StudentSchoolDetailsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            year_name = year
            year = Year.objects.filter(year=year)
            # print(year)
            
            if year.exists():
                year = year.first()
                semesters = SemesterModel.objects.filter(
                    year=year
                )
                # print(semesters)
                if semesters.exists():
                    new_semester = semesters.first()
                
                    teacher_semesters = teacher.new_semester.all()
                    # print(teacher_semesters)
                    semesters_ = []
                    for semest in teacher_semesters:
                        if semest not in semesters_:
                            if new_semester.year == semest.year:
                                semesters_.append(semest)
        else:
            print(form.errors)
    else:
        form = StudentSchoolDetailsForm()

    return render(request,
                     'pages/admin/teacher_subject_details.html',
                  {'teacher': teacher, 'semesters': semesters_, 'form': form,
                      'year_name': year_name})



@login_required
def teacher_school_details(request, pk):
    semesters = []
    semesters_ = []
    year_name = None
    try:
        teacher = TeacherNameNewModel.objects.get(pk=pk)
        semesters = teacher.new_semester.all()
    except Student.DoesNotExist:
        teacher = None

    if request.method == 'POST':
        form = StudentSchoolDetailsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            year_name = year
            year = Year.objects.filter(year=year)
            print(year)
            
            if year.exists():
                year = year.first()
                # print(year)
                semesters = SemesterModel.objects.filter(
                    year=year
                )
                # print(len(semesters))
                if semesters.exists():
                    new_semester = semesters.first()
                
                    teacher_semesters = teacher.new_semester.all()
                    print(teacher_semesters)
                    semesters_ = []
                    for semest in teacher_semesters:
                        if semest not in semesters_:
                            if new_semester.year == semest.year:
                                semesters_.append(semest)
        else:
            print(form.errors)
    else:
        form = StudentSchoolDetailsForm()
        
    return render(request,
                  'pages/admin/teacher_school_details.html',
                  {'form': form, 'teacher': teacher, 'semesters': semesters_,
                      'year_name': year_name})


@login_required
def ver_por_turma(request):
    if request.user.is_superuser:
        user = request.user
        # stud = Student.objects.filter(
        # 	first_name=user.first_name,
        # 	last_name=user.last_name)
        # if stud.exists():
        # 	return redirect(f'/perfil/{user.username}/notas/')
        # else:
        # 	teacher = Teacher.objects.filter(
        # 		first_name=user.first_name,
        # 		last_name=user.last_name)
        # 	if teacher.exists():
        # 		pass

        students = None
        students_ = None
        student = None
        message = None
        students_ = []
        if request.user.is_staff:
            if request.method == 'POST':
                form = CheckMarks(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    print(data)
                    name = data['classe']
                    turma = data['turma']
                    try:
                        classe = Classe.objects.get(
                            name=name,
                            turma=turma
                        )
                        students = Student.objects.filter(
                            classe=classe)
                        if students.exists():
                            for stud in students:
                                student = stud.serialize()
                                students_.append(student)
                                # print(json.dumps(student, indent=4, default=str))
                            # print(json.dumps(student, indent=4, default=str))
                    except Classe.DoesNotExist:
                        pass
                else:
                    print(form.errors)
            else:
                form = CheckMarks()

            return render(request,
                          'pages/admin/ver_por_turma.html',
                          {'form': form, 'student': student,
                           'students': students_})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina'

    return render(request,
                      'pages/auth/unauthorized.html',
                      {'message': message})







