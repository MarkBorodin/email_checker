from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import redirect

from email_checker.models import CSVFileResult
from email_checker.tasks import check_emails


def download(request, id):
    result_file = CSVFileResult.objects.get(csv_file=id)
    response = FileResponse(open(f'media/results/{result_file.csv_file_result}', 'rb'))
    return response


def make_checks(request, id):
    check_emails.delay(id)
    messages.info(request, 'started checking emails')
    return redirect(request.META['HTTP_REFERER'])
