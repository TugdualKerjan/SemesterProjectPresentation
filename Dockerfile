#docker run -p 80:80 -d -v ~/Documents/OTHER/coding/MUNSite/public:/usr/share/nginx/html nginx     

#Port from 80 to 80 and run in detached mode.
#Link this directory

FROM nginx
EXPOSE 80 80
COPY public/* /usr/share/nginx/html/