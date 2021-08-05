---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Fun with Gitflow
blurb: Here's a look at Gitflow
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/eNrjux4sgWw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# How Git Flow Works

Lab 1 takes a look at how Git Flow works. 

There's an even easier way to run Git Flow. Check this link out:

[The Gitflow Release Branch Process](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish)

<figure class="figure">
  <img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-release-branch.jpg" alt="Git Flow Diagram" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Sample Git Flow release branch.</figcaption>
</figure>

<pre>



git flow init

git branch -a

git tag -l

git config --global user.name "me"

git config --global user.email "me@example.com"

git flow feature start feature_branch

git branch -a

touch "feature.html"

git add .

git commit -m "feature added"

git flow feature finish feature_branch

git flow release start 0.1.0

git branch -a

touch "quick-fix.html"

git add .

git commit -m "quick fix added"

git flow release finish '0.1.0'

git branch -a

git tag -l

</pre>


<figure class="figure">
  <img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-hotfix-branch-diagram.jpg" alt="Git Flow Diagram" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">We don't deal with the hotfix branch in this example.</figcaption>
</figure>


### Commands used in Lab 1

<pre>
cd \Workspace   


mkdir gitflow_test
git init --bare remote_repo.git
tree remote_repo.git
git clone remote_repo.git local_repo

tree local_repo
cd local_repo

git config user.email "bob@abc.com"
git config user.name "Bob"

git commit --allow-empty -m "Initial commit."
git checkout -b develop

git flow init
git branch

git checkout -b feature/HOME_PAGE
git branch

git status

notepad index.html

git status

git add index.html
git add .

git commit -m "Added index.html"

git ls-tree -r --name-only feature/HOME_PAGE

git checkout develop
git merge --no-ff feature/HOME_PAGE

git ls-tree -r --name-only develop

git checkout develop
git merge --no-ff feature/HOME_PAGE

git push --all

git ls-remote

git checkout develop
git checkout -b release/REL_1.0

git checkout master
git merge release/REL_1.0
git tag REL_1.0 -m "REL_1.0"

git branch -d release/REL_1.0
git checkout develop
git merge master

git branch

git checkout master
git merge release/REL_2.0
git tag "REL_2.0" -m "REL_2.0"

git checkout master
git merge hotfix/REL_2.0.1
git tag "REL_2.0.1" -m "REL_2.0.1"
git branch -d hotfix/REL_2.0.1

git describe




</pre>


