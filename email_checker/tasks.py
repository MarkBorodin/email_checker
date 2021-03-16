import csv

import pandas as pd

from app.celery import app
from email_checker.models import CSVFile, Email
from email_checker.utils import check_email_valid, check_email_accessible, check_email_catchall


@app.task
def check_emails(id): # noqa
    obj = CSVFile.objects.get(id=id)
    fixed_df = pd.read_csv(f'media/{obj.csv_file}',
                           sep=';',
                           encoding='UTF-8',
                           dayfirst=True,
                           )
    df_list = fixed_df['Mail'].values.tolist()

    for email_name in df_list:
        # checks
        valid = check_email_valid(email_name)
        accessible = check_email_accessible(email_name)
        catchall = check_email_catchall(email_name)

        # write in the database for each email
        email_object = Email.objects.get(csv_file=id, email=email_name)
        email_object.valid = valid
        email_object.accessible = accessible
        email_object.catchall = catchall

        # write to csv file
        with open(f'media/results/{obj.CSVFileResults.csv_file_result}', "a", newline="", encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerows([[email_object.email, valid, accessible, catchall]])
