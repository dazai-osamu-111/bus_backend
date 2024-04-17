
# #!/usr/bin/bash

# sudo systemctl daemon-reload
# sudo rm -f /etc/nginx/sites-enabled/default

# sudo cp /home/ubuntu/bus_backend/nginx/nginx.conf /etc/nginx/sites-available
# sudo ln -s /etc/nginx/sites-available /etc/nginx/sites-enabled/nginx.conf
# #sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
# sudo nginx -t
# sudo gpasswd -a www-data ubuntu
# sudo systemctl restart nginx

#!/usr/bin/bash

sudo systemctl daemon-reload || exit 1
sudo rm -f /etc/nginx/sites-enabled/default || exit 1

sudo cp /home/ubuntu/bus_backend/nginx/nginx.conf /etc/nginx/sites-available/nginx.conf || exit 1
sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf || exit 1

sudo nginx -t && sudo systemctl restart nginx || exit 1
sudo gpasswd -a www-data ubuntu || exit 1

