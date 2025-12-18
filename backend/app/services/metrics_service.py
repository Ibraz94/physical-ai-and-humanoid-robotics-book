"""
Metrics and performance monitoring service
"""
import time
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsService:
    def __init__(self):
        self.metrics = {}

    async def record_api_call(self, endpoint: str, duration: float, status_code: int = 200, user_id: Optional[str] = None):
        """
        Record an API call with its duration and status
        """
        metric_key = f"api_{endpoint}"

        if metric_key not in self.metrics:
            self.metrics[metric_key] = {
                "total_calls": 0,
                "total_duration": 0.0,
                "avg_duration": 0.0,
                "min_duration": float('inf'),
                "max_duration": 0.0,
                "status_codes": {},
                "last_called": None
            }

        metric = self.metrics[metric_key]
        metric["total_calls"] += 1
        metric["total_duration"] += duration
        metric["avg_duration"] = metric["total_duration"] / metric["total_calls"]
        metric["min_duration"] = min(metric["min_duration"], duration)
        metric["max_duration"] = max(metric["max_duration"], duration)
        metric["last_called"] = datetime.utcnow()

        if str(status_code) not in metric["status_codes"]:
            metric["status_codes"][str(status_code)] = 0
        metric["status_codes"][str(status_code)] += 1

        logger.info(f"Recorded API call to {endpoint}: {duration:.3f}s, status: {status_code}")

    async def record_query_processing_time(self, duration: float, success: bool = True):
        """
        Record query processing time
        """
        metric_key = "query_processing"

        if metric_key not in self.metrics:
            self.metrics[metric_key] = {
                "total_queries": 0,
                "total_duration": 0.0,
                "avg_duration": 0.0,
                "min_duration": float('inf'),
                "max_duration": 0.0,
                "successful_queries": 0,
                "failed_queries": 0
            }

        metric = self.metrics[metric_key]
        metric["total_queries"] += 1
        metric["total_duration"] += duration
        metric["avg_duration"] = metric["total_duration"] / metric["total_queries"]
        metric["min_duration"] = min(metric["min_duration"], duration)
        metric["max_duration"] = max(metric["max_duration"], duration)

        if success:
            metric["successful_queries"] += 1
        else:
            metric["failed_queries"] += 1

        logger.info(f"Recorded query processing time: {duration:.3f}s, success: {success}")

    async def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all collected metrics
        """
        return self.metrics

    async def get_endpoint_performance(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Get performance metrics for a specific endpoint
        """
        metric_key = f"api_{endpoint}"
        return self.metrics.get(metric_key)

    async def reset_metrics(self):
        """
        Reset all collected metrics
        """
        self.metrics.clear()
        logger.info("Reset all metrics")