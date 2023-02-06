package bot;

public class Squadron implements Comparable<Squadron>, Cloneable {
	
    private int owner;
    private int numShips;
    private int sourcePlanetID;
    private int destinationPlanetID;
    private int totalTripLength;
    private int turnsRemaining;
		
    // Initializes a fleet.
    public Squadron(int owner, int numShips,
    		     int sourcePlanetID, int destinationPlanetID,
    		     int totalTripLength, int turnsRemaining) {
		this.owner = owner;
		this.numShips = numShips;
		this.sourcePlanetID = sourcePlanetID;
		this.destinationPlanetID = destinationPlanetID;
		this.totalTripLength = totalTripLength;
		this.turnsRemaining = turnsRemaining;
		
		GameState.getBase(destinationPlanetID).addArrivingSquadron(this);
    }
    
    // Accessors and simple modification functions. These should be mostly
    // self-explanatory.
    public int getOwner() {
    	return owner;
    }

    public int getNumShips() {
    	return numShips;
    }

    public int getSourcePlanetID() {
    	return sourcePlanetID;
    }
    
    public Base getSourceBase() {
    	return GameState.getBase(sourcePlanetID);
    }

    public int getDestinationPlanetID() {
    	return destinationPlanetID;
    }
    
    public Base getDestinationBase() {
    	return GameState.getBase(destinationPlanetID);
    }

    public int getTotalTripLength() {
    	return totalTripLength;
    }

    public int getRemainingTurns() {
    	return turnsRemaining;
    }

    /** Natural ordering of fleets is in fact dependent on the time of arrival.
      * <i>It is thus inconsistent with equals.</i>
      */
    public int compareTo(Squadron f) {
    	return this.turnsRemaining - f.turnsRemaining;
    }
    
    public String toShortString() {
    	String ownerStr = null;
    	switch (owner) {
		case GameState.SELF:
			ownerStr = "SELF";
			break;
		default:
			ownerStr = "OPPONENT";
			break;
		}
    	return "Fleet " + numShips + " ~ " + ownerStr + " "
    			+ sourcePlanetID + " -> " + destinationPlanetID
    			+ " [" + turnsRemaining + "/" + totalTripLength + "]";
    }
    
    public String toString() {
    	String ownerStr = null;
    	switch (owner) {
		case GameState.SELF:
			ownerStr = "SELF";
			break;
		default:
			ownerStr = "OPPONENT";
			break;
		}
    	return "Fleet " + numShips + " ~ " + ownerStr
    			+ sourcePlanetID + " -> " + destinationPlanetID
    			+ " [" + turnsRemaining + "/" + totalTripLength + "]\n"
    			+ "-> " + GameState.getBase(destinationPlanetID).toShortString() + "\n"
    			+ "<- " + GameState.getBase(sourcePlanetID).toShortString();
    }
    
}
