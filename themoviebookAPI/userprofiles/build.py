from models import *
from serializers import *
 
from django.contrib.auth.models import User
 
def buildUsers():
    # User 1 - mehtamanan
    user = User.objects.create_user(username = 'mehtamanan', password='Manan123#', first_name = 'Manan', last_name = 'Mehta')
    user.is_superuser = True
    user.is_staff = True
    user.email = 'mehtamanan@icloud.com'
    user.save()

    # User 2 - poojag
    user = User.objects.create_user(username = 'poojag', password='Pooja123#', first_name = 'Pooja', last_name = 'Ganatra')
    user.is_superuser = False
    user.is_staff = False
    user.email = 'poojaganatra1997@gmail.com'
    user.save()

   
