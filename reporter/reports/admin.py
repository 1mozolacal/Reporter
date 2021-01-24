from django.contrib import admin
from .models import Test, TestNumbers, TestText
# Register your models here.

admin.site.register(Test)
admin.site.register(TestNumbers)
admin.site.register(TestText)
