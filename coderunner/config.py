class CeleryConfig:
    # RabbitMQ
    # BROKER_URL = "amqp://webapps:webapps@localhost:5672/webapps_vhost"
    broker_url = 'redis://localhost:6379'
    result_backend = "rpc://"
    accept_content = ['application/json']
    task_serializer = 'json'
    result_serializer = 'json'
    timezone = 'Asia/Tokyo'
