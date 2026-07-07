#!/bin/bash
set +e

mkdir -p /logs/verifier

pytest /tests/test_outputs.py --ctrf
EXIT_CODE=$?

if [ -f ctrf/ctrf-report.json ]; then
  mv ctrf/ctrf-report.json /logs/verifier/ctrf.json
else
  echo "{}" > /logs/verifier/ctrf.json
fi

if [ $EXIT_CODE -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit 0
