import csv, os
import time

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse
from django.views.generic import UpdateView
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib import messages

from survey.settings import MEDIA_ROOT, HOW_MANY_CHOICE_OPTIONS, SEPARATOR
from surveyapp.forms import CustomerForm, SurveyForm
from surveyapp.models import Customer, Survey, MultipleChoicesQS



class SurveyUpdateView(UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveyapp/survey.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_success_url(self):

        # is last question ? if true, create csv and go to download
        lastServey = Survey.objects.all().last()
        if int(self.kwargs['pk']) == lastServey.pk:
            CustomerCreateView.writeCSV(self)
            return reverse('download')

        # prepare to next question
        pk = str(int(self.kwargs['pk']) + 1)
        lastServey = Survey.objects.all().last()
        return reverse('survey', kwargs={'pk': pk})

    # Add some more context ( formset )
    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # select only data of question
        qs = MultipleChoicesQS.objects.filter(survey__pk=self.kwargs['pk']).filter(~Q(choice=''))
        context['form'].fields['user_ans_multy'].queryset = qs

        return context

    def post(self, request, *args, **kwargs):

        # .save() update record if instance argument is present, but another way .save create new record
        a = Survey.objects.get(pk=self.kwargs['pk'])
        form = SurveyForm(request.POST, instance=a)
        form.data['ans_time'] = int(time.time())

        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            messages.error(request, 'Somethings went wrong')

        return super().post(self, request, *args, **kwargs)


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'surveyapp/customer_new.html'
    now_time = 0
    ipath = 0

    def __init__(self, *args, **kwargs):
        # flash db
        call_command('flush', verbosity=3, interactive=False)
        # create superuser
        User.objects.create_superuser('ama', 'admin@example.com', 'alex1972')

        super().__init__(*args, **kwargs)

    def get_success_url(self):
        return reverse('survey', kwargs={'pk': 1})

    def post(self, request, *args, **kwargs):

        form = CustomerForm(request.POST, request.FILES)

        if form.is_valid():

            form.save(commit=False)
            CustomerCreateView.ipath = MEDIA_ROOT + '/surveyapp/' + str(request.FILES['i_file'])
            if os.path.exists(CustomerCreateView.ipath):
                os.remove(CustomerCreateView.ipath)
            rec = form.save()
            try:
                input_file = open(CustomerCreateView.ipath)
            except:
                messages.error(request, 'Error opening CSV file')
                return super().post(self, request, *args, **kwargs)

            try:
                rdr = csv.reader(input_file)
            except:
                messages.error(request, 'Error parsing CSV file')
                return super().post(self, request, *args, **kwargs)

            bodyFlag = False

            # CSV parsing
            for r in rdr:
                if bodyFlag:
                    survey = Survey()
                    survey.customer = rec
                    survey.qs_id = int(r[0])
                    survey.qs_name = r[1]
                    survey.qs_text = r[2]
                    if r[3] == Survey.QS_TYPE_CHOICES[0][1]:
                        survey.qs_type = Survey.QS_TYPE_CHOICES[0][0]
                    elif r[3] == Survey.QS_TYPE_CHOICES[1][1]:
                        survey.qs_type = Survey.QS_TYPE_CHOICES[1][0]
                    else:
                        survey.qs_type = Survey.QS_TYPE_CHOICES[2][0]

                    survey.save()

                    for i in range(4, HOW_MANY_CHOICE_OPTIONS + 4):
                        mpcq = MultipleChoicesQS()
                        mpcq.choice = r[i]
                        mpcq.save()
                        survey.user_ans_multy.add(mpcq) # Many-to-many saving

                bodyFlag = True

            input_file.close()
            firstSurvey = Survey.objects.all().first()
            # start survey time recording
            customer = Customer.objects.all().first()
            customer.start_time = int(time.time())
            customer.save()
            return redirect(reverse('survey', kwargs={'pk': firstSurvey.pk}))

        else:
            messages.error(request, 'Somethings went wrong')
            return super().post(self, request, *args, **kwargs)

    def writeCSV(self):
        # create csv. Just copy input file and add some user data
        path = MEDIA_ROOT + '/surveyapp/' + 'results.csv'
        input_file = open(CustomerCreateView.ipath)
        rdr = csv.reader(input_file)
        output_file = open(path, 'w')
        wrtr = csv.writer(output_file)
        qs = Survey.objects.all()
        title = rdr.__next__()  # Skip the first line
        title.append('ans_time')
        title.append('user_ans')
        wrtr.writerow(title)
        last = 0
        for (r, q) in zip(rdr, qs): # iteration through 2 objects
            # calculation time for 1st question
            if last > 0:
                duration = q.ans_time - last
            else:   # and for others
                customer = Customer.objects.all().first()
                duration = q.ans_time - customer.start_time

            r.append(duration)
            last = q.ans_time
            # different output for different question type
            if r[3] == 'single':
                if q.qs_single_choice == 'D':
                    r.append('Depend')
                elif q.qs_single_choice == "Y":
                    r.append('Yes')
                else:
                    r.append('No')
            elif r[3] == 'multiple':
                choises=q.user_ans_multy.all()
                str=''
                for ch in choises:
                    str+=ch.choice+SEPARATOR

                r.append(str[:-5])
            else:
                r.append(q.user_ans)

            wrtr.writerow(r)

        cus = Customer.objects.all().first()
        r = [1, 2, 3, 4]
        r[0] = 'Survey name'
        r[1] = cus.survey_name
        r[2] = 'User name'
        r[3] = cus.name
        wrtr.writerow(r)

        input_file.close()
        output_file.close()

# Download results
def download(request):
    path = MEDIA_ROOT + '/surveyapp/' + 'results.csv'
    fsock = open(path, "rb")
    response = HttpResponse(fsock, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=results.csv'
    return response
