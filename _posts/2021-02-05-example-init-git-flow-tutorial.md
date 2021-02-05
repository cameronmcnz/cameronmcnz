---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Quick Git Flow Init Tutorial and Example
blurb: Want to learn Gitflow? Your journey starts with git flow init. This git flow init tutorial and example will get you started on your git branching journey.
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d4cDLBFbekw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>


# Gitflow init example

Hey, I'm Cameron McKenzie, @cameronmcnz on Twitter, and I want to talk to you about git flow, specifically how to run git flow init and get started with git flow. 

Then if you got the time I wanted to real quickly show you how to go through master to develop to feature back to develop into release and back to master and show you how after you've done a git flow init how easy it is to go through the git flow workflow.

## Issue the git flow init command

Step one of working with git flow is issuing and get flow init call. I've got a little folder called my gitflow, I've also got a nice little git flow diagram to the right which I thought we might work through. 

Before you can do any of that, you've got to issue the get flow init command. That's where everything starts. Okay, maybe it doesn't start there, maybe you actually have to [install git](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Step-by-step-guide-to-install-Git-on-Windows-desktop-computers) first and then make sure [git flow is installed](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-Windows-Install-Git-Flow-Installation) as well, but let's just say you've got that done and you want to start with git flow. The git flow init is the thing to do now. 

Right when it starts off it's going to ask you how you want to set up git flow, so it says "what's the name for production releases?" Tou can just click enter here and accept the defaults, and if you click enter it won't leave it blank, it'll leave it as master. 

## Git master vs main

You know the the proper terminology nowadays is main, not to use master to respect some of the historical indignities associated with that word. I'm going to set that as main.

I don't like the "develop" branch, I like "development" branch, so you can type that in there if you want.

I've done a couple of little changes here, but you know you shouldn't change these things, so you know the more you change it the more confusing it'll be to other people that jump on the project so for I'm just going to click enter for feature, the bug fix branch will be bugfix, the [git flow release branch](https://www.mcnz.com/2021/02/04/git-flow-release-branch-example.html) will be release, hotfix, support support and life is good.

<figure class="figure">
  <img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-hotfix-branch-diagram.jpg" alt="Git flow init branches" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">The git flow init command preps your workspace for main, master, feature, release and hotfix branch creations.</figcaption>
</figure>

<p><em>I wrote a proper tutorial on the <a href="https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish">Gitflow Release Branch</a> over on TheServerSide</em></p>

### init git flow branches

How notice it asks for a tag prefix. I'm not going to have a tag prefix so I'll just accept the default which is nothing and then I can explicitly state what my tag is going to be. You can see here it's found out where the hooks directory of my git installation is and I think that looks good.  It just needs to git hooks, it needs the hooks in order for git flow and the git flow extension to work.

The you go, that is git flow up running and initialized.

You'll notice it asked me for all of these different branches. The feature branch is where you do development, you can see it down here and that's where you have all of your topic branches off of the development branch itself, so that's where you work on features that eventually get pushed into the develop branch. The bug fix branch branches off the development branch but of course it's for just that a fix as opposed to a feature or feature enhancement releases. You see that over here when you're done in development and you actually want to release some code back into the master branch and make it publicly available you first create a release and then that gets pushed to master.

There's [git flow hotfix branch](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitFlow-Hotfix-Branch-Example-Start-Finish) as well. I don't have the hotfix here, but if there's a problem in master you branch off to a hotfix and then you push it back in in a giant hurry.

### Release, support and bugfix branches

There's a support branch so if you've got an old version and you want to have a support line for it you can use that so that's kind of how those things work now a couple of things to note notice right off the bat. 

It asked me about all these branches, but if I do a git branch -a,  how many branches do you think will be there?

Well, if you said two you'd have got the right answer. The only ones that are available at the start are development and main. That actually catches some people off guard because they think hey didn't we just create all these branches here, well, no you didn't. All we did was sort of create some organizational subfolder type of structure in order to keep track of the different branches but no actually we didn't create branches the only one created by default are development right there and main.

If we took a look at our application right now that's where we are we've got the master and the develop branch so of course if you want to do some development you don't do development directly on the develop branch you want to work in an isolated branch where you can play around and experiment a little bit, and in order to do that well you create a feature branch. So, I've only got two branches here I need to create a feature branch so I issue the git flow feature start command and provide a branch name.


<figure class="figure">
  <img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-hotfix-example.gif" alt="Git flow init branches" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">After the git flow init command runs, only master and develop branches exist. Hotfix and feature branches must be created through git flow commands.</figcaption>
</figure>

#### git flow init success

I'm going to paste a little command in there git flow feature start and put a name of a branch could be any branch that you want I'll just call mine feature branch because I'm not very creative that creates that branch but you get branch -a you'll notice that we've got a new branch called feature branch, and you'll notice as well that I've been switched onto the feature branch. What do you do here? I don't know maybe touch feature.html? I'll just create a file called feature add it to the git repository give it a commit.

And just follow through with the other git flow commands and you know you've successfully issued the git flow init command.
