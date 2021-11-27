#! /bin/sh

### BEGIN INIT INFO
# Provides:             nerf-blaster
# Required-Start:       $remote_fs $syslog
# Required-Stop:        $remote_fs $syslog
# Default-Start:        2 3 4 5
# Default-Stop:
# Short-Description:    Nerf Blaster Server
### END INIT INFO

## In order to start the server when the pi boots
## create a link to this file in /etc/init.d
##
## ln nerf-blaster ./start.sh
## sudo update-rc.d nerf-blaster defaults

cd /home/pi/Projects/nerf-blaster/backend;
sudo python3 server.py --port=80;
