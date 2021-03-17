import csv
import logging

import pandas as pd
from csv import reader

from django.contrib import messages

from app.celery import app
from email_checker.models import CSVFile, Email
from email_checker.utils import check_email_valid, check_email_accessible, check_email_catchall


logger = logging.getLogger(__name__)


@app.task
def check_emails(id): # noqa
    obj = CSVFile.objects.get(id=id)

    e_list = []

    # get emails with csv
    with open(f'media/{obj.csv_file}', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            for item in row:
                if '@' in item and "." in item:
                    e_list.append(item)

    for email_name in e_list:
        # checks
        valid = check_email_valid(email_name)
        if valid is True:
            accessible = check_email_accessible(email_name)
        else:
            accessible = False
        catchall = check_email_catchall(email_name)

        csv_file = CSVFile.objects.get(id=id)

        # write in the database for each email
        email_object = Email.objects.create(
            csv_file=csv_file,
            email=email_name,
            valid=valid,
            accessible=accessible,
            catchall=catchall
        )
        email_object.save()

        logger.info(f"{email_name}, valid: {valid}, accessible: {accessible}, catchall: {catchall},")

        # write to csv file
        with open(f'media/results/{obj.CSVFileResults.csv_file_result}', "a", newline="", encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerows([[email_object.email, valid, accessible, catchall]])

    logger.info("all checks completed")
