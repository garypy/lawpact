# coding=gbk

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from bsddb.test.test_all import verbose

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=u"�û�")
    phone_number = models.CharField(u"�绰����", max_length=15, blank=True)
    pic = models.ImageField(u"ͷ��", upload_to='images', blank=True)
    contract_url = models.URLField(blank=True)
    
    #For user active by the email
    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)
   
    class Meta:
        verbose_name = u"ע���û�"
        verbose_name_plural = u"ע���û�"
    
    def __unicode__(self):
        return self.user.username
    

class UserContract(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, verbose_name=_('name'))
    type = models.CharField(max_length=20, verbose_name=u"��ͬ����")
    contract_status = models.BooleanField(verbose_name = u"��ͬ״̬")
    law_status = models.BooleanField()
    backlog_date = models.DateField()
    backlog = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to='files', blank=True)
    
    class Meta:
        verbose_name = u"�û���ͬ"
        verbose_name_plural = u"�û���ͬ"
    
    def __unicode__(self):
        return self.name

class Backlog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()
    content = models.TextField()
    
    class Meta:
        verbose_name = u"��������"
        verbose_name_plural = u"��������"
    
    def __unicode__(self):
        return self.user.username
