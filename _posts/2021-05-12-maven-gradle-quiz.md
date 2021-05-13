---
layout: exam-questions-nolink
author: Cameron
title: Maven Gradle Quiz
blurb: How well do you know Maven and Gradle?
canonical: https://www.mcnz.com/2021/05/12/maven-gradle-quiz.html
---

<script>
var exam = null;
var questionNumber = 0;

window.addEventListener('load', function () {

 var questionBank = localStorage.getItem("questions");
 //console.log("The size is: " + questionBank.length);
 questionBank = JSON.parse(questionBank);
 questionBank = questionBank.slice(102,109);
 
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

<figure class="figure">
  <img src="/assets/gradle-vs-maven.jpg" alt="Gradle vs Git merge and build" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Just because it will merge in Git doesn't mean it will build with Maven or Gradle.</figcaption>
</figure>
