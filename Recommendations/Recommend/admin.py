from django.contrib import admin

# Register your models here.
from .models import Food, Myrating, MyList

# Register your models here.
admin.site.register(Food)
admin.site.register(Myrating)
admin.site.register(MyList)