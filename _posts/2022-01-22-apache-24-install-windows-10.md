---
layout: mcnz/basic-post
author: Cameron McKenzie
title: How to install Apache 2.4 on Windows 10 Tutorial (Apache HTTP Web Server AWS)
blurb: Here's a quick installation of Apache on Windows 10 example for anyone who wants to install version 2.4 of Apache's HTTP Server locally.
canonical: https://www.mcnz.com/2022/01/22/apache-24-install-windows-10.html
keywords: apache aws http server installation apachelounce ahs bitnami apache24 windows windows10
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/tYPQFztqV4I" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Install HTTP Sever Apache 2.4 on Windows

To <a href="https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Install-Apache-Web-Server-24-Windows-10-ServerRoot-Error">install the Apache 2.4 HTTP Server on Windows 10,</a> first head over to the Apache HTTP Server website and click on the download button. 

Then click "Files for Microsoft" because you can't get the <a href="http://www.scrumtuous.com/aws/exam/2022/01/01/apache-web-server-installation-windows.html">Apache installation</a> media directly from apache.

I like the Apache lounge. Go there and you can download the Apache 2.4 HTTP Web Server install ZIP file. 

## Apache Web Server Download

When the Apache HTTP Server for Windows download completes, extract, the compressed file to the local file system. You'll notice that there's a folder named Apache 2.4, (which proves this is Apache version 2.4). Copy this folder and paste it directly into the root of the C:\ drive. If you paste it anywhere else, you'll get the following error when you try to run it:

<pre>Syntax error on line 39 of Apache24/conf/httpd.conf: ServerRoot must be a valid directory</pre>

Open a DOS prompt, command window, terminal window or BASH shell so you can run the httpd.exe file from the C:\Apache24\bin folder. 

Run the httpd.exe file. Running httpd.exe will start the Apache web server. 

With the server started, you can go to the localhost address (127.0.0.1) and bring up the Apache 2.4 installation home page page. The page will show a text heading that says "It works!" 

To upload own website to the Apache Web Server on Windows 10, simply add any files to Apache's htdocs folder. I have a file named game.html, which I'll add. And once that file is added, I can now go to the browser and bring up the webpage in the newly installed Apache 2.4 HTTP Server on Windows 10. 

You can see this application is now being hosted by the Apache web server on Windows. The <a href="https://httpd.apache.org/">server</a> is working perfectly.

And that's how easy it is to install Apache 2.4 on Windows 10 and get your own Apache HTTP Server running locally.
