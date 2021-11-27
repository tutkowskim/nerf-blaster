## In order to start the server when the pi boots
## edit /etc/rc.local and have it call this file.
## i.e. "./start.sh &"

cd ./backend;
python3 server.py;
