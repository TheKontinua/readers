from django.contrib import admin

from mentapp.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "user_id", "is_admin")


admin.site.register(Volume)
admin.site.register(Chapter)
admin.site.register(Chapter_Loc)
admin.site.register(Question)
admin.site.register(Question_Loc)
admin.site.register(Question_Attachment)
admin.site.register(Support_Attachment)
admin.site.register(Quiz)
admin.site.register(Quiz_Question)
admin.site.register(Quiz_Rendering)
admin.site.register(Quiz_Feedback)
admin.site.register(User, UserAdmin)
admin.site.register(Chapter_Feedback)
admin.site.register(Verification)
admin.site.register(Language)
admin.site.register(Handle)
admin.site.register(Site)
admin.site.register(Support_Loc)
admin.site.register(Support)
admin.site.register(Quiz_Support)
admin.site.register(Email)
admin.site.register(Blob)