package bot;

import java.util.ArrayList;

public class GameState {
	
	public final static int NEUTRAL = 0;
	public final static int SELF = 1;
	public final static int OPPONENT = 2; // Opponents have PlayerID >= 2
	
	private static int botVersion;
	
    // Store all the planets and fleets.
    private static ArrayList<Base> bases = new ArrayList<Base>();
    private static ArrayList<Squadron> squadrons = new ArrayList<Squadron>();
    
    // Several views of planets by owner
    private static ArrayList<Base> myBases;
    private static ArrayList<Base> otherBases;
    private static ArrayList<Base> enemyBases;
    private static ArrayList<Base> neutralBases;
    
    // Several views of fleets by owner
    private static ArrayList<Squadron> mySquadrons;
    private static ArrayList<Squadron> enemySquadrons;
    
    private static int[] availableShips = new int[5]; 
    private static int[] numShips = new int[5];
    
    // Private constructor: all methods are static.
    private GameState() { }
    
    /** Return Bot version: useful for abstract class applicable to several versions. */
    public static int getBotVersion() {
    	return botVersion;
    }
    
    /** Return the distance between two planets, rounded up to the next highest
      * integer. This is the number of discrete time steps it takes to get
      * between the two planets.
      */
   public static int distance(Base source, Base dest) {
   	return source.distanceTo(dest);
   }

    /** Return the number of planets. Planets are numbered starting with 0. */
    public static int getNumPlanets() {
    	return bases.size();
    }

    /** Return the planet with the given planet_id. There are NumPlanets()
      * planets. They are numbered starting at 0.
      */
    public static Base getBase(int planetID) {
    	return bases.get(planetID);
    }

    /** Return the number of fleets.*/
    public static int getNumFleets() {
    	return squadrons.size();
    }

    /** Return the fleet with the given fleet_id. Fleets are numbered starting
      * with 0. There are NumFleets() fleets. WARNING: fleet_id's are not consistent
      * from one turn to the next.
      */
    public static Squadron getSquadron(int fleetID) {
    	return squadrons.get(fleetID);
    }

    /** Return a list of all the planets. */
    public static ArrayList<Base> getBases() {
    	return bases;
    }

    /** Return a list of all the planets owned by the current player. */
    public static ArrayList<Base> getMyBases() {
    	partBases();
    	return myBases;
    }

    /** Return a list of all neutral planets. */
    public static ArrayList<Base> getNeutralBases() {
    	partBases();
    	return neutralBases;
    }

    /** Return a list of all the planets owned by rival players. This excludes
      * planets owned by the current player, as well as neutral planets.
      */
    public static ArrayList<Base> getEnemyBases() {
    	partBases();
    	return enemyBases;
    }

    /** Return a list of all the planets that are not owned by the current
	  * player. This includes all enemy planets and neutral planets.
	  */
    public static ArrayList<Base> getOtherBases() {
    	partBases();    	
    	return otherBases;
    }
    
    private static void partBases() {
    	if (myBases == null) {
    		myBases = new ArrayList<Base>();
    		otherBases = new ArrayList<Base>();
    		enemyBases = new ArrayList<Base>();
    		neutralBases = new ArrayList<Base>();
    		for (Base b : bases) {
    			if (b.getOwner() == GameState.NEUTRAL) {
    				otherBases.add(b);
    				neutralBases.add(b);
    			} else if (b.getOwner() == GameState.SELF) {
    				myBases.add(b);
    			} else {
    				otherBases.add(b);
    				enemyBases.add(b);
    			}
    		}
    	}
    }

    /** Return a list of all the fleets. */
    public static ArrayList<Squadron> getSquadrons() {
    	return squadrons;
    }

    /** Return a list of all the fleets owned by the current player. */
    public static ArrayList<Squadron> getMySquadrons() {
    	partSquadrons();
    	return mySquadrons;
    }

    /** Return a list of all the fleets owned by enemy players. */
    public static ArrayList<Squadron> getEnemySquadrons() {
    	partSquadrons();
    	return enemySquadrons;
    }
    
    private static void partSquadrons() {
    	if (mySquadrons == null) {
    		mySquadrons = new ArrayList<Squadron>();
    		enemySquadrons = new ArrayList<Squadron>();
    		for (Squadron f : squadrons) {
    			if (f.getOwner() == GameState.SELF) {
    				mySquadrons.add(f);
    			} else {
    				enemySquadrons.add(f);
    			}
    		}
    	}
    }

    /** Sends an <i>unchecked</i> order to the game engine.
      * An order is composed of a source planet number,
      * a destination planet number, and a number of ships.
      * A few things to keep in mind:
      *   * you can issue many orders per turn if you like.
      *   * the planets are numbered starting at zero, not one.
      *   * you must own the source planet. If you break this rule, the game
      *     engine kicks your bot out of the game instantly.
      *   * you can't move more ships than are currently on the source planet.
      *   * the ships will take a few turns to reach their destination. Travel
      *     is not instant. See the distance() function for more info.
      * <heavy>No validity checks are performed.</heavy>
      */
    public static void issueOrder(int sourcePlanet, int destinationPlanet, int numShips) {
        System.out.println(""  + sourcePlanet
        		         + " " + destinationPlanet
        		         + " " + numShips);
    }

    /** Sends a <i>checked</i> order to the game engine.
      * An order is composed of a source planet number,
      * a destination planet number, and a number of ships.
      * A few things to keep in mind:
      *   * you can issue many orders per turn if you like.
      *   * the planets are numbered starting at zero, not one.
      *   * you must own the source planet. If you break this rule, the game
      *     engine kicks your bot out of the game instantly.
      *   * you can't move more ships than are currently on the source planet.
      *   * the ships will take a few turns to reach their destination. Travel
      *     is not instant. See the distance() function for more info.
      * <heavy>Order is checked against the game rules: numShips > 0; you own
      * source planet; source planet has enough ships available.</heavy>
      */
    public static void issueOrder(Base source, Base dest, int numShips) {
    	if (source.getOwner() == GameState.SELF
    			&& source.getNumShips() >= numShips
    	        && numShips > 0
    	        && source.getPlanetID() != dest.getPlanetID() ) {
	        issueOrder(source.getPlanetID(),
	        		   dest.getPlanetID(),
	        		   numShips);
    	}
    }
    
    /** Sends a <i>checked</i> order to the game engine.
      * An order is composed of a source planet number,
      * a destination planet number, and a number of ships.
      * A few things to keep in mind:
      *   * you can issue many orders per turn if you like.
      *   * the planets are numbered starting at zero, not one.
      *   * you must own the source planet. If you break this rule, the game
      *     engine kicks your bot out of the game instantly.
      *   * you can't move more ships than are currently on the source planet.
      *   * the ships will take a few turns to reach their destination. Travel
      *     is not instant. See the Distance() function for more info.
      * <heavy>Order is checked against the game rules: numShips > 0; you own
      * source planet; source planet has enough ships available.</heavy>
      */
   public static void issueOrder(Squadron f) {
       issueOrder(f.getSourceBase(),
       		      f.getDestinationBase(),
       		      f.getNumShips());
   }

    /** Sends the game engine a message to let it know that we're done sending
      * orders. This signifies the end of our turn.
      */
    private static void finishTurn() {
    	System.out.println("go");
    	System.out.flush();
    }

    /** Returns true if the named player owns at least one planet or fleet.
      * Otherwise, the player is deemed to be dead and false is returned.
      */
    public static boolean isAlive(int playerID) {
		for (Base p : bases) {
		    if (p.getOwner() == playerID) {
		    	return true;
		    }
		}
		for (Squadron f : squadrons) {
		    if (f.getOwner() == playerID) {
		    	return true;
		    }
		}
		return false;
    }

    /** Returns the number of ships that the current player has, either located
      * on planets or in flight.
      * 
	  * @param playerID player ID (0 = neutral, 1 = self, 2+ = enemy)
	  * @return number of ships the player has
      */
    public static int getNumShips(int playerID) {
		if (numShips[playerID] < 0) {
			numShips[playerID] = getAvailableShips(playerID);
			for (Squadron f : squadrons) {
			    if (f.getOwner() == playerID) {
			    	numShips[playerID] += f.getNumShips();
			    }
			}
		}
		return numShips[playerID];
    }
    
    /** Returns the number of ships available to the current player on planets.
	  * Ships in flight are not available.
	  * 
	  * @param playerID player ID (0 = neutral, 1 = self, 2+ = enemy)
	  * @return number of ships available to the player
	  */
    public static int getAvailableShips(int playerID) {
    	if (availableShips[playerID] < 0) {
    		availableShips[playerID] = 0;
    		for (Base p : bases) {
			    if (p.getOwner() == playerID) {
			    	availableShips[playerID] += p.getNumShips();
			    }
			}
    	}
    	return availableShips[playerID];
    }
    
    private static void resetGameState() {
    	mySquadrons = null;
		enemySquadrons = null;
		squadrons.clear();
		
		myBases = null;
		otherBases = null;
		enemyBases = null;
		neutralBases = null;
		bases.clear();
		
		for (int i = 0; i < numShips.length; i++) {
			availableShips[i] = -1;
			numShips[i] = -1;
		}
    }

    /** Parses a game state from a string and update game state
      * in GameState according to it.
      */
    private static void parseGameState(ArrayList<String> lines) {
    	
    	int planetID = 0;
    	    	
    	resetGameState();
    	
		for (String line : lines) {

		    int commentBegin = line.indexOf('#');
		    if (commentBegin >= 0) {
		    	line = line.substring(0, commentBegin).trim();
		    } else {
		    	line = line.trim();
		    }
		    
		    if (line.length() == 0) {
		    	continue;
		    }
		    
		    String[] tokens = line.split(" ");
		    if (tokens.length == 0) {
		    	continue;
		    }
		    
		    if (tokens[0].equals("P")) {
		    	
		    	if (tokens.length != 6) {
		    		continue;
		    	}
		    	
		    	double x = Double.parseDouble(tokens[1]);
		    	double y = Double.parseDouble(tokens[2]);
		    	int owner = Integer.parseInt(tokens[3]);
		    	int numShips = Integer.parseInt(tokens[4]);
		    	int growthRate = Integer.parseInt(tokens[5]);
		    	
		    	bases.add(new Base(planetID, x, y, owner, numShips, growthRate));

		    	planetID++;
		    	
		    } else if (tokens[0].equals("F")) {
		    	
		    	if (tokens.length != 7) {
		    		continue;
		    	}
		    	
				int owner = Integer.parseInt(tokens[1]);
				int numShips = Integer.parseInt(tokens[2]);
				int source = Integer.parseInt(tokens[3]);
				int destination = Integer.parseInt(tokens[4]);
				int totalTripLength = Integer.parseInt(tokens[5]);
				int turnsRemaining = Integer.parseInt(tokens[6]);
					
				squadrons.add(new Squadron(owner, numShips,
										   source, destination,
										   totalTripLength, turnsRemaining));
			
		    } else {
		    	continue;
		    }
		    
		}
		
		for (Base b : bases) {
			b.sortArrivingSquadrons();
		}
		
    }
    
    public static void playGame(Bot b) {
    	
    	botVersion = b.getVersion();
    	
    	int turnNum = 0;
    	String line = "";
    	ArrayList<String> message = new ArrayList<String>();
    	int c;
    	
    	try {
    	    while ((c = System.in.read()) >= 0) {
	    		switch (c) {
		    		case '\n':
		    		    if (line.equals("go")) {
		    		    	turnNum++;
		    		    	parseGameState(message);
			    			b.playTurn(turnNum);
			    		    finishTurn();
			    			message.clear();
		    		    } else {
		    		    	message.add(line);
		    		    }
		    		    line = "";
		    		    break;
		    		case '\r':
		    			break;
		    		default:
		    		    line += (char) c;
		    		    break;
	    		}
    	    }
    	} catch (Exception e) {
    	    // Owned.
    	}
    	
    }


}
