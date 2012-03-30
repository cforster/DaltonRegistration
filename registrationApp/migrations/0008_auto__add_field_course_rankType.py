# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Course.rankType'
        db.add_column('registrationApp_course', 'rankType', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Course.rankType'
        db.delete_column('registrationApp_course', 'rankType')


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
            'preapprovalRequired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rankType': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
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
