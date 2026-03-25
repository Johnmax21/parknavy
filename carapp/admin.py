from django.contrib import admin

# Register your models here.
from . models import user_reg,Feedback,Add_areas,book,icart,pay,YTRExtrapay,Slotfeedback
admin.site.register(Feedback)
admin.site.register(user_reg)
admin.site.register(Add_areas)
admin.site.register(book)
admin.site.register(pay)
admin.site.register(YTRExtrapay)
admin.site.register(Slotfeedback)

