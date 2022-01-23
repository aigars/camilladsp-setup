# camilladsp-setup

## Install cammilladsp
git clone https://github.com/HEnquist/camilladsp.git  
cargo build --release  
sudo cargo install --path . --root "/usr/local"  

## Copy config files
sudo cp asound.conf /etc/  

## Setup systemd service
sudo cp camilladsp.service /etc/systemd/system/  
sudo cp camilladsp-watcher.service /etc/systemd/system/  
sudo cp camilladsp-watcher.path /etc/systemd/system/  
sudo systemctl daemon-reload  
sudo systemctl enable camilladsp.service  
sudo systemctl enable camilladsp-watcher.service  
sudo systemctl enable camilladsp-watcher.path  
