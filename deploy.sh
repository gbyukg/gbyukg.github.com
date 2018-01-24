#!/usr/bin/env bash

gulp build && gulp lunr

cd docs || {
    echo 'Error: no docs fodler was found.'
    exit 1
}

echo 'Init git repository...'
{
    git init && \
    git add . && \
    git commit -m "$(date '+%Y-%m-%d %H:%M:%S')" && \
    git remote add origin git@github.com:gbyukg/gbyukg.github.com.git
} > /dev/null

git push origin master -f
