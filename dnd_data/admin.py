from django.contrib import admin
from .models import Race, CharacterClass, Background, Alignment

# Register your models here.
admin.site.register(Race)
admin.site.register(CharacterClass)
admin.site.register(Background)
admin.site.register(Alignment)

