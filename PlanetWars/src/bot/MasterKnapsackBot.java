package bot;

import java.util.Collections;

public class MasterKnapsackBot implements Bot {
	
	public static final int VERSION = 1;
	
	private int numTurnForward;
	private double minWeightedValue;
	
	private MasterKnapsackBot(int numTurnForward, double minWeightedValue) {
		this.numTurnForward = numTurnForward;
		this.minWeightedValue = minWeightedValue;
	}
	
	public int getVersion() {
		return VERSION;
	}
	
    /** The playTurn function is where your code goes. The PlanetWars object
      * contains the state of the game, including information about all planets
      * and fleets that currently exist. Inside this function, you issue orders
      * using the PlanetWars.IssueOrder() function. For example, to send 10 ships
      * from planet 3 to planet 8, you would say PlanetWars.IssueOrder(3, 8, 10).
      *
      * There is already a basic strategy in place here. You can use it as a
      * starting point, or you can throw it out entirely and replace it with
      * your own. Check out the tutorials and articles on the contest website at
      * http://www.ai-contest.com/resources.
      */
    public void playTurn(int turnNumber) {
    	
    	// Cannot send any flight if I have no Base!
    	if (GameState.getMyBases().isEmpty()) return;
		
    	// (1) Determine a Master Base, from / to which Squadron are sent. 
		double min = Double.MAX_VALUE;
		Base master = null;

		for (Base b : GameState.getMyBases()) {
			double d = b.distanceTo(GameState.getOtherBases());
			d /= b.getNumShips() + 1;  // In case base 'b' has no ships on it.
			if (d < min) {
				min = d;
				master = b;
			}
		}
		
		// (2) Defend my Master Base (send ships to it)
		defend(master);
		
		// (3) Attack other planets from my Master Base
		attack(master);
		
    }
    
    /** Defend Master Base. */
    private void defend(Base master) {
    	
    	// Current strategy: do nothing!
    	
//    	for (Base b : GameState.getMyBases()) {
//    		if (b != master) {
//    			GameState.issueOrder(b, master, b.getNumShips());
//    		}
//    	}
    	
    }
    
    /** Attack from Master Base. */
    private void attack(Base master) {
    	
    	// (1) Compute a value & a cost to attack each enemy/neutral planets
    	for (Base b : GameState.getOtherBases()) {
    		b.receive(master, numTurnForward);
    	}
    	
    	// (2) Greedy approximation of Knapsack problem:
    	//       - Sort according to value/cost in descending order
    	//		 - Send fleet has long has the cost is tolerable in sorted order
    	Collections.sort(GameState.getOtherBases());
    	
    	for (Base b : GameState.getOtherBases()) {
    		
    		// Cost is not tolerable if value/cost is bellow a limit
    		if (b.getWeightedValue() <= minWeightedValue) {
    			continue;
    		}
    		
    		// Send fleet if the planet contains enough ships
    		if (master.getNumShips() >= b.getShipCost()) {
    			GameState.issueOrder(master, b, b.getShipCost());
    			master.removeShips(b.getShipCost());
    		}
    		
    	}
    	
    }

    public static void main(String[] args) {
    	
    	MasterKnapsackBot b = new MasterKnapsackBot(Integer.parseInt(args[0]), Double.parseDouble(args[1]));
    	
    	GameState.playGame(b);

    }
    
}

