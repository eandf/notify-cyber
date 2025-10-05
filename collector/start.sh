# ask the user before continueing because these actions can hurt
read -p "Do you want to continue with building and running the Docker setup? (y/n): " user_input
if [[ ! "$user_input" =~ ^([yY][eE][sS]|[yY])$ ]]; then
	echo "Exiting..."
	exit 1
fi

# kill running nc-collector container if it's running (there should only be one at most)
docker kill $(docker ps | grep "nc-collector" | awk '{print $1}' | head -n 1)

# build docker image for the container
docker build -t nc-collector .

# create and run the docker container for the collector
docker run -d nc-collector

# show listing to see if it's running or not
docker ps
