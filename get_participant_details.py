from __future__ import with_statement
from __future__ import absolute_import
import csv
import os
from io import open
from django.utils.encoding import smart_str


def WriteDictToCSV(csv_file, csv_columns, dict_data):
    with open(csv_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            print(data)
            writer.writerow(data)
    return


def action():
    csv_columns = [smart_str(u'Submission Date'), smart_str(u'UID'), smart_str(u'Title'), smart_str(u'Category'), smart_str(u'Author'), smart_str(u'Co-Author'), smart_str(u'Email'), smart_str(u'Phone'),
                   smart_str(u'Alternate Phone'), smart_str(u'College')]
    dict_data = []

    csv_file = 'participant_details.csv'

    for abstract in Abstract.objects.all():
        if abstract:
            if abstract.participant is None:
                continue
            else:
                data = {smart_str(u'UID'): smart_str(abstract.uid),
                        smart_str(u'Title'): smart_str(abstract.title),
                        smart_str(u'Category'): smart_str(abstract.category.name),
                        smart_str(u'Submission Date'): smart_str(abstract.submission_date),
                        smart_str(u'Author'): smart_str(abstract.participant.author),
                        smart_str(u'Co-Author'): smart_str(abstract.participant.coauthor),
                        smart_str(u'Phone'): smart_str(abstract.participant.phone1),
                        smart_str(u'Alternate Phone'): smart_str(abstract.participant.phone2),
                        smart_str(u'College'): smart_str(abstract.participant.college.name),
                        smart_str(u'Email'): smart_str(abstract.participant.user.email)}
                dict_data.append(data)

    WriteDictToCSV(csv_file, csv_columns, dict_data)


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')
    django.setup()
    from main.models import ParticipantProfile, Abstract
    action()
