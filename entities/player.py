from entities.entity import Entity
from entities.components.position import Position
from entities.components.renderable import Renderable
from entities.components.stats import Stats
from entities.components.inventory import Inventory
from entities.components.skill_tree import SkillTree
from entities.components.status_effects import StatusEffects
from entities.components.combat import Combat
from config import config

def create_player(x, y):
    player = Entity()
    player.add_component(Position(x, y))
    player.add_component(Renderable('@', config.COLORS['player'], glow=True))
    player.add_component(Stats(
        config.PLAYER_MAX_HP, config.PLAYER_MAX_HP,
        config.PLAYER_MAX_MANA, config.PLAYER_MAX_MANA,
        config.PLAYER_ATTACK, config.PLAYER_DEFENSE,
        config.PLAYER_MAGIC, config.PLAYER_SPEED
    ))
    player.add_component(Inventory())
    player.add_component(SkillTree())
    player.add_component(StatusEffects())
    player.add_component(Combat(10, crit_chance=10, crit_multiplier=2.5, damage_type='physical'))
    player.name = "Hero"
    player.entity_type = "player"
    return player