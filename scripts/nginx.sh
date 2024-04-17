
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

echo "Reloading system daemon"
sudo systemctl daemon-reload || { echo "Failed to reload daemon"; exit 1; }

echo "Removing default nginx site"
sudo rm -f /etc/nginx/sites-enabled/default || { echo "Failed to remove default site"; exit 1; }

echo "Copying nginx configuration file"
sudo cp /home/ubuntu/bus_backend/nginx/nginx.conf /etc/nginx/sites-available/nginx.conf || { echo "Failed to copy nginx.conf"; exit 1; }

echo "Testing nginx configuration and restarting nginx"
sudo nginx -t && sudo systemctl restart nginx || { echo "Failed to test or restart nginx"; exit 1; }

echo "Adding ubuntu user to www-data group"
sudo gpasswd -a www-data ubuntu || { echo "Failed to add user to group"; exit 1; }

echo "Script completed successfully"

