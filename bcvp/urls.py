import django_databrowse

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db.models import get_models
from django.views.generic import RedirectView

from edc_call_manager.caller_site import site_model_callers
from edc_dashboard.section import site_sections
from edc_dashboard.subject.views import additional_requisition
from edc_data_manager.data_manager import data_manager
from edc_lab.lab_profile.classes import site_lab_profiles
from edc_rule_groups.classes import site_rule_groups
from edc_visit_schedule.classes import site_visit_schedules

from bcvp.app_configuration import AppConfiguration

site_lab_profiles.autodiscover()
AppConfiguration(lab_profiles=site_lab_profiles).prepare()
site_visit_schedules.autodiscover()
site_visit_schedules.build_all()
site_rule_groups.autodiscover()
data_manager.prepare()
site_sections.autodiscover()
site_sections.update_section_lists()
site_model_callers.autodiscover()
admin.autodiscover()

for model in get_models():
    try:
        django_databrowse.site.register(model)
    except:
        pass

APP_NAME = settings.APP_NAME

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
    (r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns(
    '',
    url(r'^databrowse/(.*)', login_required(django_databrowse.site.root)),
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/dashboard/visit/add_requisition/'.format(app_name=APP_NAME),
        additional_requisition, name="add_requisition"),
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/dashboard/'.format(app_name=APP_NAME),
        include('bcvp.{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
)

urlpatterns += patterns(
    '',
    (r'^bhp_sync/', include('edc_sync.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/login/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.login',
        name='{app_name}_login'.format(app_name=APP_NAME)),
    url(r'^{app_name}/logout/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.logout_then_login',
        name='{app_name}_logout'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change',
        name='password_change_url'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change_done/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'.format(app_name=APP_NAME)),
)
urlpatterns += patterns(
    '',
    url(r'^{app_name}/section/'.format(app_name=APP_NAME), include('edc_dashboard.section.urls'), name='section'),
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/$'.format(app_name=APP_NAME),
        RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
    url(r'', RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
)

urlpatterns += staticfiles_urlpatterns()
