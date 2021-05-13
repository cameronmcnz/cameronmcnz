---
layout: exam-questions-nolink
author: Cameron
title: Microservices vs Monoliths Quiz
blurb: Here's a quiz to test you on the benefts and drawbacks to microservices.
canonical: https://www.mcnz.com/2021/05/12/monolith-microservices-quiz.html
---

<script>
var exam = null;
var questionNumber = 0;

window.addEventListener('load', function () {

 var questionBank = localStorage.getItem("questions");
 //console.log("The size is: " + questionBank.length);
 questionBank = JSON.parse(questionBank);
 questionBank = questionBank.slice(86,101);
 
 try {
  exam = new Exam(questionBank);
  //console.log("Exam created without parsing the exam!");
 }
 catch(err) {
   console.log("Error creating exam! " + err.message);
 }

 displayQuestion(questionNumber);
 initializeQuestionJumper();
 
});
</script>
