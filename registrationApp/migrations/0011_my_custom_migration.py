# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute("CREATE FULLTEXT INDEX courseIndex ON Course (courseName, courseDescription)")
        print "Just created a fulltext index..."

    def backwards(self, orm):
        pass


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 31, 23, 4, 49, 794000)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 31, 23, 4, 49, 794000)'}),
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
            'corequisite': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'courseCredit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'courseDescription': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'courseName': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'courseNumber': ('django.db.models.fields.IntegerField', [], {'max_length': '9', 'primary_key': 'True', 'db_index': 'True'}),
            'gradesOffered': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '16', 'db_index': 'True'}),
            'preapprovalRequired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prerequisite': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'rankType': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'registrationApp.coursediscipline': {
            'Meta': {'object_name': 'CourseDiscipline'},
            'courseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Course']"}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Discipline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'registrationApp.departmentchair': {
            'Meta': {'object_name': 'DepartmentChair', '_ormbases': ['auth.User']},
            'favoriteColor': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'registrationApp.discipline': {
            'Meta': {'object_name': 'Discipline'},
            'departmentChair': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.DepartmentChair']"}),
            'discipline': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'registrationApp.house': {
            'Meta': {'object_name': 'House'},
            'houseAdvisorOneID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'advisor_one'", 'to': "orm['registrationApp.HouseAdvisor']"}),
            'houseAdvisorTwoID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'advisor_two'", 'null': 'True', 'to': "orm['registrationApp.HouseAdvisor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roomNumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'registrationApp.houseadvisor': {
            'Meta': {'object_name': 'HouseAdvisor', '_ormbases': ['auth.User']},
            'favoriteColor': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'registrationApp.parent': {
            'Meta': {'object_name': 'Parent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentEmail': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'parentFirstName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parentLastName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parentPhoneNumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'registrationApp.parentstudent': {
            'Meta': {'object_name': 'ParentStudent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentOneID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "' parent_one'", 'to': "orm['registrationApp.Parent']"}),
            'parentTwoID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "' parent_two'", 'null': 'True', 'to': "orm['registrationApp.Parent']"})
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
            'semesterOne': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'semesterTwo': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'registrationApp.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['auth.User']},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'advisor1Note': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'advisor1NoteRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'advisor2Note': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'advisor2NoteRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'advisorApproval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graduationYear': ('django.db.models.fields.IntegerField', [], {}),
            'houseID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.House']"}),
            'parentApproval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parentNote': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'parentNoteRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parentStudentID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.ParentStudent']"}),
            'submit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'registrationApp.studentschedule': {
            'Meta': {'object_name': 'StudentSchedule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sectionID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Section']"}),
            'studentID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registrationApp.Student']"})
        }
    }

    complete_apps = ['registrationApp']
