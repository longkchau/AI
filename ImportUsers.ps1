# Define the domain controller and OU
Import-Module ActiveDirectory

$domainController = "ad01.ad.remilon.com"
$OUPath = "OU=Contractors,OU=Content,DC=ad,DC=remilon,DC=com" 

# Connect to the domain controller
$credential = Get-Credential
$session = New-PSSession -ComputerName $domainController -Credential $credential
 

# Get a list of users in the specified OU
$Users = Get-ADUser -Filter 'enabled -eq $true' -Properties * -SearchBase $OUpath | Select-object Name,Title,Manager

# Create a new Excel workbook
$excel = New-Object -ComObject Excel.Application
$workbook = $excel.Workbooks.Add()

# Select the first worksheet in the workbook
$worksheet = $workbook.Worksheets.Item(1)

# Loop through each user in the list and print it to the worksheet
# Set the header row
$HeaderRow = 1
$Worksheet.Cells.Item($HeaderRow, 1) = "Name"
$Worksheet.Cells.Item($HeaderRow, 2) = "Title"
$Worksheet.Cells.Item($HeaderRow, 3) = "Manager"
# Set the row counter
$Row = 3

# Loop through the users and add them to the Excel file
foreach ($User in $Users) {
    $Worksheet.Cells.Item($Row, 1) = $User.Name
    $Worksheet.Cells.Item($Row, 2) = $User.Title
    $Worksheet.Cells.Item($Row, 3) = $User.Manager
    $Row++
}


# Save the workbook to a file
$workbook.SaveAs("C:\Users\lchau\Documents\Projects\file.xlsx")

# Close the workbook and Excel application
$workbook.Close()
$excel.Quit()

# Disconnect from the domain controller
Remove-PSSession $session