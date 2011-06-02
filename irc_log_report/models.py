# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Message(models.Model):
    mid = models.AutoField(primary_key=True) #if we left a primary key out then Django would create 'id' primary for us by default with auto increment or serial
    channel = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    teller = models.CharField(max_length=50)
    message = models.TextField()
    class Meta:
        db_table = u'log_messages'

