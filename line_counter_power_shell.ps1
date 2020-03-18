#If does not work run: set-executionpolicy remotesigned (in powershell and in admin mode)
dir -Recurse *.py | Get-Content | Measure-Object -Line