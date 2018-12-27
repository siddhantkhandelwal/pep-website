import os
import sys
from django.template.loader import get_template
from io import open
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.conf import settings


def abstracts_results_announcement(arg):
    if arg=='0':
        feedback_dir = 'main/Feedback-tests'
    else:
        feedback_dir = 'main/Feedback'
        
    with open(os.path.join(os.path.abspath(feedback_dir), 'results'), 'r') as f:
        for data in f:
            data = data.split(',')
            uid = data[0]
            verdict = data[1]
            try:
                abstract = Abstract.objects.get(uid=uid)
                if 'accepted' in verdict:
                    abstract.verdict = 'Abstract Selected'
                elif 'rejected' in verdict:
                    abstract.verdict = 'Abstract Rejected'
                else:
                    with open(os.path.join(os.path.abspath(feedback_dir), 'log'), 'ab') as log:
                        log.write(str(abstract.uid) + ',Result File Error\n')
                    print(str(abstract.uid) + ',Result File Error')
                    continue
                abstract.save()
                subject, from_email, to = 'Paper Presentation | APOGEE 2019', settings.EMAIL_HOST_USER, abstract.participant.user.email
                context = { 'abstract': abstract }
                text_content = ''
                html_content = ''
                if 'accepted' in verdict:
                    text_content =  get_template(os.path.join(os.path.abspath('main/templates/main/paper-presentation'), 'abstract-accepted.txt')).render(context)
                    html_content = get_template(os.path.join(os.path.abspath('main/templates/main/paper-presentation'), 'abstract-accepted.html')).render(context)    
                elif 'rejected' in verdict:
                    text_content =  get_template(os.path.join(os.path.abspath('main/templates/main/paper-presentation'), 'abstract-rejected.txt')).render(context)
                    html_content = get_template(os.path.join(os.path.abspath('main/templates/main/paper-presentation'), 'abstract-rejected.html')).render(context)
                message = EmailMultiAlternatives(subject, text_content, from_email, [to])
                if os.path.exists(os.path.join(os.path.abspath(feedback_dir), str(abstract.uid)+'.pdf')):
                    message.attach_file(os.path.join(os.path.abspath(feedback_dir), str(abstract.uid)+'.pdf'))
                else:
                    with open(os.path.join(os.path.abspath(feedback_dir), 'log'), 'ab') as log:
                        log.write(str(abstract.uid) + ',Feedback not found, Mail not Sent\n')
                    print(str(abstract.uid) + ',Feedback not found, Mail not Sent')
                    continue
                message.attach_alternative(html_content, "text/html")
                message.send()
                with open(os.path.join(os.path.abspath(feedback_dir), 'log'), 'ab') as log:
                        log.write(str(abstract.uid) + ',Mail Sent\n')
                print(str(abstract.uid) + ',Mail Sent')
            except:
                with open(os.path.join(os.path.abspath(feedback_dir), 'log'), 'ab') as log:
                    log.write(str(uid) + ',Abstract Not Found Error\n')
                print(str(uid) + ',Abstract Not Found Error')
        
        subject = 'Abstract Results Log File'
        message = 'Log File is attached'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['f20170127@pilani.bits-pilani.ac.in', ]
        email = EmailMessage(subject, message, email_from, recipient_list,)
        email.attach_file(os.path.join(os.path.abspath(feedback_dir), 'log'))
        email.send()

if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')
    django.setup()
    from main.models import Abstract
    if len(sys.argv) == 1:
        print("Arguments Needed")
        sys.exit()
    else:
        abstracts_results_announcement(sys.argv[1])
