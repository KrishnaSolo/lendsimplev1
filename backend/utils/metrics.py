# Metrics utility code
import time
import functools
from typing import Dict
from google.cloud import monitoring_v3


PROJECT_ID = "<PROJECT_ID>"
METRICS_CLIENT = monitoring_v3.MetricServiceClient()


def create_metric_descriptor(
    metric_type: str, metric_kind: str, value_type: str, description: str, unit: str
) -> str:
    descriptor = monitoring_v3.types.MetricDescriptor()
    descriptor.type = f"custom.googleapis.com/{metric_type}"
    descriptor.metric_kind = metric_kind
    descriptor.value_type = value_type
    descriptor.description = description
    descriptor.unit = unit

    try:
        descriptor = METRICS_CLIENT.create_metric_descriptor(
            name="projects/{}".format(PROJECT_ID), metric_descriptor=descriptor
        )
    except Exception:
        descriptor = METRICS_CLIENT.get_metric_descriptor(
            name="projects/{}/metricDescriptors/{}".format(PROJECT_ID, descriptor.type)
        )

    return descriptor.name


def record_metric(metric_type: str, value: float, labels: Dict[str, str] = {}):
    series = monitoring_v3.types.TimeSeries()
    series.metric.type = f"custom.googleapis.com/{metric_type}"
    series.resource.type = "global"
    series.metric_kind = monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE
    series.value_type = monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE

    point = series.points.add()
    point.value.double_value = value
    point.interval.end_time.seconds = int(time.time())
    for k, v in labels.items():
        series.resource.labels[k] = v

    METRICS_CLIENT.create_time_series(
        name="projects/{}".format(PROJECT_ID), time_series=[series]
    )


def record_execution_time(metric_type: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            record_metric(metric_type, execution_time)
            return result

        return wrapper

    return decorator
