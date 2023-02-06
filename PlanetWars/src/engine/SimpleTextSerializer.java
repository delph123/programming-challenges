package engine;

import java.util.ArrayList;
import java.util.List;

public class SimpleTextSerializer implements Serializer {
	
	private char argOpen;
	private char argClose;
	private char argSeparator;

	public SimpleTextSerializer() {
		this('<', '>', ',');
	}
	
	public SimpleTextSerializer(char argOpen, char argClose, char argSeparator) {
		this.argOpen = argOpen;
		this.argClose = argClose;
		this.argSeparator = argSeparator;
	}
	
	public List<String> serialize(GameStatistics gs) {
		ArrayList<String> text = new ArrayList<String>();
		for (Battle b : gs.getBattles()) {
			text.add(serialize(b).get(0));
		}
		return text;
	}
	
	public List<String> serialize(Battle b) {
		List<String> map = serialize(b.getMap());
		List<String> player = serialize(b.getPlayer());
		List<String> opponent = serialize(b.getOpponent());
		String turn = String.valueOf(b.getTurn());
		String winner = String.valueOf(b.getWinner());
		return toStringList(buildText("Battle", map.get(0), player.get(0), opponent.get(0), turn, winner));
	}

	public List<String> serialize(Player p) {
		return toStringList(buildText("Player", p.getName(), p.getCommand()));
	}

	public List<String> serialize(Map m) {
		String set = String.valueOf(m.getSet());
		String num = String.valueOf(m.getNum());
		return toStringList(buildText("Map", set, num));
	}
	
	public String buildText(String name, String... args) {
		String params = "";
		boolean needComa = false;
		for (String arg : args) {
			if (needComa) {
				params += argSeparator + " " + arg;
			} else {
				params += arg;
				needComa = true;
			}
		}
		return name + argOpen + params + argClose;
	}
	
	public GameStatistics parseGameStatistics(List<String> text) throws IllegalArgumentException {
		GameStatistics gs = new GameStatistics();
		ArrayList<String> arg = new ArrayList<String>();
		arg.add("");
		
		for (String line : text) {
			arg.set(0, line);
			gs.addBattle(parseBattle(arg));
		}
		
		return gs;
	}
	
	public Battle parseBattle(List<String> lines) throws IllegalArgumentException {
		if (lines.size() != 1) {
			throw new IllegalArgumentException();
		}
		
		String text = lines.get(0);
		
		if ( ! text.startsWith("Battle") ) {
			throw new IllegalArgumentException();
		}
		
		ArrayList<String> args = parseArgs(text);
		
		if (args.size() != 5) {
			throw new IllegalArgumentException();
		}
		
		ArrayList<String> arg = new ArrayList<String>();
		arg.add("");
		
		arg.set(0, args.get(0));
		Map m = parseMap(arg);
		
		arg.set(0, args.get(1));
		Player p = parsePlayer(arg);
		
		arg.set(0, args.get(2));
		Player o = parsePlayer(arg);
		
		int turn = Integer.parseInt(args.get(3));
		int winner = Integer.parseInt(args.get(4));
		
		return new Battle(m, p, o, turn, winner);
	}
	
	public Player parsePlayer(List<String> lines) throws IllegalArgumentException {
		if (lines.size() != 1) {
			throw new IllegalArgumentException();
		}
		
		String text = lines.get(0);
		
		if ( ! text.startsWith("Player") ) {
			throw new IllegalArgumentException();
		}
		
		ArrayList<String> args = parseArgs(text);
		
		if (args.size() != 2) {
			throw new IllegalArgumentException();
		}
		
		return new Player(args.get(0), args.get(1));
	}
	
	public Map parseMap(List<String> lines) throws IllegalArgumentException {
		if (lines.size() != 1) {
			throw new IllegalArgumentException();
		}
		
		String text = lines.get(0);
		
		if ( ! text.startsWith("Map") ) {
			throw new IllegalArgumentException();
		}
		
		ArrayList<String> args = parseArgs(text);
		
		if (args.size() != 2) {
			throw new IllegalArgumentException();
		}
		
		if (args.get(0).length() != 1) {
			throw new IllegalArgumentException();
		}
		
		char set = args.get(0).charAt(0);
		int num = Integer.parseInt(args.get(1));
		
		return new Map(num, set);
	}
	
	public ArrayList<String> parseArgs(String text) throws IllegalArgumentException {
		
		ArrayList<String> argList = new ArrayList<String>();
		
		char[] value = text.toCharArray();
		int level = 0;
		int offset = 0;
		for (int i = 0; i < value.length; i++) {
			if (value[i] == argOpen) {
				level++;
				if (level == 1) {
					offset = i + 1;
				}
			} else if (value[i] == argClose) {
				level--;
				if (level < 0) {
					throw new IllegalArgumentException();
				} else if (level == 0) {
					// last arg is not added if it's empty.
					if (offset < i) {
						String arg = String.copyValueOf(value, offset, i - offset).trim();
						if ( ! arg.isEmpty() ) {
							argList.add(arg);
						}
					}
					return argList;
				}
			} else if (value[i] == argSeparator && level == 1) {
				String arg = String.copyValueOf(value, offset, i - offset).trim();
				argList.add(arg);
				offset = i + 1;
			}
		}
		
		if (level == 0) {
			return argList;
		} else {
			throw new IllegalArgumentException();
		}
		
	}
		
	public static List<String> toStringList(String s) {
		List<String> text = new ArrayList<String>();
		text.add(s);
		return text;
	}
	
}
