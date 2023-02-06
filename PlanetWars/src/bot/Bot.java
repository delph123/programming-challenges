package bot;

public interface Bot {

	/** Bot version */
	public int getVersion();
	
	/** Play one turn. Issue commands on System.out, except "go". */
	public void playTurn(int turnNum);
	
}
