---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Some Docker Commands
blurb: Let's have some fun with Docker
canonical: https://www.mcnz.com/2021/10/18/fun-with-docker.html
---

## Docker Login

I'm not exactly sure why, but an access token does not you to push to your dockerhub account. To do the push, log into docker with your username and PASSWORD, not your token.
<hr/>
<pre>
docker login -u cameronmcnz90210 -p *your-password*
</pre>

## Share Docker Login with Kubernetes

You must make Kubernetes aware of your Docker credentials so it can pull images. This is on page 29 of your lab guide.

Note the space between .json /var

Also, this will need to be done with sudo.
<hr/>
<pre>
sudo cp ~/.docker/config.json /var/lib/kubelet/config.json
</pre>
<hr/>

## Clone a GitHub Repository
<hr/>
<pre>
git clone https://github.com/cameronmcnz/spock-lizard-docker.git
</pre>
<hr/>


## Move into the Spock* Folder and Build Image

For the next set of steps, use your own name instead of 'cams', and your own dockerhub account instead of cameronmcnz90210.

Feel free to name the image something other than 'cams-rps-service'. Just make sure you use that same name throughout.
<hr/>
<pre>

cd spock*

sudo docker build -t cams-rps-service .

sudo docker ps -a

sudo docker images

sudo docker run -p 8085:8080 -t cams-rps-service

sudo docker ps -a


</pre><hr/>

## Push to DockerHub

Make sure you've logged into Docker. Use your own DockerHub ID and password. Don't use cameronmcnz90210

You need to tag your image with your DockerHub username as a prefix.

Name the image anything you want.

<hr/><pre>
docker login --username=cameronmcnz90210
*provide actual password, not the token*

docker tag **??a70e7b4f9e4d?? cameronmcnz90210/cams-rps-service:first

docker push cameronmcnz90210/cams-rps-service:first

</pre>
<hr/>

## Deploy the app with Kubernetes

Now deploy it with Kubernetes. Use your own image.
<hr/>
<pre>
kubectl create deployment rps --image=cameronmcnz90210/cams-rps-service:first --port=8080 

kubectl expose deployment rps --type=NodePort

</pre>

## Run the Web Application
Make sure you start minikube before you do the deployment. Check the syntax of the minikube start command.

Use the URL and port generated by the next step to get the web address of your application:
<hr/>
<pre>
minikube start --driver=none
kubectl expose deployment rps --type=NodePort

</pre>
<hr/>
## Scale your App!
Now scale it!
<hr/>


<hr/><pre>
kubectl scale --replicas=3 deployment/rps

kubectl get deployment
</pre><hr/>
<hr/>


