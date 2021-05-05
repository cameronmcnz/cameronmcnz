---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Fun with Git
blurb: Here's how Git add, commit and reset works.
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/XTolZqmZq6s" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>


# Basic Git Commands Overview

Git is great for doing personal devleopment, let alone collaborative development in groups and teams.

Git lets you commit changes, and revert back to a previous save state if you mess things up. Actually, the proper term is reset. Revert has a slightly different meaning in Git. But you get the point.

Follow these steps to get a better idea of how to initalize a Git repo, commit code, and go back to the way things were in a previous commit. There is a full write-up on this <a href="https://www.theserverside.com/video/How-to-use-the-git-reset-hard-command-to-change-a-commit-history">Git reset hard example</a> on TheServerSide.

## Initialize and commit to a Git repo

<pre>

$ git init
Initialized empty Git repository in C:/_repositories/git reset hard/.git/

$ git config --global user.name me

$ git config --global user.email me@example.com

$ touch a.html
$ git add --all 
$ git commit -m "Commit #1 - 1 file"

$ touch b.html
$ git add --all
$ git commit -m "Commit #2 - 2 files"

$ touch c.html
$ git add --all 
$ git commit -m "Commit #3 - 3 files"

$ touch d.html
$ git add --all
$ git commit -m "Commit #4 - 4 files"

$ touch e.html
$ git add . 
$ git commit -m "Commit #5 - 5 files"

</pre>

### A history of commits

Now see what git reflog shows

<pre>

$ git reflog
2e1dd0a (HEAD -> master) HEAD@{0}: Commit #5 - 5 files
868ca7e HEAD@{1}: commit: Commit #4 - 4 files
ebbbca3 HEAD@{2}: commit: Commit #3 - 3 files
882bf98 HEAD@{3}: commit: Commit #2 - 2 files
2f24f15 HEAD@{4}: commit (initial): Commit #1 - 1 file

</pre>

Now list what's in the current directory:

<pre>
$ ls
a.html  b.html  c.html  d.html  e.html
</pre>

## Git reset hard

Now reset. Make sure you use the commit id from your reflog command.

<pre>
$ git reset --hard ebbbca3
HEAD is now at ebbbca3 Commit #3 - 3 files

$ ls
a.html  b.html  c.html
</pre>

Pretty cool, eh?


<figure class="figure">
  <img src="https://cdn.ttgtmedia.com/rms/editorial/071918_help_file_half_column_desktop.png" alt="Git Flow Diagram" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Here's the documentation on git reset.</figcaption>
</figure>

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/rX80eKPdA28" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>




