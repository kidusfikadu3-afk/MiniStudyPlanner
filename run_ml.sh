#!/bin/bash

# Get the folder where this script is saved
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Launching ML Predictor..."
./venv/bin/python ml_gui.py