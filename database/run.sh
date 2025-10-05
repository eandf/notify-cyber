if [ $(docker container list | grep "pgDB" | wc -l) -eq 0 ]; then
	echo "Creating new Postgres Docker Container..."
	docker run --name "pgDB-$(date +%s)" -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres
	echo "Created container, waiting 5 seconds before psql into it..."
	sleep 5
fi

docker exec -it $(docker container list | grep 'postgres' | awk '{print $1}') psql -U postgres
