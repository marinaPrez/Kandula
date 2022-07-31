"""Views module."""

from flask import render_template, flash, url_for, request
from dependency_injector.wiring import inject, Provide
from werkzeug.utils import redirect
from app.src.services import app_health, instance_shutdown_scheduling
from app.src.services.instance_actions import InstanceActions
from app.src.services.instance_data import InstanceData
from app.containers import Container
from botocore.exceptions import ClientError
from flask.views import MethodView
from prometheus_client import Counter, Summary, generate_latest, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, Gauge
import logging
import time

logger = logging.getLogger()


LATENCY = Summary('kandula_page_latency_seconds', 'Time to serve a web page', ["method"])
PAGE_VISITS = Counter('kandula_monitor_page_count', 'Number of visits per-page', ["endpoint"])



class InstanceAPI(MethodView):
    @inject
    def __init__(self, instance_actions: InstanceActions = Provide[Container.instance_actions]) -> None:
        self.instance_actions = instance_actions
        super().__init__()

    def get(self, instance_id, instance_action):
        try:
            action_to_run = self.instance_actions.action_selector(instance_action)
            action_to_run(instance_id)
            flash("Your request to {} instance {} is in progress".format(instance_action, instance_id), "info")
        except (ClientError, RuntimeError) as e:
            flash("Cannot perform action '{}' on instance: {}".format(instance_action, instance_id), "danger")
            logger.exception(e)

        return redirect(url_for('instances'))

    def post(self, instance_id, instance_action):
        try:
            action_to_run = self.instance_actions.action_selector(instance_action)
            action_to_run(instance_id)
            flash("Your request to {} instance {} is in progress".format(instance_action, instance_id), "info")
        except (ClientError, RuntimeError) as e:
            flash("Cannot perform action '{}' on instance: {}".format(instance_action, instance_id), "danger")
            logger.exception(e)

        return redirect(url_for('instances'))


def home():
    PAGE_VISITS.labels(endpoint='about').inc()
    time_request = time.time()
    logger.info("Home view")
    time_response = time.time()
    LATENCY.labels(method='home').observe(time_response - time_request)
    return render_template('home.html', title='Welcome to Kandula')


def about():
    PAGE_VISITS.labels(endpoint='about').inc()
    time_request = time.time()
    time_response = time.time()
    LATENCY.labels(method='about').observe(time_response - time_request)
    return render_template('about.html', title='About')


def health():
    PAGE_VISITS.labels(endpoint='health').inc()
    time_request = time.time()
    health_metrics, is_app_healthy = app_health.get_app_health()
    time_response = time.time()
    LATENCY.labels(method='health').observe(time_response - time_request)
    return render_template('health.html', title='Application Health',
                           healthchecks=health_metrics), 200 if is_app_healthy else 500


def metrics():
    PAGE_VISITS.labels(endpoint='metrics').inc()
    return generate_latest()
    # return render_template('metrics.html', title='metrics', )


@inject
def instances(instance_data: InstanceData = Provide[Container.instance_data]):
    PAGE_VISITS.labels(endpoint='instances').inc()
    time_request = time.time()
    instances_response = instance_data.get_instances()
    time_response = time.time()
    LATENCY.labels(method='instances').observe(time_response - time_request)
    return render_template('instances.html', title='Instances',
                           instances=instances_response['Instances'])


def scheduler():
    PAGE_VISITS.labels(endpoint='scheduler').inc()
    time_request = time.time()
    if request.method == 'POST':
        instance_shutdown_scheduling.handle_instance(request.form)
    scheduled_instances = instance_shutdown_scheduling.get_scheduled_instances()
    time_response = time.time()
    LATENCY.labels(method='scheduler').observe(time_response - time_request)
    return render_template('scheduler.html', title='Scheduling',
                           scheduled_instances=scheduled_instances["Instances"])
