#!/bin/bash

# Run query-adsb.sh every 3 min each day from 06:00 ... 21:50

set -euo pipefail

trap '[[ $? == 0 ]] && echo SUCCESS; rm -f "/tmp/cron-$USER-$$"' EXIT

dpkg -l jq &>/dev/null ||
{
	echo "jq not installed." >&2
	exit 1
}

crontab -l |
sed '/hems-lookout/d; $ a */3 6-21 * * * $HOME/hems-lookout/query-adsb.sh' \
	> "/tmp/cron-$USER-$$"

crontab "/tmp/cron-$USER-$$"
