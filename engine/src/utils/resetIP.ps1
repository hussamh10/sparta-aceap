# Function to convert Subnet Mask to CIDR notation
Function Convert-MaskToCidr {
    param ($NetMask)
    $bits = $NetMask.Split('.') | ForEach-Object { [Convert]::ToString([byte]$_, 2) }
    $cidr = ($bits | ForEach-Object { $_.ToCharArray() } | Where-Object { $_ -eq "1" }).Count
    return $cidr
}

# Configuration
$IPAddress = "128.255.45.133"
$SubnetMask = "255.255.240.0"
$InterfaceName = "Ethernet 2"
$DefaultGateway = "128.255.44.1"
$DnsServers = @("128.255.1.3", "128.255.64.11", "128.255.1.8")

# Remove existing IP configuration for the specified interface
Get-NetIPAddress -InterfaceAlias $InterfaceName | Remove-NetIPAddress -Confirm:$false
Get-NetRoute -InterfaceAlias $InterfaceName | Remove-NetRoute -Confirm:$false

# Set the IP address, Subnet Mask, and Default Gateway
New-NetIPAddress -InterfaceAlias $InterfaceName -IPAddress $IPAddress -PrefixLength (Convert-MaskToCidr -NetMask $SubnetMask) -DefaultGateway $DefaultGateway

# Set the DNS server addresses
Set-DnsClientServerAddress -InterfaceAlias $InterfaceName -ServerAddresses $DnsServers
