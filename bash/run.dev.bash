#!/bin/bash

ROOT=$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")
NAME=${ROOT##*/}
SOCKET_FILE=/tmp/webapps/${NAME}.sock
USER=$(id -un)
GROUP=$(id -gn)
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=project.settings.dev
DJANGO_WSGI_MODULE=project.wsgi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE}"
export PYTHONPATH="${ROOT}":$PYTHONPATH

RUN_DIR=$(dirname "${SOCKET_FILE}")
test -d "${RUN_DIR}" || mkdir -p "${RUN_DIR}"

exec "${ROOT}"/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name "${NAME}" \
    --workers "${NUM_WORKERS}" \
    --user="${USER}"  --group="${GROUP}" \
    --bind=unix:"${SOCKET_FILE}" \
    --log-level=debug \
    --log-file=-
