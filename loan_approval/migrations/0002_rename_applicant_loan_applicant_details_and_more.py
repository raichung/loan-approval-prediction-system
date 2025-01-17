# Generated by Django 4.1.2 on 2023-04-25 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan_approval', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='applicant',
            new_name='applicant_details',
        ),
        migrations.RenameField(
            model_name='loandetails',
            old_name='loan',
            new_name='loan_request',
        ),
        migrations.RenameField(
            model_name='loanprediction',
            old_name='loan',
            new_name='loan_data',
        ),
        migrations.RemoveField(
            model_name='loandetails',
            name='employee',
        ),
        migrations.AddField(
            model_name='loan',
            name='managed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loan_approval.employee'),
        ),
    ]
