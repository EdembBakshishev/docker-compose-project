#!/bin/bash

URL="https://www.nropyag.pp.ua/" 

status_code=$(curl -o /dev/null -s -w "%{http_code}" $URL)

if [ $status_code -eq 200 ]; then
  echo "Site is UP"
  exit 0
else
  echo "Site is DOWN. Status code: $status_code"
  exit 1
fi
