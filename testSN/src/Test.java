public class Test {
	public static void main(String[] args) {

		//String sn = "41003B000657334D37373920";
		String sn = "003832394D33570B001D0038";
		int number1 = (int) Long.parseLong(sn.substring(0, 8), 16);
		int number2 = (int) Long.parseLong(sn.substring(8, 16), 16);
		int number3 = (int) Long.parseLong(sn.substring(16, 24), 16);

		int uniqueID = ((number3 >> 1) + (number2 >> 2) + (number1 >> 3)) & 0xFFFFFF;

		System.out.println("number1: " + number1 + "  number2: " + number2
				+ " number3:  " + number3);

		System.out.println("sn: " + sn);
		System.out.println("uniqueID: " + format(uniqueID));
	}

	public static String format(int n) {
		String str = Integer.toHexString(n);
		int l = str.length();
		if (l == 1)
			return "0" + str;
		else
			str.substring(l - 2, l);
		return str;
	}
}