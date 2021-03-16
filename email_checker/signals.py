import csv

import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver

from email_checker.models import CSVFile, Email, CSVFileResult


@receiver(post_save, sender=CSVFile)
def phase_number(sender, instance, created, **kwargs):
    """read csv, take emails and create objects in the database for each email"""
    if created:

        # get emails from file
        fixed_df = pd.read_csv(f'media/{instance.csv_file}',
                               sep=';',
                               encoding='UTF-8',
                               dayfirst=True,
                               )
        df_list = set(fixed_df['Mail'].values.tolist())

        # create results file object in db
        results_file = CSVFileResult.objects.create(
            csv_file_result=f'result_{instance.csv_file}',
            csv_file=instance,
        )
        results_file.save()

        # results list
        emails = [['email', 'valid', 'accessible', 'catchall']]

        # create results csv file
        with open(f'media/results/{results_file.csv_file_result}', "w", newline="", encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerows(emails)

        for email_name in df_list:
            # create object in the database for each email
            email_object = Email.objects.create(
                email=email_name,
                csv_file=instance,
            )
            email_object.save()
