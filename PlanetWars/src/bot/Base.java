package bot;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Base implements Comparable<Base> {
	
    private int planetID;
    private double x, y;
    private int owner;
    private int numShips;
    private int growthRate;
    
    private ArrayList<Squadron> arrivingSquadrons;
        
    public Base(int planetID, double x, double y,
    			int owner, int numShips, int growthRate) {
    	
		this.planetID = planetID;
		this.x = x;
		this.y = y;
		this.owner = owner;
		this.numShips = numShips;
		this.growthRate = growthRate;
		
		arrivingSquadrons = new ArrayList<Squadron>();
		
    }
    
    protected Base(Base b) {
    	this(b.planetID, b.x, b.y, b.owner, b.numShips, b.growthRate);
    	arrivingSquadrons.addAll(b.arrivingSquadrons);
    }
    
    // Accessors and simple modification functions. These should be mostly
    // self-explanatory.
    public int getPlanetID() {
    	return planetID;
    }

    public double getX() {
    	return x;
    }

    public double getY() {
    	return y;
    }

    public int getOwner() {
    	return owner;
    }

    public int getNumShips() {
    	return numShips;
    }

    public int getGrowthRate() {
    	return growthRate;
    }

    public void setOwner(int newOwner) {
    	this.owner = newOwner;
    }
    
    public void setNumShips(int newNumShips) {
    	this.numShips = newNumShips;
    }

    public void addShips(int amount) {
    	numShips += amount;
    }

    public void removeShips(int amount) {
    	numShips -= amount;
    }
        
    public void addArrivingSquadron(Squadron s) {
    	arrivingSquadrons.add(s);
    }
    
    /** Sort arriving fleets by arrival turn.
      * First in list = first arriving.
      */
    public void sortArrivingSquadrons() {
    	Collections.sort(arrivingSquadrons);
    }
    
    public List<Squadron> getArrivingSquadrons() {
    	return arrivingSquadrons;
    }
    
    /** Returns the distance between two planets, rounded up to the next highest
     * integer. This is the number of discrete time steps it takes to get
     * between the two planets.
     */
    public int distanceTo(Base dest) {
    	if (dest == this) { return 0; }
    	double dx = this.x - dest.x;
    	double dy = this.y - dest.y;
    	return (int) Math.ceil(Math.sqrt(dx * dx + dy * dy));
    }
    
    /** Euclidean distance to several planets */
    public double distanceTo(List<Base> bases) {
    	double dist = 0L;
    	for (Base b : bases) {
    		double d = (double) this.distanceTo(b);
    		dist += d * d;
    	}
    	return Math.sqrt(dist);
    }
    
    public String getArrivingSquadronsToShortString() {
    	String s = "[ ";
		for (Squadron f : arrivingSquadrons) {
			s += f.toShortString() + ", ";
		}
		s += "]";
		return s;
    }
    
    public String toShortString() {
    	String ownerStr = null;
    	switch (owner) {
		case GameState.SELF:
			ownerStr = "SELF";
			break;
		case GameState.NEUTRAL:
			ownerStr = "NEUTRAL";
			break;
		default:
			ownerStr = "OPPONENT";
			break;
		}
    	return "Planet @" + planetID + " " + numShips + " ~ " + ownerStr
    			+ " ^" + growthRate + " (" + x + "," + y + ")";
    }
    
    public String toString() {
    	String ownerStr = null;
    	switch (owner) {
		case GameState.SELF:
			ownerStr = "SELF";
			break;
		case GameState.NEUTRAL:
			ownerStr = "NEUTRAL";
			break;
		default:
			ownerStr = "OPPONENT";
			break;
		}
    	return "Planet @" + planetID + " " + numShips + " ~ " + ownerStr
    			+ " ^" + growthRate + " (" + x + "," + y + ")\n"
    			+ getArrivingSquadronsToShortString();
    }
    
    //
    // From here, AI helpful methods & 
    // 
    
    private int shipCost;
    private int shipValue;
    
	public int getShipCost() {
		return shipCost;
	}
	
	public int getShipValue() {
		return shipValue;
	}
	
    public double getWeightedValue() {
    	if (shipCost == 0) {
    		return -1000000; // A high negative value => MIN
    	} else {
    		return ((double) shipValue) / ((double) shipCost);
    	}
	}
	
	public int compareTo(Base o) {
		return Double.compare(o.getWeightedValue(), this.getWeightedValue());
	}
	
	/** Simple method for Knapsack algorithm of attack. */
    public void receive(Base master, int horizon) {
    	
    	int d = this.distanceTo(master);
    	
    	if (owner == GameState.NEUTRAL) {
    		shipCost = numShips + 1;
    		shipValue = growthRate * (horizon - d) - shipCost;
    	} else if (owner >= GameState.OPPONENT) {
    		shipCost = numShips + growthRate * d + 1;
    		shipValue = 2 * growthRate * (horizon - d);
    	}
    	
    }
    
    public void defend(int horizon) {
    	
    	int ct = 0; // Current turn number (relative)
    	int cas = 0; // Current arriving ships until the turn (enemy minus self)
    	
    	int start = 0; // Moment where it's beginning to be useful to keep some ships
    	int end = 0; // Moment where it's no longer possible to defend my planet
    	
    	shipCost = 0; // Number of ships needed
    	
    	for (Squadron s : arrivingSquadrons) {
    		
    		if (s.getRemainingTurns() != ct) {
    			int k = cas - growthRate * ct;
    			if (k > 0 && k <= numShips) {
    				shipCost = Math.max(shipCost, k);
    				if (start == 0) { start = ct; }
    			} else if (k > 0 && k > numShips) {
    				if (end == 0) { end = ct; }
    			}
    			ct = s.getRemainingTurns();
    		}
    		
			if (s.getOwner() == GameState.SELF) {
				cas -= s.getNumShips();
			} else {
				cas += s.getNumShips();
			}
    		
    	}
    	
		int k = cas - growthRate * ct;
		if (k > 0 && k <= numShips) {
			shipCost = Math.max(shipCost, k);
			if (start == 0) { start = ct; }
		} else if (k > 0 && k > numShips) {
			if (end == 0) { end = ct; }
		}
    	
    	if (start != 0 && (end == 0 || start < end)) {
    		if (end == 0) { end = horizon; }
    		shipValue = 2 * growthRate * (end - start);
    	}
    	
    }
    
    /** More complex method for Knapsack algorithm of attack & defend. */
	public void receive2(Base visitor, int horizon) {
		
		// If visitor is the planet itself, it means, compute how much ships
		// to defend the planet using ships from the planet itself
		if (visitor == this) { defend(horizon); return; }
		
		int d = this.distanceTo(visitor); // Time of arrival of my fleet (if sent now)
		
		int currShipNum = numShips; // Current number of ships
		int baseOwner = owner; // Base owner for current number of ships
		
		int numShipsBeforeArrival = numShips; // Number of ships on planet before arrival of fleet (at turn d)
		int shipsNeeded = 0; // Number of ships needed to take back the planet from Opponent
		
		int ftt = 0; // First time taken turn
		int fto = GameState.NEUTRAL; // First time owner
		
		int stt = 0; // Second time taken turn
		int sto = GameState.NEUTRAL; // Second time owner
		
		if (owner >= GameState.OPPONENT) {
			shipsNeeded = numShips + 1; 
		}
		
		for (Squadron s : arrivingSquadrons) {
			
			// Don't take into account fleets arriving after the date
			// of maximum vision in the future.
			if (s.getRemainingTurns() > horizon) continue;
			
			// If the fleet's owner is the same as the planet's owner
			// this is reinforcement, otherwise it's an attack.
			if (s.getOwner() == baseOwner) {
				currShipNum += s.getNumShips();
			} else {
				currShipNum -= s.getNumShips();
			}
			
			// Adjust number of ships before arrival of my fleet (at turn d).
			// Useful if planet is neutral.
			if (s.getRemainingTurns() < d) {
				numShipsBeforeArrival = currShipNum;
			}
			
			// Compute the number of ships needed to take back the planet
			// from the opponent. [WARNING: insufficient if planet is neutral.]
			if (baseOwner < GameState.OPPONENT && s.getOwner() >= GameState.OPPONENT
					&& currShipNum < 0) {
				shipsNeeded = Math.max(shipsNeeded, -currShipNum + 1);
			} else if (baseOwner >= GameState.OPPONENT && currShipNum >= 0) {
				shipsNeeded = Math.max(shipsNeeded, currShipNum + 1);
			}
			
			// If the current number of ships falls bellow zero,
			// the owner has changed. Register First and Second
			// owner change.
			if (currShipNum < 0) {
				if (fto == GameState.NEUTRAL) {
					baseOwner = s.getOwner();  // Change owner
					currShipNum = -currShipNum;
					ftt = s.getRemainingTurns(); // Register Owner Change turn
					fto = s.getOwner();
				} else if (sto == GameState.NEUTRAL) {
					baseOwner = s.getOwner();  // Change owner
					currShipNum = -currShipNum;
					stt = s.getRemainingTurns(); // Register Owner Change turn
					sto = s.getOwner();
				}
			}
		}
		
		shipCost = 0;
		shipValue = 0;
		
		if (owner == GameState.SELF) {
			
			if (fto != GameState.NEUTRAL &&
				 ((sto != GameState.SELF || currShipNum < 0) && d < horizon)
				   || (sto == GameState.SELF && currShipNum >= 0 && d < stt)) {
				// My planet was taken and I can take it back before NTF or STT
				shipCost = shipsNeeded - growthRate * ftt;
				
				if (sto != GameState.SELF || currShipNum < 0) {
					// I didn't take it back, compute until NTF
					stt = horizon;
				}
				if (d > ftt) {
					// I arrive after time taken, compute until D.
					shipCost += growthRate * (d - ftt);
					ftt = d;
				}
				
				shipValue = 2 * growthRate * (stt - ftt);
			}
		
		} else if (owner == GameState.NEUTRAL) {
			
			if (fto == GameState.NEUTRAL) {
				// Owner of the planet is still Neutral
				shipCost = numShipsBeforeArrival + 1;
				shipValue = growthRate * (horizon - d) - shipCost;
			} else if (fto == GameState.SELF) {
				// I was the first to take the planet
				if (d <= ftt) {
					shipCost = numShipsBeforeArrival + 1;
					shipValue = growthRate * (ftt - d) - shipCost;
				}
				if (sto >= GameState.OPPONENT && currShipNum > 0) {
					// Opponent has re-taken the planet after me and kept it. 
					if (d <= stt) {
						shipCost = Math.max(shipCost, shipsNeeded);
						shipValue += 2 * growthRate * (horizon - stt);
					} else {
						shipCost = Math.max(shipCost, shipsNeeded + growthRate * (d - stt));
						shipValue += 2 * growthRate * (horizon - d);
					}
				}
			} else {
				// Opponent was the first to take the planet
				if (d <= ftt) {
					// I come before Opponent take the planet (cost me a lot of ships)
					shipCost = 2 * numShipsBeforeArrival + shipsNeeded;
					if (sto == GameState.SELF && currShipNum > 0) {
						// I took it back and kept it.
						shipValue = growthRate * (ftt - d) - numShipsBeforeArrival + 2 * growthRate * (stt - ftt);
					} else {
						// I did not take it bake or did not keep it.
						shipValue = growthRate * (ftt - d) - numShipsBeforeArrival + 2 * growthRate * (horizon - ftt);
					}
				} else {
					// I come after Opponent has taken the planet, good for me!
					shipCost = shipsNeeded + growthRate * (d - ftt);					
					// If I did not take it back compute until NTF otherwise until STT 
					if (sto != GameState.SELF || currShipNum < 0)  { stt = horizon; }
					shipValue = 2 * growthRate * (stt - d);
				}
			}
			
		} else { // Owner >= GameState.OPPONENT
		
			if (fto == GameState.NEUTRAL) {
				shipCost = shipsNeeded + growthRate * d;
				shipValue = 2 * growthRate * (horizon - d);
			} else {
				if (d < ftt) {
					shipCost = shipsNeeded + growthRate * d;
					shipValue = 2 * growthRate * (ftt - d);
				}
				if (sto >= GameState.OPPONENT && currShipNum >= 0) {
					if (d >= stt) {
						shipCost = Math.max(shipCost, shipsNeeded + growthRate * (d - stt));
						shipValue += 2 * growthRate * (horizon - d);
					} else {
						shipCost = Math.max(shipCost, shipsNeeded);
						shipValue += 2 * growthRate * (horizon - stt);
					}
				}
			}
			
		}
	
	}

}
