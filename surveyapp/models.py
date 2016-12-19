from django.db import models


class Customer(models.Model):
    name = models.CharField("Customer name", max_length=100, unique=True)
    survey_name = models.CharField("Survey name", max_length=100, unique=True)
    start_time = models.PositiveIntegerField('Start survey time', blank=True, null=True)
    # upload_to - URL relation to MEDIA_URL
    i_file = models.FileField('Input file', upload_to='surveyapp/')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        unique_together = (("name", "survey_name"),)

    def __str__(self):
        return '%s' % (self.name)

class MultipleChoicesQS(models.Model):

    choice = models.CharField("Choice", max_length=100)

    class Meta:
        verbose_name = 'Multiple choice question'
        verbose_name_plural = 'Multiple choice questions'

    def __str__(self):
        return '%s' % (self.choice)


class Survey(models.Model):

    QS_TYPE_CHOICES = (
        ('S', 'single'),
        ('M', 'multiple'),
        ('T', 'string'),
    )

    QS_SINGLE_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('D', 'Depends'),
    )

    qs_id = models.PositiveIntegerField('Question ID')
    qs_name = models.CharField("Question name", max_length=100)
    qs_text = models.CharField("Question text", max_length=200)
    qs_type = models.CharField('Question type', max_length=1, choices=QS_TYPE_CHOICES, blank=True, null=True)
    qs_single_choice = models.CharField('Single choices', max_length=1, choices=QS_SINGLE_CHOICES, blank=True, default="Y")

    # ------------ answer fields -----------------------
    ans_time = models.PositiveIntegerField('Answer_time', blank=True, null=True)
    user_ans = models.CharField("User answer", max_length=200, blank=True, null=True)

    user_ans_multy = models.ManyToManyField(MultipleChoicesQS, blank=True)

    customer = models.ForeignKey(Customer)  # Many-to-One relation

    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'

    def __str__(self):
        return '%s' % (self.qs_id)





