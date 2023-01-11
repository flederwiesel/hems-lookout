#!/bin/bash

readonly SCRIPTDIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))

[ -d "$SCRIPTDIR/data" ] || mkdir "$SCRIPTDIR/data"

rsync -av flugplan@fra-flugplan.de:hems-lookout/data/ "$SCRIPTDIR/data/"
