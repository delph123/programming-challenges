package engine;

import java.util.LinkedList;
import java.util.List;

public class Map implements Comparable<Map> {

	public final static int DUMMY_MAP_NUM = -1;
	public final static char DUMMY_MAP_SET = '*';
	
	private int num;
	private char set;
	
	public Map(int num, char set) {
		this.num = num;
		this.set = set;
	}
	
	public int getNum() {
		return num;
	}
	
	public char getSet() {
		return set;
	}
	
	public String getName() {
		if (num == DUMMY_MAP_NUM) {
			return "map " + set + "/***";
		} else {
			return String.format("map " + set + "/%1$3d", num);
		}
	}
	
	public String getCommand() {
		return "..\\maps" + set + "\\map" + num + ".txt";
	}
	
	public static List<Map> getAllMaps() {
		List<Map> list = new LinkedList<Map>();
		list.addAll(getAllMaps('A'));
		list.addAll(getAllMaps('B'));
		list.addAll(getAllMaps('C'));
		return list;
	}
	
	public static List<Map> getAllMaps(char set) {
		if (set == 'B') {
			return getMaps('B', 1, 199);
		} else if (set == 'C') {
			return getMaps('C', 1, 200);
		} else {
			return getMaps(set, 1, 100);
		}
	}
	
	public static List<Map> getMaps(char set, int start, int end) {
		List<Map> list = new LinkedList<Map>();
		for (int i = start; i <= end; i++) {
			list.add(new Map(i, set));
		}
		return list;
	}
	
	public static List<Map> getMaps(String s) {
		if (s.equalsIgnoreCase("all")) {
			return getAllMaps();
		} else if (s.contains(",")) {
			List<Map> list = new LinkedList<Map>();
			for (String sub : s.split(",")) {
				list.addAll(getMaps(sub));
			}
			return list;
		} else if (s.contains("/")) {
			String[] sub = s.split("/");
			return getMaps(sub[0].charAt(0), sub[1]);
		} else if (s.contains(":")) {
			String[] sub = s.split(":");
			return getMaps('A', Integer.parseInt(sub[0]), Integer.parseInt(sub[1]));
		} else {
			List<Map> list = new LinkedList<Map>();
			list.add(new Map(Integer.parseInt(s), 'A'));
			return list;
		}
	}
	
	public static List<Map> getMaps(char set, String s) {
		if (s.equalsIgnoreCase("all")) {
			return getAllMaps(set);
		} else if (s.contains(":")) {
			String[] sub = s.split(":");
			return getMaps(set, Integer.parseInt(sub[0]), Integer.parseInt(sub[1]));
		} else {
			List<Map> list = new LinkedList<Map>();
			list.add(new Map(Integer.parseInt(s), set));
			return list;
		}
	}
	
	public static boolean applicable(Map map, Map filter) {
		return (map.set == filter.set || filter.set == DUMMY_MAP_SET)
			&& (map.num == filter.num || filter.num == DUMMY_MAP_NUM);
	}
	
	public int compareTo(Map o) {
		return this.set < o.set ? -1 : (this.set > o.set ? 1 : (this.num < o.num ? -1 : (this.num > o.num ? 1 : 0)));
	}
	
}
