# Run from the script directory
if ($PSScriptRoot) {
	Set-Location $PSScriptRoot
} else {
	Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)
}

Write-Host "Checking for Python..."

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
	Write-Host "Using python from PATH:`t$($pythonCmd.Source)"
	python gui_app.py
	exit
}

try {
	$pyVersion = (& py -3 --version) -join ""
	if ($pyVersion) {
		Write-Host "Using py launcher:`t$pyVersion"
		py -3 gui_app.py
		exit
	}
} catch {
	# ignore
}

$known = "C:\Users\hp\AppData\Local\Programs\Python\Python313\python.exe"
if (Test-Path $known) {
	Write-Host "Using known Python path:`t$known"
	& $known gui_app.py
	exit
}

Write-Host "Python interpreter not found."
Write-Host "- Install Python from https://www.python.org/downloads/ and enable 'Add Python to PATH'."
Write-Host "- Or disable the Microsoft Store app execution alias: Settings → Apps → Advanced app settings → App execution aliases."
Write-Host "After installing or adjusting aliases, reopen the terminal and run this script again."
