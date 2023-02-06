type Owner = Neutral | Self | Opponent;;

type Planet = {
  id: int;
  x: float;
  y: float;
  owner: Owner;
  mutable ships: int;
  growth: int;
};;

type Fleet = {
  f_owner: Owner;
  f_ships: int;
  source: int;
  dest: int;
  tot_turn: int;
  rem_turn: int;
};;


let dummy_planet = { id = -1; x = 0.0; y = 0.0; owner = Neutral; ships = 0; growth = 0; };;
let dummy_fleet = { f_owner = Neutral; f_ships = 0; source = -1; dest = -1; tot_turn = 0; rem_turn = 0; };;

let pid = ref 0;;
let planets = ref ([]:Planet list);;
let fleets = ref ([]:Fleet list);;


let convert_owner = function
 | 0 -> Neutral
 | 1 -> Self
 | _ -> Opponent
;;

let issue_order source dest ships =
	print_int source;
	print_char ` `;
	print_int dest;
	print_char ` `;
	print_int ships;
	print_newline ()
;;

let send_fleet s d p =
	if s.owner = Self && s.ships > p && p > 0
	then begin
		s.ships <- s.ships - p;
		issue_order s.id d.id p
	end else begin
		()	(* do nothing because this move is not allowed *)
	end
;;

let finish_turn () =
  print_string "go";
  print_newline ();
;;

let read_stats mess_list =

  let rec split s c =
    try
	  let o = index_char s c in
	  if o = 0
	  then
	    if string_length s = 1
		then
		  []
		else
		  split (sub_string s (o+1) (string_length s - o - 1)) c
	  else
	    if o + 1 = string_length s
		then
		  [sub_string s 0 o]
		else
		  (sub_string s 0 o)::(split (sub_string s (o+1) (string_length s - o - 1)) c)
    with Not_found -> if s = "" then [] else [s]
  in

  let add_planet args =
    match args with
	 | [x;y;o;s;g] -> try
						let p = {
							id = !pid;
							x = float_of_string x;
							y = float_of_string y;
							owner = convert_owner (int_of_string o);
							ships = int_of_string s;
							growth = int_of_string g;
						} in
						( planets := p :: !planets;
						  pid := !pid + 1 )
					  with _ -> ()
	 | _ -> ()
  and add_fleet args =
    match args with
	 | [o;sh;s;d;tt;rt] -> try
							let f = {
								f_owner = convert_owner (int_of_string o);
								f_ships = int_of_string sh;
								source = int_of_string s;
								dest = int_of_string d;
								tot_turn = int_of_string tt;
								rem_turn = int_of_string rt;
							} in
							fleets := f :: !fleets
						   with _ -> ()
	 | _ -> ()
  in
  
  let read_stat s =
    let s1 = try let o = index_char s `#` in sub_string s 0 o with Not_found -> s in
	let stat_list = split s1 ` ` in
	match stat_list with
	 | "P" :: p -> add_planet p
	 | "F" :: f -> add_fleet f
	 | _ -> ()
  in

  do_list read_stat mess_list
;;

let rec filter cond = function
 |  []  -> []
 | t::q -> if cond t then t::(filter cond q)
                     else filter cond q
;;

let rec part cond = function
 |  []  -> [],[]
 | t::q -> let y,n = part cond q in
           if cond t then (t::y),n
		             else y,(t::n)
;;
 
let rec nth_list = fun
 | 0 (t::q) -> t
 | n (t::q) -> nth_list (n-1) q
 | _ _ -> failwith ""
;;

let get_planets owner_list p_list =
  filter (fun p -> mem p.owner owner_list) p_list
;;

let distance s d =
  let x = s.x -. d.x
  and y = s.y -. d.y in
  int_of_float (ceil (sqrt (x *. x +. y *. y)))
;;

let play_turn planets fleets nb_planets =

  (*   Strategy: send from my strongest planet to the weakest enemy / neutral planet a number of ship equal to:             *)
  (*     -   number of ships of destination planet + 1 if my source planet has enough ships				         *)
  (*     -   number of ships of source planet - 1 otherwise									         *)
  (*    If I have strictly more than 3 fleets ongoing, do nothing.								         *)
  
  let my_planets,other_planets = part (fun p -> p.owner = Self) planets
  and my_fleets = filter (fun f -> f.f_owner = Self) fleets in
  
  if my_planets <> [] && other_planets <> [] && list_length my_fleets <= 3 then begin

    try 

      let p_source = it_list (fun a b -> if a = dummy_planet then b else if a.ships > b.ships then a else b) dummy_planet my_planets
      and p_dest = it_list (fun a b -> if a = dummy_planet then b else if a.ships < b.ships then a else b) dummy_planet other_planets in
  
      send_fleet p_source p_dest (if p_source.ships > p_dest.ships + 2 then p_dest.ships + 1 else p_source.ships - 1)
  
    with _ -> ()

  end else if my_planets <> [] then begin
   
    ()
  
  end
  
;;


let main () =

	try
		let message = ref [] in
		while true
		do
			let s = input_line stdin in
			if s = "go"
			then begin
				pid := 0;
				planets := [];
				fleets := [];
				read_stats (rev !message);
				message := [];
				play_turn  (rev !planets) (rev !fleets) !pid;
				finish_turn ();
			end else begin
				message := s::!message
			end
		done
	with End_of_file -> ()

in

main ();;