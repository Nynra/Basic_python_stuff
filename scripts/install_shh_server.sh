#!/bin/bash
sudo apt update
sudo apt install openssh-server
sudo ufw allow ssh
sudo systemctl status ssh
echo "Sucesfully installed the openssh server, and added exeption to ufw firewall"

