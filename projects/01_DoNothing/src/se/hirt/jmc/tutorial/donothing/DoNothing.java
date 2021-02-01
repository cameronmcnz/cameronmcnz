package se.hirt.jmc.tutorial.donothing;

import java.io.IOException;

/**
 * Program that doesn't do much.
 */
public class DoNothing {
	public static void main(String[] args) throws IOException {
		System.out.println("Press <enter> to quit!");
		System.in.read();
	}
}


