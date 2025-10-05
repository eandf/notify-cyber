export APP_LOG_FILE_PATH="/app/logfile.log"

# print the last few logs for debugging/checking
logs() {
	tail -n 100 $APP_LOG_FILE_PATH
	echo -e "\033[31m$(date -u +'%m-%d-%Y %H:%M:%S UTC')\033[0m - NOT A LOG, JUST THE CURRENT TIME"
}

# print real errors by removing a lot of "not so important" logs (this is very custom)
realerrors() {
	local log_file="$APP_LOG_FILE_PATH"
	local lines_to_print=10

	# check if "-all" or "-a" option is specified
	if [[ $1 == "-all" || $1 == "-a" ]]; then
		# no limit on the number of lines to print
		lines_to_print=""
	fi

	# set up all the patterns you want to exclude
	local exclude_patterns="INFO|DEBUG|failed to scrape cve|failed to scrape tlix|\
the key recorded in entry|c-teaser__date|successfully scraped from sources|\
data has zero entries|list index out of range|Retrying for scraper dr_get|\
attempting BRUTE FORCE|attempting to scrape_with_webcrawlerapi|\
Get_content\(\) failed to scrape https://www.itsecurityguru.org|\
Get_content\(\) failed to scrape https://www.darkreading.com"

	# apply the exclusion and optionally tail the result
	grep -Ev "$exclude_patterns" "$log_file" |
		if [[ -z "$lines_to_print" ]]; then
			cat
		else
			tail -n "$lines_to_print"
		fi
}

# quickly print some quick stats about the PI and the collector
stats() {
	RED='\033[4;31m'
	NC='\033[0m'

	echo -e "${RED}➜  CURRENT STATE:${NC}\n" # header

	echo "$(date), $(who | wc -l) who(s), $(uptime -p)"

	echo -e "\n${RED}➜  PYTHON PROCESSES:${NC}\n" # header

	{
		ps -fA | head -n 1
		ps -fA | grep "collect" | grep "sh"
	} | awk '{printf "%-10s %-7s %-8s %s\n", $1, $2, $7, substr($0, index($0,$8))}'

	if command -v pydf &>/dev/null; then
		echo -e "\n${RED}➜  TOTAL SYSTEM STORAGE:${NC}\n" # header
		pydf
	fi

	echo -e "\n${RED}➜  LAST LOGS & REAL ERRORS:${NC}\n" # header

	realerrors | tail -n 1 | awk '{print $1, $2, $3, "- Real Error Date"}'
	tail -n 1 $APP_LOG_FILE_PATH
	echo $(date -u +"%m-%d-%Y %H:%M:%S UTC")" - Current Date"
}

# main calls
stats
