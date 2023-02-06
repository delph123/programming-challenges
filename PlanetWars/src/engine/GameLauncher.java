package engine;

import java.io.File;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

public class GameLauncher {
	
	public static String rootPath = "C:\\Users\\Delph\\workspace\\PlanetWars\\";
	public static String statsFilePath = "statistics\\stats_all_maps.txt";
	
	public static final int maxThreadNum = 2;
	public static int timeOut = 20000;
	public static int maxTurns = 200;
	
	public static String maps = "B/all";
	public static String[] players = new String[] { "LeJ_V3" };
	public static String[] opponents = new String[] {
		"CKS7<18, 0.05>", "CKS7<19, 0.00>", "CKS7<20, 0.00>", "CKS7<21, 0.20>",
		"CKS6<18, 0.05>", "CKS6<19, 0.00>", "CKS6<20, 0.00>", "CKS6<21, 0.20>",
		"CKS5<18, 0.05>", "CKS5<19, 0.00>", "CKS5<20, 0.00>", "CKS5<21, 0.20>",
		"mmKS-f-Bot<18, 0.05>", "mmKS-f-Bot<19, 0.15>", "mmKS-f-Bot<20, 0.00>", "mmKS-f-Bot<21, 0.10>",
		"mmKSBot<17, 0.15>", "mmKSBot<18, 0.05>", "mmKSBot<19, 0.20>",
		"MKS-f-Bot<19, 0.00>", "MKS-f-Bot<20, 0.00>", "MKS-f-Bot<21, 0.00>",
		"MKSBot<15,-0.20>", "MKSBot<16,-0.05>", "MKSBot<17, 0.10>",
		"RageBot.exe", "DualBot.exe", "BullyBot.exe", "ProspectorBot.exe",
		"LeJ_V3", //"BubbleBot", "LeJ_V1",
																											};
	public static int minKSvision = 17; // 17 (19) ->
	public static int maxKSvision = 21; //         -> (21) 23
	
	public static float minKSweightedVal =  0.0001f; // -0.3 (-0.2) ->
	public static float maxKSweightedVal =  0.2101f; //             -> (0.1) 0.3
	public static float stepKSweightedVal = 0.05f;

	public static boolean displayResults = true;

	public static void main(String[] args) {
		GameLauncher.getInstance().play(Map.getMaps(maps), Player.getPlayers(players), Player.getPlayers(opponents));
//		GameLauncher.getGameStatistics().printFilteredStats("mapSet", "player", "opponent");	// Print statistics filtered by a list of components (map/player/opponent)
//		System.out.println("--");
//		GameLauncher.getGameStatistics().printFilteredStats("player", "opponent");
//		System.out.println("--");
		GameLauncher.getGameStatistics().printFilteredStats("player");
//		System.out.println("--");
//		GameLauncher.getGameStatistics().printFilteredStats("opponent");
//		GameLauncher.getGameStatistics().printLost();
	}

	private int runningBattles;
	private int waitingBattles;

	private final LinkedList<Log> availableLogs;
	private final LinkedList<Log> usedLogs;
	
	private GameStatistics gameStatistics;
	
	private static GameLauncher instance;
	
	private GameLauncher() {
		
		runningBattles = 0;
		waitingBattles = 0;
		
		availableLogs = new LinkedList<Log>();
		usedLogs = new LinkedList<Log>();
		
		gameStatistics = new GameStatistics();
		
		for (int i = 1; i <= maxThreadNum; i++) {
			availableLogs.addLast(new Log(i));
		}
		
	}
	
	public static GameLauncher getInstance() {
		if (instance == null) instance = new GameLauncher();
		return instance;
	}
	
	public static GameStatistics getGameStatistics() {
		return getInstance().gameStatistics;
	}
	
	private void play(List<Map> ml, List<Player> pl, List<Player> ol) {
		
		GameStatistics recordedStats = null;
		
		try {
			recordedStats = GameStatistics.loadFromFile(new File(rootPath + statsFilePath), new SimpleTextSerializer());
		} catch (Exception e) {
			recordedStats = null;
		}
		
		long clock = System.currentTimeMillis();
		
		for (Map map : ml) {
			for (Player player : pl) {
				for (Player opponent : ol) {
					
					Battle b = new Battle(map, player, opponent);
					
					Battle bs = null;
					if (recordedStats != null) {
						bs = recordedStats.getBattle(map, player, opponent);
					}
					
					if (bs != null) {
						b.setResult(bs.getTurn(), bs.getWinner());
						gameStatistics.addBattle(b);
					} else {
						if (recordedStats != null) {
							recordedStats.addBattle(b);
						}
						launch(b);
					}
					
				}
			}
		}
		
		waitStatisticsComputed();
		
		clock = System.currentTimeMillis() - clock;
		
		System.out.println("--");
		System.out.printf("%1$d games played in %2$1.2f seconds (with an average of %3$1.1f ms by turn). %n", gameStatistics.getBattleCount(), ((float)clock) / 1000f, ((float)clock) / ((float)gameStatistics.getTotalTurnCount()));
		System.out.println("--");
		
		if (recordedStats == null) {
			// Initiate the file with current statistics. 
			recordedStats = gameStatistics;
		}
		recordedStats.writeToFile(new File(rootPath + statsFilePath), new SimpleTextSerializer());
		
	}
	
	private Log getLog() {
		Log l = availableLogs.removeFirst();
		usedLogs.addLast(l);
		
		return l;
	}
	
	private void releaseLog(Log l) {
		usedLogs.remove(l);
		availableLogs.add(l);
	}
	
	public synchronized void waitStatisticsComputed() {
		
		while ( waitingBattles > 0 || runningBattles > 0) {
			try {
				wait();
			} catch (InterruptedException e) {
				
			}
		}
		
	}
	
	public synchronized void launch(Battle b) {
		
		waitingBattles++;
		
		while (runningBattles >= maxThreadNum) {
			try {
				wait();
			} catch (InterruptedException e) {
				
			}
		}
		
		waitingBattles--;
		
		runningBattles++;
		
		Launcher l = new Launcher(b, getLog());
		l.start();
		
	}
	
	public synchronized void battleFinished(Battle b, Log l) {
		
		runningBattles--;
		gameStatistics.addBattle(b);
		
		releaseLog(l);
		
		notifyAll();
		
	}
	
	private static class Launcher extends Thread {
		
		private Battle battle;
		private Log log;
		
		public Launcher(Battle battle, Log log) {
			this.battle = battle;
			this.log = log;
		}
		
		public void run() {
			
			try {
				
				Process p = new ProcessBuilder(//"java", "-jar", "PlayGame.jar",
											   rootPath + "bin\\playgame.exe",
											   battle.getMap().getCommand(),
											   "" + GameLauncher.timeOut,
											   "" + GameLauncher.maxTurns,
											   log.getCommand(),
											   "\"" + battle.getPlayer().getCommand() + "\"",
											   "\"" + battle.getOpponent().getCommand() + "\"")
									.directory(new File(rootPath + "bin"))
									.start();
				
				AsyncStreamConsumer asc = new AsyncStreamConsumer(p.getInputStream());
				asc.start();
				
				GameAnalyser ga = new GameAnalyser(battle, p.getErrorStream());
				ga.start();
				
				p.waitFor();
				
				GameLauncher.getInstance().battleFinished(battle, log);
				
			} catch (IOException e) {
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
		}
		
	}
	
}
