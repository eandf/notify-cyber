export TERM=xterm-256color

# Detect if we need sudo for docker commands (Raspberry Pi)
DOCKER_CMD="docker"
if groups | grep -q docker; then
	DOCKER_CMD="docker"
else
	DOCKER_CMD="sudo docker"
fi

stats() {
	$DOCKER_CMD exec -it $(docker ps | grep "nc-" | awk '{print $1}') bash checkup.sh
}

nce() {
	$DOCKER_CMD exec -it $(docker ps | grep "nc-" | awk '{print $1}') bash
}

report() {
	$DOCKER_CMD exec -it $(docker ps | grep "nc-" | awk '{print $1}') bash checkup.sh | grep "UID\|root\|UTC" | grep -v "minutes" | tail -n 3
	echo
	$DOCKER_CMD exec -it $(docker ps | grep "nc-" | awk '{print $1}') bash checkup.sh | grep "UID\|root\|UTC" | grep -v "minutes" | head -n 2
	echo
	printf "Last RS Feed: "
	curl -s --max-time 10 https://notifycyber.com/rss\?sources\=dr%2Cisg%2Cthn%2Ccaisa | tr "<" "\n" | tr ">" "\n" | grep "GMT" | head -n 1
}

# Additional Pi-specific aliases and functions
alias sl="ls"
alias hidden='ls -a | grep "^\."'
alias c="clear"

space() {
	if [ -z "$1" ]; then
		hidden=$(ls -A | grep "^\." | wc -l | sed 's/^ *//g')
		not_hidden=$(ls | wc -l | sed 's/^ *//g')
		if [ "$hidden" != "0" ] && [ "$not_hidden" != "0" ]; then
			du -hs .[^.]* * | sort -hr
		elif [ "$hidden" != "0" ]; then
			du -hs .[^.]* | sort -hr
		elif [ "$not_hidden" != "0" ]; then
			du -hs * | sort -hr
		fi
	else
		for argument in "$@"; do
			if [[ -d "$argument" ]] || [[ -f "$argument" ]]; then
				du -hs $argument
			fi
		done
	fi
}

# Set vim alias to helix if available
if command -v hx >/dev/null; then
	alias vim="hx"
fi
