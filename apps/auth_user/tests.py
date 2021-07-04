from django.test import TestCase
import datetime, random
from auth_user.models import Sensitives
# from .models import Verification_Code
# Create your tests here.
def get_all_sensitives():
    sensitives_obj = Sensitives.objects.all()
    print(sensitives_obj, type(sensitives_obj))
get_all_sensitives()