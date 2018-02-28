from __future__ import absolute_import

class CeleryConfig(object):
    BROKER_URL = "amqp://webapps:webapps@localhost:5672/webapps_vhost"
    #CELERY_RESULT_BACKEND = "amqp://webapps:webapps@localhost:5672/webapps_vhost"
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Tokyo'