$Cmd = "mv /var/www/icoatlas-pro/backend/* /var/www/icoatlas-pro/ 2>/dev/null; rmdir /var/www/icoatlas-pro/backend 2>/dev/null; docker ps --format '{{.Names}}'; systemctl restart icoatlas-pro-api; sleep 2; systemctl status icoatlas-pro-api --no-pager"
$SSH_CMD = "ssh -i $env:USERPROFILE\.ssh\id_rsa -o StrictHostKeyChecking=no root@80.211.196.34 `"$Cmd`""
Invoke-Expression $SSH_CMD
