[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$VMHost_Info = Get-VMHost

write-host "{"
foreach ($i in $VMHost_Info)
{
    $line = "`'" + $i.ComputerName + "`': {"
    write-host $line
    $line = "`'FullyQualifiedDomainName`': `'" + $i.FullyQualifiedDomainName + "`',"
    write-host $line
    $line = "`'VMMigrationEnabled`': `'" + $i.VirtualMachineMigrationEnabled + "`',"
    write-host $line
    $line = "`'MemoryCapacity`': `'" + $i.MemoryCapacity + "`'," 
    write-host $line
    write-host "},"
}
write-host "}"
