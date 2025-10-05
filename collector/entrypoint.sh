#!/bin/bash

set -e

# if no arguments are passed, execute the collect.sh script
if [ "$#" -eq 0 ]; then
	exec bash /app/collect.sh
else
	# otherwise, execute the provided command
	exec "$@"
fi
