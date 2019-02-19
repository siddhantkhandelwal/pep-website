from __future__ import with_statement
from __future__ import absolute_import
from django.conf import settings
import os
import sys
import csv
from io import open
from django.utils.encoding import smart_str
from django.core.mail import send_mail, EmailMessage


def WriteDictToCSV(csv_file, csv_columns, dict_data):
    with open(csv_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            print(data)
            writer.writerow(data)
    return


def get_details():
    csv_columns = [smart_str(u'Author'), smart_str(u'Co-Author'), smart_str(u'Phone'),
                   smart_str(u'Alternate Phone'), smart_str(u'College'), smart_str(u'Email')]

    csv_file = 'outstation_participant_details.csv'

    participants_list = []
    participants_profile_list = ParticipantProfile.objects.all().exclude(college__name__contains="BIRLA INSTITUTE OF TECHNOLOGY & SCIENCE PILANI")
    for participant in participants_profile_list:
        if participant is None:
            continue
        else:
            participant_data = {smart_str(u'Author'): smart_str(participant.author),
                                smart_str(u'Co-Author'): smart_str(participant.coauthor),
                                smart_str(u'Phone'): smart_str(participant.phone1),
                                smart_str(u'Alternate Phone'): smart_str(participant.phone2),
                                smart_str(u'College'): smart_str(participant.college.name),
                                smart_str(u'Email'): smart_str(participant.user.email)}
            participants_list.append(participant_data)

    WriteDictToCSV(csv_file, csv_columns, participants_list)
    subject = 'Outstation Participants'
    message = 'Outstation Participants details are attached'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['pep@bits-apogee.org', ]
    email = EmailMessage(subject, message, email_from, recipient_list,)
    email.attach_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'outstation_participant_details.csv'))
    email.send()


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')
    django.setup()
    from main.models import ParticipantProfile, College
    get_details()
