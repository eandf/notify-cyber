#!/bin/bash

kill_port() {
	if [[ "$OSTYPE" == "linux-gnu"* ]]; then
		if command -v fuser &>/dev/null && fuser 8001/tcp >/dev/null 2>&1; then
			fuser -k 8001/tcp
		elif command -v lsof &>/dev/null; then
			local pids=$(lsof -ti:8001 2>/dev/null)
			if [[ -n "$pids" ]]; then
				echo "$pids" | xargs kill 2>/dev/null
			fi
		fi
	elif [[ "$OSTYPE" == "darwin"* ]]; then
		if command -v lsof &>/dev/null; then
			local pids=$(lsof -ti:8001 2>/dev/null)
			if [[ -n "$pids" ]]; then
				echo "$pids" | xargs kill 2>/dev/null
			fi
		fi
	elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
		local pids=$(netstat -ano 2>/dev/null | grep :8001 | awk '{print $5}' | sort -u)
		if [[ -n "$pids" ]]; then
			echo "$pids" | xargs -n1 taskkill //F //PID 2>/dev/null
		fi
	fi
}

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null && ! command -v py &>/dev/null; then
	echo "Error: No Python installation found (python3, python, or py)"
	exit 1
fi

if command -v python3 &>/dev/null; then
	PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
	PYTHON_CMD="python"
else
	PYTHON_CMD="py"
fi

echo "Stopping any existing server on port 8001..."
kill_port

echo "Starting Python HTTP server on port 8001..."
$PYTHON_CMD -m http.server 8001 &
SERVER_PID=$!

sleep 1

if ! kill -0 $SERVER_PID 2>/dev/null; then
	echo "Error: Failed to start server"
	exit 1
fi

echo "Server started successfully (PID: $SERVER_PID)"
echo "Opening http://localhost:8001/ in browser..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	xdg-open http://localhost:8001/ 2>/dev/null || sensible-browser http://localhost:8001/ 2>/dev/null || echo "Please open http://localhost:8001/ manually"
elif [[ "$OSTYPE" == "darwin"* ]]; then
	open http://localhost:8001/
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
	start http://localhost:8001/ 2>/dev/null
else
	echo "Please open http://localhost:8001/ manually"
fi

echo "Press Ctrl+C to stop the server"

cleanup() {
	echo ""
	echo "Stopping server..."
	if kill -0 $SERVER_PID 2>/dev/null; then
		kill $SERVER_PID 2>/dev/null
		sleep 1
		if kill -0 $SERVER_PID 2>/dev/null; then
			kill -9 $SERVER_PID 2>/dev/null
		fi
	fi
	kill_port
	echo "Server stopped"
	exit 0
}

trap cleanup INT TERM EXIT
wait $SERVER_PID
