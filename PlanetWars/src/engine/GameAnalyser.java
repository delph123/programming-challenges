package engine;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class GameAnalyser extends Thread {
	
	private BufferedReader in;
	
	private Battle battle;
	private boolean parsed = false;
	private int turn = 0;
	private int winner = -1;
	
	public GameAnalyser(Battle b, InputStream in) {
		this.battle = b;
		this.in = new BufferedReader(new InputStreamReader(in));
	}
	
	public void run() {
		try {
			String s = null;
			while ( (s = in.readLine()) != null ) {
				parse(s);
			}
			in.close();
		} catch (IOException e) { }
		
		if (parsed) {
			battle.setResult(turn, winner);
		}
		
		if (GameLauncher.displayResults) {
			System.out.println(battle.toString());
		}
	}
	
	public void parse(String s) {
		
		String[] tokens = s.split(" ");
		
		if (tokens.length == 2 && tokens[0].equals("Turn")) {
			turn = Integer.parseInt(tokens[1]);
			return;
		} else if (tokens.length == 3 && tokens[0].equals("Player") && tokens[2].equals("Wins!")) {
			try {
				winner = Integer.parseInt(tokens[1]);
				parsed = true;
				return;
			} catch (NumberFormatException e) { /* Continue: cannot parse string. */ }
		} else if (tokens.length == 1 && tokens[0].equals("Draw!")) {
			winner = 0;
			parsed = true;
			return;
		}
		
		// String could not be parsed.
		System.err.println(battle.toString() + "Turn " + turn + ": " + s);
		
	}
	
}
