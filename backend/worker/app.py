import os
from dotenv import load_dotenv
from celery import Celery
import ssl

#load environment variables
load_dotenv()

#get redis url from environment variable
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

#configure SSL for rediss:// connections
broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}

#initialize celery app
app = Celery(
    'keyframe_worker',
    broker=redis_url,
    backend=redis_url,
    # broker_use_ssl=broker_use_ssl,
    # redis_backend_use_ssl=broker_use_ssl
)

# celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_time_limit=300,
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s',  
    imports=(
        'orchestrator', 
    )
)

#import the task from orchestrator
# from orchestrator import process_video_job

#register the task with celery
# app.task(process_video_job)


if __name__ == '__main__':
    app.start()