#usr/bin/bash
cont_name=$1
sudo docker build -t print_image .  
sudo docker run  -t -i --privileged -v /var/run/cups/cups.sock:/var/run/cups/cups.sock -d --restart always --name $cont_name -p 8080:8080 print_image
