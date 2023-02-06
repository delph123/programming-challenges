/****************************************************************************/
//	Neverstu - AI Contest 2010 - stuartscandrett.com
/****************************************************************************/

#include <iostream>
#include <queue>
#include <algorithm>
#include "PlanetWars.h"

bool verbose = false;

//*******************************************************************
//																	*
//																	*
//*******************************************************************

struct ConstGlobals
{
	int max_distance;
	int num_planets;
	int* distances;
	
	int Distance( int a, int b ) { return distances[b*num_planets + a]; }
	void Init( const PlanetWars& pw );
};

void ConstGlobals::Init( const PlanetWars& pw )
{
	DbgScope( "ConstGlobals::Init" );
		
	num_planets = pw.NumPlanets();
	
	max_distance = 0;
	distances = new int[num_planets*num_planets];
	for( int j=0; j<num_planets; j++ )
	{
		for( int i=0; i<num_planets; i++ )
		{
			int idx = j*num_planets + i;
			if( i == j )
			{
				distances[idx] = 0;
			}
			else
			{
				const int d = pw.Distance( i, j );
				distances[idx] = d;
				max_distance = Max( max_distance, d );
				
				{
					DbgScope( "D( %d, %d )", i, j );
					DbgPLine( i, j, 255, 255, 255 );
					DbgPMessage( i, 255, 255, 255, "dist: %d", Distance( i, j ) );
				}
			}
		}
	}
}

ConstGlobals g_const;

//*******************************************************************
//																	*
//																	*
//*******************************************************************

class GameState
{
private:
	mutable std::vector< const PlanetWars* > turns;

public:
	const PlanetWars& At( int turn ) const
	{
		const int idx = ( turn - Current().Turn() );
		Assert( idx >= 0 );
		while( idx >= turns.size() )
		{
			static const TOrderList null_orders;
			PlanetWars* next = new PlanetWars( *turns.back() );
			next->AdvanceSimulation( null_orders, null_orders );
			AddTurn( next );
		}
		Assert( turns[idx]->Turn() == turn );
		return *turns[idx];
	}
			
	const PlanetWars& Current() const { return *turns.front(); }
	
	GameState( const std::string map_data, int turn );
	explicit GameState( const PlanetWars& start );
	~GameState();
	
	void AddTurn( const PlanetWars* p_new ) const;
};

GameState::~GameState()
{
	for( int i=0; i<turns.size(); ++i )
	{
		delete turns[i];
	}
}

GameState::GameState( const std::string map_data, int turn )
{
	PlanetWars* current_turn = new PlanetWars( map_data, turn );
	DbgTurn( current_turn );
	turns.push_back( current_turn );
}

GameState::GameState( const PlanetWars& start )
{
	turns.push_back( new PlanetWars( start ) );
}

void GameState::AddTurn( const PlanetWars* p_new ) const
{
	MsgAssert( p_new->Turn() == turns.back()->Turn()+1, "%d - %d", Current().Turn(), p_new->Turn() );
	turns.push_back( p_new );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

template< typename T >
struct PlanetData : std::vector< T >
{
	PlanetData() : std::vector< T >( g_const.num_planets ) { }
};

struct PlanetEvent
{	
	bool valid;
	int turn;
	int old_owner;
	int new_owner;
	int num_ships_after_takeover;
};

struct EventTracker
{
	PlanetData< PlanetEvent > pevents;

	void GeneratePredictions( const GameState& g );
	const PlanetEvent& LastPredictedTakeover( int planet_num ) const { return pevents[planet_num]; }
};

void EventTracker::GeneratePredictions( const GameState& g )
{
	DbgScope( "Predictions" );
	
	for( int i=0; i<g_const.num_planets; ++i )
	{
		pevents[i].valid = false;
	}

	const PlanetWars* current = &g.Current();	
	int printed = -1;
	
	// find out where all fleets land
	// always simulate to the max travel time
	for( int t=0; t<g_const.max_distance || !current->Fleets().empty(); ++t )
	{
		const PlanetWars* next = &g.At( current->Turn()+1 );
		
		// check for takeovers
		for( int i=0; i<g_const.num_planets; ++i )
		{
			const Planet& p1 = current->GetPlanet(i);
			const Planet& p2 = next->GetPlanet(i);
			Assert( p1.PlanetID() == p2.PlanetID() && p1.PlanetID() == i );
			if( p1.Owner() != p2.Owner() )
			{
				// new event!
				PlanetEvent& event = pevents[ p1.PlanetID() ];
				event.valid = true;
				event.old_owner = p1.Owner();
				event.new_owner = p2.Owner();
				event.turn = next->Turn();
				event.num_ships_after_takeover = p2.NumShips();
				
				if( printed != next->Turn() )
				{
					printed = next->Turn();
					DbgGameState( next );
				}
				
				DbgPush( "Takeover" );
				DbgPHighlight( i, 255, 255, 255 );
				DbgPMessage( i, 255, 255, 255, "%d->%d", event.old_owner, event.new_owner );
				DbgPop();
			}
		}
		
		current = next;
	}
	
	if( printed != current->Turn() )
	{
		DbgGameState( current );
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

typedef std::vector<int> TPlanetIDList;

struct PlayerIDs
{
	int player_id;
	int enemy_id;
};

#define INVALID_PLANET (-1)
#define INVALID_DIST (9999999)

enum SupplyRole
{
	S_None		= 0,
	S_Receiving = (1<<0),
	S_Sending	= (1<<1),
};

struct PlanetKnowledge
{
	int supply_role;
	int supply_dest;
	float relevance_score;
	
	PlanetKnowledge()
	{
		supply_dest = INVALID_PLANET;
		supply_role = S_None;
		relevance_score = 1.0f;
	}
};

struct MapAnalysis
{
	MapAnalysis( const PlayerIDs& p )
	{
		player = p;
	}
	
	PlayerIDs player;
	PlanetData< PlanetKnowledge > planets;
};

struct Attacker
{
	int source;
	int actual_target;
	int num_ships;
	int scheduled_departure;
};

enum AttackType
{
	A_Defense,
	A_Offense,
	A_Growth,
};

struct ResourceRequest
{
	int destination_planet;
	int deadline;
	int num_ships;
	AttackType type;
};

struct ResourceRequestEvaluation
{
	ResourceRequest request;
	float value;
	float cost;
	
	// "less" == "worse"
	bool operator< ( const ResourceRequestEvaluation& rhs ) const
	{
		return (value/cost) < (rhs.value/rhs.cost) ;
	}
};

typedef std::vector< Attacker > AttackerList;

struct AttackPlan
{
	AttackPlan() { sources.reserve( g_const.num_planets ); }
	
	PlayerIDs player;
	int arrival;
	int target;
	ResourceRequest request;
	AttackerList sources;
};

typedef std::vector< AttackPlan > AttackPlanList;
typedef std::vector< int > ShipCountList;

struct PlanetResourceAvailability
{
	PlanetResourceAvailability() : ships_on_future_turn( g_const.max_distance+1, 0 ) { }
	ShipCountList ships_on_future_turn;
};

struct MapResourceAvailability
{
	PlanetData< PlanetResourceAvailability > planets;
};

struct TurnInfo
{
	PlayerIDs			player;
	const GameState*	gamestate;
	MapAnalysis*		map;
};

typedef std::vector< ResourceRequest > ResourceRequestList;

//*******************************************************************
//																	*
//																	*
//*******************************************************************

struct DistanceAndShipsPrioritization
{
	const int target;
	const PlanetWars& state;
	explicit DistanceAndShipsPrioritization( const PlanetWars& pw, const int t ) : target( t ), state( pw ) {}
	bool operator()( const int& a, const int& b ) 
	{
		const int dist_a = g_const.Distance( a, target );
		const int dist_b = g_const.Distance( b, target );
		
		if( dist_a == dist_b )
		{
			const int ships_a = state.GetPlanet( a ).NumShips();
			const int ships_b = state.GetPlanet( b ).NumShips();
			
			if( ships_a == ships_b )
			{
				const int growth_a = state.GetPlanet( a ).GrowthRate();
				const int growth_b = state.GetPlanet( b ).GrowthRate();
			
				return growth_a > growth_b;
			}
			else
			{
				return ships_a > ships_b;
			}
		}
		else
		{
			return dist_a < dist_b;
		}
	}
};

struct SupplyPrioritization
{
	const int source;
	const MapAnalysis& map;
	explicit SupplyPrioritization( const MapAnalysis& m, const int s ) : source( s ), map( m ) {}
	bool operator()( const int& a, const int& b ) 
	{
		const int dist_a = g_const.Distance( a, source );
		const int dist_b = g_const.Distance( b, source );
		
		const float score_a = map.planets[a].relevance_score / (float)dist_a;
		const float score_b = map.planets[b].relevance_score / (float)dist_b;
		
		return score_a > score_b;
	}
};

//*******************************************************************
//																	*
//																	*
//*******************************************************************

bool Side( const Vec2 pt, const Vec2 v1, const Vec2 v2 )
{
	const Vec2 dir = ( v2 - v1 ).normalize();
	const Vec2 perp( dir[1], -dir[0] );
	const Vec2 dir2 = ( pt - v1 ).normalize();
	return dot( dir2, perp ) <= 0.0f;
}

bool PointInRect( const Vec2 pt, const Vec2 v1, const Vec2 v2, const Vec2 v3, const Vec2 v4 )
{
	return(	Side( pt, v1, v2 )
		&&	Side( pt, v2, v3 )
		&&	Side( pt, v3, v4 )
		&&	Side( pt, v4, v1 ) );
}

bool PointInCone( const Vec2 pt, const Vec2 v1, const Vec2 v2, const Vec2 v3 )
{
	return(	Side( pt, v2, v1 )
		&&	Side( pt, v1, v3 ) );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GetNearestFriendlyAndEnemy( const GameState& g, const PlayerIDs& player, int turn, int planet, int& nearest_friendly, int& nearest_enemy )
{
	nearest_friendly = INVALID_DIST;
	nearest_enemy = INVALID_DIST;
	
	for( int j=0; j<g_const.num_planets; ++j )
	{
		if( planet==j ) { continue; }
		const Planet& other = g.At(turn).GetPlanet(j);
		if( other.Owner() == player.player_id )
		{
			const int d = g_const.Distance( planet, j );
			nearest_friendly = Min( d, nearest_friendly );
		}
		else if( other.Owner() == player.enemy_id )
		{
			const int d = g_const.Distance( planet, j );
			nearest_enemy = Min( d, nearest_enemy );
		}
	}
}

int CountFleetsWithDestinationAfterTurn( const GameState& g, int destination, int player_id, int turn )
{
	int c = 0;
	
	for( int i=0; i<g.Current().NumFleets(); ++i )
	{
		const Fleet& f = g.Current().GetFleet(i);
		if(		f.DestinationPlanet() == destination 
			&&	f.Owner() == player_id 
			&&	( f.TurnsRemaining() + g.Current().Turn() ) > turn )
		{
			c += f.NumShips();
		}
	}
	
	return c;
}

int GetPossibleShipsToTargetSingle( const GameState& g, int source, int dest, int turn, int player_id )
{
	if( source == dest ) { return 0; }
	
	int last_chance = turn - g_const.Distance( source, dest );
	int max_for_this_planet = 0;
	
	for( int t=g.Current().Turn()+1; t<=last_chance; ++t )
	{
		const Planet& p2 = g.At(t).GetPlanet(source);
		if( p2.Owner() == player_id )
		{
			max_for_this_planet = Max( max_for_this_planet, p2.NumShips() );
		}
	}
	
	return max_for_this_planet;
}

int GetPossibleShipsToTargetAll( const GameState& g, int destination_planet, int turn, int player_id )
{
	int total = 0;
	
	for( int i=0; i<g_const.num_planets; ++i )
	{
		total += GetPossibleShipsToTargetSingle( g, i, destination_planet, turn, player_id );
	}
	
	return total;
}

bool IsPlanetInPlayerTerritory( const GameState& g, const PlayerIDs& player, int turn, int planet )
{
	int nearest_friendly = INVALID_DIST;
	int nearest_enemy = INVALID_DIST;
	
	GetNearestFriendlyAndEnemy( g, player, turn, planet, nearest_friendly, nearest_enemy );
	
	DUMPI( nearest_friendly );
	DUMPI( nearest_enemy );

	if( nearest_enemy == INVALID_DIST || nearest_friendly == INVALID_DIST )
	{
		return true;
	}

	if( nearest_friendly < nearest_enemy )
	{
		DUMPS( "player territory" );
		return true;
	}
	
	DUMPS( "enemy territory" );
	return false;
}

TPlanetIDList GetPlanetsInCone( const PlanetWars& pw, int source, const Vec2& dir, float angle )
{
	DbgScope( "GetPlanetsInCone" );
	
	const Vec2 origin = pw.GetPlanet( source ).Origin();
	const Vec2 s1 = rotate_vector_2D( dir, angle );
	const Vec2 s2 = rotate_vector_2D( dir, -angle );
	
	DbgLine( origin, (origin+s1*100.0f), 255, 255, 255 );
	DbgLine( origin, (origin+s2*100.0f), 255, 255, 255 );
	
	TPlanetIDList aligned;
	
	for( int j=0; j<g_const.num_planets; ++j )
	{
		if( j == source ) { continue; }
		
		const Planet& p2 = pw.GetPlanet( j );
	
		if(	PointInCone( p2.Origin(), origin, origin+s1, origin+s2 ) )
		{
			DbgPHighlight( j, 0, 255, 0 );
			
			aligned.push_back( j );
		}
	}
	
	return aligned;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void InitMapAnalysis( const GameState& g, const PlayerIDs& player, MapAnalysis& map )
{
	DbgScope( "InitMapAnalysis" );

	std::vector< float > score( g_const.num_planets, 0.0f );

	for( int i=0; i<g_const.num_planets; ++i )
	{
		const Vec2 a = g.Current().GetPlanet(i).Origin();
		
		for( int j=0; j<i; ++j )
		{
			const Vec2 b = g.Current().GetPlanet(j).Origin();
			
			const Vec2 dir = ( b-a ).normalize();
			const float dist = ( b-a ).length();
			
			DbgScope( "P %d- %d", i, j );
			DbgPHighlight( i, 255, 255, 0 );
			DbgPHighlight( j, 0, 255, 255 );
				
			// find distance from each planet to the chord from i-j
			for( int k=0; k<g_const.num_planets; ++k )
			{
				if( k == i || k == j ) { continue; }
				
				const Vec2 c = g.Current().GetPlanet(k).Origin();
				
				const float d = dot( dir, c-a );
				const float dn = d / dist;
				
				// intersection between endpoints?
				if( dn < 0.0f || dn > 1.0f ) { continue; }
				const Vec2 p = a + dir*d;
				const float l = 1.0f / ( 1.0f + ( c-p ).length() );
				
				score[k] += l;
				
				{
					DbgScope( "P %d", k );
					
					DbgLine( a, p, 255, 255, 0 );
					DbgLine( b, p, 0, 255, 255 );
					DbgLine( c, p, 255, 255, 255 );
					DbgPHighlight( k, 255, 255, 255 );
					DbgPMessage( k, 255, 255, 255, "%f", l );
				}
			}
		}
	}
	
	float max_score = 0.0f;
	float min_score = 1e6f;
	
	for( int i=0; i<g_const.num_planets; ++i )
	{
		max_score = Max( max_score, score[i] );
		min_score = Min( min_score, score[i] );
	}

	for( int i=0; i<g_const.num_planets; ++i )
	{
		float s = LinearMap( 1.0f, 2.0f, score[i], min_score, max_score );
		DbgPMessage( i, 255, 255, 255, "%f", s );
		map.planets[i].relevance_score = s;
		//DbgPHighlight( i, heat_score[i], heat_score[i], heat_score[i] );
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GenerateResourceRequests( const TurnInfo& turn, const MapAnalysis& map, ResourceRequestList& requests )
{
	DbgScope( "GenerateResourceRequests" );
	
	EventTracker events;
	events.GeneratePredictions( *turn.gamestate );
		
	// generate requests for each planet
	for( int i=0; i<g_const.num_planets; ++i )
	{
		const Planet& p = turn.gamestate->Current().GetPlanet(i);
		const PlanetEvent& e = events.LastPredictedTakeover(i);
		if( !e.valid )
		{
			const int o = p.Owner();
			
			if( o == turn.player.player_id )
			{
				// nothing to do, sources calculated later
			}
			else
			{
				if(		turn.gamestate->Current().GetPlanet(i).GrowthRate() > 0
					||	o == turn.player.enemy_id )
				{
					// submit request to kill
					ResourceRequest r;
					r.destination_planet = i;
					r.deadline = 0;
					r.num_ships = 0;
					r.type = ( o == turn.player.enemy_id ) ? A_Offense : A_Growth;
					requests.push_back( r );
				
					DbgPMessage( i, 255, 0, 0, "Kill" );
				}
			}
		}
		else
		{
			if( e.new_owner != turn.player.player_id )
			{
				if( e.old_owner == turn.player.player_id )
				{
					// player -> enemy: reinforcements needed!
					ResourceRequest r;
					r.destination_planet = i;
					r.deadline = e.turn;
					r.num_ships = e.num_ships_after_takeover;
					r.type = A_Defense;
					requests.push_back( r );
					
					DbgPMessage( i, 0, 255, 255, "Defend (%d)", e.turn );
				}
				else 
				{
					// neutral -> enemy: snipe it!
					ResourceRequest r;
					r.destination_planet = i;
					r.deadline = e.turn + 1;
					r.num_ships = 0;
					r.type = A_Offense;
					requests.push_back( r );
					
					DbgPMessage( i, 255, 0, 0, "Snipe (%d)", r.deadline );
				}
			}
		}
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GenerateOrdersFromPlans( const PlanetWars& pw, const PlayerIDs& player, const AttackPlanList& plans, TOrderList& confirmed_orders )
{
	DbgScope( "GenerateOrdersFromPlans Turn %d", pw.Turn() );
	
	PlanetWars working_state( pw );
	
	for( AttackPlanList::const_iterator i=plans.begin(); i!=plans.end(); ++i )
	{
		const AttackPlan plan = *i;
	
		DbgScope( "Plan for target %d with %d sources", plan.target, plan.sources.size() );
		DbgPHighlight( plan.target, 255, 255, 255 );
		
		for( int i=0; i<plan.sources.size(); ++i )
		{
			const Attacker& a = plan.sources[i];
			Assert( a.source != plan.target );
			
			// Historical departures possible during predictions
			// Assert( a.scheduled_departure >= working_state.Turn() );
			
			if( working_state.Turn() == a.scheduled_departure )
			{
				if( working_state.GenerateOrder( player.player_id, confirmed_orders, a.source, a.actual_target, a.num_ships ) )
				{
					DbgPLine( a.source, a.actual_target, 255, 255, 0 );
					DbgPMessage( a.source, 255, 0, 0, "Sending: %d", a.num_ships );
				}
				else
				{
					MsgAssert( false, "Order Rejected!" );
				}
			}
			else
			{
				DbgPLine( a.source, a.actual_target, 0, 255, 0 );
				DbgPMessage( a.source, 0, 255, 0, "Send delayed" );
			}
		}
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void CalculateResourceAvailabilityForPlanet( const GameState& g, const MapAnalysis& map, const AttackPlanList& current_plans, int source, PlanetResourceAvailability& resources )
{
//	DbgScope( "CalculateResourceAvailabilityForPlanet for source %d", source );
//	DbgPHighlight( source, 255, 255, 0 )
	const int turn = g.Current().Turn();
	int running_commitment = 0;
	
	for( int t=turn; t<=turn+g_const.max_distance; ++t )
	{
		const Planet& p = g.At( t ).GetPlanet( source );
		
		const int idx = t-turn;
		Assert( idx >= 0);
		Assert( idx < resources.ships_on_future_turn.size() );
		
		if( p.Owner() != map.player.player_id )
		{
			resources.ships_on_future_turn[idx] = 0;
		}
		else
		{
			for( int i=0; i<current_plans.size(); ++i )
			{
				const AttackPlan& p = current_plans[i];
				for( int j=0; j<p.sources.size(); ++j )
				{
					const Attacker& a = p.sources[j];
					if( a.source != source ) { continue; }
				
					if( a.scheduled_departure == t )
					{
						running_commitment += a.num_ships;
						break;
					}
				}
			}
			
			resources.ships_on_future_turn[idx] = p.NumShips() - running_commitment;
			MsgAssert( resources.ships_on_future_turn[idx] >= 0, "ships at %d=%d", idx+turn, resources.ships_on_future_turn[idx] );
		}
	}

//	for( int i=0; i<resources.ships_on_future_turn.size(); ++i )
//	{
//		DbgMessage( "ships[%d]=%d (%d)", i, resources.ships_on_future_turn[i], i+g.Current().Turn() );
//	}
}

void CalculateResourceAvailability( const GameState& g, const MapAnalysis& map, const AttackPlanList& current_plans, MapResourceAvailability& resources )
{
//	DbgScope( "CalculateResourceAvailability" );
	for( int i=0; i<g_const.num_planets; ++i )
	{
		CalculateResourceAvailabilityForPlanet( g, map, current_plans, i, resources.planets[i] );
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

int GetMinimumAvailableShipsFromList( const ShipCountList& ships, int current_turn, int min_turn, int max_turn )
{
	int t = INVALID_PLANET;
			
	for( int j=min_turn; j<=max_turn; ++j )
	{
		const int idx = Clamp( j - current_turn, 0, (int)ships.size()-1 );
		
		Assert( ships[idx] >= 0 );
		
		const int val = ships[idx];
		// DUMPI( val );
		
		if( t == INVALID_PLANET ) { t = val; }
		else { t = Min( t, val ); }
	}
	
	if( t == INVALID_PLANET ) { return 0; }
	else { return t; }
}

int GetMinimumAvailableShips( const GameState& g, int source, int minturn, const MapResourceAvailability& resources )
{
	return GetMinimumAvailableShipsFromList( resources.planets[source].ships_on_future_turn, g.Current().Turn(), minturn, g.Current().Turn()+g_const.max_distance );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

bool AnyShipsHaveDepartureAtTurn( const AttackerList& sources, int turn )
{
	for( int i=0; i<sources.size(); ++i )
	{
		if( sources[i].scheduled_departure == turn )
		{
			return true;
		}
	}
	
	return false;
}

int CountPlanShips( const AttackPlan& plan )
{
	int t = 0;
	
	for( int i=0; i<plan.sources.size(); ++i )
	{
		t += plan.sources[i].num_ships;
	}
	
	return t;
}

int PlanInvestmentInTurns( const GameState& g, const AttackPlan& plan, int speculation = 0 )
{
	const Planet& pl = g.Current().GetPlanet( plan.target );
	
	int num_ships = CountPlanShips( plan ) + speculation;
	int dist = plan.arrival - g.Current().Turn();
	
//	DUMPI( num_ships );
//	DUMPI( dist );

	int ROI = dist + (int)ceil( (float)num_ships/(float)Max( pl.GrowthRate(), 1 ) );
	
//	DUMPI( ROI );
	
	return ROI;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

bool PartOfSupplyChain( const MapAnalysis& map, int source, int dest, int recurse_depth = 0 )
{
	if( recurse_depth > g_const.num_planets )
	{
		return false;
	}
	
	if( source == INVALID_PLANET || dest == INVALID_PLANET ) 
	{ 
		return false; 
	}
	
	if( source == dest ) 
	{	
		return true;
	}
	
	Assert( source >= 0 && source < g_const.num_planets );
	const PlanetKnowledge& pk = map.planets[source];
	
	return PartOfSupplyChain( map, pk.supply_dest, dest, recurse_depth+1 );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GetSpeculativeAttackersAndReinforcements( const GameState& g, const MapAnalysis& map, const MapResourceAvailability& resources, const AttackPlan& plan, const AttackerList& new_sources, int source, ShipCountList& ships )
{
//	if( g.Current().Turn() == 11 ) verbose = true;
	
//	DbgScope( "GenerateWorkingNumShips - %d", source );
	if( verbose ) DbgPHighlight( source, 255, 255, 255 );
	
	ships.clear();
	ships.resize( g_const.max_distance+1, 0 );
	
	Assert( ships.size() == resources.planets[source].ships_on_future_turn.size() );
	
	const int turn = g.Current().Turn();
	
	for( int t=turn; t<=turn+g_const.max_distance; ++t )
	{
		const int idx = t-turn;
		Assert( idx >= 0);
		Assert( idx < ships.size() );
		
		ships[idx] = resources.planets[source].ships_on_future_turn[idx];
	}
	
	ShipCountList player_planet_commitments( g_const.num_planets, 0 );
	ShipCountList enemy_planet_commitments( g_const.num_planets, 0 );
	ShipCountList planet_plan_commitment( g_const.num_planets, 0 );
		
	// now apply attackers, reinforcements
	for( int t=turn; t<=turn+g_const.max_distance; ++t )
	{
		const int idx = t-turn;
		Assert( idx >= 0);
		Assert( idx < ships.size() );
		
		DbgScopeB( verbose, "T %d", t );
		
		const Planet& source_planet = g.At( t ).GetPlanet( source );
		
		if( source_planet.Owner() != plan.player.player_id ) { continue; }
		
		for( int p=0; p<g_const.num_planets; ++p )
		{
			if( p == source ) { continue; }
			if( p == plan.target ) { continue; }
			
			DbgScopeB( verbose, "P %d", p );
			
			const Planet& planet = g.At( t ).GetPlanet( p );
			const int d = g_const.Distance( p, source );
			int send_turn = 0;
			
			// don't care anymore, too late
			if( idx+d >= ships.size() ) { continue; }
			
			// count usage in attack plan already
			for( int j=0; j<new_sources.size(); ++j )
			{
				const Attacker& a = new_sources[j];
				if( a.source != p ) { continue; }
			
				if( a.scheduled_departure == t )
				{
					planet_plan_commitment[p] += a.num_ships;
					break;
				}
			}
		
			if( planet.Owner() == plan.player.player_id )
			{
				if( map.planets[source].supply_role & S_Sending )
				{
					// suppliers should not assume reinforcements
					player_planet_commitments[p] = 0;
				}
				else
				{
					if( PartOfSupplyChain( map, p, source ) )
					{
						// if this planet is a supplier of the source, give the minimum each turn
						const int possible = Clamp( resources.planets[p].ships_on_future_turn[idx] - planet_plan_commitment[p], 0, planet.GrowthRate() );
						player_planet_commitments[p] += possible;
					}
					else if( !( map.planets[p].supply_role & S_Sending ) )
					{
						// this planet is not a supplier, it may send its minimum
						const int possible = Max(	GetMinimumAvailableShipsFromList( resources.planets[p].ships_on_future_turn, turn, turn, turn+g_const.max_distance )
												-	planet_plan_commitment[p], 0 );
						player_planet_commitments[p] = possible;
					}
					else
					{
						// supplier of a different chain, it will send nothing
						player_planet_commitments[p] = 0;
					}
				}
				
				// assume reactivity
				send_turn++;
				if( idx+d+send_turn >= ships.size() ) { continue; }
			}
			else if( planet.Owner() == plan.player.enemy_id )
			{
				const int possible = planet.NumShips();
				enemy_planet_commitments[p] = Max( possible, enemy_planet_commitments[p] );
			}
			else
			{
				player_planet_commitments[p] = 0;
			}
	
			Assert( idx+d+send_turn < ships.size() );
			ships[idx+d+send_turn] += player_planet_commitments[p] - enemy_planet_commitments[p];
		}
	}

	for( int i=0; i<ships.size(); ++i )
	{
		ships[i] = Max( ships[i], 0 );
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

bool GetAvailableSources( const GameState& g, const MapAnalysis& map, const MapResourceAvailability& resources, int ships_needed, AttackPlan& plan )
{
	DbgScopeB( verbose, "GetAvailableSources" );
	
	AttackerList new_sources;
	new_sources.reserve( g_const.num_planets );
	
	const int current_turn = g.Current().Turn();
	int remaining = ships_needed;
	
	if( verbose ) DbgPHighlight( plan.target, 255, 0, 0 );
	if( verbose ) DbgPMessage( plan.target, 255, 255, 255, "Need %d at Turn %d", ships_needed, plan.arrival );
	
	if( remaining <= 0 ) { return false; }
		
	ShipCountList working_ships;
	
	for( int i=0; i<plan.sources.size(); ++i )
	{
		if( remaining <= 0 ) { Assert( false ); break; }
		
		Attacker a = plan.sources[i];
		if( verbose ) DbgPHighlight( a.source, 0, 255, 0 );
		
		const int dist = g_const.Distance( a.source, plan.target );
		// if( dist > g_const.max_distance/2 ) { continue; }
		
		// try to leave right now
		a.scheduled_departure = current_turn;
		if( a.scheduled_departure+dist > plan.arrival ) { continue; }
		
		int minimum_available = GetMinimumAvailableShips( g, a.source, a.scheduled_departure, resources );
		if( minimum_available <= 0 ) 
		{
			// if it becomes available later, commit a virtual allocation. it will not be sent this turn, but it will
			// be removed from the available resource pool for this turn. on the next turn we may not decide to actually
			// use these resources.
			a.scheduled_departure = plan.arrival - dist;
			if( a.scheduled_departure < current_turn ) { continue; }
			minimum_available = GetMinimumAvailableShips( g, a.source, a.scheduled_departure, resources );
			if( minimum_available <= 0 ) { continue; }
		}
		
		const int speculative_allocation = Min( minimum_available, remaining );
		const int turn_on_which_attack_is_profitable = current_turn + PlanInvestmentInTurns( g, plan, speculative_allocation ) - 1;
		const int maxturn = plan.request.type == A_Growth ? turn_on_which_attack_is_profitable : plan.arrival;
		
		GetSpeculativeAttackersAndReinforcements( g, map, resources, plan, new_sources, a.source, working_ships );
		const int num_with_attackers = GetMinimumAvailableShipsFromList( working_ships, current_turn, current_turn, maxturn );  
		
		a.num_ships = Min( minimum_available, num_with_attackers );
		
		if( a.num_ships > 0 )
		{
			if( verbose ) DbgPMessage( a.source, 255, 255, 255, "num_ships: %d", a.num_ships );
		
			if( a.num_ships >= remaining )
			{
				a.num_ships = remaining;
				new_sources.push_back( a );
				
				if( AnyShipsHaveDepartureAtTurn( new_sources, current_turn ) )
				{
					plan.sources = new_sources;
					return true;
				}
				else
				{
					return false;
				}
			}
			
			remaining -= a.num_ships;
			new_sources.push_back( a );
		}
		else
		{
			if( verbose ) DbgPMessage( a.source, 0, 255, 0, "No ships available (t %d)", turn_on_which_attack_is_profitable );
		}
	}
	
	return false;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

bool AdjustPlanSources( const GameState& g, const MapAnalysis& map, const MapResourceAvailability& resources, AttackPlan& plan )
{
	const Planet& p = g.At( plan.arrival ).GetPlanet( plan.target );
	const int total_planet_ships = p.NumShips();
	int ships_needed = 0;
	
	// defense special case
	if( plan.request.type == A_Defense && plan.arrival <= plan.request.deadline )
	{
		// use the minimum from the request
		ships_needed = plan.request.num_ships;
	}
	else if( p.Owner() == 0 )
	{
		if( IsPlanetInPlayerTerritory( g, map.player, plan.arrival, plan.target ) )
		{
			ships_needed = total_planet_ships + 1;
		}
		else
		{
			const int max_reinforcements =		GetPossibleShipsToTargetAll( g, plan.target, plan.arrival+1, map.player.enemy_id )
											+	CountFleetsWithDestinationAfterTurn( g, plan.target, map.player.enemy_id, plan.arrival+1 );
			ships_needed = total_planet_ships + max_reinforcements + 1;
		}
	}
	else
	{
		const int max_reinforcements = GetPossibleShipsToTargetAll( g, plan.target, plan.arrival, map.player.enemy_id );
		ships_needed = total_planet_ships + max_reinforcements + 1;
	}
		
	if( !GetAvailableSources( g, map, resources, ships_needed, plan ) )
	{
		plan.sources.clear();
		return false;
	}
	
	DbgPMessage( plan.target, 255, 255, 255, "Attack Possible" );
	
	return true;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void HighlightPlanSources( const PlanetWars& pw, const AttackPlan& plan )
{
	DbgPHighlight( plan.target, 0, 255, 255 );
	
	for( int i=0; i<plan.sources.size(); ++i )
	{
		const Attacker& a = plan.sources[i];
		
		DbgPHighlight( a.source, 255, 255, 0 );
	
		DbgPMessage( a.source, 255, 255, 0, "Send %d on turn %d", a.num_ships, a.scheduled_departure );
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

TPlanetIDList GetSortedOthers( const PlanetWars& pw, int planet )
{
	TPlanetIDList n;
	n.reserve( g_const.num_planets-1 );
	
	for( int i=0; i<g_const.num_planets; ++i )
	{
		if( i != planet )
		{
			n.push_back( i );
		}
	}
	
	std::sort( n.begin(), n.end(), DistanceAndShipsPrioritization( pw, planet ) );
	return n;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

AttackPlan GenerateNewPlan( const GameState& g, const MapAnalysis& map, const ResourceRequest& r, const MapResourceAvailability& resources )
{
	DbgScope( "GenerateNewPlan (target %d, type %s)", r.destination_planet, r.type == A_Offense ? "Offense" : r.type == A_Defense ? "Defense" : "Growth" );

	const int turn = g.Current().Turn();
	const int target = r.destination_planet;
	DbgPHighlight( target, 0, 255, 255 );

	bool attack_possible = false;
	AttackPlan plan;
	plan.player = map.player;
	plan.target = target;
	plan.arrival = turn;
	plan.request = r;
	
	int min_arrival = turn+1;// +1 for min distance between planets
	int max_arrival = turn+g_const.max_distance;
	
	if( r.deadline )
	{
		if( r.type == A_Offense ) { min_arrival = r.deadline; }
		// Still want to go after the planet in this case, will adjust needed ships later
		// if( r.type == A_Defense ) { max_arrival = r.deadline; }
	}
	
	const TPlanetIDList others = GetSortedOthers( g.Current(), target );
	
	// step forward in time
	for( int t=min_arrival; t<=max_arrival && !attack_possible; ++t )
	{
		DbgScope( "GenerateNewPlan %d<=%d<=%d", min_arrival, t, max_arrival );
		DbgPHighlight( target, 0, 255, 255 );
		plan.sources.clear();
		plan.sources.reserve( g_const.num_planets );
		plan.arrival = t;
		
		// look at all planets each turn. start over each turn, as eligibility may change frequently
		for( int i=0; i<others.size(); ++i )
		{
			const int source = others[i];
			
			Attacker a;
			a.source = source;
			a.actual_target = plan.target;
			a.num_ships = 0;				// will be adjusted later
			a.scheduled_departure = turn;	// will be adjusted later
			plan.sources.push_back( a );
		}
		
		attack_possible = AdjustPlanSources( g, map, resources, plan );
	}
	
	if( attack_possible )
	{
		HighlightPlanSources( g.Current(), plan );
	}
	else
	{
		plan.sources.clear();
	}
	
	return plan;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void EvaluateResourceRequest( const GameState& g, const MapAnalysis& map, const AttackPlan& plan, ResourceRequestEvaluation& eval )
{
	DbgScope( "EvaluateResourceRequest( %d )", plan.target );
	
	const Planet& pl = g.Current().GetPlanet( plan.target );
	const PlanetKnowledge& p = map.planets[ plan.target ];
	
	eval.value = pl.GrowthRate() * p.relevance_score;
	eval.cost = PlanInvestmentInTurns( g, plan );
	
	if( plan.request.type != A_Growth )
	{
		eval.value *= 2.0f;
	}
	
	DbgPHighlight( plan.target, 255, 255, 255 );
	DbgPMessage( plan.target, 255, 255, 255, "%f, %f", eval.value, eval.cost );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GeneratePlansFromRequests( const GameState& g, const MapAnalysis& map, const ResourceRequestList& requests, AttackPlanList& new_plans )
{
	DbgScope( "GeneratePlansFromRequests" );
	
	Assert( new_plans.empty() );
	
	// generate the plan-in-a-vacuum list. this is assumed to be the best-case cost for each move. as we assign future moves
	// this cost must increase to keep the algorithm correct (not proven!)
	std::priority_queue< ResourceRequestEvaluation > plan_evaluation;

	for( ResourceRequestList::const_iterator i=requests.begin(); i!=requests.end(); ++i )
	{
		const ResourceRequest& r = *i;
		
		MapResourceAvailability resources;
		CalculateResourceAvailability( g, map, new_plans, resources );
		
		AttackPlan p = GenerateNewPlan( g, map, r, resources );
		if( !p.sources.empty() ) 
		{ 
			ResourceRequestEvaluation eval;
			eval.request = r;
			EvaluateResourceRequest( g, map, p, eval );
			plan_evaluation.push( eval );
		}
	}
	
	while( !plan_evaluation.empty() )
	{
		ResourceRequestEvaluation eval = plan_evaluation.top();
		plan_evaluation.pop();
		
		MapResourceAvailability resources;
		CalculateResourceAvailability( g, map, new_plans, resources );
		
		AttackPlan p = GenerateNewPlan( g, map, eval.request, resources );
		if( !p.sources.empty() ) 
		{
			EvaluateResourceRequest( g, map, p, eval );
			
			if( eval < plan_evaluation.top() )
			{
				// try again later
				plan_evaluation.push( eval );
			}
			else
			{
				// this is the lowest cost with the latest allocations. make this permanent!
				new_plans.push_back( p );
			}
		}
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

int GetRandomEnemy( const GameState& g, const PlayerIDs& player )
{
	for( int i=0; i<g_const.num_planets; ++i )
	{
		if( g.Current().GetPlanet(i).Owner() == player.enemy_id )
		{
			return i;
		}
	}
	
	return INVALID_PLANET;
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void ExtrapolateGameStateFromPlans( const PlayerIDs& player, const AttackPlanList& plans, GameState& g )
{
	DbgScope( "ExtrapolateGameStateFromPlans" );
	
	const TOrderList null_orders;
	
	for( int i=0; i<=g_const.max_distance; ++i )
	{
		const int turn = g.Current().Turn()+i;
		TOrderList orders_for_this_turn;
		
		const PlanetWars& pw = g.At( turn );
		GenerateOrdersFromPlans( pw, player, plans, orders_for_this_turn );
		
		PlanetWars* next = new PlanetWars( pw );
		next->AdvanceSimulation( orders_for_this_turn, null_orders );
		g.AddTurn( next );
	}
	
	DbgGameState( &g.At( g.Current().Turn() + g_const.max_distance ) );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

bool GetThreatDirection( const GameState& g, int source, int player_id, Vec2& dir )
{
	dir = Vec2( 0.0f, 0.0f );
	float w = 0.0f;
	
	Vec2 origin = g.Current().GetPlanet( source ).Origin();
	
	for( int i=0; i<g_const.num_planets; ++i )
	{
		if( i == source ) { continue; }
		
		const int d = g_const.Distance( i, source );
		const int t = g.Current().Turn()+d;
		const Planet& p2 = g.At( t ).GetPlanet( i );
		if(	p2.Owner() == player_id )
		{
			const float s = (float)p2.NumShips() / (float)( d*d );
			dir += ( p2.Origin() - origin ).normalize() * s;
			w += s;
		}
	}
	
	if( dir.length() < .0001f )
	{
		DbgLine( origin, (origin+dir), 255, 255, 255 );
		return false;
	}
	else
	{
		dir.normalize();
		return true;
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GenerateSupplyPlan( const GameState& real_state, MapAnalysis& map, AttackPlanList& new_plans )
{
	DbgScope( "GenerateSupplyPlan" );	

	MapResourceAvailability resources;
	CalculateResourceAvailability( real_state, map.player, new_plans, resources );
	
	AttackPlan plan;
	plan.player = map.player;
	plan.target = GetRandomEnemy( real_state, map.player );
	plan.arrival = 0;
	plan.request.type = A_Defense;
	
	if( plan.target == INVALID_PLANET )
	{
		return;
	}
	
	GameState predicted_state( real_state.Current() );
	ExtrapolateGameStateFromPlans( map.player, new_plans, predicted_state );

	// funnel the remainder of the ships to the front line
	for( int i=0; i<g_const.num_planets; ++i )
	{
		const int planetnum = i;
		
		PlanetKnowledge& k_sender = map.planets[planetnum];
		k_sender.supply_role = S_None;
		k_sender.supply_dest = INVALID_PLANET;
		
		if( predicted_state.Current().GetPlanet( planetnum ).Owner() != map.player.player_id ) { continue; }
		
		const int minimum_available = GetMinimumAvailableShips( predicted_state, planetnum, predicted_state.Current().Turn(), resources );
		if( minimum_available <= 0 ) { DbgPMessage( i, 255, 255, 255, "none available?" ); continue; }
		
		DbgScope( "Source: %d", planetnum );
		DbgPHighlight( planetnum, 255, 255, 255 );
		
		Vec2 dir;
		bool found_enemy = GetThreatDirection( predicted_state, i, map.player.enemy_id, dir );
		if( !found_enemy ) { DbgPMessage( i, 255, 255, 255, "no enemy" ); continue; }
		
		const float angle = DegToRad( 45.0f );
		TPlanetIDList between = GetPlanetsInCone( predicted_state.Current(), i, dir, angle );
		
		std::sort( between.begin(), between.end(), DistanceAndShipsPrioritization( predicted_state.Current(), i ) );
		
		// find all planets between the source and the nearest enemy
		TPlanetIDList mine;
		mine.reserve( between.size() );
		
		for( int j=0; j<between.size(); ++j )
		{
			const int neighbor = between[j];
			
			const int t = predicted_state.Current().Turn()+g_const.Distance( planetnum, neighbor );
			const Planet& p2 = predicted_state.At( t ).GetPlanet( neighbor );
			
			if( p2.Owner() == map.player.player_id )
			{
				mine.push_back( neighbor );
			}
			else if( p2.Owner() == map.player.enemy_id )
			{
				break;
			}
		}
		
		if( mine.empty() ) { continue; }
		
		// prioritize based on distance and relevance
		std::sort( mine.begin(), mine.end(), SupplyPrioritization( map, planetnum ) );
		
		const int supply_planet = mine.front();
		
		// prevent cycles
		if( PartOfSupplyChain( map, supply_planet, planetnum ) ) { continue; }
		
		Attacker a;
		a.source = planetnum;
		a.actual_target = supply_planet;
		a.num_ships = minimum_available;
		a.scheduled_departure = predicted_state.Current().Turn();
		plan.sources.push_back( a );
		
		DbgPLine( planetnum, supply_planet, 255, 255, 0 );
		
		PlanetKnowledge& k_dest = map.planets[supply_planet];
		
		k_sender.supply_dest	= supply_planet;
		k_sender.supply_role	|= S_Sending;
		k_dest.supply_role		|= S_Receiving;
	}
	
	if( !plan.sources.empty() )
	{
		new_plans.push_back( plan );
	}
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void GetOrders( const TurnInfo& turn, TOrderList& confirmed_orders ) 
{	
	ResourceRequestList requests;
	GenerateResourceRequests( turn, *turn.map, requests );
	
	AttackPlanList new_plans;
	GeneratePlansFromRequests( *turn.gamestate, *turn.map, requests, new_plans );
	GenerateSupplyPlan( *turn.gamestate, *turn.map, new_plans );

	GenerateOrdersFromPlans( turn.gamestate->Current(), turn.player, new_plans, confirmed_orders );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

void SendTurn( const TOrderList& orders ) 
{
	for( TOrderList::const_iterator i=orders.begin(); i!=orders.end(); ++i )
	{
		const Order& o = *i;
		std::cout << o.source_planet_ << " " << o.destination_planet_ << " " << o.num_ships_ << std::endl;
	}
	
	std::cout << "go" << std::endl;
	std::cout.flush();
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

TurnInfo t;
	
void TurnMain( const std::string& map_data, int turn )
{
	GameState gamestate( map_data, turn );
	
	t.player.player_id	= 1;
	t.player.enemy_id	= 2;
	t.gamestate = &gamestate;
	
	if( turn == 0 )
	{
		g_const.Init( gamestate.Current() );
		
		t.map = new MapAnalysis( t.player );
		InitMapAnalysis( *t.gamestate, t.player, *t.map );
	}
	
	TOrderList orders;
	GetOrders( t, orders );
	
	SendTurn( orders );
}

//*******************************************************************
//																	*
//																	*
//*******************************************************************

int main(int argc, char *argv[]) 
{
	InitLog( argv[0] );
	DbgMessageType( "Version", "[[Bot built on %s %s]]", __DATE__, __TIME__ );

	std::string current_line;
	std::string map_data;
	int turn_num = 0;
	
	while (true) 
	{
		int c = std::cin.get();
		current_line += (char)c;
		if (c == '\n') 
		{
			if (current_line.length() >= 2 && current_line.substr(0, 2) == "go") 
			{
				TurnMain( map_data, turn_num );	
				map_data = "";
				turn_num++;
			} 
			else 
			{
				map_data += current_line;
			}
			current_line = "";
		}
	}
	
	return 0;
}

