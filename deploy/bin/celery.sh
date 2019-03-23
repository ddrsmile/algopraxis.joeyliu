#!/bin/bash

DEPLOYDIR=$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")
ROOT=$( dirname $DEPLOYDIR)
DJANGODIR=${ROOT}/src

cd ${DJANGODIR}
exec ${DEPLOYDIR}/venv/bin/celery worker --app=coderunner.celery.app --loglevel=INFO
