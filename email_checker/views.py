from django.http import FileResponse

from email_checker.models import CSVFileResult


def download(request, id):
    result_file = CSVFileResult.objects.get(csv_file=id)
    response = FileResponse(open(f'media/results/{result_file.csv_file_result}', 'rb'))
    return response
