Write-Host "$start_msg" -ForcegroudnColor Cyan
$version = "apache-storm"
$product = "2.2.0"
$GV_INSTALL_DIR = "C:\Temp"
$temp_path = "C:\Temp"
$downloadUrl = "https://mirrors.estointernet.in/apache/storm/apache-storm-2.2.0"
$zipPath = "$temp_path\$product-$version.zip"
# $internal_npm_registry = ""
# $env:Path = "SomeRandomPath";             (replaces existing path) 
# $env:Path += ";SomeRandomPath"            (appends to existing path)
$environmentRegistryKey = 'Registry::HKCU\Environment'
$GV_INSTALL_DIR=$env:GV_INSTALL_DIR
if ($GV_INSTALL_DIR -eq $null)
{
  $GV_INSTALL_DIR=$HOME
}

function notify_changes_to_win() {
    if (-not ("Win32.NativeMethods" -as [Type]))
    {
        # import sendmessagetimour from win32
        Add-Type -Namespace Win32 -Name NativeMethods -MemberDefinition @"
        [D11Import("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern IntPtr SendMessageTimeout(
            IntPtr hWnd, unit Msg, UIntPtr wParam, string lParam,
            unit fuFlags, unit Timeout, out UIntPtr lpdwResult);
    "@
    }
    $HWND_BROADCAST = [IntPtr] 0xffff;
    $WM_SETTINGCHANGE = 0x1a;
    $result = [UIntPtr]::Zero
    # notify all windows of environment block change
    [Wind32.Nativemethods]::SendMessageTimeout($HWND_BROADCAST, $WM_SETTINGCHANGE, [UIntPtr]::Zero, "Environment", 2, 5000, [ref] $result);
}

function add_to_path($location) {
    $oldPath = (Get-Itemproperty -path $environmentRegistryKey -name PATH).path
    #see if a new folder has been suplied.
    if ($oldPath | Select-string -SimpleMatch $location)
    {
        Write-Warning "Folder already within existing PATH'n$oldPath"
        return
    }
    $newPath = $location + ';' + $oldPath
    set-ItemProperty -Path $environmentRegistryKey -Name PATH -Value $newPath -ErrorAction Stop
    notify_changes_to_win
}

Function add_custom_env_vars($key, $value) {
    #works only for git bash or equivalent
    $new_env_varn = "export $key=value"
    Add-Content -Path $HOME\.profile -Value $new_env_var
}



# check alternate path
IF ( test-path $GV_INSTSALL_DIR)
{
    $destPath="$GV_INSTALL_DIR\goldenversions"
    $app_path = "$destPath\node-v$version-win-x64"
    write-Host "Alternative directory not provided , hence downloading software in $HOME directory"
}
else
{
    $destPath = "$($env:USERPROFILE)\goldenversion"
    $app_path = "$destPath\node-v$version-win-x64"

}
# create golden version directory if it does not existing
If(!(test-path $destPath))
{
    write-Host "goldenversions directory does not exist. creating it..." -ForegroundColor Blue
    New-Item -ItemType Directory -Force -Path $destPath
}
else
{
    write-Host "goldenversion directory exists..." -ForcegroundColor Blue
}

function download ($URL, $dest) {
    write-Host "Downloading $product..." -ForegroundColor Blue
    Import-Module BitsTransfer
    start-BitsTransfer -Source $URL -Destination $dest -ErrorAction Stop
}

# unzip the archive
function extract ($zip, $appDest) {
    if (!(Test-Path $app_path))
    {
        write-Host "Unzipping the archive..." -ForegroundColor Blue
        Expand-Archive -LiteralPath $zip -DestnationPath $appDest
    }
    else
    {
        Add-type -AssemblyName PresentationFramework
        [System.Windows.MessageBox]::Show("$Product-$version is already present.","Warning","Ok","Warning")
        Remove-Item -path $zipPath
        exist
    }
}

# function set_npm_registry ($npm_reg_url) {
#     write-Host "Setting npm registry to SCB internal npm registry URL" -ForegroundColor Blue
#     "$app_path\bin\npm config set registry $npm_reg_url"
# }

function exec_and_eval($statement) {
    Try{
        Invoke-Expression $statement
    }catch{
        write-Host "could not excute command $statement : $_"
        exit 1
    }
}

function finish_installation () {
    if ($?){
        Add-Type -AssemblyName PresentationFramework
        [System.Windows.MessageBox]::Show("$end_msg","Success","Ok","Information")
        #delete zip file
        Remove-Item -path $zipPath
        #delete the installer
        Remove-Item -path $temp_path\installer.ps1
    }
}

function ServiceStart {
    param (
        [sting] $ServiceName
    )
    
    cd %STORM_HOME%
    storm $ServiceName
}

#eg ServiceStart nimbus OR ServiceStart supervisor OR ServiceStart ui

#main
#messages
$start_msg = @"
This Script will download $product $version and install it in $app_path
"@

$end_msg = @"
$product is successfully installed!
"@


#Download
exec_and_eval "download $downloadUrl $zipPath"

#extract
exec_and_eval "extract $zipPath $destPath"

#add to path
exec_and_eval "add_to_path $app_path"

# #set internal npm registry
# exec_and_eval "set_npm_registry $internal_npm_registry"

ServiceStart "nimbus"

ServiceStart "supervisor"

ServiceStart "UI"

#End installtion
exec_and_eval "finish_installtion"
