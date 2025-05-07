---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Underwater cannon cleaning
blurb: How to clean cannons that are underwater.
---

Here's the solution all in one file. 


```
package com.mcnz.batch;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.ItemProcessListener;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobExecutionListener;
import org.springframework.batch.core.SkipListener;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.job.builder.JobBuilder;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.batch.core.step.builder.StepBuilder;
import org.springframework.batch.item.ItemProcessor;
import org.springframework.batch.item.file.FlatFileItemReader;
import org.springframework.batch.item.file.FlatFileItemWriter;
import org.springframework.batch.item.file.builder.FlatFileItemReaderBuilder;
import org.springframework.batch.item.file.builder.FlatFileItemWriterBuilder;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.FileSystemResource;
import org.springframework.stereotype.Component;
import org.springframework.transaction.PlatformTransactionManager;


/*

STEP 0

Create a Spring project with Batch and H2 dependencies

Step 1

Add the following to application.properties:

path.file.input  = data-file.csv
path.file.output = src/main/resources/masked-data.csv
spring.profiles.active=dev
spring.devtools.restart.enabled=false
logging.console.pattern: %n %d{HH:mm:ss} | %level | %msg

#---

spring.config.activate.on-profile=dev
path.file.output = src/main/resources/masked-dev-data.csv
debug=true

#---

spring.config.activate.on-profile=prod
path.file.input  = data-file.csv
path.file.output = src/main/resources/masked-prod-data.csv
spring.main.banner-mode=off


STEP 2

In resources create a file name data-file.csv with this content (add your own lines to make it more fun!):

The phone number is 905-683-3033
The SSN is 3772-242-1212
The air miles code is 524 563 2323
My 2025 Visa card is 4334 8588 3422
My email password is 3rn13andb3rt

Step 3

Add the following annotations:

@SpringBootApplication @Component @Bean @Bean @Bean @Bean

Step 4 

Run the application


Step 5 

Refactor the application.

Remove the one @Component annotation and then run the application. It should fail.

Then create the following classes:

BatchConfiguration
UnmaskedItemProcessor (include the listener)
MaskingExecutionListener
MaskingSkippedListener

BONUS

Add a MaskingChunkListener and MaskingRetryListener

Step 6

Use the values injected into the application for the input and output files.

Only the output file will really make a difference.

Step 7

Change the active profile

Step 8

BONUS: Replace the Spring Boot banner with your own custom banner.

Step 9

Here is a class that replaces blanks:

@Component
class BlanksProcessor implements ItemProcessor<String, String> {
	
	public String process(String message) throws Exception {
		return message.replaceAll(" ", "@");
	}

}


Create a method that returns a Step that uses this ItemProcessor.

Create a method that returns a Job that has uses two steps. The UnmaskedItemProcessor runs first, and "next()" the the BlanksProcessor runs.
This job only runs in prod.

Your configuration will now have two methods that return a Step and two methods that return a Job. How will Spring know when to use which one?



 */


@SpringBootApplication
@Component
public class MySpringBatchExampleApplication implements ItemProcessor<String, String>, JobExecutionListener, SkipListener<String, String>, ItemProcessListener<String, String> {
	
	@Value("${path.file.input}")
	String outputFile;
	
	@Value("${path.file.output}")
	String inputFile;
	
	@Value("${spring.profiles.active}")
	String activeProfile;
	
	
	public void onSkipInRead(Throwable t) {
		System.out.println("A record was skipped for some reason?");
	}

	public void afterJob(JobExecution jobExecution) {
		if (jobExecution.getStatus() == BatchStatus.COMPLETED) {
			
			String filePath = "src/main/resources/masked-data.csv";
			try {
				Files.lines(Paths.get(filePath)).forEach(System.out::println);
			} catch (IOException e) {
				e.printStackTrace();
			}
			System.out.println("The input file is: " + inputFile);
			System.out.println("The output file is: " + outputFile);
			System.out.println("The currently active profile is: " + activeProfile);
		}
	}
	
	public void beforeJob(JobExecution jobExecution) {
		System.out.println("The job is about to start!!!");
	}
	
	public String process(String message) throws Exception {
		return message.replaceAll("\\d", "*");
	}
	
	@Bean
	@Primary
	protected Step maskingStep(JobRepository jobRepo, PlatformTransactionManager manager,
			FlatFileItemReader<String> reader, MySpringBatchExampleApplication processor, FlatFileItemWriter<String> writer) {
		
		return new StepBuilder("masking-step", jobRepo)
				.<String, String> chunk(2, manager)
				.reader(reader)
				.processor(processor)
				.writer(writer)
				.build();
	}
	
	@Bean(name="blanking")
	protected Step unblankingStep(JobRepository jobRepo, PlatformTransactionManager manager,
			FlatFileItemReader<String> reader, BlanksProcessor processor, FlatFileItemWriter<String> writer) {
		
		return new StepBuilder("unblanking-step", jobRepo)
				.<String, String> chunk(3, manager)
				.reader(reader)
				.processor(processor)
				.writer(writer)
				.build();
	}
	
	@Bean
	@Profile("dev")
	protected Job maskingJob(JobRepository jobRepository, Step maskingStep, Step unblankingStep, MySpringBatchExampleApplication listener) {
		return new JobBuilder("masking-job", jobRepository)
				.start(maskingStep).next(unblankingStep).listener(listener)
				.build();
	}
	
	@Bean
	@Profile("prod")
	protected Job maskingNumbersAndBlanksJob(JobRepository jobRepository, Step maskingStep, @Qualifier("blanking")Step unblankingStep, MySpringBatchExampleApplication listener) {
		return new JobBuilder("masking-job", jobRepository)
				.start(maskingStep).next(unblankingStep)
				.listener(listener)
				.build();
	}
	
	public void afterProcess(String item, String result) {
		System.out.println("This is called after the item is processed.");
	}
	
	public void onProcessError(String item, Exception e) {
		System.out.println("This is called when an error happens during item processing.");
	}
	
	@Bean
	protected FlatFileItemReader<String> reader() {
		return new FlatFileItemReaderBuilder<String>()
				.resource(new ClassPathResource("data-file.csv"))
				.name("csv-reader")
				.lineMapper((line, lineNumber) -> line)
				.build();
	}
	
	public static void main(String[] args) {
		SpringApplication.run(MySpringBatchExampleApplication.class, args);
	}
	
	@Bean
	protected FlatFileItemWriter<String> writer() {
		String fileLocation = "src/main/resources/masked-data.csv";
		return new FlatFileItemWriterBuilder<String>()
				.name("csv-writer")
				.resource(new FileSystemResource(fileLocation))
				.lineAggregator(item -> item)
				.build();
	}

	
	public void beforeProcess(String item) {
		System.out.println("This is called before the itme is processed.");
	}


}


@Component
class BlanksProcessor implements ItemProcessor<String, String> {
	
	public String process(String message) throws Exception {
		return message.replaceAll(" ", "@");
	}

}
```
