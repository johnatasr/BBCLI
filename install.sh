#!/bin/bash

if [[ "$(uname)" == "Linux" ]]; then
    if [[ -f /etc/os-release ]]; then
        source /etc/os-release
        if [[ "$ID" == "debian" || "$ID" == "ubuntu" ]]; then
            echo "Detected Debian/Ubuntu. Proceeding with installation..."
            if command -v python3.12 &>/dev/null; then
                echo "Python 3.12 is already installed."
            else
                echo "Python 3.12 is not installed. Installing..."
                sudo apt update
                sudo apt install python3.12 python3.12-venv
            fi
            python3.12 -m venv bbclienv
            cd bbclienv/bin && source activate && cd .. && cd ..
            pip install poetry
            poetry install
            alias bbcli="python main.py"
        else
            echo "Sorry! This script is allowed only for Debian-based systems."
        fi
    else
        echo "Unable to determine the distribution. Please run this script on a Debian-based system."
    fi
else
    echo "This script is intended for Linux systems. Exiting..."
fi
