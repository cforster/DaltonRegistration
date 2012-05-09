import ldap;
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.db.models import get_model
from registrationApp.models import Student
import os

class customBackend:
    AD_LDAP_URL = 'ldap://directory89.dalton.org';
    AD_SEARCH_DN = 'OU=Dalton Users,DC=dalton,DC=org';
    AD_SEARCH_FIELDS = ['mail','givenName','sn','sAMAccountName','description','employeeID','memberOf'];
    AD_NT4_DOMAIN = 'dalton.org'; 

    def authenticate(self,username=None,password=None):
        try:
            debug= open(('/home/ddesai/registration/registrationApp/open/ldap.txt'), 'w')
            print >>debug, "create user %s" % username
            if len(password) == 0:
                return None
            l = ldap.initialize(self.AD_LDAP_URL)
            binddn = "%s@%s" % (username,self.AD_NT4_DOMAIN)
            l.simple_bind_s(binddn,password)
            l.unbind_s()
            return self.get_or_create_user(username,password)

        except ImportError:
            pass
        except ldap.INVALID_CREDENTIALS:
            pass

    def get_or_create_user(self, username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                ldap.set_option(ldap.OPT_REFERRALS,0) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!      
                l = ldap.initialize(self.AD_LDAP_URL)
                l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                binddn = "%s@%s" % (username,self.AD_NT4_DOMAIN)
                l.bind_s(binddn,password)
                debug= open(('/home/ddesai/registration/registrationApp/open/ldap3.txt'), 'w')
                result = l.search_ext_s(self.AD_SEARCH_DN,ldap.SCOPE_SUBTREE,"sAMAccountName=%s" % username,self.AD_SEARCH_FIELDS)[0][1]
                student = False
                faculty = False
                if result.has_key('memberOf'):
                    memberGroups = result['memberOf']
                else:
                    memberGroups = None
                   #can be both student and faculty? 
                   #all groups formatted the same?
                if memberGroups is not None:

                    for groups in memberGroups:

                        group = groups.split(",")
                        print >>debug, "g: %s" % group

                        for grp in group:
                            if "CN=Students" == grp:
                                student = True
                            if "CN=Faculty" == grp:
                                faculty = True
                 # get email
                if result.has_key('mail'):
                    mail = result['mail'][0]
                else:
                    mail = None
       
                # get surname
                if result.has_key('sn'):
                    last_name = result['sn'][0]
                else:
                    last_name = None

                # get first name
                if result.has_key('givenName'):
                    first_name = result['givenName'][0]
                else:
                    first_name = None

                if student:                
                    # get graduation year
                    if result.has_key('description'):
                        gradYear = int(result['description'][0])
                    else:
                        gradYear = None

                    #get student ID
                    if result.has_key('employeeID'):
                        studentID = int(result['employeeID'][0])
                    else:
                        studentID = None

                    l.unbind_s()

                    user = Student(username=username,id=studentID,first_name=first_name,last_name=last_name,email=mail,graduationYear=gradYear)
                    
                elif faculty:
                    l.unbind_s()

                    user = User(username=username,first_name=first_name,last_name=last_name,email=mail)

            except Exception, e:
                return None

            user.is_staff = False
            user.is_superuser = False
            user.set_password('ldap authenticated')
            user.save()
            if student:
                group=Group.objects.get(pk=2)
            elif faculty:
                group = Group.objects.get(pk=1)
            user.groups.add(group)
            user.save()
           
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None