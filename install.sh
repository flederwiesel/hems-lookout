#!/bin/bash

# Run query-adsb.sh every 3 min each day from 06:00 ... 21:50

set -euo pipefail

_trap()
{
	local status="$1"
	local lineno="$2"
	local line=$(sed -n "$lineno p" "$0")

	sed $'s/\\\\033/\033/g' <<-EOF >&2
		\033[1;37;41m*** FAILED ***\033[m
		[=\033[1;37m$status\033[m] \033[36m$0($lineno)\033[m: \033[1;37m$line\033[m
		EOF
}

trap '_trap $? $LINENO' ERR

# query-adsb.sh needs `jq`
dpkg -l jq &>/dev/null ||
{
	echo "jq not installed." >&2
	exit 1
}

if [ -f "$HOME/hems-lookout.conf" ]; then
	source "$HOME/hems-lookout.conf"
fi

# If HEMS_LOOKOUT_FCM_AUTH not set, try setting to found file
if [[ ! ${HEMS_LOOKOUT_FCM_AUTH:-} ]]; then
	if [ -f "$HOME/hems-lookout-fcm.json" ]; then
		HEMS_LOOKOUT_FCM_AUTH="$HOME/hems-lookout-fcm.json"
	fi
fi

[[ ${HEMS_LOOKOUT_FCM_AUTH:-} ]] ||
{
	echo "Unable to determine firebase credentials. Cannot continue." >&2
	exit 1
}

readonly SCRIPTDIR=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

# Setup venv
uv sync

# Adjust crontab
crontab < <(
crontab -l | sed '/hems-lookout/d' || true # An empty crontab would error out
echo "*/3 7-22 * * * '$SCRIPTDIR/query-adsb.sh'"
)
