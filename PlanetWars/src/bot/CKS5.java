package bot;

public class CKS5 extends CollaborativeKnapsackBot {
	
	public static final int VERSION = 5;
	
	private CKS5(int horizon, double minWeightedValue) {
		super(horizon, minWeightedValue);
	}
	
	public int getVersion() {
		return VERSION;
	}
	
	public static void main(String[] args) {
		CKS5 b = new CKS5(Integer.parseInt(args[0]), Double.parseDouble(args[1]));
    	GameState.playGame(b);
    }

}
