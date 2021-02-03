---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Install Kubernetes minikube on Ubuntu 20
blurb: A quick, 5-minute tutorial on how to install Kubernetes minikube on Ubuntu 20. I use a virtual image here but this Kubernetes minikube on Ubuntu example works on bare metal too.

---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/DaQLWrS04h8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
# How to Install Kubernetes minikube & containerd on Ubuntu 20

Hey, I'm Cameron McKenzie, @cameronmcnz on Twitter, and I wanted to show you how to install Kubernetes minikube on Ubuntu 20 and even pull a container from [my Dockerhub account](https://hub.docker.com/u/cameronmcnz). 

In my case it'll be a Spring Boot microservice based container. I'll actually deploy it and run it on minikube Kubernetes.

## Docker and minicube

As you can see I've got a pretty basic installation of Ubuntu 20 right here, although I did just install Docker. If I do docker version you'll see that I've got docker 20.10.3 installed. 

Now I want to do a little bit of Kubernetes work and in order to do some Kubernetes work well I'm going to install minicube. There's a couple of things I need to do before I install minicube. I'm going to do a sudo apt-get update and pass in my password and I'll do a little update there do a little sudo apt get upgrade after that's done.

There's a few little tools that you need to install to make sure that mini cube's going to work and I found that a couple of the tutorials oline left out a few of these and it was a little bit annoying. So I'm going to install these one by one.

I'm installing socat. I'm just going to do demonstrate a install of curl but that's all been installed already and I believe that when I did the https based repo installation I had the app transporter there I don't think I've got contract in and this one you're going to need if you do some port forwarding so that one's important and that was just so you saw a contract there and then finally I'm going to install a virtual bo

And we'll do this with the sudo app install virtual box right there.

### Download minikube on Ubuntu

Now it's time to actually just download go and download minicube so that's the next step here so I'm going to paste in this url do the wget on the minicube latest release and so that's going to do a little bit of a download there once the download is complete I'm actually going to copy that file to user local bin mini cube and so I do this command sudo copy mini cube linux amd64 to this mini cube directory and then of course we want to have rights to be able to execute that file so after it's copied I need to change the user rights to it so that we can actually execute that

Now let's go take a look and see what the version of minicube that's running is and it says hey it's mini cube version 1.17 so that all looks pretty good let's get Kubernetes in here cube control and so we need the component that's going to control our mini cube and so we do a sudo curl on the cube control so we get that locally that'll just take a minute

Take a little bit of a look at the version that we've got there oh and it looks like I got a little ahead of myself there I got to do it change mod command first and then make sure there's a sudo change mod command there and then move this file into user local bin cube control so I'll do a little move next so there we go we've got that somewhere that we can run it and interact with it and now it's time to do the sudo hey cubecontrol what version are you running there and it's going to tell us that well let's pull from git 1.20.2 so 2021 build date looks like we've got the latest there. 

So why don't we actually go and start mini cube so the next step is this do sudo mini cube start and say no vm driver so dash dash vm driver equals none this will start things up and there we go we now have cube control up and configured so you can grab a little bit of info at uh cube control cluster info so we can see that it's running there let's see what kind of pod information we've got by passing in sudo cube control get pod and we've got nothing in the default namespace but that kind of makes sense to me there so why don't we do something a little bit more interesting let's take a look at what we've got in terms of deployments it wouldn't be it'd be nice to actually kind of maybe deploy a resource or not so we don't have any deployments there we can look at some events I don't know we can look at the config.

### Spring Boot and minikube on Ubuntu

So this is all interesting I do have some docker images available so I'm going to take a look at some of my docker images here you notice that a number of docker images have been brought locally one of the images that I've got is cameronmcnz/rock-paper-spring so I was thinking I might actually try to go ahead and deploy that so I'm going to open up a new terminal window.

Let's see if I can't deploy that particular container onto this local mini cube so first step here is to go in and create a deployment so I'm going to go sudo cube control create deployment rps node stands for rock paper scissors and the image is cameron mckenzie rock paper spring which you can see is right up there.

#### minikube port forwarding

You can take a look at the pods that are created and associated with it so we've got one there associated with rps take a look at the con fig as well if we really wanted to I think I'll skip over that let's expose that on port 8080 so we'll expose the deployment so that we can actually gain access to it and of course you have to spell these things correctly so that's q control ctl so there we go we've got the node exposed and then we do a little bit of port forwarding so we map port 7070 to port 8080 sudo cube control port forward and if we come over to our browser and go to localhost in this case it's 7070 index.html

##### microservice deployment to minikube ubuntu

we now get our rock paper scissors application this is the same one that I deployed on the installation of docker in a previous tutorial but now we've got it all wrapped up and running through mini cube and cube control and there you go that's how you install mini cube Kubernetes on ubuntu 20. and there you go that's how easy it is to install Kubernetes mini cube on your ubuntu 20 workstation now if you enjoyed that tutorial head over to theserverside.com I'm the editor in chief over there lots of great tutorials on ubuntu Kubernetes docker devops you name it if you're interested in my personal antics you can always follow me on twitter cameronmcnz and subscribe on the youtube


##### Commands to install minikube on Ubuntu 20

<pre>
sudo apt-get update

sudo apt-get upgrade

sudo apt-get install socat

sudo apt-get install curl

sudo apt-get install apt-transport-https

sudo apt install conntrack

sudo apt install virtualbox virtualbox-ext-pack

wget https://storage.googleapis.com/miniku...​

sudo cp minikube-linux-amd64 /usr/local/bin/minikube

sudo chmod 777 /usr/local/bin/minikube

sudo minikube version


sudo curl -LO https://storage.googleapis.com/kubern...​`curl -s https://storage.googleapis.com/kubern...​`/bin/linux/amd64/kubectl

chmod +x ./kubectl

sudo mv ./kubectl /usr/local/bin/kubectl

kubectl version -o json

sudo kubectl version -o json

sudo minikube start --vm-driver=none

sudo kubectl cluster-info

sudo kubectl get deployments

sudo kubectl get pods

sudo kubectl get events

sudo kubectl config view

sudo docker images

sudo kubectl create deployment rps-node --image="cameronmcnz/rock-paper-spring"

sudo kubectl get pods

sudo kubectl expose deployment rps-node --type=LoadBalancer --port=8080

sudo kubectl port-forward service/rps-node 7070:8080

http://localhost:7070/index.html

</pre>
