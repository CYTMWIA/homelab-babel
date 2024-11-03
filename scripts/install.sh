#! /bin/bash
set -e

git submodule init
git submodule update

pushd modules/iapyc
git checkout master
popd

uv sync
