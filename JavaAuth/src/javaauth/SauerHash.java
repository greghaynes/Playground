package javaauth;

public class SauerHash extends TigerHash {
	
	public static String printBlock(byte[] block, int offset, int length) {
		char[] hex_chars = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
		String result = "";
		for (int x = offset; x < (offset + length); x++) {
			result = result + hex_chars[0x0F & (block[x] >> 4)] + hex_chars[0x0F & block[x]];
		}
		return result;
	}
	
	// Taken from Eric Seidel's Java TigerHash implementation
	public byte[] hash(String instr) {
		byte[] block = new byte[64];
		byte[] bytes = instr.getBytes();
		long length = bytes.length;
		
		if (length > 55)
			length = 55;
		
		for (int x = 0; x < length; x++) {
			block[x] = bytes[x];
		}
		
		block[(int)length] = (byte)0x01; // 1000 0000
		
		int offset = 56;
		long bits = 8 * length;
		// 64-bit length is appended in little endian order
		for(int i=0; i<64; i+=8)
			block[offset++] = (byte)(bits >>> (i) );
		
		this.coreUpdate(block, 0, 27);
		this.coreDigest(block, 0);
		return block;
	}

}
