class Pokemon: 
  def __init__(self, ID, name, type1, type2, atk, defence, hp, speed, moves):
    self.ID = ID
    self.name = name
    self.type1 = type1
    self.type2 = type2
    self.atk = atk
    self.defence = defence
    self.hp = hp
    self.speed = speed
    self.moves = moves
    self.moveIndex = None
    self.fainted = False
    
  def __lt__(self, other):
    if isinstance(other, Pokemon):
      return self.speed < other.speed
    return True
    
class MyType:
  def __init__(self, name, ID):
    self.name = name
    self.ID = ID
    
class Types:
    GRASS = MyType('Grass', 0)
    FIRE = MyType('Fire', 1)
    WATER = MyType('Water', 2)
    GROUND = MyType('Ground', 3)
    ROCK = MyType('Rock', 4)
    BUG = MyType('Bug', 5)
    ELECTRIC = MyType('Electric', 6)
    NORMAL = MyType('Normal', 7)
    FIGHT = MyType('Fight', 8)
    FLYING = MyType('Flying', 9)
    POISON = MyType('Poison', 10)
    GHOST = MyType('Ghost', 11)
    PSYCHIC = MyType('Psychic', 12)
    ICE = MyType('Ice', 13)
    DRAGON = MyType('Dragon', 14)

mapp = [[0.5, 2.0, 0.5, 0.5, 0.5, 2.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 1.0],
       [0.5, 0.5, 2.0, 2.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0], 
       [2.0, 0.5, 0.5, 0.5, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0], 
       [2.0, 0.5, 2.0, 1.0, 0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 2.0, 1.0], 
       [2.0, 0.5, 2.0, 2.0, 1.0, 0.5, 0.5, 0.5, 2.0, 0.5, 0.5, 1.0, 2.0, 1.0, 1.0], 
       [0.5, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 1.0], 
       [1.0, 1.0, 0.5, 2.0, 2.0, 1.0, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
       [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
       [1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 0.0, 2.0, 0.5, 1.0],
       [0.5, 1.0, 1.0, 0.0, 2.0, 0.5, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0], 
       [0.5, 1.0, 1.0, 2.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0],
       [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0],
       [1.0, 0.5, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0],
       [0.5, 2.0, 1.0, 0.5, 1.0, 0.5, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
       [1.0, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0]]


             
class Move:
  def __init__(self, name, power, types):
    self.name = name
    self.power = power
    self.types = types
    
magical_leaf = Move ('magical leaf', 60, Types.GRASS)
sludge_bomb = Move ('sludge bomb', 90, Types.POISON)
body_slam = Move ('body slam', 85, Types.NORMAL)

flamethrower = Move ('flamethrower', 95, Types.FIRE)
earthquake = Move ( 'earthquake', 100, Types.GROUND)
dragon_claw = Move ('dragon claw', 80, Types.DRAGON)

surf = Move ('surf', 95, Types.WATER)
ice_beam = Move ('ice beam', 95, Types.ICE)
submission = Move ('submission', 80, Types.FIGHT)
    
venusaur = Pokemon (0, 'venusaur', Types.GRASS, Types.POISON, 82, 83, 80, 80, magical_leaf, sludge_bomb, body_slam) 
charizard  = Pokemon (1, 'Charizard', Types.FIRE, Types.FLYING, 84, 78, 78, 100, flamethrower, earthquake, dragon_claw) 
blastoise = Pokemon (2, 'Blastoise', Types.WATER, '', 83, 100, 79, 78, surf, ice_beam, submission)  

pokemans = [
            venusaur,
            charizard,
            blastoise
            ]

def Battle_calc(pokemon1, pokemon2):
  messages = []
  pokemon = sorted([pokemon1, pokemon2], reverse=True)
  for p, poke in enumerate(pokemon):
    poke2 = pokemon[1-p]
    damage = Damage_calc(poke, poke2, poke.moves[poke.moveIndex])
    pokemon[1-p].hp -= damage
    
    messages.append('{} used {}!'.format(poke.name, poke.moves[poke.moveIndex]))
    if poke2.hp <= 0:
      messages.append('{} fainted!'.format(poke2.name))
      pokemon[1-p].fainted = True
      break
  
  return [[pokemon1, pokemon2], messages]

def Damage_calc(atk_pokemon, defence_pokemon, move):
  damage = atk_pokemon.atk + move.power
  damage = damage / 1.5 
  damage = damage - defence_pokemon.defence
  damage = damage * mapp[defence_pokemon.type1.ID][move.types.ID]
  damage = damage * mapp[defence_pokemon.type2.ID][move.types.ID]
  
  return damage 