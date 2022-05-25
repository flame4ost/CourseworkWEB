from django.contrib import admin
from parking.models import ParkingSpot,ParkingInfo

# Register your models here.
admin.site.register(ParkingSpot)
admin.site.register(ParkingInfo)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]