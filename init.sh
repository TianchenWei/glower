#!/bin/bash

script_path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "Script Path: $script_path"
function sbt(){
  local user="winter" # User defined in your .ssh/config
  local host="s0" # Host defined in your .ssh/config
  $script_path/bin/sb "$@" --remote-user "$user@$host" --remote-home /home/$user
}
complete -F _sb_completions -o dirnames sbt



