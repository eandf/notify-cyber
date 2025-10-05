# Run the loop
while true; do
	python3 /app/collector/collector.py
	sleep 3600                   # pause for 60 minutes
	sleep $((RANDOM % 121 + 60)) # pause between 1 - 3 minutes
done
