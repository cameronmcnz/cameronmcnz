---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Spring JPA
blurb: How to create a JPA app in Spring
canonical: https://www.mcnz.com/2020/06/23/spring-jpa-roshambo.html
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

## The POM

<pre>
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.5.1</version>
		<relativePath /> <!-- lookup parent from repository -->
	</parent>
	<groupId>com.mcnz.rps.rest</groupId>
	<artifactId>Roshambo</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<packaging>war</packaging>
	<name>Roshambo</name>
	<description>Demo project for Spring Boot</description>
	<properties>
		<java.version>11</java.version>
	</properties>
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-jpa</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-devtools</artifactId>
			<scope>runtime</scope>
			<optional>true</optional>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-tomcat</artifactId>
			<scope>provided</scope>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>
		<!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>8.0.25</version>
		</dependency>
	</dependencies>

	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>

</project>

</pre>
