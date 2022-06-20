# camilladsp-setup

## Install cammilladsp
git clone https://github.com/HEnquist/camilladsp.git  
cargo build --release  
sudo cargo install --path .  

## Install configuration and scripts
sudo cp asound.conf /etc/  
mkdir -p /home/dsp-user/dsp  
cp -r configuration /home/dsp-user/dsp/  
cp -r firs /home/dsp-user/dsp/  
cp -r web /home/dsp-user/  
cp -r scripts /home/dsp-user/  

## Setup systemd service
sudo cp services/camilladsp.service /etc/systemd/system/  
sudo cp services/camilladsp-watcher.service /etc/systemd/system/  
sudo cp services/camilladsp-watcher.path /etc/systemd/system/  
sudo cp services/camilladsp-remote.service /etc/systemd/system/  
sudo cp services/camilladsp-configuration.service /etc/systemd/system/  
sudo cp services/camilladsp-amixer.service /etc/systemd/system/  
sudo systemctl daemon-reload  
sudo systemctl enable camilladsp.service  
sudo systemctl enable camilladsp-watcher.service  
sudo systemctl enable camilladsp-watcher.path  
sudo systemctl enable camilladsp-remote.service  
sudo systemctl enable camilladsp-configuration.service  
sudo systemctl enable camilladsp-amixer.service  

## Configure usb serial device for remote
sudo stty -F /dev/ttyACM0 cs8 115200 -ignbrk -brkint -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts

## Get alsa device info
aplay -D hw:CARD=HDSPMxe053ac --dump-hw-params test.wav  

## Set sample rate for card to 44100
sudo amixer -c0 cget iface=MIXER,name='Internal Clock'  
sudo amixer -c0 cset iface=MIXER,name='Internal Clock' 2  
sudo amixer -c0 cget iface=MIXER,name='System Sample Rate'  
sudo amixer -c0 cset iface=MIXER,name='System Sample Rate' 44100  

## Set clock parameters
sudo amixer -c0 cset iface=MIXER,name='Preferred Sync Reference' 0  
sudo amixer -c1 cset iface=MIXER,name='Preferred Sync Reference' 9  
sudo amixer -c2 cset iface=MIXER,name='Preferred Sync Reference' 9  

sudo amixer -c0 cset iface=MIXER,name='System Clock Mode' 0  
sudo amixer -c1 cset iface=MIXER,name='System Clock Mode' 1  
sudo amixer -c2 cset iface=MIXER,name='System Clock Mode' 1  
