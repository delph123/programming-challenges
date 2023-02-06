package engine;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import bot.GameState;

public class GameStatistics {
	
	private TreeSet<Battle> battles;
	
	private Set<Map> maps;
	private Set<Player> players;
	private Set<Player> opponents;
	
	public GameStatistics() {
		battles = new TreeSet<Battle>();
		maps = new TreeSet<Map>();
		players = new TreeSet<Player>();
		opponents = new TreeSet<Player>();
	}
	
	public static GameStatistics loadFromFile(File file, Serializer ser) throws IOException, IllegalArgumentException {
		
		BufferedReader bfr = new BufferedReader(new FileReader(file));
		
		ArrayList<String> text = new ArrayList<String>();
		String line = null;
		while ( (line = bfr.readLine()) != null ) {
			text.add(line);
		}
		
		return ser.parseGameStatistics(text);
		
	}
	
	public void writeToFile(File file, Serializer ser) {
		try {
			
			PrintWriter pfw = new PrintWriter(file);
			
			for (String line : ser.serialize(this)) {
				pfw.println(line);
			}
			
			pfw.close();
			
		} catch (IOException e) { }
	}
	
	public Set<Battle> getBattles() {
		return battles;
	}
	
	public Battle getBattle(Map map, Player player, Player opponent) {
		Battle bs1 = new Battle(map, player, opponent);
		Battle bf1 = battles.floor(bs1);
		if (bf1 != null && bf1.compareTo(bs1) == 0 && bf1.hasResult()) {
			return bf1;
		} else {
			Battle bs2 = new Battle(map, opponent, player);
			Battle bf2 = battles.floor(bs2);
			if (bf2 != null && bf2.compareTo(bs2) == 0 && bf2.hasResult()) {
				return new Battle(map, player, opponent, bf2.getTurn(), swapWinner(bf2.getWinner()));
			} else {
				return null;
			}
		}
	}
	
	private int swapWinner(int winner) {
		if (winner == 1) {
			return 2;
		} else if (winner == 2) {
			return 1;
		} else {
			return winner;
		}
	}
	
	public void addBattle(Battle b) {
		
		battles.add(b);
		
		maps.add(b.getMap());
		players.add(b.getPlayer());
		opponents.add(b.getOpponent());
		
	}
	
	public int getBattleCount() {
		GameLauncher.getInstance().waitStatisticsComputed();
		return battles.size();
	}
	
	public int getTotalTurnCount() {
		GameLauncher.getInstance().waitStatisticsComputed();
		int turnCount = 0;
		for (Battle b : battles) {
			if (b.getWinner() >= 0) turnCount += b.getTurn();
		}
		return turnCount;
	}
	
	public void printLost() {
		
		GameLauncher.getInstance().waitStatisticsComputed();
		
		for (Battle b : battles) {
			if (b.getWinner() >= GameState.OPPONENT) {
				System.out.println(b.toString());
			}
		}
		
	}
	
	public void printFilteredStats(String... filters) {
		
		GameLauncher.getInstance().waitStatisticsComputed();
		
		Map dummyMap = new Map(Map.DUMMY_MAP_NUM, Map.DUMMY_MAP_SET);
		List<Map> mapCats = new ArrayList<Map>();
		mapCats.add(new Map(Map.DUMMY_MAP_NUM, 'A'));
		mapCats.add(new Map(Map.DUMMY_MAP_NUM, 'B'));
		mapCats.add(new Map(Map.DUMMY_MAP_NUM, 'C'));
		Player dummyPlayer = new Player("Dummy Player", "Dummy Player");
		
		List<Map> maps1 = new ArrayList<Map>();
		List<Map> maps2 = new ArrayList<Map>();
		List<Map> maps3 = new ArrayList<Map>();
		List<Player> players1 = new ArrayList<Player>();
		List<Player> players2 = new ArrayList<Player>();
		List<Player> opponents1 = new ArrayList<Player>();
		List<Player> opponents2 = new ArrayList<Player>();
		
		if (filters.length > 0 && filters[0].startsWith("map")) {
			if (filters[0].equals("mapSet")) {
				maps1.addAll(mapCats);
			} else {
				maps1.addAll(maps);
			}			
			maps2.add(dummyMap);
			maps3.add(dummyMap);
		} else if (filters.length > 1 && filters[1].startsWith("map")) {
			maps1.add(dummyMap);
			if (filters[0].equals("mapSet")) {
				maps2.addAll(mapCats);
			} else {
				maps2.addAll(maps);
			}
			maps3.add(dummyMap);
		} else if (filters.length > 2 && filters[2].startsWith("map")) {
			maps1.add(dummyMap);
			maps2.add(dummyMap);
			if (filters[0].equals("mapSet")) {
				maps3.addAll(mapCats);
			} else {
				maps3.addAll(maps);
			}
		} else {
			maps1.add(dummyMap);
			maps2.add(dummyMap);
			maps3.add(dummyMap);
		}
		
		if (filters.length > 0 && filters[0].equals("player")) {
			players1.addAll(players);
			opponents1.add(dummyPlayer);
		} else if (filters.length > 0 && filters[0].equals("opponent")) {
			players1.add(dummyPlayer);
			opponents1.addAll(opponents);
		}

		if (filters.length > 1 && filters[1].equals("player")) {
			if (players1.isEmpty()) {
				players1.addAll(players);
				opponents1.add(dummyPlayer);
			} else {
				players2.addAll(players);
				opponents2.add(dummyPlayer);
			}
		} else if (filters.length > 1 && filters[1].equals("opponent")) {
			if (opponents1.isEmpty()) {
				players1.add(dummyPlayer);
				opponents1.addAll(opponents);
			} else {
				players2.add(dummyPlayer);
				opponents2.addAll(opponents);
			}
		}

		if (filters.length > 2 && filters[2].equals("player")) {
			players2.addAll(players);
			opponents2.add(dummyPlayer);
		} else if (filters.length > 2 && filters[2].equals("opponent")) {
			players2.add(dummyPlayer);
			opponents2.addAll(opponents);
		}
		
		if (players1.isEmpty())   { players1.add(dummyPlayer);   }
		if (players2.isEmpty())   { players2.add(dummyPlayer);   }
		if (opponents1.isEmpty()) { opponents1.add(dummyPlayer); }
		if (opponents2.isEmpty()) { opponents2.add(dummyPlayer); }
		
		for (Map m1 : maps1) {
		for (Player p1 : players1) {
		for (Player o1 : opponents1) {
		for (Map m2 : maps2) {
		for (Player p2 : players2) {
		for (Player o2 : opponents2) {
		for (Map m3 : maps3) {
				
			int draw = 0, wins = 0, lose = 0, turns = 0;
			
			for (Battle b : battles) {
				if (   (b.getPlayer() == p1 || b.getPlayer() == p2 || p1 == dummyPlayer && p2 == dummyPlayer)
					&& (b.getOpponent() == o1 || b.getOpponent() == o2 || o1 == dummyPlayer && o2 == dummyPlayer)
					&& (Map.applicable(b.getMap(), m1) && Map.applicable(b.getMap(), m2) && Map.applicable(b.getMap(), m3))) {
				
					if (b.getWinner() == GameState.NEUTRAL)  draw++;
					if (b.getWinner() == GameState.SELF) 	 wins++;
					if (b.getWinner() >= GameState.OPPONENT) lose++;
					
					if (b.getWinner() >= 0) 				 turns += b.getTurn();
					
				}
			}
			
			String fs, ps = null;
			if (p1 != dummyPlayer) {
				fs = "%1$-20s ";
				ps = p1.getName();
			} else if (p2 != dummyPlayer) {
				fs = "%1$-20s ";
				ps = p2.getName();
			} else {
				fs = "";
				ps = "";
			}
			
			String os = null;
			if (o1 != dummyPlayer) {
				fs += "vs %2$-20s ";
				os = o1.getName();
			} else if (o2 != dummyPlayer) {
				fs += "vs %2$-20s ";
				os = o2.getName();
			} else {
				os = "";
			}
			
			if (m1 != dummyMap) {
				fs += "on " + m1.getName() + " ";
			} else if (m2 != dummyMap) {
				fs += "on " + m2.getName() + " ";
			} else if (m2 != dummyMap) {
				fs += "on " + m3.getName() + " ";
			}
			
			fs += "%3$3d /%4$3d /%5$3d wins/draw/lose";
			
			if (draw + wins + lose != 0) {
				
				turns = turns / (draw + wins + lose);
				fs += " in average %6$4d turns";
				
				System.out.format(fs + "%n", ps, os, wins, draw, lose, turns);
				
			}
		}
		}
		}
		}
		}
		}
		}
	}
	
}
