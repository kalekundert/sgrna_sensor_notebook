#!/usr/bin/env bash
set -eo pipefail

if [ $# != 1 ]; then
    echo "Usage: format_gel.sh <tif>"
    exit 1
fi

tif=$1
png=${tif%%.tif}.png

if [ -e "$png" ]; then
    echo "$png already exists!  Aborting."
    exit 2
fi

convert \
    ../../data/gels/$tif \
    -fill white \
    -opaque red \
    -negate \
    $png
gimp $png

