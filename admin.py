from django.contrib import admin

# Register your models here.
from .models import Food

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','description','product_image',)

admin.site.register(Food)    
#admin.site.register(Myrating)
#admin.site.register(MyList)
