package bot;

import java.util.ArrayList;

public class AttackPlan implements Comparable<AttackPlan> {

//	private double positionalRelevance;
	
	private int shipValue;
	private int shipCost;
	
	private PlanVertex target;
	private ArrayList<PlanVertex> sources;
	
	private AttackPlan byPlan;
	
	private int allocatedShips;
	
	public AttackPlan(PlanVertex source, PlanVertex target) {
		this.target = target;
		this.sources = new ArrayList<PlanVertex>();
		sources.add(source);
	}
	
	public AttackPlan(PlanVertex source, PlanVertex target, int shipValue, int shipCost) {
		this(source, target);
		this.shipValue = shipValue;
		this.shipCost = shipCost;
	}
	
	public int getShipValue() {
		return shipValue;
	}

	public int getShipCost() {
		return shipCost;
	}

	public PlanVertex getTarget() {
		return target;
	}

	public ArrayList<PlanVertex> getSources() {
		return sources;
	}
	
	public ArrayList<Base> getReferenceSources() {
		ArrayList<Base> list = new ArrayList<Base>();
		for (PlanVertex pv : sources) {
			list.add(pv.getReference());
		}
		return list;
	}

	public AttackPlan getByPlan() {
		return byPlan;
	}

	public int getAllocatedShips() {
		return allocatedShips;
	}
	
	public boolean isOfInterest()  {
		return shipCost > 0 && shipValue > 0 && shipCost <= GameState.getAvailableShips(GameState.SELF);
	}
	
	public double getWeightedValue() {
    	if (shipCost == 0) {
    		return -1000000; // A high negative value => MIN
    	} else {
    		return ((double) shipValue) / ((double) shipCost);
    	}
	}
	
	public int compareTo(AttackPlan o) {
		long l1 = ((long) this.shipValue) * ((long) o.shipCost);
		long l2 = ((long) o.shipValue) * ((long) this.shipCost);
		if (l1 < l2) return -1;
		if (l1 > l2) return 1;
		if (this.shipValue < o.shipValue) return -1;
		if (this.shipValue > o.shipValue) return 1;
		double d1 = this.target.getReference().distanceTo(this.getReferenceSources());
		double d2 = o.target.getReference().distanceTo(o.getReferenceSources());
		if (d1 > d2) return -1;
		if (d1 < d2) return 1;
		return 0;
	}
	
	public int allocateShips(PlanVertex pv) {
		int maxNumShips = Math.max(shipCost - allocatedShips, 0);
		int numShips = Math.min(maxNumShips, pv.getAvailableShips());
		allocatedShips += numShips;
		return numShips;
	}
	
	public void schedule() {
		
		AttackPlan scheduledPlan = target.getScheduledPlan();
		
		if (scheduledPlan == null) {
			
			AttackPlan ap = this;
			
			if ( ! target.getWaitingPlans().isEmpty() ) {
				ap = target.getWaitingPlans().poll().merge(this);
			}
			
			int availableShips = 0;
			for (PlanVertex pv : ap.sources) {
				availableShips += pv.getAvailableShips();
			}
			
			if (availableShips >= shipCost) {
				
				target.schedule(ap);
				
			} else {
				
				// TODO try to change allocation strategy to release some ships
				// from other attack plans and use these ships for the AttackPlan.
				
				target.remember(ap);
				
			}
			
		} else {
			
			target.remember(this);
			
		}
		
	}
	
	public AttackPlan merge(AttackPlan other) {
		if (this.target != other.target) {
			throw new RuntimeException("Cannot merge attack plan's with different targets.");
		}
		shipValue = Math.min(this.shipValue, other.shipValue);
		shipCost = Math.max(this.shipCost, other.shipCost);
		sources.addAll(other.sources);
		if (other.byPlan != null) { this.byPlan = other.byPlan; }
		allocatedShips += other.allocatedShips;
		return this;
	}
	
	public String getSourcesToShortString() {
		String s = "[ ";
		for (PlanVertex pv : sources) {
			s += pv.getReference().toShortString() + ", ";
		}
		s += "]";
		return s;
	}
	
	public String toShortString() {
		return "Plan >" + target.getReference().getPlanetID()
			+ " (" + shipValue + "/" + shipCost + ") "
			+ allocatedShips + "$  <- " + getSourcesToShortString();
	}
	
	public String toString() {
		return "Plan >" + target.getReference().getPlanetID()
				+ " (" + shipValue + "/" + shipCost + ") "
				+ allocatedShips + " $\n"
				+ "-> " + target.getReference().toShortString() + "\n"
				+ "<- " + getSourcesToShortString();
	}
	
}
