---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Spring MVC
blurb: A little Spring MVC application
canonical: https://www.mcnz.com/2021/06/24/spring-mvc.html
---

## Spring MVC Example

The Spring MVC Example has a few parts. You can find all the code on [GitHub](https://github.com/cameronmcnz/spring-boot-examples/tree/master/simple-spring-mvc-rps/src/main/java/com/mcnz/rps/smvc)


## Spring Project

You'll need a Spring project that uses Spring Web and the <b>ThymeLeaf Template Engine</b>. Add the dev tools as well.


## index.html

This file goes in the \resources\templates folder and is named index.html

[index.html](https://github.com/cameronmcnz/spring-boot-examples/blob/master/simple-spring-mvc-rps/src/main/resources/templates/index.html)

## WebController

<pre>
@Controller
public class WebController {
	
	@GetMapping ("/playagame")
	public String playGame(
			@RequestParam(name="choice", required=false) 
			    String theChoice, 
			       Model model) {
		
		if (theChoice == null) {
			return "index";
		}
		
		String theOutcome = "error";
		if (theChoice.equals("rock")) {
			theOutcome = "tie";
		}
		if (theChoice.equals("paper")) {
			theOutcome = "win";
		}
		if (theChoice.equals("scissors")) {
			theOutcome = "loss";
		}
		
		model.addAttribute("outcome", theOutcome);
		return "results";
		
	}
}
</pre>

## results.html

The results page goes in the templates folder as well:

[results.html](https://github.com/cameronmcnz/spring-boot-examples/blob/master/simple-spring-mvc-rps/src/main/resources/templates/results.html)


## application.properties

Check the application.properties file. There used to be a requirement to reference thymeleaf in there, but that requirement may no longer exist.

Play the game!





