#!/bin/bash

ROOT=$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")
exec "${ROOT}"/venv/bin/celery worker --app=coderunner.celery.app --loglevel=INFO
