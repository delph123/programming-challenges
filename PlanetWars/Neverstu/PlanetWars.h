// This file contains helper code that does all the boring stuff for you.
// The code in this file takes care of storing lists of planets and fleets, as
// well as communicating with the game engine. You can get along just fine
// without ever looking at this file. However, you are welcome to modify it
// if you want to.
#ifndef PLANET_WARS_H_
#define PLANET_WARS_H_

#include <stdio.h>
#include <string>
#include <vector>
#include <cmath>
#include "mathutil.h"
#include "SSAssert.h"


typedef cml::vector<double, fixed<2> > Vec2;

inline double DistanceSqr( const Vec2& a, const Vec2& b )
{
	return ( a-b ).length_squared();
}

inline double Distance( const Vec2& a, const Vec2& b )
{
	return sqrt( DistanceSqr( a, b ) );
}

inline int DistanceRoundedUp( const Vec2& a, const Vec2& b )
{
	return (int)ceil( Distance( a, b ) );
}

// This is a utility class that parses strings.
class StringUtil 
{
public:
	// Tokenizes a string s into tokens. Tokens are delimited by any of the
	// characters in delimiters. Blank tokens are omitted.
	static void Tokenize(const std::string& s,
						 const std::string& delimiters,
						 std::vector<std::string>& tokens);
	
	// A more convenient way of calling the Tokenize() method.
	static std::vector<std::string> Tokenize(
											 const std::string& s,
											 const std::string& delimiters = std::string(" "));
};

struct Order
{
	int source_planet_;
	int destination_planet_;
	int num_ships_;
};

typedef std::vector< Order > TOrderList;

// This class stores details about one fleet. There is one of these classes
// for each fleet that is in flight at any given time.
class Fleet 
{
public:
	// Initializes a fleet.
	Fleet(int owner,
		  int num_ships,
		  int source_planet = -1,
		  int destination_planet = -1,
		  int total_trip_length = -1,
		  int turns_remaining = -1);
	
	// Returns the playerID of the owner of the fleet. Your player ID is always
	// 1. So if the owner is 1, you own the fleet. If the owner is 2 or some
	// other number, then this fleet belongs to your enemy.
	int Owner() const { return owner_; }
	
	// Returns the number of ships that comprise this fleet.
	int NumShips() const { return num_ships_; }
	
	// Returns the ID of the planet where this fleet originated.
	int SourcePlanet() const { return source_planet_; }
	
	// Returns the ID of the planet where this fleet is headed.
	int DestinationPlanet() const { return destination_planet_; }
	
	// Returns the total distance that is being traveled by this fleet. This
	// is the distance between the source planet and the destination planet,
	// rounded up to the nearest whole number.
	int TotalTripLength() const { return total_trip_length_; }
	
	// Returns the number of turns until this fleet reaches its destination. If
	// this value is 1, then the fleet will hit the destination planet next turn.
	int TurnsRemaining() const { return turns_remaining_; }
	
	void Advance() { --turns_remaining_; }
	
private:
	int owner_;
	int num_ships_;
	int source_planet_;
	int destination_planet_;
	int total_trip_length_;
	int turns_remaining_;
};

typedef std::vector<Fleet> TFleetList;

// Stores information about one planet. There is one instance of this class
// for each planet on the map.
class Planet 
{
public:
	// Initializes a planet.
	Planet(int planet_id,
		   int owner,
		   int num_ships,
		   int growth_rate,
		   double x,
		   double y);
	
	// Returns the ID of this planets. Planets are numbered starting at zero.
	int PlanetID() const { return planet_id_; }
	
	// Returns the ID of the player that owns this planet. Your playerID is
	// always 1. If the owner is 1, this is your planet. If the owner is 0, then
	// the planet is neutral. If the owner is 2 or some other number, then this
	// planet belongs to the enemy.
	int Owner() const { return owner_; }
	
	// The number of ships on the planet. This is the "population" of the planet.
	int NumShips() const { return num_ships_; }
	
	// Returns the growth rate of the planet. Unless the planet is neutral, the
	// population of the planet grows by this amount each turn. The higher this
	// number is, the faster this planet produces ships.
	int GrowthRate() const { return growth_rate_; }
	
	// The position of the planet in space.
	Vec2 Origin() const { return origin_; }
	
	// Use the following functions to set the properties of this planet. Note
	// that these functions only affect your program's copy of the game state.
	// You can't steal your opponent's planets just by changing the owner to 1
	// using the Owner(int) function! :-)
	void Owner(int new_owner) { owner_ = new_owner; }
	void NumShips(int new_num_ships) { num_ships_ = new_num_ships; }
	void AddShips(int amount) { num_ships_ += amount; }
	void RemoveShips(int amount) { num_ships_ -= amount; }
	
	
private:
	int planet_id_;
	int owner_;
	int num_ships_;
	int growth_rate_;
	Vec2 origin_;
};

typedef std::vector<Planet> TPlanetList;

class PlanetWars 
{
public:
	// Initializes the game state given a string containing game state data.
	PlanetWars(const std::string& game_state, int turn);
	
	// Returns the number of planets on the map. Planets are numbered starting
	// with 0.
	int NumPlanets() const;
	
	// Returns the planet with the given planet_id. There are NumPlanets()
	// planets. They are numbered starting at 0.
	const Planet& GetPlanet(int planet_id) const;
	
	// Returns the number of fleets.
	int NumFleets() const;
	
	// Returns the fleet with the given fleet_id. Fleets are numbered starting
	// with 0. There are NumFleets() fleets. fleet_id's are not consistent from
	// one turn to the next.
	const Fleet& GetFleet(int fleet_id) const;
	
	// Returns a list of all the planets.
	const TPlanetList& Planets() const { return planets_; }
	
	// Return a list of all the fleets.
	const TFleetList& Fleets() const { return fleets_; }
	
	// Writes a string which represents the current game state. This string
	// conforms to the Point-in-Time format from the project Wiki.
	std::string ToString() const;
	
	// Returns the distance between two planets, rounded up to the next highest
	// integer. This is the number of discrete time steps it takes to get between
	// the two planets.
	int Distance(int source_planet, int destination_planet) const;
	
	// Sends an order to the game engine. The order is to send num_ships ships
	// from source_planet to destination_planet. The order must be valid, or
	// else your bot will get kicked and lose the game. For example, you must own
	// source_planet, and you can't send more ships than you actually have on
	// that planet.
	bool GenerateOrder( int player_id,
						TOrderList& orders, 
						int source_planet,
						int destination_planet,
						int num_ships);
	
	// Returns true if the named player owns at least one planet or fleet.
	// Otherwise, the player is deemed to be dead and false is returned.
	bool IsAlive(int player_id) const;
	
	// Returns the number of ships that the given player has, either located
	// on planets or in flight.
	int NumShips(int player_id) const;
	int GrowthRate(int player_id) const;
	
	void AdvanceSimulation( const TOrderList& orders_p1, const TOrderList& orders_p2 );
	
	int Turn() const { return turn_; }
	
private:
	void ApplyOrders( const TOrderList& orders, int player_id );
	// Parses a game state from a string. On success, returns 1. On failure,
	// returns 0.
	int ParseGameState(const std::string& s, int turn);
	
	int turn_;
	
	// Store all the planets and fleets. OMG we wouldn't wanna lose all the
	// planets and fleets, would we!?
	TPlanetList planets_;
	TFleetList fleets_;
};


#endif
