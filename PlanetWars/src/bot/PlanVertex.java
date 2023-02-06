package bot;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

public class PlanVertex {
	
	private Base reference;
	
	private int availableShips;
	private HashMap<PlanVertex, Integer> allocatedShips;
	
	private LinkedList<AttackPlan> waitingPlans;
	private AttackPlan scheduledPlan;
	
	public PlanVertex(Base reference) {
		this.reference = reference;
		waitingPlans = new LinkedList<AttackPlan>();
		allocatedShips = new HashMap<PlanVertex, Integer>();
	}
	
	public Base getReference() {
		return reference;
	}
	
	public int getAvailableShips() {
		return availableShips;
	}
	
	public LinkedList<AttackPlan> getWaitingPlans() {
		return waitingPlans;
	}
	
	public AttackPlan getScheduledPlan() {
		return scheduledPlan;
	}
	
	public HashMap<PlanVertex, Integer> getAllocatedShips() {
		return allocatedShips;
	}
	
	public void reset() {
		
		availableShips = 0;
		allocatedShips.clear();
		
		waitingPlans.clear();
		scheduledPlan = null;
		
		if (reference.getOwner() == GameState.SELF) {
			availableShips = reference.getNumShips();
		}
		
	}

	public void remember(AttackPlan ap) {
		waitingPlans.add(ap);
	}
	
	public void schedule(AttackPlan ap) {
				
		scheduledPlan = ap;
		
		for (PlanVertex pv : ap.getSources()) {
			int numShips = ap.allocateShips(pv);
			Integer currentlyAllocatedShips = pv.allocatedShips.get(ap.getTarget());
			if (currentlyAllocatedShips == null) {
				pv.allocatedShips.put(ap.getTarget(), numShips);
			} else if (numShips != 0) {
				pv.allocatedShips.put(ap.getTarget(), currentlyAllocatedShips.intValue() + numShips);
			}
			pv.availableShips -= numShips;
		}
		
	}
	
	public String getAllocatedShipsToShortString() {
		String s = "{ ";
		for (Map.Entry<PlanVertex, Integer> entry : allocatedShips.entrySet()) {
			s += entry.getValue().intValue() + " => " + entry.getKey().toShortString() + ", ";
		}
		s += "}";
		return s;
	}
	
	public String getWaitingPlansToShortString() {
		String s = "[ ";
		for (AttackPlan ap : waitingPlans) {
			s += ap.toShortString() + ", ";
		}
		s += "]";
		return s;
	}
	
	public String toShortString() {
		return "Node @" + reference.getPlanetID() + " " + availableShips + "$";
	}
	
	public String toString() {
		String s = "";
		if (scheduledPlan != null) {
			s = "s " + scheduledPlan.toShortString();
		}
		return "Node @" + reference.getPlanetID() + " " + availableShips + "$\n"
				+ "$ " + getAllocatedShipsToShortString() + "\n"
				+ "-> " + reference.toShortString() + "\n"
				+ "w " + getWaitingPlansToShortString() + "\n"
				+ s;
	}
	
}
