
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/bus_backend/nginx/nginx.conf /etc/nginx/sites-available/bus_backend
sudo ln -s /etc/nginx/sites-available/bus_backend /etc/nginx/sites-enabled/bus_backend
#sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx

