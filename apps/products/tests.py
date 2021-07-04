from django.test import TestCase
from auth_user.models import Sensitives
from IcpSide import settings
# Create your tests here.
import os
import django
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'IcpSide.settings')
# django.setup()
# settings.configure()
def get_all_sensitives():
    sensitives_obj = Sensitives.objects.all()
    print(sensitives_obj, type(sensitives_obj))
get_all_sensitives()