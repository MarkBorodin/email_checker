from django.contrib import admin # noqa
from django.urls import reverse
from django.utils.safestring import mark_safe

from email_checker.models import CSVFile


class CSVFileAdmin(admin.ModelAdmin):
    model = CSVFile
    list_display = (
        'id', 'create_date', 'csv_file', 'get_CSV'
    )
    search_fields = ('id', 'create_date', 'csv_file')
    list_filter = ('id', 'create_date', 'csv_file')

    def get_CSV(self, obj): # noqa
        return mark_safe(
            f'<a class="button" href="{reverse("email_checker:get_csv", args=[obj.pk])}">Get CSV</a>'
        )


admin.site.register(CSVFile, CSVFileAdmin)
