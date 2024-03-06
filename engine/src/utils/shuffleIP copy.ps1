function Test-InternetConnection {
    try {
        $response = Test-Connection -ComputerName "www.google.com" -Count 1 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}


# set the IP address of the interface as the one given in ipaddress.txt file
function Set-IP {
    param (
        [string]$interfaceName,
        [string]$ipAddress,
        [string]$subnetMask,
        [string]$defaultGateway,
        [string[]]$dnsServers
    )
    $ipAddress = Get-Content "ipaddress.txt"

    Get-NetIPAddress -InterfaceAlias $InterfaceName | Remove-NetIPAddress -Confirm:$false
    Get-NetRoute -InterfaceAlias $InterfaceName | Remove-NetRoute -Confirm:$false
    # Set the new IP address
    New-NetIPAddress -InterfaceAlias $interfaceName -IPAddress $ipAddress -PrefixLength 20 -DefaultGateway $defaultGateway
    Set-DnsClientServerAddress -InterfaceAlias $interfaceName -ServerAddresses $dnsServers
}

# load the IP address from the file


function Increment-IPAddress {
    param (
        [string]$IPAddress
    )

    $ipParts = $IPAddress.Split('.')
    [int]$lastByte = $ipParts[3]
    if ($lastByte -lt 255) {
        $lastByte++
        $ipParts[3] = $lastByte.ToString()
        return $ipParts -join '.'
    } else {
        throw "IP Address incrementation exceeded subnet range."
    }
}

# Configuration
$interfaceName = "Ethernet 2"
$subnetMask = "255.255.240.0"
$defaultGateway = "128.255.44.1"
$dnsServers = @("128.255.1.3", "128.255.64.11", "128.255.1.8")

# Get current IP Address
$currentIPAddress = (Get-NetIPAddress -InterfaceAlias $interfaceName -AddressFamily IPv4).IPAddress

# Main loop
do {
    $newIPAddress = Increment-IPAddress -IPAddress $currentIPAddress

    Get-NetIPAddress -InterfaceAlias $InterfaceName | Remove-NetIPAddress -Confirm:$false
    Get-NetRoute -InterfaceAlias $InterfaceName | Remove-NetRoute -Confirm:$false
    # Set the new IP address
    New-NetIPAddress -InterfaceAlias $interfaceName -IPAddress $newIPAddress -PrefixLength 20 -DefaultGateway $defaultGateway
    Set-DnsClientServerAddress -InterfaceAlias $interfaceName -ServerAddresses $dnsServers

    # Wait for a moment to allow network settings to apply
    Start-Sleep -Seconds 30

    # Check Internet Connectivity
    $hasInternet = Test-InternetConnection

    if ($hasInternet) {
        Write-Host "Successfully changed IP to $newIPAddress and confirmed internet connectivity."
        break
    } else {
        Write-Host "IP $newIPAddress did not provide internet connectivity. Trying next IP..."
        $currentIPAddress = $newIPAddress
    }

    # Clear the existing IP configuration before the next loop iteration

    Get-NetIPAddress -InterfaceAlias $InterfaceName | Remove-NetIPAddress -Confirm:$false
    Get-NetRoute -InterfaceAlias $InterfaceName | Remove-NetRoute -Confirm:$false
    Remove-NetIPAddress -InterfaceAlias $interfaceName -IPAddress $currentIPAddress -Confirm:$false

} while ($true)
