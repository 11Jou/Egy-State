from django.contrib import admin
from .models import Apertment , Image , Connection , Prediction 
from import_export.admin import ImportExportModelAdmin

@admin.register(Apertment)
class userdat(ImportExportModelAdmin):
    pass
@admin.register(Image)
class userdat(ImportExportModelAdmin):
    pass
admin.site.register(Connection)
admin.site.register(Prediction)