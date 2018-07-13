[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$VM_Info = Get-VM

write-host "{"
foreach ($i in $VM_Info)
{
    $line = "`'" + $i.VMId + "`': {"
    write-host $line
    $line = "`'VMName`': `'" + $i.VMName + "`',"
    write-host $line
    $line = "`'ComputerName`': `'" + $i.ComputerName + "`',"
    write-host $line
    $line = "`'Path`': `'" + $i.Path + "`',"
    write-host $line
    $line = "`'CreationTime`': `'" + $i.CreationTime + "`'," 
    write-host $line
    $line = "`'State`': `'" + $i.State + "`'," 
    write-host $line
    $line = "`'ReplicationMode`': `'" + $i.ReplicationMode + "`'," 
    write-host $line
    $line = "`'MemoryAssigned`': `'" + $i.MemoryAssigned + "`'," 
    write-host $line
    $line = "`'MemoryStartup`': `'" + $i.MemoryStartup + "`'," 
    write-host $line
    $line = "`'Notes`': `'" + $i.Notes + "`'," 
    write-host $line
    write-host "},"
}
write-host "}"
