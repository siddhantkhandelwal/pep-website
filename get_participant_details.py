import csv
import os


def WriteDictToCSV(csv_file, csv_columns, dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return


def action():
    csv_columns = ['Submission Date', 'UID', 'Title', 'Category', 'Author', 'Co-Author', 'Email', 'Phone',
                   'Alternate Phone', 'College']
    dict_data = []

    currentPath = os.getcwd()
    csv_file = currentPath + "/participant_details.csv"

    for abstract in Abstract.objects.all():
        if abstract:
            if abstract.participant is None:
                continue
            else:
                data = {'UID': abstract.uid,
                    'Title': abstract.title,
                    'Category': abstract.category.name,
                    'Submission Date': abstract.submission_date,
                    'Author': abstract.participant.author,
                    'Co-Author': abstract.participant.coauthor,
                    'Phone': abstract.participant.phone1,
                    'Alternate Phone': abstract.participant.phone2,
                    'College': abstract.participant.college.name,
                    'Email': abstract.participant.user.email}
                dict_data.append(data)

    WriteDictToCSV(csv_file, csv_columns, dict_data)


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')
    django.setup()
    from main.models import ParticipantProfile, Abstract
    action()
