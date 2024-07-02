#!/bin/bash

readonly SCRIPTDIR=$(dirname "${BASH_SOURCE[0]}")

ssh flugplan@fra-flugplan.de mkdir -p hems-lookout

rsync -av "$SCRIPTDIR/" flugplan@fra-flugplan.de:hems-lookout \
	--filter='+ gcmath.py' \
	--filter='+ install.sh' \
	--filter='+ notify.py' \
	--filter='+ query-adsb.sh' \
	--filter='- *' \
	"$@"
