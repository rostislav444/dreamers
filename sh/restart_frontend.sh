pm2 delete dreamers
pm2 start npm --name "dreamers" --cwd /var/www/dreamers/frontend -- start -- --port 3001

