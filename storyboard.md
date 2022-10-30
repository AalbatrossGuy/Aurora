# RPG Game Run-through

player gets a character with a chosen name and starts advancing through the forest.
executes a command to do a task, gets random result
levels up to gain more hp.
armors, magic, weapons, etc. found
add pixel arts.

xp gain -> hunting, attacking, exploring, finding valuables, winning duels(?????) ; when player gains a certain amount of xp then levels up
levelling up -> increases attack damage by 10, increases defense by 10, increases magic damage by 10, increases health by 10 (you start with 100hp)

every artifacts/entities/objects will be a dataclass which'll have their own powerups. assign it to a dictionary and fetch it.

badges -> Honor every player with badges once they reach a certain requirement, e.g., "Slayer" badge if you've killed over 500 mobs, etc.

## Rough Story 
ultimate goal : kill the dragon 

the dragon lives in a realm with a set point of (let's say 550)
any player can challenge the dragon 
if the player has <550 points - instant death
if the player has >550 points - wins
the player does not know how much points are needed to win the game 

the player does side quests
your point decreases with each try on the quest
(lets say 6) 
each has 100 points 
you get potions based on how good you perform 
higher level potions give you more points

when player has (lets say) 6 eyes of the dragon they challenge dragons
if he has more points than dragon he wins 
if he has less points than dragon he loses and game resets 


# Important Criterias
- ### Actions depending on Player / Mob Level 
    - Attack Damage
    - Defense
    - Magic Power / Mana
    - Health

## Basic Navigation
Player randomly moves either +ve (up) or -ve (down) directions. We have x number of maps and a +- 10 radius around it made up of the same terrain(desert, tropical, etc.)
Terrain specific artifacts will be found. Each map will have its own metadata from where we can fetch the direction coordinates. While exploring, player encounters quests/missions. 
Once player visits a map, the map is ticked off from the player's database. Once the player completes all the maps in the +ve or -ve direction, they'll go the next direction. There will be a buffer time for that where no quests will be found (probably; undecided yet)
