---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Git Flow Release Branch Tutorial
blurb: Here's an example of how the Git Flow release branch works and how the release branche merges into master and develop Gitflow branches.
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/rX80eKPdA28" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Git Flow Release Branch Tutorial

Hi I'm Cameron Mckenzie, @cameronmcnz on Twitter and I wanted to talk to you about the release branch in git flow, how it works, what you do with the git flow release branch and how you merge the release branch into master and develop.

<em>I write a full write-up on the [Gitflow Release Branch](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish) over on TheServerSide</em>

So there is the get flow release branch right there, and this is sort of a prototypical little git flow example whenever you initialize git flow you get your master branch and you get a develop branch that is branched directly off of it.

On this develop branch well we add some features and we do some commits until finally, boom, we end up having a project that is feature complete. When that happens, what we do is we create a release branch. 

## Gitflow release branch creation

That's what we're talking about right here when we create the release branch. We don't add any other features to it, but you know some last minute testing might show some bugs in which case we do bug fixes. 

To fix a problem you do a branch off the release branch a topic branch and then merge it back into release.

We do some last minute testing and then finally when we're done this release branch gets merged into master and it gets tagged. 

## Gitflow release fixes and merges

Also, just to make sure that any fixes that happen to the release branch also get pushed back to develop we do a merge back into develop as well. The git flow release branch branches off of develop but it merges into both master and into develop.

When that's complete  we delete the git flow release branch because we don't need it anymore. That's how it works.

As it starts to initialize it asks me what I want for master.

### Gitflow release branch lifecycle

I'm just going to click enter to accept the default master develop feature bug fix release hotfix support I'm not going to have any prefix to my tab that looks like a good hooks directory and all of a sudden we now have git flow initialized now you might be curious what branches are available after it's been initialized now you might assume bug fix is released hotfield all these branches are created after all it asked us what we wanted to support but look at this only two branches are actually created right at the beginning master and developed and I as I mentioned earlier master and develop those are the only two that are created right off the bat with git flow but you know if you're doing development typically what you do is you create some feature branches so in order to add a feature branch all you have to do is say git flow hey create a feature branch for me let's start that feature branch give it a name I'm not very creative so I'm just going to call it feature branch and all of a sudden that gets created and if you now take a look at the different branches that are available there you go you see that feature branch now by the way something I forgot to do I like to actually take a look at the different tags that are available at the beginning of the process and you can see there's actually one tag there 0.1.0 that's already been created and it's a hold over from my git flow history but it's interesting to see what's there because we will improve on that a little bit later okay so now we take a look we've seen the branches we've got we've got the different tags that we've got as well well we're going to work on that feature commit commit commit and then finally that feature branch is done and what we do is we say hey let's finish that feature branch and so git flow says okay we'll take care of that feature branch we will merge that branch right back into develop so that feature branch is down here I don't have it on that particular diagram but you can see it on some of the others on the server side okay now if I do a git branch dash a and see what's floating around you'll see that feature branch is gone we are feature complete and everything's in develop so what do you do once you are feature complete well what you do is you get that get flow release branch started so I'm going to paste in here git flow release start well we saw that we had a tag called 0.1.0 that's a holdover from when I did this tutorial before so let's change it let's do 0 2 0 let's increase that tag by a decimal increment so we've started the release branch now let's take a look at all the different branches that are available right now dash a so you see we do indeed have this release branch and we have been switched onto it now let's assume we've got a couple of changes to be made that to that release branch those are called bug fixes and so you might create a bug fix branch and then merge it back into the release branch and once you're done you then finish the release and it was released 0.2 0.2.0 that we had before so I'm going to now finish that release git flow release finish and all of a sudden what do you think happens there well that release branch is going to be deleted now as it's deleted it's actually going to ask me for a little bit of information on the merge so I'm going to say yeah you know release done and it's good actually that's a really poor git commit message but it'll do for this and all of a sudden we now get that new tag added now if I do a git branch dash a notice the release branch is gone it's been deleted where is it well it's been merged into master and you know what it's been merged and to develop as well so we were in this situation here before we did that git flow release finish call when we did the finish well deleted that branch but before deleting it merged into master and it merged that content into develop just in case there was a fix in here that made the release branch different from development you want those fixes that would happen here to make sure they find their way into development too but of course it gets put into master and now one last thing git tag dash l for list and you see boom we've got another tag in there 0 2 0 because it was 0 2 0 that we released into the master and the develop branches and there you go that's how the get flow release branch works and there you go that's how easy it is to work with the release branch in git flow now if you enjoyed that tutorial why don't you head over to the serverside.com I'm the editor in chief over there we've got lots of great tutorials on git github git flow devops enterprise software development you name it if you're interested in my personal antics you can always follow me on twitter at cameronmcnz and subscribe on the youtube
