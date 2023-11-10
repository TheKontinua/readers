from django.contrib import admin

from mentapp.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'org_name')


admin.site.register(Volume)
admin.site.register(Chapter)
admin.site.register(Chapter_Loc)
admin.site.register(Question)
admin.site.register(Question_Loc)
admin.site.register(Question_Attachment)
admin.site.register(Quiz)
admin.site.register(Quiz_Question)
admin.site.register(Quiz_Rendering)
admin.site.register(Quiz_Feedback)
admin.site.register(User, UserAdmin)
admin.site.register(Email)



