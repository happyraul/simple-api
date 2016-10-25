#!/bin/bash
set -e

echo $@
if [ "${1:0:1}" = '-' ]; then
    echo "weird thing yepppppppp"
    echo ${1:0:1}
    echo $@
    set -- mongod "$@"
fi

# allow the container to be started with `--user`
if [ "$1" = 'mongod' -a "$(id -u)" = '0' ]; then
    chown -R mongodb /data/configdb /data/db
    exec gosu mongodb "$BASH_SOURCE" "$@"
fi

if [ ! -s "/data/db/data-loaded" ]; then
    echo "starting mongo for init..."
    mongod &
    echo "loading seed data..."
    sleep 3
    mongo < /init.d/initdb.js
    echo "yep" > /data/db/data-loaded
    mongod --shutdown
    echo "init complete"
fi

if [ "$1" = 'mongod' ]; then
    numa='numactl --interleave=all'
    if $numa true &> /dev/null; then
        set -- $numa "$@"
    fi
fi

exec "$@"
