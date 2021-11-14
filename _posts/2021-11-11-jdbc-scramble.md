---
layout: mcnz/2271-jenkins-course
author: Cameron McKenzie
title: JDBC Scramble
blurb: How well do you know the fundamentals of JDBC?
canonical: https://www.mcnz.com/2021/11/11/jdbc-scramble.html
---


<pre>
class GameSummary {

	public long id;
	public String toString() {
		return "GameSummary [id=" + id + ", client=" + client + ", server=" + server + ", result=" + result + ", date="
				+ date + "]";
	}
	public String client;
	public String server;
	public String result;
	public java.util.Date date;

}
</pre>

See if you can unscramble the code below. The code will compile in Eclipse if the GameSummary class above if reachable. 

It might even run if your drivers and database tables are set up accordingly. But for this exercise, 'compilation' is the definition of done.

<pre>
package com.mcnz.jdbc.scramble;
System.out.println("\n-------------------------------------------------------");
GameSummary gameSummary = new GameSummary();
for (int i = 1; i <= numberCols - 1; i++) 
import java.sql.Connection;
ResultSet results = stmt.executeQuery("select * from GAMESUMMARY");
import java.sql.DriverManager;
Statement stmt = conn.createStatement();
results.close();
ResultSetMetaData rsmd = results.getMetaData();
import java.sql.ResultSetMetaData;
int numberCols = rsmd.getColumnCount();
public class JDBCTesting 
System.out.print(rsmd.getColumnLabel(i) + "\t\t");
gameSummary.id = results.getInt(1);
import java.sql.ResultSet;
Class.forName("org.apache.derby.jdbc.ClientDriver").newInstance();
public static void main(String[] args) throws Exception 
stmt.close();
gameSummary.server = results.getString(3);
String dbURL = "jdbc:derby://localhost:1527/rpsdb;user=guest;password=password";
gameSummary.result = results.getString(4);
import java.sql.Statement;
System.out.println(gameSummary.id + "\t\t" + gameSummary.client + "\t\t" + gameSummary.server + "\t\t" + gameSummary.result);
Connection conn = DriverManager.getConnection(dbURL);
gameSummary.client = results.getString(2);
while (results.next()) 


/*

ID		CLIENT		SERVER		RESULT		
---------------------------------------
1		ROCK		ROCK		TIE
2		PAPER		ROCK		TIE
3		ROCK		ROCK		TIE
4		Rock		Paper		Loss
5		Rock		Paper		Loss

*/



</pre>
