from django.db import models


class BaseModel(models.Model):
    """base model"""
    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    write_date = models.DateTimeField(null=True, auto_now=True)


class CSVFile(BaseModel):
    """model for csv file"""
    csv_file = models.FileField()


class CSVFileResult(BaseModel):
    """model for csv file results"""
    csv_file_result = models.TextField(max_length=128)
    csv_file = models.OneToOneField(to=CSVFile, related_name='CSVFileResults', on_delete=models.CASCADE)


class Email(BaseModel):
    """model for each email from csv file"""
    email = models.TextField(max_length=256)
    valid = models.BooleanField(null=True, blank=True, default=False)
    accessible = models.BooleanField(null=True, blank=True, default=False)
    catchall = models.BooleanField(null=True, blank=True, default=False)
    csv_file = models.ForeignKey(to=CSVFile, related_name='emails', on_delete=models.CASCADE)
