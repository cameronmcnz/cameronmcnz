---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Spring JPA
blurb: How to create a JPA app in Spring
canonical: https://www.mcnz.com/2021/06/23/spring-jpa-roshambo.html
---

# Spring, JPA and Databases

JDBC and Spring is a bit more complicated than most other activities. There are a lot of steps. Some will inevitably be missed here. But I'll give it a try:

1. Close any other open projects for now
2. Create a Spring project named ScoreData
4. Add Dev Tools, <b>SQL -- </b> Spring Data JDBC <i>and</i> the <b>MySQL Driver</b> to the project
5. In the 'Application' class, implement CommandLineRunner
6. Add the required <b>public void run(String... args) throws Exception</b> method
7. Mark the class as @Transactional
8. Add the Score class
9. Decorate the Score class
10. Inject the EntityManager as a @PersistenceContext
11. Write some JPA code in the run method
12. Update the application.properties file


<hr/>

## The Score Class

<pre>
@Entity
@Table(name = "score")
public class Score {

	@Id 
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	public int id;

	public int wins;
	public int losses;
	public int ties;
	
}
</pre>


## The Application Class

<pre>
@SpringBootApplication
@Transactional
public class PersistentScoreApplication implements CommandLineRunner {
	
	@PersistenceContext
	private EntityManager entityManager;

	public static void main(String[] args) {
		SpringApplication.run(PersistentScoreApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
	
		Score score = entityManager.find(Score.class, 1);
		System.out.println(score.wins);
		score.wins++;
		
	}
}
</pre>

## application.properties

<pre>
spring.datasource.url=jdbc:mysql://rps.cyvpttibbqrc.us-east-1.rds.amazonaws.com/ROSHAMBO
spring.datasource.username=cameronmcnz
spring.datasource.password= ASK THE INSTRUCTOR
spring.jpa.database-platform=org.hibernate.dialect.MySQLDialect
spring.thymeleaf.enabled=true
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
</pre>


