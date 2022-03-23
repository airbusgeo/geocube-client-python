#!/bin/bash

set -x

# loop_exec automatically restarts command in case of failure
function loop_exec () {
    while :
    do
        echo "start '$1'"
        $1
        sleep $2
    done
}

# We start Downloader.
loop_exec "/usr/bin/downloader -port 8083 -with-gcs" 10 > /var/log/downloader_output.log 2>&1 &

# We start by adding extra apt packages, since pip modules may required library
if [ "$EXTRA_APT_PACKAGES" ]; then
    echo "EXTRA_APT_PACKAGES environment variable found.  Installing."
    apt update -y
    apt install -y $EXTRA_APT_PACKAGES
fi

if [ "$EXTRA_PIP_PACKAGES" ]; then
    echo "EXTRA_PIP_PACKAGES environment variable found.  Installing".
    python3 -m pip install $EXTRA_PIP_PACKAGES
fi

# Run extra commands
exec "$@" > /var/log/python_output.log 2>&1