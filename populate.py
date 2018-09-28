import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')

import django
django.setup()

from main.models import College

def add_colleges():
	for line in open('colleges.txt', 'r'):
		c = College.objects.get_or_create(name=line)[0]
		c.save()

def populate():
	add_colleges()

if __name__ == '__main__':
	print("Starting population script...")
	populate()