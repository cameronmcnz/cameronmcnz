---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Some Docker Commands
blurb: Let's have some fun with Docker
canonical: https://www.mcnz.com/2021/10/18/fun-with-docker.html
---

## Docker Integration



<pre>
git clone https://github.com/cameronmcnz/spock-lizard-docker.git
</pre>
For the next set of steps, use your own name instead of 'cams', and your own dockerhub account instead of cameronmcnz90210.
<pre>

cd spock*

sudo docker build -t cams-rps-service .

sudo docker ps -a

sudo docker images

sudo docker run -p 8085:8080 -t cams-rps-service

sudo docker ps -a

docker login --username=cameronmcnz90210
<provide actual password, not the token>

docker tag **??a70e7b4f9e4d?? cameronmcnz90210/cams-rps-service:first

docker push cameronmcnz90210/cams-rps-service:first

</pre>

Now deploy it with Kubernetes. Use your own image.

<pre>
kubectl create deployment rps --image=cameronmcnz90210/cams-rps-service:first --port=8080 

kubectl expose deployment rps --type=NodePort

kubectl expose deployment rps --type=NodePort

</pre>


