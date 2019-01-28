from main.models import College, ParticipantProfile
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')

django.setup()


def clean_college_data():
    if College.objects.all():
        for college in College.objects.all():
            college.delete()


def add_colleges():
    for line in open('colleges.txt', 'r'):
        c = College.objects.get_or_create(name=line)[0]
        c.save()


def add_participants():
    user = User.objects.get_or_create()
    user.username = 'pdummy1'
    user.set_password('smellycat')
    pdummy1 = ParticipantProfile()


def populate():
    clean_college_data()
    add_colleges()
    add_participants()


if __name__ == '__main__':
    print("Starting population script...")
    populate()
