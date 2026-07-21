from entities.entity import Entity
from entities.components.position import Position
from entities.components.renderable import Renderable
from entities.components.stats import Stats
from entities.components.ai import AI
from entities.components.combat import Combat
from entities.components.status_effects import StatusEffects
from config import config
import random

def create_skeleton(x, y, level=1):
    skeleton = Entity()
    skeleton.add_component(Position(x, y))
    skeleton.add_component(Renderable('S', config.COLORS['enemy']))
    hp = 25 + level * 8
    skeleton.add_component(Stats(hp, hp, 0, 0, 7 + level, 3 + level//2, 0, 3))
    skeleton.add_component(AI('aggressive'))
    skeleton.add_component(Combat(3, crit_chance=3, damage_type='physical'))
    skeleton.add_component(StatusEffects())
    skeleton.name = "Skeleton"
    skeleton.entity_type = "enemy"
    skeleton.xp_value = 20 + level * 5
    skeleton.gold_value = random.randint(5, 15)
    return skeleton

def create_goblin(x, y, level=1):
    goblin = Entity()
    goblin.add_component(Position(x, y))
    goblin.add_component(Renderable('G', (100, 200, 50)))
    hp = 18 + level * 5
    goblin.add_component(Stats(hp, hp, 0, 0, 10 + level, 2, 0, 5 + level))
    goblin.add_component(AI('cowardly'))
    goblin.add_component(Combat(4, crit_chance=8, damage_type='physical'))
    goblin.add_component(StatusEffects())
    goblin.name = "Goblin"
    goblin.entity_type = "enemy"
    goblin.xp_value = 15 + level * 5
    goblin.gold_value = random.randint(3, 10)
    return goblin

def create_orc(x, y, level=1):
    orc = Entity()
    orc.add_component(Position(x, y))
    orc.add_component(Renderable('O', (200, 100, 0)))
    hp = 50 + level * 12
    orc.add_component(Stats(hp, hp, 0, 0, 14 + level*2, 5 + level, 0, 2))
    orc.add_component(AI('aggressive'))
    orc.add_component(Combat(6, crit_chance=5, crit_multiplier=3.0, damage_type='physical'))
    orc.add_component(StatusEffects())
    orc.name = "Orc"
    orc.entity_type = "enemy"
    orc.xp_value = 45 + level * 10
    orc.gold_value = random.randint(10, 25)
    return orc

def create_dark_mage(x, y, level=1):
    mage = Entity()
    mage.add_component(Position(x, y))
    mage.add_component(Renderable('M', (150, 0, 200)))
    hp = 30 + level * 6
    mana = 50 + level * 10
    mage.add_component(Stats(hp, hp, mana, mana, 5 + level, 2, 15 + level*2, 3))
    mage.add_component(AI('caster'))
    mage.add_component(Combat(8, crit_chance=5, damage_type='magic', elemental_power=10))
    mage.add_component(StatusEffects())
    mage.name = "Dark Mage"
    mage.entity_type = "enemy"
    mage.xp_value = 40 + level * 10
    mage.gold_value = random.randint(8, 20)
    return mage

def create_boss(x, y, floor_number):
    boss = Entity()
    boss.add_component(Position(x, y))
    boss.add_component(Renderable('B', (255, 0, 100), size=40, glow=True))
    hp = 200 + floor_number * 50
    mana = 100 + floor_number * 20
    boss.add_component(Stats(hp, hp, mana, mana, 25 + floor_number*3, 10 + floor_number, 
                             15 + floor_number*2, 2))
    boss.add_component(AI('boss'))
    boss.add_component(Combat(15, crit_chance=15, crit_multiplier=2.5, 
                              damage_type='dark', elemental_power=20))
    boss.add_component(StatusEffects())
    boss.name = "Dungeon Lord"
    boss.entity_type = "boss"
    boss.xp_value = 150 + floor_number * 50
    boss.gold_value = random.randint(100, 300)
    return boss

def spawn_enemies_for_room(room, floor_number):
    enemies = []
    num_enemies = random.randint(1, 3 + floor_number // 2)
    enemy_types = [create_skeleton, create_goblin, create_orc, create_dark_mage]
    for _ in range(num_enemies):
        pos = room.get_random_position()
        enemy_type = random.choice(enemy_types)
        enemy = enemy_type(pos[0], pos[1], floor_number)
        enemies.append(enemy)
    return enemies

def spawn_boss_for_room(room, floor_number):
    pos = room.center
    return [create_boss(pos[0], pos[1], floor_number)]