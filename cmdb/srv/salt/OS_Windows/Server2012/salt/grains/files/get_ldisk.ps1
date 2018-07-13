[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$LogicalDisk_info = Get-WMIObject Win32_LogicalDisk

write-host "{"
foreach ($i in $LogicalDisk_info)
{
    $line = "`'" + $i.DeviceID + "`': {"
    write-host $line
    $line = "`'DriveType`': `'" + $i.DriveType + "`',"
    write-host $line
    $line = "`'FreeSpace`': `'" + $i.FreeSpace + "`',"
    write-host $line
    $line = "`'Size`': `'" + $i.Size + "`',"
    write-host $line
    write-host "},"
}
write-host "}"
