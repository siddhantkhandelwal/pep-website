import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')

import django
django.setup()

from main.models import Abstract
from django_file_md5 import calculate_md5

def check_duplicate_abstracts():
    abstracts = Abstract.objects.all()
    
    md5_dict = {}

    for abstract in abstracts:
        md5_dict[abstract.uid] = calculate_md5(abstract.document)
    
    rev_multiduct_md5_dict = {}

    for uid, md5 in md5_dict.items():
        rev_multiduct_md5_dict.setdefault(md5, set()).add(uid)
    
    with open('duplicate_abstracts_uid_list', 'w') as f:
        for uid_set in [uids for md5, uids in rev_multiduct_md5_dict.items() if len(uids) > 1]:
            f.write("%s\n" % uid_set)
    
if __name__ == '__main__':
	print("Finding duplicate abstracts")
	check_duplicate_abstracts()