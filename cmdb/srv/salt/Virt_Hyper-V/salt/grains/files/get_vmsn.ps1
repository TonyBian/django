[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$SN_Info = get-vmhost | foreach-object {Get-WmiObject -ComputerName $_.name -Namespace root\virtualization\v2 -class Msvm_VirtualSystemSettingData | Where-object { $_.BIOSSerialNumber -ne $null } | Where-object { $_.SnapshotDataRoot -ne $null } | select elementname, ConfigurationID, BIOSSerialNumber, VirtualSystemIdentifier}

write-host "{"
foreach ($i in $SN_Info)
{
    $line = "`'" + $i.ConfigurationID + "`': {"
    write-host $line
    $line = "`'ElementName`': `'" + $i.ElementName + "`',"
    write-host $line
    $line = "`'BIOSSerialNumber`': `'" + $i.BIOSSerialNumber + "`',"
    write-host $line
    $line = "`'VirtualSystemIdentifier`': `'" + $i.VirtualSystemIdentifier + "`',"
    write-host $line
    write-host "},"
}
write-host "}"
