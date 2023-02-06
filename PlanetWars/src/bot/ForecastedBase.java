package bot;

import java.util.Arrays;
import java.util.LinkedList;

public class ForecastedBase {
	
	private Base reference;
	private int horizon;
	
	private int owner, numShips;
	private int myNumShips, enemyNumShips, neutralNumShips;
	private LinkedList<Squadron> arrivingSquadrons;
	
	private int[] forecastedNumShips, forecastedOwner;
	private int[] forecastedShipsLost, forecastedShipsNeeded;
	
	private int[] forecastedShipCost, forecastedShipValue;
	
	public ForecastedBase(Base reference, int horizon) {
		this.reference = reference;
		this.horizon = horizon;
		this.arrivingSquadrons = new LinkedList<Squadron>();
		this.forecastedNumShips = new int[horizon+1];
		this.forecastedOwner = new int[horizon+1];
		this.forecastedShipsLost = new int[horizon+1];
		this.forecastedShipsNeeded = new int[horizon+1];
		this.forecastedShipCost = new int[horizon+1];
		this.forecastedShipValue = new int[horizon+1];
	}
	
	/** Get ShipCost for given Turn.
	  * 
	  * @param turnNum
	  * @return ShipCost
	  */
	public int getShipCost(int turnNum) {
		return getShipCost(turnNum, Integer.MAX_VALUE);
	}
	
	public int getShipCost(int turnNum, int maxNumShips) {
		if (turnNum > horizon) {
			return 0;
		}
		defendFrom(turnNum, maxNumShips);
		return forecastedShipCost[turnNum];
	}
	
	/** Get ShipValue for given Turn.
	  * 
	  * @param turnNum
	  * @return ShipValue
	  */
	public int getShipValue(int turnNum) {
		return getShipValue(turnNum, Integer.MAX_VALUE);
	}
	
	public int getShipValue(int turnNum, int maxNumShips) {
		if (turnNum > horizon) {
			return 0;
		}
		defendFrom(turnNum, maxNumShips);
		return forecastedShipValue[turnNum];
	}
	
	/** Compute how much ships I need to keep on planet
	  * to defend it.
	  * 
	  * Use getShipCost(0) & getShipValue(0) to retrieve
	  * figures.
	  */
	public void defend() {
		int numShips = reference.getNumShips();
		
		reference.setNumShips(0);
		playTurns();
		reference.setNumShips(numShips);
		defendFrom(0, numShips);
	}
	
	private void defendFrom(int turnNum, int maxNumShips) {
		
		// Exit if already computed
		if (forecastedShipCost[turnNum] >= 0) return;
		
		// Maximum number of ships to defend  
		int maxDefenseNumShips = maxNumShips - forecastedShipsNeeded[turnNum];
		if (forecastedOwner[turnNum] == GameState.SELF) {
			maxDefenseNumShips = Math.max(maxDefenseNumShips, maxDefenseNumShips + forecastedNumShips[turnNum]);
    	} else if (forecastedOwner[turnNum] == GameState.NEUTRAL ||
    				 forecastedOwner[turnNum] == GameState.OPPONENT &&
    				   (turnNum == 0 || forecastedOwner[turnNum-1] != GameState.SELF)) {
    		maxDefenseNumShips = Math.max(maxDefenseNumShips, maxDefenseNumShips + 1);
    	}
		
		// Not enough ships to take the planet!
		if (maxDefenseNumShips < 0) {
			forecastedShipCost[turnNum] = 0;
			forecastedShipValue[turnNum] = 0;
			return;
		}
		
		int endTurn = -1; // Moment where it's no longer possible to defend my planet
		
		// (1) Compute ShipCost for the given turn number.
		
		forecastedShipCost[turnNum] = 0; // Number of ships needed to defend = 0
		
		if (turnNum < horizon) {
			
			int ct = turnNum + 1; // Current turn number (relative)
	    	int cas = 0; // Current arriving ships until the turn (enemy minus self)
	    	
	    	for (Squadron s : reference.getArrivingSquadrons()) {
	    		
	    		if (s.getRemainingTurns() <= turnNum) continue;
	    		if (s.getRemainingTurns() > horizon) break;
	    		
	    		if (s.getRemainingTurns() != ct) {
	    			int k = cas - reference.getGrowthRate() * (ct - turnNum);
	    			if (k > 0 && k <= maxDefenseNumShips) {
	    				forecastedShipCost[turnNum] = Math.max(forecastedShipCost[turnNum], k);
	    			} else if (k > maxDefenseNumShips) {
	    				if (endTurn < 0) { endTurn = ct; }
	    			}
	    			ct = s.getRemainingTurns();
	    		}
	    		
				if (s.getOwner() == GameState.SELF) {
					cas -= s.getNumShips();
				} else {
					cas += s.getNumShips();
				}
	    		
	    	}
	    	
			int k = cas - reference.getGrowthRate() * (ct - turnNum);
			if (k > 0 && k <= maxDefenseNumShips) {
				forecastedShipCost[turnNum] = Math.max(forecastedShipCost[turnNum], k);
			} else if (k > maxDefenseNumShips) {
				if (endTurn < 0) { endTurn = ct; }
			}
			
			if (forecastedOwner[turnNum] == GameState.SELF) {
	    		forecastedShipCost[turnNum] -= forecastedNumShips[turnNum];
	    	} else if (forecastedOwner[turnNum] == GameState.NEUTRAL ||
	    				 forecastedOwner[turnNum] == GameState.OPPONENT &&
	    				   (turnNum == 0 || forecastedOwner[turnNum-1] != GameState.SELF)) {
	    		forecastedShipCost[turnNum]--;
	    	}
	    	
	    	forecastedShipCost[turnNum] = Math.max(forecastedShipCost[turnNum], 0);
			
		}
		
		forecastedShipCost[turnNum] += forecastedShipsNeeded[turnNum];
    	
		// (2) Compute ShipValue for the given turn number.
		
		forecastedShipValue[turnNum] = 0;
		
		if (endTurn < 0) endTurn = horizon + 1;
		
    	for (int i = turnNum; i < endTurn; i++) {
    		switch (forecastedOwner[i]) {
    		case GameState.SELF:
    			break;
			case GameState.NEUTRAL:
				forecastedShipValue[turnNum] += reference.getGrowthRate();
				break;
			default:
				forecastedShipValue[turnNum] += 2 * reference.getGrowthRate();
				break;
			}
    	}
    	
    	forecastedShipValue[turnNum] -= forecastedShipsLost[turnNum];
    	
	}
	
	/** Play all turns until the horizon and generates statistics about future of planet
	  * and everything needed to have an estimation of ShipCost and ShipNeeded.
	  */
	public void playTurns() {
		
		// Retrieve data for first turn from reference planet.
		
		owner = reference.getOwner();
		if (GameState.getBotVersion() <= CKS5.VERSION || owner != GameState.SELF) {
			numShips = reference.getNumShips();
		} else {
			numShips = 0;
		}
		
		arrivingSquadrons.addAll(reference.getArrivingSquadrons());
		
		// Turn 0.
		
		forecastedOwner[0] = owner;
		
		// Play each turn one by one from turn 1 to horizon.
		
		for (int i = 1; i <= horizon; i++) {
			
	    	// Clean my/enemy/neutral number of ships.
	    	prepare();
	    	
	    	// Add growthRate to owner.
	    	grow();
	    	
	    	// Receive fleets.
	    	while (! arrivingSquadrons.isEmpty() &&
	    			arrivingSquadrons.peek().getRemainingTurns() == i) {
	    		receiveSquadron(arrivingSquadrons.poll());
	    	}
	    	
	    	// Duel fleets.
	    	fight();
			
	    	store(i);
			
		}
		
		arrivingSquadrons.clear();
		
		// Clear ShipCost
		
		for (int i = 0; i <= horizon; i++) {
			forecastedShipCost[i] = -1;
		}
		
	}
    
    private void prepare() {
    	
    	// Back to a two players game.
		if (owner > GameState.OPPONENT) owner = GameState.OPPONENT;
    	
		// Fill my/enemy/neutral number of ships.
    	switch (owner) {
		case GameState.NEUTRAL:
			myNumShips = enemyNumShips = 0;
			neutralNumShips = numShips;
			break;
		case GameState.SELF:
			enemyNumShips = neutralNumShips = 0;
			myNumShips = numShips;
			break;
		default:
			myNumShips = neutralNumShips = 0;
			enemyNumShips = numShips;
			break;
		}
    	
    }
    
    private void grow() {
    	switch (owner) {
		case GameState.NEUTRAL:
			break;
		case GameState.SELF:
			myNumShips += reference.getGrowthRate();
			break;
		default:
			enemyNumShips += reference.getGrowthRate();
			break;
		}
    }
    
    private void receiveSquadron(Squadron s) {
    	switch (s.getOwner()) {
		case GameState.SELF:
			myNumShips += s.getNumShips();
			break;
		default:
			enemyNumShips += s.getNumShips();
			break;
		}
    }
    
    private void fight() {
    	if (neutralNumShips >= myNumShips && neutralNumShips >= enemyNumShips) {
    		if (myNumShips >= enemyNumShips) {
    			numShips = neutralNumShips - myNumShips;
    		} else {
    			numShips = neutralNumShips - enemyNumShips;
    		}
    		// Owner doesn't change (case 0/0/0)
    	} else if (myNumShips > enemyNumShips) {
    		if (enemyNumShips >= neutralNumShips) {
    			numShips = myNumShips - enemyNumShips;
    		} else {
    			numShips = myNumShips - neutralNumShips;
    		}
    		owner = GameState.SELF;
    	} else if (enemyNumShips > myNumShips) {
    		if (myNumShips >= neutralNumShips) {
    			numShips = enemyNumShips - myNumShips;
    		} else {
    			numShips = enemyNumShips - neutralNumShips;
    		}
    		owner = GameState.OPPONENT;
    	} else {
    		// Owner doesn't change
    		numShips = 0;
    	}
    }

    private void store(int i) {
    	forecastedNumShips[i] = numShips;
		forecastedOwner[i] = owner;
		switch (owner) {
		case GameState.SELF:
			forecastedShipsLost[i] = 0;
			forecastedShipsNeeded[i] = 0;
			break;
		case GameState.NEUTRAL:
			forecastedShipsLost[i] = Math.max(neutralNumShips - Math.max(myNumShips, enemyNumShips), 0);
			forecastedShipsNeeded[i] = Math.max(neutralNumShips - myNumShips, 0) + 1;
			break;
		default:
			forecastedShipsLost[i] = 0;
			forecastedShipsNeeded[i] = enemyNumShips - myNumShips;
			if (i == 0 || forecastedOwner[i-1] != GameState.SELF) forecastedShipsNeeded[i]++;
			break;
		}
    }
    
    public String toString() {
    	return "Forecast @" + reference.getPlanetID() + "\n"
    			+ "-> " + reference.toShortString() + "\n"
    			+ "{  " + Arrays.toString(forecastedNumShips) + "\n"
    			+ " ~ " + Arrays.toString(forecastedOwner) + "\n"
    			+ " - " + Arrays.toString(forecastedShipsLost) + "\n"
    			+ " * " + Arrays.toString(forecastedShipsNeeded) + " }\n"
    			+ "$ " + Arrays.toString(forecastedShipValue) + "\n"
    			+ "/ " + Arrays.toString(forecastedShipCost);
    }
    
}
