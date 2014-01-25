from django.contrib import admin
import ExobrainLTA.models
 
admin.site.register(ExobrainLTA.models.UserProfile)
admin.site.register(ExobrainLTA.models.Message)
admin.site.register(ExobrainLTA.models.Like)
admin.site.register(ExobrainLTA.models.Task)
admin.site.register(ExobrainLTA.models.Knowledge)
