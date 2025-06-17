#!/bin/sh
celery -A monitoria worker --loglevel=info &
python worker_dummy.py
