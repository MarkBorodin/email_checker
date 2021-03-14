import csv
import time

from django.db.models.signals import post_save
from django.dispatch import receiver

from email_checker.models import CSVFile, Email, CSVFileResult
from email_checker.utils import check_email_valid, check_email_catchall, bounceback_check, send_email_for_check


@receiver(post_save, sender=CSVFile)
def phase_number(sender, instance, created, **kwargs):
    """read csv, take emails and create objects in the database for each email"""
    if created:
        with open(f'media/{instance.csv_file}', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            # create results file object in db
            results_file = CSVFileResult.objects.create(
                csv_file_result=f'result_{instance.csv_file}',
                csv_file=instance,
            )
            results_file.save()

            # results list
            emails = [['email', 'valid', 'accessible', 'catchall']]
            emails_list = []

            for row in spamreader:
                if check_email_valid(row[0]):
                    send_email_for_check(row[0])
                    emails_list.append(row[0])

            time.sleep(20)

            for email_name in emails_list:
                valid = check_email_valid(email_name)
                accessible = bounceback_check(email_name)
                catchall = check_email_catchall(email_name)

                email_object = Email.objects.create(
                    email=email_name,
                    valid=valid,
                    accessible=accessible,
                    catchall=catchall,
                    csv_file=instance,
                )
                email_object.save()
                emails.append([
                    email_name,
                    valid,
                    accessible,
                    catchall,
                ])

            # create results csv file
            with open(f'media/results/{results_file.csv_file_result}', "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(emails)
