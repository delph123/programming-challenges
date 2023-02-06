package engine;

public class Log {

	private int num;
	
	public Log(int num) {
		this.num = num;
	}
	
	public String getCommand() {
		return "..\\logs\\log" + num + ".txt";
	}
	
}
