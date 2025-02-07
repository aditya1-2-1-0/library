# tasks.py in one of your Django apps

from celery import shared_task

@shared_task
def my_task():
    # Your task logic here
    return "Task completed!"
