package bot;

public class CKS6 extends CollaborativeKnapsackBot {

	public static final int VERSION = 6;
	
	private CKS6(int horizon, double minWeightedValue) {
		super(horizon, minWeightedValue);
	}
	
	public int getVersion() {
		return VERSION;
	}
	
	public static void main(String[] args) {
		CKS6 b = new CKS6(Integer.parseInt(args[0]), Double.parseDouble(args[1]));
    	GameState.playGame(b);
    }
	
}
