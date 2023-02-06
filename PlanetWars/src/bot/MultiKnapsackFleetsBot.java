package bot;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;

public class MultiKnapsackFleetsBot implements Bot {

	public static final int VERSION = 4;
	
	private int horizon;
	private double minWeightedValue;
	
	private ArrayList<ForecastedBase> forecastedBases;
	private ArrayList<PlanVertex> planVertices;

	private MultiKnapsackFleetsBot(int horizon, double minWeightedValue) {
		this.horizon = horizon;
		this.minWeightedValue = minWeightedValue;
		this.forecastedBases = new ArrayList<ForecastedBase>();
		this.planVertices = new ArrayList<PlanVertex>();
	}
	
	public int getVersion() {
		return VERSION;
	}
	
    public static void main(String[] args) {
    	
    	MultiKnapsackFleetsBot b = new MultiKnapsackFleetsBot(Integer.parseInt(args[0]), Double.parseDouble(args[1]));
    	
    	GameState.playGame(b);

    }
    
    /** Initialization (must be done at first turn):
	  * Generates ForecastedBase and PlanVertices for each existing Base.
	  */
	private void init() {
		forecastedBases.clear();
		for (Base b : GameState.getBases()) {
			forecastedBases.add(new ForecastedBase(b, horizon));
		}
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
		
		// (1) Simulate fleets arrival everywhere until horizon.
		for (ForecastedBase fb : forecastedBases) {
			fb.playTurns();
		}
		
		// (2) Attack phase (attack enemy or neutral planet and defend friendly planet)
		LinkedList<AttackPlan> attackPlans = new LinkedList<AttackPlan>();
		
		// My bases attack/defend other bases.
		for (Base source : GameState.getMyBases()) {
			for (Base target : GameState.getBases()) {
				if (source != target) {
					
					int d = source.distanceTo(target);
			    	
					ForecastedBase fb = forecastedBases.get(target.getPlanetID());
					PlanVertex pvSource = planVertices.get(source.getPlanetID());
					PlanVertex pvTarget = planVertices.get(target.getPlanetID());
					
					int shipCost = fb.getShipCost(d);
					int shipValue = fb.getShipValue(d);
										
					AttackPlan ap = new AttackPlan(pvSource, pvTarget, shipValue, shipCost);
					if (ap.isOfInterest()) attackPlans.add(ap);
					
				}
			}
		}
		
		// My bases defend themselves.
		for (Base b : GameState.getMyBases()) {
			
			ForecastedBase fb = forecastedBases.get(b.getPlanetID());
			PlanVertex pv = planVertices.get(b.getPlanetID());
			
			fb.defend();
			
			int shipCost = fb.getShipCost(0);
			int shipValue = fb.getShipValue(0);
								
			AttackPlan ap = new AttackPlan(pv, pv, shipValue, shipCost);
			if (ap.isOfInterest()) attackPlans.add(ap);
			
		}
		
		Collections.sort(attackPlans, Collections.reverseOrder());
		
		AttackPlan ap = attackPlans.poll();
		
		while (ap != null && ap.getWeightedValue() > minWeightedValue) {
			
			Base source = ap.getSources().get(0).getReference();
			
			if (source.getNumShips() >= ap.getShipCost()) {
				GameState.issueOrder(source, ap.getTarget().getReference(), ap.getShipCost());
				source.removeShips(ap.getShipCost());
			}
			
			ap = attackPlans.poll();
			
		}
		
	}
		
}
