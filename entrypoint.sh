#!/bin/bash
# Set virtual memory limit to 5 MiB (5242880 bytes)
ulimit -v 5242880

# Execute the main Python script and redirect output to a log file
exec uv run python -m memory_profiler submissions/main.py
