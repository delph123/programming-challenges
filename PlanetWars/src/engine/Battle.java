package engine;

public class Battle implements Comparable<Battle> {
	
	private Map map;
	private Player player;
	private Player opponent;
	
	private int turn;
	private int winner;
	
	public Battle(Map map, Player player, Player opponent) {
		this.map = map;
		this.player = player;
		this.opponent = opponent;
		this.turn = 0;
		this.winner = -1; // No winner, battle hasn't been played yet.
	}
	
	public Battle(Map map, Player player, Player opponent, int turn, int winner) {
		this.map = map;
		this.player = player;
		this.opponent = opponent;
		this.turn = turn;
		this.winner = winner;
	}
	
	public void setResult(int turn, int winner) {
		this.turn = turn;
		this.winner = winner;
	}
	
	public boolean hasResult() {
		return winner >= 0;
	}
	
	public Map getMap() {
		return map;
	}

	public Player getPlayer() {
		return player;
	}

	public Player getOpponent() {
		return opponent;
	}

	public int getTurn() {
		return turn;
	}

	public int getWinner() {
		return winner;
	}
	
	public String toString() {
		String res;
		if (winner == 1) {
			res = "wins at turn " + getTurn();
		} else if (winner == 2) {
			res = "lose at turn " + getTurn();
		} else if (winner == 0) {
			res = "draw at turn " + getTurn();
		} else {
			res = "";
		}
		return player.getName()
				+  " vs "
				+  opponent.getName()
				+  " on "
				+  map.getName()
				+  " -> "
				+  res;
	}
	
	public int compareTo(Battle o) {
		int r = this.map.compareTo(o.map);
		if (r != 0) return r;
		r = this.player.getName().compareTo(o.player.getName());
		if (r != 0) return r;
		r = this.player.getCommand().compareTo(o.player.getCommand());
		if (r != 0) return r;
		r = this.opponent.getName().compareTo(o.opponent.getName());
		if (r != 0) return r;
		r = this.opponent.getCommand().compareTo(o.opponent.getCommand());
		return r;
	}
	
}
