#!/bin/bash

echo "Installing Dev Dashboard..."

git clone https://github.com/jwestgarth/dev-dashboard.git
cd dev-dashboard

pip3 install -r requirements.txt

echo ""
echo "Installation complete."
echo ""
echo "Run with:"
echo ""
echo "python app/main.py"
