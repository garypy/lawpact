# coding=utf-8
from django.core.management.base import BaseCommand
from contract.models import Backlog
from django.utils import timezone
from django.core.mail import send_mail
import time

class Command(BaseCommand):
    help= 'Send mail to user regularly if there have contacts needs reminder'
    
    def handle(self, *args, **options):
        now = timezone.now().date()
        #print "now is: %s" % now
           
        count = 0
        backlogs = Backlog.objects.all()
        for backlog in backlogs.iterator():
            #print backlog.user
            count = count + 1
            #print "count is: %d" % count
            start_date = backlog.start_date
            #print "start_date is: %s" % start_date
            end_date = backlog.end_date
            #print "end_date is: %s" % end_date
            if start_date <= now and now < end_date:
                print "Send a mail to the user"
                user = backlog.user
                user_email = user.email
                user_name = user.username
                if user_email is not None:
                    print user_email
                    mail_title = u'合同事件处理--来自有娱网'
                    mail_content = u"亲爱的:%s，您有事件需要处理，请登录有娱网或者复制下面网址到浏览器查看\n\n" % user_name
                    #link = u"<a href='http://23.83.231.182/contract-info/'>点我查看</a>"
                    link = u"http://101.201.70.131/contract-info/"
                    mail_content += link;
                    print "mail_content:%s" % mail_content
                    mail_from = 'imblues@126.com'
                    mail_to = [user_email]
                    send_mail(mail_title,
                          mail_content,
                          mail_from,
                          mail_to)
                    time.sleep(5)