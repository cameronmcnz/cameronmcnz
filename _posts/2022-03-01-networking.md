---
layout: mcnz/java8-course
author: Cameron McKenzie
title: Java 8 Networking
blurb: Just some simple networking
canonical: https://www.mcnz.com/2022/03/01/networking.html
---

## Networking

Here is a super-simple reduction of the code you will see in the Networking lab.

Note there are two separate classes here. Both need to run separately, with the server being run first.

<hr/>
<pre>

package com.example.client;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public class ClientClass {


       public static void main(String args[]) throws IOException {

              SocketChannel sc = SocketChannel.open();

              sc.connect(new InetSocketAddress("localhost",9999));

              ByteBuffer bb = ByteBuffer.allocate(1024);

              bb.put("Hello world".getBytes());

              bb.flip();

              sc.write(bb);

              sc.close();

       }

} 



package com.example.server;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;

public class ServerClass {

       public static void main(String args[]) 
       {

              try(ServerSocketChannel ss = ServerSocketChannel.open()){

              ss.bind(new InetSocketAddress("localhost", 9999));

              while(true) {

                     final SocketChannel sc = ss.accept();

                      Runnable handler= ()-> {                      

                                  ByteBuffer bb = ByteBuffer.allocate(1024);

                                  try {

                                         sc.read(bb);

                                  } catch (IOException e) {

                                         e.printStackTrace();

                                  }

                                  try {

                                         System.out.print("*********************");

                                         System.out.println(new String(bb.array(),"ASCII"));

                                  } catch (UnsupportedEncodingException e) {

                                         e.printStackTrace();

                                  }

                           

                     }; 

                     new Thread(handler).start();

              }

       } catch(IOException e) {

           e.printStackTrace();

       }

    }

} 

</pre>
<hr/>
