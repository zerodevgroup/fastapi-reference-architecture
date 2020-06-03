#/bin/bash

cd app
gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker --daemon main:app
