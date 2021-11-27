## In order to start the server when the pi boots
## edit /etc/rc.local and have it call this file.
## i.e. "./start.sh &"

# Clean repo
git clean -xfd;
git pull;

# Rebuild frontend
cd ./frontend;
npm install;
npm run build -- --prod

# Start server
cd ../backend;
python3 server.py