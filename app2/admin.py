from django.contrib import admin
from django.utils.safestring import mark_safe

# from .models import (
# 	SubjectName, SubjectMark, Turma, 
#     Classe, Test,
# 	Student, Teacher, Parent, Semester,
# )
from .models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel,
    TestNewModel, StudentNameNewModel, SubjectNewModel,
    SubjectNameNewModel, Year, SemesterModel, SubjectTestsNewModel,
    ParentNameNewModel, TeacherNameNewModel, StudentMessageAdmin,
    ParentToAdminMessage, AdminToParentsMessage, AdminToTeacherMessage,
    Attendance, SubjectTimetable, TimeTable, 
    TeacherClassAttendance, TeacherSchoolAttended, StudentAttendance,
    AttendanceQRcode, TeacherAndStudentMessage, TimeTableDay,
    TimeTableTurma,
)


@admin.register(TimeTableTurma)
class TimeTableTurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester')

@admin.register(TimeTableDay)
class TimeTableDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'subject', 'class_start_time', 'class_end_time')

@admin.register(TeacherAndStudentMessage)
class TeacherAndStudentMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at', 'resent_at')

@admin.register(AttendanceQRcode)
class AttendanceQRcodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'teacher', 'year', 'semester', 'classe', 'turma',
                    'subject', 'class_datetime', 'attended', 'comment')

@admin.register(TeacherSchoolAttended)
class TeacherSchoolAttendedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'country', 'degree',
                    'major', 'start_date', 'end_date')

@admin.register(TeacherClassAttendance)
class TeacherClassAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'turma', 'classe', 'subject',
                    'class_date', 'class_time', 'attended')
    # filter_horizontal = ('teacher',) # msust be many-to-many
    list_filter = ('turma', 'classe')
    list_editable = ('class_date', 'class_time')

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma', 'classe', 'year', 'semester')

@admin.register(SubjectTimetable)
class SubjectTimetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'class_day', 'class_start_time', 'class_end_time')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'student', 'semester', 'reason', 'is_present', 'class_time')

@admin.register(AdminToTeacherMessage)
class AdminToTeacherMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')

@admin.register(AdminToParentsMessage)
class AdminToParentMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')

@admin.register(ParentToAdminMessage)
class ParentToAadminMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')

@admin.register(StudentMessageAdmin)
class StudentMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')
    # list_editable = ('message',)
    # search_fields = ('receiver',)

@admin.register(SubjectTestsNewModel)
class SubjectTestsNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link_is_open')
    list_editable = ('link_is_open',)
    list_per_page = 700

@admin.register(SemesterModel)
class SemesterModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'turma', 'classe', 'year', 'created_at', 'updated_at')
    list_per_page = 700

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')

@admin.register(SemesterNewModel)
class SemesterNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year')
	

@admin.register(ClasseNewModel)
class ClasseNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
@admin.register(TurmaNewModel)
class TurmaNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(TestNewModel)
class TestNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mark')
    list_per_page = 700

@admin.register(SubjectNewModel)
class SubjectNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'turma', 'classe', 'semester')
    list_per_page = 700
    list_filter = ('turma', 'classe', 'semester')

@admin.register(SubjectNameNewModel)
class SubjectNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 700

@admin.register(StudentNameNewModel)
class StudentNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 
                    'profile_pic_',
                    'numero_de_bi',
                    'gender', 'birth_date', 'phone_number', 'email',
                    'province', 'city', 'bairro',
                    # 'turma', 'classe', 'semester', 
                    'year_', 'created_at', 'updated_at')
    # list_filter = ('turma', 'classe', 'semester')
    list_display_links = ('id', 'first_name')
    list_per_page = 700

    def profile_pic_(self, obj):
        profile_pic = obj.profile_pic
        img = mark_safe(f'''
            <img src="/media/{ profile_pic }" style="width:100px;height:100px;border-radius:50%;" />
        ''')
        return img
    profile_pic_.short_description = 'Image de perfil'


    def year_(self, obj):
        years = obj.year.all()
        ol = '<ol>'
        for year in years:
            ol += f'<li>{year}</li>'
        ol += '</li>'
        return mark_safe(ol)
    year_.short_description = 'Year'


@admin.register(TeacherNameNewModel)
class TeacherNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 
                    'profile_pic_',
                    'gender', 
                    'phone_number', 'email',
                    'province', 'city', 'bairro', 'created_at', 'updated_at')
    list_display_links = ('id', 'first_name')
    list_per_page = 700
    list_filter = ('gender',)
    # list_editable = ('subjects',)

    def profile_pic_(self, obj):
        profile_pic = obj.profile_pic
        img = mark_safe(f'''
            <img src="/media/{ profile_pic }" style="width:100px;height:100px;border-radius:50%;" />
        ''')
        return img
    profile_pic_.short_description = 'Image de perfil'


@admin.register(ParentNameNewModel)
class ParentNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'gender', 
                    'phone_number', 'email', 'job_title',
                    'province', 'city', 'bairro', 'created_at', 'updated_at')
    list_per_page = 700
    list_filter = ('gender',)

















# @admin.register(Semester)
# class SemesterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'classe', 'year')


# @admin.register(Test)
# class TestAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name', 'mark')

# @admin.register(Turma)
# class TurmaAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name')


# @admin.register(SubjectName)
# class SubjectNameAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'year')
#     # list_editable = ('name',)

# @admin.register(SubjectMark)
# class SubjectMarkAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'subject')


# @admin.register(Classe)
# class ClasseAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name', 'turma')
# 	# list_editable = ('turma',)


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name',
#     				'numero_de_bi', 'gender', 'birth_date',
#     				'phone_number_', 'email_', 'province', 'city', 'bairro', 
#     				'quarteirao', 'father_name', 'mother_name', 'classe',
#     				'turma', 'semester', 'subjects_')
#     list_filter = ('gender', 'classe')
#     list_per_page = 25
#     # inlines = [
#     #     Inline,
#     # ]
#     # raw_id_fields = ('',)
#     # readonly_fields = ('',)
#     search_fields = ('first_name', 'last_name')

#     def email_(self, obj):
#     	email = obj.email
#     	return mark_safe(f'''
#     		<a href="mailto:{email}">{email}</a>
#     	''')
#     email_.short_descriptin = 'Email'

#     def phone_number_(self, obj):
#     	phone_number = obj.phone_number
#     	return mark_safe(f'''
#     		<a href="tel:{phone_number}">{phone_number}</a>
#     	''')
#     phone_number_.short_descriptin = 'Phone number'

#     def subjects_(self, obj):
#     	subjects = obj.subjects.all()
#     	li = '<ol>'
#     	for subj in subjects:
#     		li += f'<li>{subj.subject.name}</li>'
#     	li += '</ol>'
#     	return mark_safe(li)
#     subjects_.short_descriptin = 'Subjects'

#     def turma(self, obj):
#     	return obj.classe.turma
#     turma.short_descriptin = 'Turma'



# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name',
#     				'numero_de_bi', 'gender', 'birth_date',
#     				'phone_number_', 'email_', 'province', 'city', 
#     				'bairro', 'quarteirao', 'year', 'semester', 
#                     'classe_', 'subjects_')
#     list_per_page = 25
#     list_filter = ('gender',)
#     # list_editable = ('gender',)

#     def email_(self, obj):
#     	email = obj.email
#     	return mark_safe(f'''
#     		<a href="mailto:{email}">{email}</a>
#     	''')
#     email_.short_descriptin = 'Email'

#     def phone_number_(self, obj):
#     	phone_number = obj.phone_number
#     	return mark_safe(f'''
#     		<a href="tel:{phone_number}">{phone_number}</a>
#     	''')
#     phone_number_.short_descriptin = 'Phone number'

#     def classe_(self, obj):
#     	classes = obj.classe.all()
#     	li = '<ol>'
#     	for classe in classes:
#     		li += f'<li>{classe.name}</li>'
#     	li += '</ol>'
#     	return mark_safe(li)
#     classe_.short_descriptin = 'Subjects'

#     def subjects_(self, obj):
#     	subjects = obj.subjects.all()
#     	li = '<ol>'
#     	for subj in subjects:
#     		li += f'<li>{subj.name}</li>'
#     	li += '</ol>'
#     	return mark_safe(li)
#     subjects_.short_descriptin = 'Subjects'

#     def turma(self, obj):
#     	return obj.classe.turma
#     turma.short_descriptin = 'Turma'



# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name',
#     				'gender',  'phone_number_', 
#     				'email_', 'province', 'city', 'bairro', 
#     				'quarteirao', 'is_male')
#     list_display_links = ('id', 'first_name')
#     search_fields = ('first_name',)

#     def email_(self, obj):
#     	email = obj.email
#     	return mark_safe(f'''
#     		<a href="mailto:{email}">{email}</a>
#     	''')
#     email_.short_descriptin = 'Email'

#     def phone_number_(self, obj):
#     	phone_number = obj.phone_number
#     	return mark_safe(f'''
#     		<a href="tel:{phone_number}">{phone_number}</a>
#     	''')
#     phone_number_.short_descriptin = 'Phone number'