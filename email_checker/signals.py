import csv
from csv import reader
import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver

from email_checker.models import CSVFile, Email, CSVFileResult


@receiver(post_save, sender=CSVFile)
def phase_number(sender, instance, created, **kwargs):
    """read csv, take emails and create objects in the database for each email"""
    if created:

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
