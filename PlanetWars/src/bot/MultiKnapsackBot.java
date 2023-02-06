package bot;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;

public class MultiKnapsackBot implements Bot {
	
	public static final int VERSION = 3;

	private int horizon;
	private double minWeightedValue;
	
	private ArrayList<PlanVertex> planVertices;

	private MultiKnapsackBot(int horizon, double minWeightedValue) {
		this.horizon = horizon;
		this.minWeightedValue = minWeightedValue;
		this.planVertices = new ArrayList<PlanVertex>();
	}
	
	public int getVersion() {
		return VERSION;
	}
	
	/** Initialization (must be done at first turn):
	  * Generates ForecastedBase and PlanVertices for each existing Base.
	  */
	private void init() {
		planVertices.clear();
		for (Base b : GameState.getBases()) {
			planVertices.add(new PlanVertex(b));
		}
	}
	
	public void playTurn(int turnNum) {
		
		// (0) Prepare data.
		init();
		
		// Cannot send any flight if I have no Base!
		if (GameState.getMyBases().isEmpty()) return;
		
		
		// (1) Attack phase (attack enemy or neutral planet and defend friendly planet)
		LinkedList<AttackPlan> attackPlans = new LinkedList<AttackPlan>();
		
		for (Base source : GameState.getMyBases()) {
			for (Base target : GameState.getOtherBases()) {
				AttackPlan ap = simulate(source, target, horizon);
				if (ap.isOfInterest()) attackPlans.add(ap);
			}
		}
		
		Collections.sort(attackPlans, Collections.reverseOrder());
		
		AttackPlan ap = attackPlans.poll();
		
		while (ap != null && ap.getWeightedValue() > minWeightedValue) {
			
			Base b = ap.getSources().get(0).getReference();
			
			if (b.getNumShips() >= ap.getShipCost()) {
				GameState.issueOrder(b, ap.getTarget().getReference(), ap.getShipCost());
				b.removeShips(ap.getShipCost());
			}
			
			ap = attackPlans.poll();
		}
		
		// (2) Reorganize fleet on planets to maximize attack force.
		
	}
	
	
	private AttackPlan simulate(Base source, Base target, int horizon) {
		int shipValue = 0;
		int shipCost = 0;
		
    	int d = source.distanceTo(target);
    	
    	if (target.getOwner() == GameState.NEUTRAL) {
    		shipCost = target.getNumShips() + 1;
    		shipValue = target.getGrowthRate() * (horizon - d) - shipCost;
    	} else if (target.getOwner() >= GameState.OPPONENT) {
    		shipCost = target.getNumShips() + target.getGrowthRate() * d + 1;
    		shipValue = 2 * target.getGrowthRate() * (horizon - d);
    	}
		
		return new AttackPlan(planVertices.get(source.getPlanetID()), planVertices.get(target.getPlanetID()), shipValue, shipCost);
	}
	
    public static void main(String[] args) {
    	
    	MultiKnapsackBot b = new MultiKnapsackBot(Integer.parseInt(args[0]),
    											  Double.parseDouble(args[1]));
    	
    	GameState.playGame(b);

    }

}
