#!/bin/bash

# Pull ADS-B data from adsbexchange.com's API
# https://rapidapi.com/adsbx/api/adsbexchange-com1/

set -euo pipefail

readonly SCRIPTDIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))

cd "$SCRIPTDIR"
source "$HOME/hems-lookout.conf"

readonly lat=51.0
readonly lon=10.3
readonly radius=360 # nautical miles, see https://jsfiddle.net/1jsaw50m/ for coverage

d=$(date +%F)
t=$(date +%H-%M)

# Pull json data and store in folders by date
[ -d "data/adsb/$d" ] || mkdir -p "data/adsb/$d"
[ -d "data/hems/$d" ] || mkdir -p "data/hems/$d"

curl -sS https://adsbexchange-com1.p.rapidapi.com/v2/lat/$lat/lon/$lon/dist/$radius/ \
	--header "X-RapidAPI-Host: adsbexchange-com1.p.rapidapi.com" \
	--header "X-RapidAPI-Key: $RAPIDAPI_KEY_ADSBEXCHANGE" \
	> "data/adsb/${d}/${d}_${t}.json"

# Filter HEMS by squawk 0020/0034 and regex.
# For compatibility, prepend format description
regex="^(AIRESC|C|CH(R|XE?)|DOC|DRAGO|KR|LIFELN|MEDIC|NHX|RESQ|RGA|RK|SA(MU|REX))[0-9]+[A-Z]* *"

jq '{
"time": '$(date +%s)',
"desc": [
	"icao24",
	"callsign",
	"reg",
	"squawk",
	"lat",
	"lon",
	"alt(baro)[ft]",
	"vrate(baro)[ft/min]",
	"track[deg]",
	"groundspeed[kts]"
],
"states": [
	.ac[] |
	select((.squawk == ("0020", "0034")) or
			(.flight // "" | match("'"$regex"'"))) |
			[
				.hex,
				.flight,
				.r,
				.squawk,
				.lat,
				.lon,
				.alt_baro,
				.baro_rate,
				.track,
				.gs
			]
] | unique
}' "data/adsb/${d}/${d}_${t}.json" \
>  "data/hems/${d}/${d}_${t}.json"

"$SCRIPTDIR/notify.py" "data/hems/${d}/${d}_${t}.json"

# Compress original JSON
xz -z9 "data/adsb/${d}/${d}_${t}.json"
