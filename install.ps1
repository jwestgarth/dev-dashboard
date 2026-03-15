Write-Host "Installing Dev Dashboard..."

git clone https://github.com/jwestgarth/dev-dashboard.git

cd dev-dashboard

pip install -r requirements.txt

Write-Host ""
Write-Host "Installation complete."
Write-Host ""
Write-Host "Run with:"
Write-Host "python app/main.py"
