#!/usr/bin/env bash

set -euxo pipefail

docker build -t nexus:5000/sphinx .
docker push nexus:5000/sphinx

ssh yaba docker-compose images
ssh yaba docker-compose pull sphinx
ssh yaba docker-compose rm -sf sphinx
ssh yaba docker-compose up -d sphinx
ssh yaba docker-compose images
