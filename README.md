# camilladsp-setup

## Install cammilladsp
git clone https://github.com/HEnquist/camilladsp.git  
cargo build --release  
sudo cargo install --path . --root "/usr/local"  

## Copy config files
sudo cp asound.conf /etc/  

## Setup systemd service
sudo cp services/camilladsp.service /etc/systemd/system/  
sudo cp services/camilladsp-watcher.service /etc/systemd/system/  
sudo cp services/camilladsp-watcher.path /etc/systemd/system/  
sudo cp services/camilladsp-remote.service /etc/systemd/system/  
sudo cp services/camilladsp-configuration.service /etc/systemd/system/  
sudo systemctl daemon-reload  
sudo systemctl enable camilladsp.service  
sudo systemctl enable camilladsp-watcher.service  
sudo systemctl enable camilladsp-watcher.path  
sudo systemctl enable camilladsp-remote.service  
sudo systemctl enable camilladsp-configuration.service


## Get alsa device info
aplay -D hw:CARD=HDSPMxe053ac --dump-hw-params test.wav

## Set sample rate for card to 44100
sudo amixer -c0 cget iface=MIXER,name='Internal Clock'
sudo amixer -c0 cset iface=MIXER,name='Internal Clock' 2
sudo amixer -c0 cget iface=MIXER,name='System Sample Rate' 
sudo amixer -c0 cset iface=MIXER,name='System Sample Rate' 44100
