from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..classes import SubjectDashboard


@login_required
def subject_dashboard(request, **kwargs):
    dashboard = SubjectDashboard(
        dashboard_type=kwargs.get('dashboard_type'),
        dashboard_id=kwargs.get('dashboard_id'),
        dashboard_model=kwargs.get('dashboard_model'),
        dashboard_category=kwargs.get('dashboard_category'),
        registered_subject=kwargs.get('registered_subject'),
        show=kwargs.get('show'),
        dashboard_type_list=['subject'], )
    dashboard.set_context()
    return render_to_response(
        'subject_dashboard.html',
        dashboard.context.get(),
        context_instance=RequestContext(request))
