package javaauth;

public class Main {
	
	public static void main(String[] args)
	{
		SauerHash sh = new SauerHash();
		byte[] block = sh.hash("foo");
		System.out.println("Hash: " + SauerHash.printBlock(block, 0, 24));
	}

}
