package bot;

import java.util.List;
import java.util.Vector;

public class BubbleBot implements Bot {

	public int getVersion() {
		return 0;
	}

	public void playTurn(int turnNum) {
		initNewTargets();
		for (Base myBase : GameState.getMyBases()){
			Base bestTarget = getBestTarget(myBase);
			if (bestTarget != null){
				// on marque la planete comme etant ciblee ce tour
				markAsTargeted(bestTarget);
				GameState.issueOrder(myBase, bestTarget, getShipsAtContact(myBase, bestTarget)+1);
			}
		}
	}
	
	private static List<Base> targetedBases;
	
	private static void initNewTargets(){
		targetedBases = new Vector<Base>(); 
	}
	
	private static void markAsTargeted(Base target){
		targetedBases.add(target);
	}
	
	private static boolean isNewlyTargeted(Base target){
		for (Base alreadyTargeted: targetedBases){
			if (alreadyTargeted.getPlanetID() == target.getPlanetID()){
				return true;
			}
		}
		return false;
	}
	
	public static void main(String[] args) {
		BubbleBot b = new BubbleBot();
		GameState.playGame(b);
	}
	
	


	public static Base getBestTarget(Base sourceBase){
		Base result = null;
		float tempValue = 0;
		// toutes les bases (neutres et ennemies) sont des cibles potentielles
		for (Base potentialTarget: GameState.getOtherBases()){
			// on ne vise que des planetes pas deja ciblees par nos flottes
			if (!isAlreadyTargeted(potentialTarget) && !isNewlyTargeted(potentialTarget)){
				// on calcule la masse de vaisseau a l'arrivee
				int shipsAtContact = getShipsAtContact(sourceBase,potentialTarget);
				if (shipsAtContact < sourceBase.getNumShips()){
					// on n'attaque que les cibles vainquables
					float value = getBaseValue(sourceBase, potentialTarget);
					if (value > tempValue){
						result = potentialTarget;
						tempValue = value;
					}
				}
			}
		}
		return result;
	}
	
	/**
	 * Indique le nombre de vaisseau presents pour une flotte lancee au tour actuel<br />
	 * TODO: prendre en compte les flottes actuellement en mouvement
	 * @param source
	 * @param target
	 * @return
	 */
	public static int getShipsAtContact(Base source, Base target){
		if (target.getOwner() == GameState.NEUTRAL){
			// pas de croissance dans une planete neutre
			return target.getNumShips();
		}else{
			// croissance dans une planete ennemie
			return target.getNumShips()+source.distanceTo(target)*target.getGrowthRate();
		}
	}
	
	private static int distanceCoeff = 1;
	private static int regenCoeff = 1;
	private static int shipsCoeff = 1;
	
	public static float getBaseValue(Base source, Base target){
		float distance = (float) source.distanceTo(target);
		float shipsCost = (float) getShipsAtContact(source, target);
		float regen = (float) target.getGrowthRate();
		
		return regen*regenCoeff/(distance*distanceCoeff*shipsCost*shipsCoeff);
		
	}
	
	
	public static boolean isAlreadyTargeted(Base base){
		boolean result = false;
		for (Squadron squadron: GameState.getMySquadrons()){
			if (squadron.getDestinationBase().getPlanetID() == base.getPlanetID()){
				result = true;
			}
		}
		return result;
	}
}
