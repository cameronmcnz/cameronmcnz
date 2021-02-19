---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Docker quiz!
blurb: Here's a fun Docker and Kubernetes quiz
---

## Command to copy git repo to var

git clone .git /var/lib/jenkins/repos/hello-node

## Command to move to the repo directory

cd /var/lib/jenkins/repos/hello-node




<pre>

'use strict';

const express = require('express');

const PORT = 9090;
const HOST = '0.0.0.0';

const app = express();

app.get('/', (req, res) => {
  res.send('Hello Node.js v1.0\n');
});

app.listen(PORT, HOST);


</pre>

<hr/>


Question: If not found locally, Docker will try to pull images from:
(Choose one)

- [ ] &nbsp;  GitHub
- [ ] &nbsp;  DockerHub
- [ ] &nbsp;  KubernetesHub
- [ ] &nbsp;  Git

Question: A single computer in a Kubernetes cluster is known as a:
(Choose one)

- [ ] &nbsp;  Node
- [ ] &nbsp;  Replicant
- [ ] &nbsp;  Pod
- [ ] &nbsp;  Deployment

Question: Red Hat's Kubernetes based software offering is known as:
(Choose one)

- [ ] &nbsp;  RHEL
- [ ] &nbsp;  WebSphere
- [ ] &nbsp;  Apache
- [ ] &nbsp;  OpenShift

Question: Which of the following two statements are most correct?

- [ ] &nbsp;  You run images and download containers
- [ ] &nbsp;  You run containers and download images
- [ ] &nbsp;  Containers can be stopped and started
- [ ] &nbsp;  Images can be stopped and started

Question: Administrators interact directly with which component to scale a Kubernetes hosted application:
(Choose one)

- [ ] &nbsp;  Node
- [ ] &nbsp;  Deployment
- [ ] &nbsp;  Replicant
- [ ] &nbsp;  Pod

Question: To define in YAML how a single container is configured you write a:
(Choose one)

- [ ] &nbsp;  Docker service
- [ ] &nbsp;  Docker compose
- [ ] &nbsp;  Dockerfile
- [ ] &nbsp;  Docker image

Question: To run wordpress in docker, the following two commands must be run:
<pre>
docker run --name some-wordpress --network some-network -d wordpress
docker run --name some-wordpress -p 8088:80 -d wordpress
</pre>
Why is the second command necessary? 
(Choose 2. Mildly unfair question)

- [ ] &nbsp;  By default Docker and Kubernetes block access on all ports
- [ ] &nbsp;  To download wordpress from an external service repo
- [ ] &nbsp;  To map the external port 8080 to the internal port used by wordpress
- [ ] &nbsp;  To confirm that wordpress is running


Question: In Kubernetes, to expose a common port across pods (to access a web server or database, etc), you create a:
(Choose 1. Lab page 32)

- [ ] &nbsp;  replicant
- [ ] &nbsp;  node
- [ ] &nbsp;  service
- [ ] &nbsp;  container


Question: Running multiple pods on a single node to take advantage of muliple processors is known as: 
(Mea Culpa: Instructor was unclear on pods and nodes yesterday.)

- [ ] &nbsp;  Vertical scaling
- [ ] &nbsp;  Horizontal scaling
  

Question: To make a port in a container that runs in a Kubernetes cluster accessible to the public Internet, which command would be run?
(Choose 1. Lab page 31)


- [ ] &nbsp;  kubectl expose node
- [ ] &nbsp;  kubectl expose pods
- [ ] &nbsp;  kubectl expose deployment
- [ ] &nbsp;  kubectl expose replicant


<img src="https://miro.medium.com/max/700/1*CdyUtG-8CfGu2oFC5s0KwA.png" class="img-fluid"/>
