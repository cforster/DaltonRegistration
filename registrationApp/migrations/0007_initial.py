# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'House'
        db.create_table('registrationApp_house', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('houseAdvisorOne_firstName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('houseAdvisorOne_lastName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('houseAdvisorTwo_firstName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('houseAdvisorTwo_lastName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('roomNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('studentNumber', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('registrationApp', ['House'])

        # Adding model 'Parent'
        db.create_table('registrationApp_parent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parentFirstName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('parentLastName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('parentEmail', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('parentPhoneNumber', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('registrationApp', ['Parent'])

        # Adding model 'ParentStudent'
        db.create_table('registrationApp_parentstudent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parentOneID', self.gf('django.db.models.fields.related.ForeignKey')(related_name=' parent_one', to=orm['registrationApp.Parent'])),
            ('parentTwoID', self.gf('django.db.models.fields.related.ForeignKey')(related_name=' parent_two', to=orm['registrationApp.Parent'])),
        ))
        db.send_create_signal('registrationApp', ['ParentStudent'])

        # Adding model 'Student'
        db.create_table('registrationApp_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('grade', self.gf('django.db.models.fields.IntegerField')()),
            ('houseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.House'])),
            ('parentStudentID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.ParentStudent'])),
            ('submit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('advisorApproval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('advisor1Note', self.gf('django.db.models.fields.CharField')(max_length=100000)),
            ('advisor2Note', self.gf('django.db.models.fields.CharField')(max_length=100000)),
            ('advisor1NoteRead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('advisor2NoteRead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parentApproval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parentNote', self.gf('django.db.models.fields.CharField')(max_length=100000)),
            ('parentNoteRead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('registrationApp', ['Student'])

        # Adding model 'DepartmentChair'
        db.create_table('registrationApp_departmentchair', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('registrationApp', ['DepartmentChair'])

        # Adding model 'Discipline'
        db.create_table('registrationApp_discipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discipline', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('departmentChair', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.DepartmentChair'])),
        ))
        db.send_create_signal('registrationApp', ['Discipline'])

        # Adding model 'Course'
        db.create_table('registrationApp_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseName', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('courseDescription', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('preapprovalRequired', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('grades_Offered', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=16)),
            ('courseNumber', self.gf('django.db.models.fields.IntegerField')(max_length=9)),
        ))
        db.send_create_signal('registrationApp', ['Course'])

        # Adding model 'CourseDiscipline'
        db.create_table('registrationApp_coursediscipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Course'])),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Discipline'])),
        ))
        db.send_create_signal('registrationApp', ['CourseDiscipline'])

        # Adding model 'Section'
        db.create_table('registrationApp_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Course'])),
            ('semesterOne', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('semesterTwo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('roomNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('APeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('BPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('CPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('DPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('EPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('FPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('GPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('HPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('IPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('KPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
            ('ZPeriodDays', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('registrationApp', ['Section'])

        # Adding model 'StudentSchedule'
        db.create_table('registrationApp_studentschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('studentID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Student'])),
            ('sectionID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Section'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('registrationApp', ['StudentSchedule'])

        # Adding model 'PreApproval'
        db.create_table('registrationApp_preapproval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('studentID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Student'])),
            ('courseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Course'])),
        ))
        db.send_create_signal('registrationApp', ['PreApproval'])

        # Adding model 'RequiredObjects'
        db.create_table('registrationApp_requiredobjects', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Course'], null=True, blank=True)),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registrationApp.Discipline'], null=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal('registrationApp', ['RequiredObjects'])


    def backwards(self, orm):
        
        # Deleting model 'House'
        db.delete_table('registrationApp_house')

        # Deleting model 'Parent'
        db.delete_table('registrationApp_parent')

        # Deleting model 'ParentStudent'
        db.delete_table('registrationApp_parentstudent')

        # Deleting model 'Student'
        db.delete_table('registrationApp_student')

        # Deleting model 'DepartmentChair'
        db.delete_table('registrationApp_departmentchair')

        # Deleting model 'Discipline'
        db.delete_table('registrationApp_discipline')

        # Deleting model 'Course'
        db.delete_table('registrationApp_course')

        # Deleting model 'CourseDiscipline'
        db.delete_table('registrationApp_coursediscipline')

        # Deleting model 'Section'
        db.delete_table('registrationApp_section')

        # Deleting model 'StudentSchedule'
        db.delete_table('registrationApp_studentschedule')

        # Deleting model 'PreApproval'
        db.delete_table('registrationApp_preapproval')

        # Deleting model 'RequiredObjects'
        db.delete_table('registrationApp_requiredobjects')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'registrationApp.course': {
            'Meta': {'object_name': 'Course'},
            'courseDescription': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'courseName': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'courseNumber': ('django.db.models.fields.IntegerField', [], {'max_length': '9'}),
            'grades_Offered': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preapprovalRequired': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'registrationApp.coursediscipline': {
            'Meta': {'object_name': 'CourseDiscipline'},
            'courseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Course']"}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Discipline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'registrationApp.departmentchair': {
            'Meta': {'object_name': 'DepartmentChair'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'registrationApp.discipline': {
            'Meta': {'object_name': 'Discipline'},
            'departmentChair': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.DepartmentChair']"}),
            'discipline': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'registrationApp.house': {
            'Meta': {'object_name': 'House'},
            'houseAdvisorOne_firstName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'houseAdvisorOne_lastName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'houseAdvisorTwo_firstName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'houseAdvisorTwo_lastName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roomNumber': ('django.db.models.fields.IntegerField', [], {}),
            'studentNumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'registrationApp.parent': {
            'Meta': {'object_name': 'Parent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentEmail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parentFirstName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parentLastName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parentPhoneNumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'registrationApp.parentstudent': {
            'Meta': {'object_name': 'ParentStudent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentOneID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "' parent_one'", 'to': "orm['registrationApp.Parent']"}),
            'parentTwoID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "' parent_two'", 'to': "orm['registrationApp.Parent']"})
        },
        'registrationApp.preapproval': {
            'Meta': {'object_name': 'PreApproval'},
            'courseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'studentID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Student']"})
        },
        'registrationApp.requiredobjects': {
            'Meta': {'object_name': 'RequiredObjects'},
            'courseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Course']", 'null': 'True', 'blank': 'True'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Discipline']", 'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'registrationApp.section': {
            'APeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'BPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'CPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'DPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'EPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'FPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'GPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'HPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'IPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'KPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Section'},
            'ZPeriodDays': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'courseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roomNumber': ('django.db.models.fields.IntegerField', [], {}),
            'semesterOne': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'semesterTwo': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'registrationApp.student': {
            'Meta': {'object_name': 'Student'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'advisor1Note': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            'advisor1NoteRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'advisor2Note': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            'advisor2NoteRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'advisorApproval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'grade': ('django.db.models.fields.IntegerField', [], {}),
            'houseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parentApproval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parentNote': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            'parentNoteRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parentStudentID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.ParentStudent']"}),
            'submit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'registrationApp.studentschedule': {
            'Meta': {'object_name': 'StudentSchedule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'sectionID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Section']"}),
            'studentID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Student']"})
        }
    }

    complete_apps = ['registrationApp']
