package engine;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class Player implements Comparable<Player> {
	
	private static int playerCount = 0;
	
	private int pid;
	private String name;
	private String command;
	
	public Player(String name, String command) {
		playerCount++;
		this.pid = playerCount;
		this.name = name;
		this.command = command;
	}

	public String getName() {
		return name;
	}
	
	public String getCommand() {
		return command;
	}
	

	public int compareTo(Player o) {
		return this.pid < o.pid ? -1 : (this.pid == o.pid ? 0 : 1);
	}
	
	public static List<Player> getPlayers(String... players) {
		
		ArrayList<Player> list = new ArrayList<Player>();
		
		for (String name : players) {
			
			if (name.endsWith(".exe")) {
				
				list.add(new Player(name.substring(0, name.length() - 4), name));
				
			} else if (name.contains("<")) {
				
				int o = name.indexOf("<");
				
				String shortName = name.substring(0, o);
				String longName = getLongName(shortName);
				
				List<String> args = new SimpleTextSerializer().parseArgs(name);
				
				String flatArgs = "";
				for (String arg : args) {
					if (arg.equals("0.00")) {
						flatArgs += " 0.00001";
					} else {
						flatArgs += " " + arg;						
					}
				}
				
				list.add(new Player(name, "java bot." + longName + flatArgs));
				
			} else if (name.contains("KS")) {
				
				for (int i = GameLauncher.minKSvision; i <= GameLauncher.maxKSvision; i++) {
					for (float d = GameLauncher.minKSweightedVal; d <= GameLauncher.maxKSweightedVal; d += GameLauncher.stepKSweightedVal) {
						String longName = getLongName(name);
						String vision = String.format(Locale.US, "%1$2d", i);
						String weight = String.format(Locale.US, "%1$ 1.2f", d);
						String longVision = vision.trim();
						String longWeight = weight.trim();
						if (d > -0.01f && d < 0.01f) {
							weight = " 0.00";
							longWeight = "0.00001";
						}
						list.add(new Player(name + "<" + vision + "," + weight + ">", "java bot." + longName + " " +  longVision + " " + longWeight));
					}
				}
			
			} else {
				
				list.add(new Player(name, "java -jar " + name + ".jar"));
				
			}
			
		}
		
		return list;
	}
	
	public static String getLongName(String name) {
		if (name.equals("MKSBot")) {
			return "MasterKnapsackBot";
		} else if (name.equals("mmKSBot")) {
			return "MultiKnapsackBot";
		} else if (name.equals("MKS-f-Bot")) {
			return "MasterKnapsackFleetsBot";
		} else if (name.equals("mmKS-f-Bot")) {
			return "MultiKnapsackFleetsBot";
		} else {
			return name;
		}
	}
	
}
