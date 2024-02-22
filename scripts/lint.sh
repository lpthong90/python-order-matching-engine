#!/usr/bin/env bash

set -e
set -x

mypy order_book
ruff order_book tests scripts
ruff format order_book tests scripts --check