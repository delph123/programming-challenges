package bot;

public class CKS7 extends CollaborativeKnapsackBot {

	public static final int VERSION = 7;
	
	private CKS7(int horizon, double minWeightedValue) {
		super(horizon, minWeightedValue);
	}
	
	public int getVersion() {
		return VERSION;
	}
	
	public static void main(String[] args) {
		CKS7 b = new CKS7(Integer.parseInt(args[0]), Double.parseDouble(args[1]));
    	GameState.playGame(b);
    }
	
}
