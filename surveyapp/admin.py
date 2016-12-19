from django.contrib import admin

from surveyapp.models import Survey, Customer, MultipleChoicesQS

admin.AdminSite.index_title = 'Survey app simple admin'
admin.AdminSite.site_title = 'Survey app admin panel'
admin.AdminSite.site_header = 'Survey app admin panel'


class SurveyAdmin(admin.ModelAdmin):
    model = Survey
    list_display = ('qs_id', 'customer')


class CustomerAdmin(admin.ModelAdmin):
    model = Customer


class MultipleChoicesQSAdmin(admin.ModelAdmin):
    model = MultipleChoicesQS
    list_display = ('choice',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(MultipleChoicesQS, MultipleChoicesQSAdmin)

