from django.conf.urls import patterns, url
from contract import views

from wkhtmltopdf.views import PDFTemplateView

import os
from django.conf.urls.static import static
from django.conf import settings
from numpy.distutils.from_template import template_name_re

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^register/$', views.register, name='register'),
        url(r'^activate/(?P<key>.+)$', views.activation, name='activation'),
        url(r'^spdf/(?P<html>.+)$', views.save_pdf, name='generate_pdf'),
        url(r'^get_test_pdf/$', views.print_test_pdf, name='get_pdf_file'),

        url(r'^pdf/$', PDFTemplateView.as_view(template_name='contract/3.html', filename='my_pdf.pdf'),
            name='pdf'),

        #url(r'^about/$', views.about, name='about'),
        #url(r'^add_category/$', views.add_category, name='add_category'),
        #url(r'^register/$', views.register, name='register'),
        #url(r'^login/$', views.user_login, name='login'),
        #url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        )

if settings.DEBUG:
    media_root = os.path.join(settings.PROJECT_PATH, 'media')
    urlpatterns += static('/media/', document_root=media_root)