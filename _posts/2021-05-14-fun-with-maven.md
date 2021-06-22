---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Maven Jenkins Bash Commands
blurb: Some commands and code for maven and Jenkins
canonical: https://www.mcnz.com/2021/05/14/fun-with-maven.html
---


<pre>
<code>

ls
cd target
ls

java -jar spock-lizard-1.0.jar --server.port=8088 & echo $! > pid.pid

cat pid.pid

sleep 15
echo "**********"

webpage_http_status_code=$(curl --head --silent http://localhost:8088/increasewins | head -n 1)
echo $webpage_http_status_code

echo "**********"

curl http://localhost:8088/increasewins



JSON=$(curl http://localhost:8088/increasewins)
WINS='wins'
if [[ "$JSON" == *"$WINS"* ]]; 
then
  echo "The JSON string is valid."
else
  echo "The JSON string is not valid. Failing the build..."
  kill -9 $(cat pid.pid)
  exit 1
fi

echo "**********"

kill -9 $(cat pid.pid)
</pre>
</code>
