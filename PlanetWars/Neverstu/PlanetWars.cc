#include "PlanetWars.h"
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>


void StringUtil::Tokenize(const std::string& s,
                          const std::string& delimiters,
                          std::vector<std::string>& tokens) 
{
	std::string::size_type lastPos = s.find_first_not_of(delimiters, 0);
	std::string::size_type pos = s.find_first_of(delimiters, lastPos);
	while (std::string::npos != pos || std::string::npos != lastPos) 
	{
		tokens.push_back(s.substr(lastPos, pos - lastPos));
		lastPos = s.find_first_not_of(delimiters, pos);
		pos = s.find_first_of(delimiters, lastPos);
	}
}

std::vector<std::string> StringUtil::Tokenize(const std::string& s,
                                              const std::string& delimiters) 
{
	std::vector<std::string> tokens;
	Tokenize(s, delimiters, tokens);
	return tokens;
}

Fleet::Fleet(int owner,
             int num_ships,
             int source_planet,
             int destination_planet,
             int total_trip_length,
             int turns_remaining) 
{
	owner_ = owner;
	num_ships_ = num_ships;
	source_planet_ = source_planet;
	destination_planet_ = destination_planet;
	total_trip_length_ = total_trip_length;
	turns_remaining_ = turns_remaining;
}

Planet::Planet(int planet_id,
               int owner,
               int num_ships,
               int growth_rate,
               double x,
               double y) 
{
	planet_id_ = planet_id;
	owner_ = owner;
	num_ships_ = num_ships;
	growth_rate_ = growth_rate;
	origin_ = Vec2( x, y );
}


PlanetWars::PlanetWars(const std::string& gameState,int turn) 
{
	ParseGameState(gameState,turn);
}

int PlanetWars::NumPlanets() const 
{
	return planets_.size();
}

const Planet& PlanetWars::GetPlanet(int planet_id) const 
{
	MsgAssert( planet_id >= 0 && planet_id < planets_.size(), "Invalid planet index: %d (%d)", planet_id, (int)planets_.size() );
	return planets_[planet_id];
}

int PlanetWars::NumFleets() const 
{
	return fleets_.size();
}

const Fleet& PlanetWars::GetFleet(int fleet_id) const 
{
	MsgAssert( fleet_id >= 0 && fleet_id < fleets_.size(), "Invalid fleet index: %d (%d)", fleet_id, (int)fleets_.size() );
	return fleets_[fleet_id];
}

std::string PlanetWars::ToString() const 
{
	std::stringstream s;
	
	s << "T " << Turn() << std::endl;
	
	for (unsigned int i = 0; i < planets_.size(); ++i) 
	{
		const Planet& p = planets_[i];
		s << "P " << p.Origin()[0] << " " << p.Origin()[1] << " " << p.Owner() << " " << p.NumShips() << " " << p.GrowthRate() << std::endl;
	}
	
	for (unsigned int i = 0; i < fleets_.size(); ++i) 
	{
		const Fleet& f = fleets_[i];
		s << "F " << f.Owner() << " " << f.NumShips() << " " << f.SourcePlanet() << " " << f.DestinationPlanet() << " " << f.TotalTripLength() << " " << f.TurnsRemaining() << std::endl;
	}
	
	return s.str();
}

int PlanetWars::Distance(int source_planet, int destination_planet) const 
{
	const Planet& source = planets_[source_planet];
	const Planet& destination = planets_[destination_planet];
	return DistanceRoundedUp( source.Origin(), destination.Origin() );
}

bool PlanetWars::GenerateOrder(	int player_id, 
								TOrderList& orders, 
								int source_planet,
								int destination_planet,
								int num_ships)
{
	if( num_ships <= 0 )
	{
		DbgMessage( "Rejecting order (%d, %d, %d) due to bad size", source_planet, destination_planet, num_ships );
		return false;
	}
	
	if( source_planet == destination_planet )
	{
		DbgMessage( "Rejecting order (%d, %d, %d) due to planet match", source_planet, destination_planet, num_ships );
		return false;
	}
	
	if( GetPlanet( source_planet ).Owner() != player_id )
	{
		DbgMessage( "Rejecting order (%d, %d, %d) due to invalid owner %d", source_planet, destination_planet, num_ships, GetPlanet( source_planet ).Owner() );
		return false;
	}
	
	if( GetPlanet( source_planet ).NumShips() < num_ships )
	{
		DbgMessage( "Rejecting order (%d, %d, %d) due to ship count %d", source_planet, destination_planet, num_ships, GetPlanet( source_planet ).NumShips() );
		return false;
	}
	
	DbgMessage( "Accepting order (%d, %d, %d)", source_planet, destination_planet, num_ships );
	
	DUMPI( planets_[source_planet].NumShips() );
	planets_[source_planet].RemoveShips( num_ships );
	DUMPI( planets_[source_planet].NumShips() );
	
	Order o = { source_planet, destination_planet, num_ships };
	orders.push_back( o );
	
	return true;
}

bool PlanetWars::IsAlive(int player_id) const 
{
	for (unsigned int i = 0; i < planets_.size(); ++i) 
	{
		if (planets_[i].Owner() == player_id) 
		{
			return true;
		}
	}
	for (unsigned int i = 0; i < fleets_.size(); ++i) 
	{
		if (fleets_[i].Owner() == player_id) 
		{
			return true;
		}
	}
	return false;
}

int PlanetWars::GrowthRate(int player_id) const
{
	int rate = 0;
	for (unsigned int i = 0; i < planets_.size(); ++i) 
	{
		if (planets_[i].Owner() == player_id) 
		{
			rate += planets_[i].GrowthRate();
		}
	}
	return rate;
}

int PlanetWars::NumShips(int player_id) const 
{
	int num_ships = 0;
	for (unsigned int i = 0; i < planets_.size(); ++i) 
	{
		if (planets_[i].Owner() == player_id) 
		{
			num_ships += planets_[i].NumShips();
		}
	}
	for (unsigned int i = 0; i < fleets_.size(); ++i) 
	{
		if (fleets_[i].Owner() == player_id) 
		{
			num_ships += fleets_[i].NumShips();
		}
	}
	return num_ships;
}

#define NUM_FORCES 3

int second_highest( const int forces[NUM_FORCES], int max )
{
	int second = 0;
	
	for( int x=0; x<NUM_FORCES; ++x )
	{
		if( forces[x] != max )
		{
			second = Max( second, forces[x] );
		}
	}
	
	return second;
}

int index_of( const int forces[NUM_FORCES], int f )
{
	for( int x=0; x<NUM_FORCES; ++x )
	{
		if( forces[x] == f )
		{
			return x;
		}
	}
	
	return 0;
}

int count_of( const int forces[NUM_FORCES], int f )
{
	int c = 0;
	
	for( int x=0; x<NUM_FORCES; ++x )
	{
		if( forces[x] == f )
		{
			++c;
		}
	}
	
	return c;
}

bool resolve_battle( const int forces[NUM_FORCES], int& new_owner, int& new_count )
{
/*  
	http://ai-contest.com/specification.php
	
	the largest force wins, and the second largest force is subtracted from the first, and in the case of a tie 
	the original owner keeps the planet with zero ships remaining. A critical detail is that if forces completely 
	cancel out then the original owner retains the planet.
*/
	const int max = Max( forces[0], forces[1], forces[2] );
	
	if( count_of( forces, max ) > 1 )
	{
		// tie!
		new_count = 0;
		return false;
	}
	else 
	{
		new_owner = index_of( forces, max );
		new_count = max - second_highest( forces, max );
		return true;
	}
}

void PlanetWars::AdvanceSimulation( const TOrderList& orders_p1, const TOrderList& orders_p2 )
{
	++turn_;
	
	// departure
	ApplyOrders( orders_p1, 1 );
	ApplyOrders( orders_p2, 2 );
	
	// advancement
	for ( int i=0; i<fleets_.size(); ++i )
	{
		fleets_[i].Advance();
	}
	
	for ( int i=0; i<planets_.size(); ++i  ) 
	{
		Planet& p = planets_[i];
		if( p.Owner() != 0 )
		{
			p.AddShips( p.GrowthRate() );
		}
	}
	
	// arrival
	TFleetList fleets_to_resolve;
	
	for ( TFleetList::iterator i = fleets_.begin(); i!=fleets_.end();  ) 
	{
		if( (*i).TurnsRemaining() == 0 )
		{
			fleets_to_resolve.push_back( *i );
			i = fleets_.erase( i );
		}
		else 
		{
			++i;
		}
	}
	
	for ( int i=0; i<planets_.size(); ++i  ) 
	{
		Planet& p = planets_[i];
		TFleetList fleets_at_this_planet;
		
		for ( TFleetList::iterator j = fleets_to_resolve.begin(); j!=fleets_to_resolve.end();  ) 
		{
			if( (*j).DestinationPlanet() == p.PlanetID() )
			{
				fleets_at_this_planet.push_back( *j );
				j = fleets_to_resolve.erase( j );
			}
			else 
			{
				++j;
			}
		}
		
		if( !fleets_at_this_planet.empty() )
		{
			// weight of force for neutral, p1, p2
			int forces[NUM_FORCES] = { 0, 0, 0 };
			
			forces[ p.Owner() ] += p.NumShips();
			
			for ( TFleetList::iterator j = fleets_at_this_planet.begin(); j!=fleets_at_this_planet.end(); ++j ) 
			{
				forces[ (*j).Owner() ] += (*j).NumShips();
			}
			
			int new_owner = p.Owner();
			int new_count = p.NumShips();
			
			if( resolve_battle( forces, new_owner, new_count ) )
			{
				p.Owner( new_owner );
			}
			
			p.NumShips( new_count );
		}
		
		if( fleets_to_resolve.empty() )
		{
			break;
		}
	}
}


void PlanetWars::ApplyOrders( const TOrderList& orders, int player_id )
{
	for( TOrderList::const_iterator i=orders.begin(); i!=orders.end(); ++i )
	{
		const Order& o = *i;
		
		planets_[ o.source_planet_ ].RemoveShips( o.num_ships_ );
		
		int d = Distance( o.source_planet_, o.destination_planet_ );
		
		Fleet f(
				player_id,
				o.num_ships_,
				o.source_planet_,
				o.destination_planet_,
				d,
				d
				);
		
		fleets_.push_back( f );
	}
}

int PlanetWars::ParseGameState(const std::string& s, int turn) 
{
	turn_ = turn;
	planets_.clear();
	fleets_.clear();
	std::vector<std::string> lines = StringUtil::Tokenize(s, "\n");
	int planet_id = 0;
	
	for (unsigned int i = 0; i < lines.size(); ++i) 
	{
		std::string& line = lines[i];
		size_t comment_begin = line.find_first_of('#');
		if (comment_begin != std::string::npos) 
		{
			line = line.substr(0, comment_begin);
		}
		std::vector<std::string> tokens = StringUtil::Tokenize(line);
		if (tokens.size() == 0)
		{
			continue;
		}
		if (tokens[0] == "P") 
		{
			if (tokens.size() != 6) 
			{
				return 0;
			}
			Planet p(planet_id++,              // The ID of this planet
					 atoi(tokens[3].c_str()),  // Owner
					 atoi(tokens[4].c_str()),  // Num ships
					 atoi(tokens[5].c_str()),  // Growth rate
					 atof(tokens[1].c_str()),  // X
					 atof(tokens[2].c_str())); // Y
			planets_.push_back(p);
		} 
		else if (tokens[0] == "F") 
		{
			if (tokens.size() != 7) 
			{
				return 0;
			}
			Fleet f(atoi(tokens[1].c_str()),  // Owner
					atoi(tokens[2].c_str()),  // Num ships
					atoi(tokens[3].c_str()),  // Source
					atoi(tokens[4].c_str()),  // Destination
					atoi(tokens[5].c_str()),  // Total trip length
					atoi(tokens[6].c_str())); // Turns remaining
			fleets_.push_back(f);
		}
		else if (tokens[0] == "T")
		{
			if( tokens.size() != 2)
			{
				return 0;
			}
			turn_ = atoi(tokens[1].c_str());
		}
		else 
		{
			return 0;
		}
	}
	return 1;
}
