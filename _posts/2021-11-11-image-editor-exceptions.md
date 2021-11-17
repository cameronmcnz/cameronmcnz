---
layout: mcnz/java8-course
author: Cameron McKenzie
title: Java 8 Day One
blurb: Day one of the Java 8 course
canonical: https://www.mcnz.com/2021/11/11/image-editor-exceptions.html
---

## Exception Handling

The following code doesn't work. But it should.

Identify the various exceptions this code is throwing, fix them, and then run the application.

<hr/>
<pre>
package com.mcnz.jfr.jmc;

import java.awt.image.BufferedImage;
import java.io.File;

import javax.imageio.ImageIO;

public class ImageChanger {
	
	public static void main(String args[]) throws Exception {
		
        String sourceImageName = "C:\\_instaloader\\nasa-logo.jpg";
        File sourceImage = new File(sourceImageName);
        BufferedImage image = ImageIO.read(sourceImage);

        int w = image.getWidth();
        int h = image.getHeight();
 
        int[] src = image.getRGB(0, 0, w, h, null, 0, w);
        int[] edited = new int[src.length];

        System.out.println("Array size is " + src.length);
 
        long startTime = System.currentTimeMillis();

		for (int i=0; i<src.length; i++) {
			edited[i] = (src[i]/(src[i]%2) + src[i-1] + src[i+2]);
		}
		
        long endTime = System.currentTimeMillis();
 
        System.out.println("Image changer took " + (endTime - startTime) + 
                " milliseconds.");
 
        BufferedImage editedImage = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        
        editedImage.setRGB(0, 0, w, h, edited, 0, w);
		
        String editedName = "C:\\_instaloader\\blurred-nasa-logo.jpg";
        File editedFile = new File(editedName);
        ImageIO.write(editedImage, "png", editedFile);
		
	}

}

</pre>
<hr/>
