from userprofiles.models import *
from userprofiles.serializers import *
 
from django.contrib.auth.models import User
 
def buildUsers():
    # User 1 - mehtamanan
    user = User.objects.create_user('mehtamanan', password='Manan123#', first_name = 'Manan')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    rs = RegistrationSerializer(user)
    print rs.data
    print ""

    # User 2 - poojag
    user = User.objects.create_user('poojag', password='Pooja123#', first_name = 'Pooja')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'poojaganatra1997@gmail.com'
    user.save()
    rs = RegistrationSerializer(user)
    print rs.data
    print ""

    # UserProfile for user 1
    userprofile1 = UserProfile()
    userprofile1.user = User.objects.get(pk = 1)
    userprofile1.bio = 'Computer programmer'
    userprofile1.user.email = 'mehtamanan@icloud.com'
    userprofile1.birth_date = '1997-04-18'
    userprofile1.save()

    # Userprofile for user 2
    userprofile2 = UserProfile()
    userprofile2.user = User.objects.get(pk = 2)
    userprofile2.bio = 'Yo friend'
    userprofile2.birth_date = '1997-08-09'
    userprofile2.save()

    userprofile1.follows.add(userprofile2)

    ups = UserProfileSerializer(userprofile1)
    print ups.data
    print ""
    
    ups = UserProfileSerializer(userprofile2)
    print ups.data
    print ""
