---
layout: mcnz/basic-post
author: Cameron McKenzie
title: How to install Docker in Ubuntu 20
blurb: A quick, 5-minute tutorial on how to install Docker on Ubuntu 20. I use a virtual image here but this Docker & containerd on Ubuntu example works on bare metal too.
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/Jn9iKEjlmio" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
# How to Install Docker on Ubuntu 20

Hey, I'm Cameron Mckenzie, @cameronmcnz on Twitter, and I wanted to talk to you about Docker. Specifically, installing Docker on  Ubuntu 20.0. And then maybe even pulling a container from Docker hub and running it.

 I've got the hello world container I've also got a special Spring Boot micro service app I'm going to try and run as well. 
 
 You can see here I've got a base install of Ubuntu 20.04 and the only thing I've done here is add the terminal to my favorites I put a little bit of text inside of this text file to guide me through the installation of Docker on Ubuntu. I've also got a little Firefox browser open to my Docker hub account where I've got a Docker container hosted over there called rock paper spring I thought it might be nice to prove that Docker is installed on Ubuntu successfully by running that little Spring Boot microservice container.

First things first. You want to update the app package index and make sure that we can install all of our components over https so we first do the sudo apt-get update throw my password in there and once that's done the next line is installing all of these components here as I said this will allow me to do the update over https so that means installing app transport ca certificates curl new pg agents some software common properties anyways that all gets in there and it gets done fairly quickly.

## Download and install Docker on Ubuntu

 Once that's done we use the curl that we just installed to grab Docker's official gpg key there we go it doesn't take long to download a gpg key once we've got that we want to grab the stable debs the stable binaries the stable information about Docker so we go to downloads.docker.com. I'm on the focal version of Ubuntu I want a stable release you could have a test release you could have a nightly release too and now we're going to add all of the information about that deb to our local repository this should only take a second.

 Once this completes we're going to do the sudo apt update once again you can never ever do the sudo apt update too many times I might even do a little sudo app cache policy just to see what we've got available to us.

## docker-ce docker-cli & containerd.io on Ubuntu
 
 We've got all sorts of different archives available to you that's too much for me to even keep track of you know what I'm just going to do the basic install Docker ce I'm not going to specify a version or anything like that I'm going to say sudo apt-get install docker-ce docker-cli containerd.io and that's going to go ahead and that's going to install Docker.

 I click yes on that yes no option okay that's complete it might be nice to take a look at the version of Docker that we're running so we'll do a sudo Docker version 20.10.3.

 I'm pretty happy with that. Maybe we can take a little look at the status see if the process is actually running looks like we've got everything running it's active it's running I'm pretty happy about that you know anytime you install Docker it is customary to do the old Docker hello world so I'm going to do a sudo Docker run hello world.

### Docker Ubuntu HelloWorld container
 
 hello world is a container hosted over on Docker hub and you see it says hey I can't find this image locally is that first command but it searches for it it downloads it it says it's pulling it it's pulling it from Docker hub it downloads it and says hey hello from Docker that's all it does it's not that interesting but it proves that things are working it's also cool if you go sudo Docker images you'll notice that that hello world image is registered.
 
 I've got a little container over on Docker hub it runs on port 8080 so I got to do a little razzle dazzle if I want that one to run so I do sudo Docker run it runs internally on port 8080 I'm going to map that to port 8088 and say hey I want to run my rock paper scissors container I'll click enter notice it again says can't find cameron mckenzie locally but there is this one over on Dockerhub.com hub.Docker.com. There's my account and there's the little repository that we are trying to download it's only going to take a second.

### Spring Boot Microservice on Docker

You'll notice It's a Spring Boot application running in Docker. You can see the spring banner that just came up there a second ago I'm going to drag up there to see if we can see it just to prove what it is you can see spring there see some references to Hibernate and JPA in there because that Spring Boot applications uses that for a little bit of persistence only took about seven and a half seconds for that to run and now let's see if we can run that locally in our browser.


 I incorrectly typed localhost:8080. Of course I mapped it to localhost:8088 and so you got to have the right port mapping otherwise of course it's not going to work and there we go index.html like I had originally except I didn't have the right port number and then there's our little rock paper scissors game so can we play the game we can keep playing rock paper and scissors if you can figure out the trick well you can win every time but there you go that's a little Spring Boot application running in Docker pulled from Docker hub all within just about five minutes doing the installation.

 And that's about it and there you go that's how easy it is to install Docker on Ubuntu 20 and run a couple of containers from Docker hub including the hello world and a beautiful little rock paper scissors done with a Spring Boot now if you enjoyed that tutorial I want you to head over to theserverside.com. I'm the Editor-in-Chief over there we've got lots of great tutorials on spring Docker devops you name it if you're interested in my personal antics you can always follow me on twitter @cameronmcnz and subscribe on the Youtube.
 
 
#### Commands to install Docker on Ubuntu
 
 
<pre>
sudo apt update

sudo apt install apt-transport-https ca-certificates curl  gnupg-agent  software-properties-common

curl -fsSL https://download.docker.com/linux/ubu...​ | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu​ focal stable"

sudo apt update

sudo apt-cache policy 

sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo systemctl status docker

sudo docker run hello-world

sudo docker run -p 8088:8080 -t cameronmcnz/rock-paper-docker

localhost:8088/index.html

 </pre>
