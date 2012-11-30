# Usage

sh update.sh <Apple ID> <Password>

# Notes

This will fetch all development and distribution provisioning profiles to a temporary directory. If the fetch is successful, it will delete all existing provisioning profiles from ~/Library/MobileDevice/Provisioning Profiles/ and copy in all of the downloaded provisioning profiles.

If the download fails for any reason the script aborts before touching your installed profiles.
