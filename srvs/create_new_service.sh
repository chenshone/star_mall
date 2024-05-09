#!/bin/bash

generate_directory_structure() {
  local directory=$1
  local depth=$2

  mkdir -p "$directory"

  if [ $depth -gt 0 ]; then
    for dir in handler logs model proto settings test; do
      generate_directory_structure "$directory/$dir" $((depth - 1))
    done
  fi

  if [ "$directory" != "$root_directory/logs" ]; then
    touch "$directory/__init__.py"
  fi

  if [ "$directory" = "$root_directory" ]; then
    touch "$directory/server.py"
  fi
}

if [ $# -ne 1 ]; then
  echo "Usage: $0 <directory_name>"
  exit 1
fi

root_directory=$1

generate_directory_structure "$root_directory" 1
