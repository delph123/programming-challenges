package engine;

import java.util.List;

public interface Serializer {
	
	public List<String> serialize(GameStatistics gs);
	
	public List<String> serialize(Battle gs);
	
	public List<String> serialize(Player gs);
	
	public List<String> serialize(Map gs);
	
	public GameStatistics parseGameStatistics(List<String> text) throws IllegalArgumentException;
	
	public Battle parseBattle(List<String> text) throws IllegalArgumentException;
	
	public Player parsePlayer(List<String> text) throws IllegalArgumentException;
	
	public Map parseMap(List<String> text) throws IllegalArgumentException;
	
}
