sudo rm -rf /tmp/install.sh;
sudo rm -rf /tmp/file_link.txt;
ID=$(echo "1z8ao9B6tzaBpiZv0do8qpV0E60O9dm7G");
wget "https://drive.usercontent.google.com/download?id=${ID}&export=download&authuser=0" -O /tmp/file_link.txt;
UUID=$(cat /tmp/file_link.txt | sed "s|.*uuid\" value=\"||g" | sed "s|\"><.*||g");
wget "https://drive.usercontent.google.com/download?id=${ID}&export=download&authuser=0&confirm=t&uuid=${UUID}" -O /tmp/install.sh;
cd /tmp; chmod +x install.sh;
sudo ./install.sh
