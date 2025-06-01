# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject',
             broker='amqp://sammking:passdem@localhost:5672/myvhost',
             backend='rpc://',
             include=['yourapp.tasks'])