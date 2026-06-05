#!/bin/bash
echo "============================================"
echo "  SUPERBEV - Starting up..."
echo "============================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed on this computer."
    echo ""
    echo "Please install Python 3 from:"
    echo "   https://www.python.org/downloads/"
    echo ""
    echo "After installing, double-click run_game.sh again."
    open "https://www.python.org/downloads/"
    exit 1
fi

echo "Python 3 found. Installing required libraries..."
echo "(This only happens once - future launches will be instant)"
echo ""

pip3 install --upgrade pip --quiet
pip3 install pygame pillow --quiet

echo ""
echo "Launching game..."
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Something went wrong launching the game."
    echo "Please take a screenshot of this window and share it for help."
    read -p "Press Enter to close..."
fi