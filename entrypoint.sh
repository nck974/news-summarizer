#!/bin/bash

# Export all Docker environment variables to a file. This sed is needed
# to be able to source env variables with spaces
printenv | sed 's/^\([^=]*\)=\(.*\)$/export \1="\2"/' > /etc/environment

# Set cron
echo "${CRON_PATTERN} /bin/bash -c 'source /etc/environment && cd /app && /usr/local/bin/python /app/main.py' > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/news-summarizer
chmod 0644 /etc/cron.d/news-summarizer
crontab /etc/cron.d/news-summarizer

# Start cron in foreground
exec cron -f
