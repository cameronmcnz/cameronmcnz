---
layout: default
author: Cameron McKenzie
title: How to use UiPath Picture-in-Picture
blurb: Improve your RPA robots with the new UiPath Picture-in-Picture (PiP) feature available through UiPath Assistant. Your attended automations will never be the same!
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/KOjVaJ7aPdA" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
# UiPath Picture in Picture Example (PiP)a

Hey I'm Cameron McKenzie, @cameronmcnz on Twitter and I want to talk to you about UiPath Picture-in-Picture (PiP).  It's a really cool new feature that you can use with attended and unattended robots in UiPath. 

I have a neat little application here that listens for files to be dropped into this downloads folder. I can start it over on UiPath Assistant. I click play and it begins. 

Here's how the robot works. 

I have this little downloads folder here and if I paste something into it you'll notice that a whole registration form pops up. There we go, we've got my Chrome browser starting up and now that application is going through my whole Excel file, doing all these registrations for me. It's a pretty cool, pretty neat little application but right now it's just kind of monopolizing my entire screen as it runs. 

Let me get out of here... come on UiPath assistant I want you to stop... 

## UiPath Picture in Picture example (PiP)

And here we go the job is now stopped now let's take a look at how we can actually isolate that robot a little bit by running this in UiPath's picture-in-picture feature. 

I think this feature is really cool.  Instead of monopolizing all of my browser space I'm just going to delete that file copy it again so I can paste it back in and trigger this in picture-in-picture mode there we go just setting things up a little bit here but as you can see this this application. 

Here i've got the option to start it in pip picture in picture I can also click this button here that says hey this will always run in picture-in-picture but either way I want to restart this application but put it in picture-in-picture and you'll watch how differently it runs it runs in what looks like an isolated window and I say <em>looks like</em> because I'll show you some of the drawbacks in a second. 

I'll say start in picture-in-picture. The robot wasn't verified and tested in picture-in-picture and I know I should have clicked those buttons in UiPath Studio but whatever (I was in a hurry)...

### How to use Picture-in-Picture with UiPath Assistant


Now you actually see the UiPath robot running in Picture-in-Picture (PiP). 

It kind of opens up its own window in its own window it simulates a login into the windows environment I guess i've got to paste that file into the downloads folder to kick off the automation but when I do on the host machine and it's all the host machine it's not like a virtual environment or anything it's just an isolated picture in picture 

#### UiPath Picture in Picture drawbacks

Notice how this picture in picture window is now taking all of the input and the whole thing is being processed not on one of the browsers that's sitting right next to me but right inside of this picture in picture window and I think all of that is pretty cool.

Now there are some drawbacks to UiPath PiP. One of the drawbacks to this is the fact that I can still go in here and type so notice that if I type something in here like provide user input, my keyboard, my mouse: THAT'S NOT BLOCKED! You need to use the <a href="https://youtu.be/OBHm7BJSr7Q">UiPath block user input</a> activity to fix that.

The great thing about UiPath picture-in-picture is it allows you to look at what's going on and see the process run but it doesn't actually block the user input if you want to do that you got to use the block user input activity and if you stick around for the next tutorial I'll show you exactly how to do that but there you go that's how easy it is to run an application picture in picture just publish I'm going to stop my application here but just publish your application from UiPath studio into assistant go to assistant find the process that you've run and then just say start in picture in picture and it will and there you go that's how you use picture-in-picture and UiPath Studio and Assistant.