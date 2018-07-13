[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$nameservers_info = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object {$_.ServerAddresses -ne "{}"}

write-host "{"
foreach ($i in $nameservers_info)
{
    $line = "`'" + $i.InterfaceAlias + "`': `'" + $i.ServerAddresses + "`',"
    write-host $line
}
write-host "}"
