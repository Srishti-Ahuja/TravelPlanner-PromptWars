import logging
from google.cloud import logging as cloud_logging
from google.cloud import monitoring_v3
import time

class LoggingService:
    def __init__(self, project_id: str):
        self.project_id = project_id
        # Cloud Logging
        self.client = cloud_logging.Client(project=project_id)
        self.client.setup_logging()
        self.logger = logging.getLogger("orbit_app")
        self.logger.setLevel(logging.INFO)

        # Cloud Monitoring (Metrics)
        self.metric_client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{project_id}"

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def record_itinerary_generation(self):
        """Custom metric for Itinerary Generation Count"""
        series = monitoring_v3.TimeSeries()
        series.metric.type = "custom.googleapis.com/itinerary_generation_count"
        series.resource.type = "global"
        
        point = monitoring_v3.Point()
        point.value.int64_value = 1
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        point.interval.end_time.seconds = seconds
        point.interval.end_time.nanos = nanos
        
        series.points = [point]
        try:
            self.metric_client.create_time_series(
                request={"name": self.project_name, "time_series": [series]}
            )
        except Exception as e:
            # Fallback if metric doesn't exist yet or auth fails
            self.logger.warning(f"Failed to record metric: {e}")
