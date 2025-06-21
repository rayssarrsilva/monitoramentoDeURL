#!/bin/sh
celery -A monitoria beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
python worker_dummy.py
