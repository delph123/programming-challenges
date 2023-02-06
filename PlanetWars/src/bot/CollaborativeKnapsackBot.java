package bot;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.Map;

public abstract class CollaborativeKnapsackBot implements Bot {
	
	private int horizon;
	private double minWeightedValue;
	
	private ArrayList<ForecastedBase> forecastedBases;
	private ArrayList<PlanVertex> planVertices;

	protected CollaborativeKnapsackBot(int horizon, double minWeightedValue) {
		this.horizon = horizon;
		this.minWeightedValue = minWeightedValue;
		this.forecastedBases = new ArrayList<ForecastedBase>();
		this.planVertices = new ArrayList<PlanVertex>();
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
		
		// Cannot send any flight if I have no ship available!
		if (GameState.getAvailableShips(GameState.SELF) == 0) return;
		
		// (1) Simulate fleets arrival everywhere until horizon.
		for (ForecastedBase fb : forecastedBases) {
			fb.playTurns();
		}
		
		for (PlanVertex pv : planVertices) {
			pv.reset();
		}
		
		// (2) Simulation phase (simulate an attack of any enemy or neutral planet
		//     and a defense of any friendly planet from each friendly planets).
		LinkedList<AttackPlan> attackPlans = new LinkedList<AttackPlan>();
		
		for (Base source : GameState.getMyBases()) {
			for (Base target : GameState.getBases()) {
				
				if (getVersion() >= CKS6.VERSION || source != target) {
					
					int d = source.distanceTo(target);
			    	
					ForecastedBase fb = forecastedBases.get(target.getPlanetID());
					PlanVertex pvSource = planVertices.get(source.getPlanetID());
					PlanVertex pvTarget = planVertices.get(target.getPlanetID());
					
					int shipCost = fb.getShipCost(d, GameState.getAvailableShips(GameState.SELF));
					int shipValue = fb.getShipValue(d, GameState.getAvailableShips(GameState.SELF));
					
					AttackPlan ap = new AttackPlan(pvSource, pvTarget, shipValue, shipCost);
					if (ap.isOfInterest()) attackPlans.add(ap);
					
				}
					
			}
		}
		
		// My bases defend themselves.
		if (getVersion() < CKS6.VERSION) {
			for (Base b : GameState.getMyBases()) {
				
				ForecastedBase fb = forecastedBases.get(b.getPlanetID());
				PlanVertex pv = planVertices.get(b.getPlanetID());
				
				fb.defend();
				
				int shipCost = fb.getShipCost(0);
				int shipValue = fb.getShipValue(0);
									
				AttackPlan ap = new AttackPlan(pv, pv, shipValue, shipCost);
				if (ap.isOfInterest()) attackPlans.add(ap);
				
			}
		}
				
		// (3) Knapsack problem resolution (simple solution here:
		//     descending sort of attack plans according to plan's ShipValue / plan's ShipCost) 
		Collections.sort(attackPlans, Collections.reverseOrder());
		
		// (4) Merge attack plans to schedule a collaborative attack and defense of planets.
		AttackPlan ap = attackPlans.poll();
		
		while (ap != null && ap.getWeightedValue() > minWeightedValue) {
			
			ap.schedule();
			
			ap = attackPlans.poll();
			
		}
		
		// (5) Issue Orders
		for (PlanVertex pv : planVertices) {
			for (Map.Entry<PlanVertex, Integer> entry : pv.getAllocatedShips().entrySet()) {
				int numShips = entry.getValue().intValue();
				if (numShips > 0 && !entry.getKey().getReference().equals(pv.getReference())) {
					GameState.issueOrder(pv.getReference().getPlanetID(),
										 entry.getKey().getReference().getPlanetID(),
										 numShips);
				}
			}
		}
		
	}

}
