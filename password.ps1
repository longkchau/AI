# Random Password Generator Program in PowerShell

# Set the length of the password
$length = 10

# Define the character set for the password
$charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':\"

# generate the random password
$password = -join (($charset.ToCharArray() | Get-Random -Count $length))

# ask where to save and what is it for funciton... 


# Save the password to a file
$filename = "password.txt"
Add-Content -Path $filename -Value $password

# Print the password to the console
Write-Host "Random Password: $password"
