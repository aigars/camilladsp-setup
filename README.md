# camilladsp-setup

## Install cammilladsp
git clone https://github.com/HEnquist/camilladsp.git  
cargo build --release  
sudo cargo install --path .

## Install scripts
cp -r web /home/dsp-user/

## Setup systemd service
sudo cp services/camilladsp.service /etc/systemd/system/  
sudo cp services/camilladsp-watcher.service /etc/systemd/system/  
sudo cp services/camilladsp-watcher.path /etc/systemd/system/  
sudo cp services/camilladsp-configuration.service /etc/systemd/system/  
sudo systemctl daemon-reload  
sudo systemctl enable camilladsp.service  
sudo systemctl enable camilladsp-watcher.service  
sudo systemctl enable camilladsp-watcher.path  
sudo systemctl enable camilladsp-configuration.service

## Get alsa device info
aplay -D hw:CARD=HDSPMxe053ac --dump-hw-params test.wav
