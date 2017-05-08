rm stdout.txt
echo "Hold On"
cd /
cd /home/pi
rm stdout.txt
echo "Initializing PIGPIOD"
sudo pigpiod
curl http://buildstatuscapone.herokuapp.com/status
sleep 20
echo "Kicking off the script"
sudo python gopi_leds.py &
echo "Script initiated and running in background and tail stdout file created in the root"
