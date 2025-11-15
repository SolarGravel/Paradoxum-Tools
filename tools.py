import pandas
from pandas import DataFrame
from dataclasses import dataclass, field
from enum import Enum, auto

stats_df: DataFrame = pandas.read_csv("data/stats.csv")


class DamageType(Enum):
    PHYSICAL = auto()
    MAGIC = auto()
    TRUE = auto()


@dataclass
class DamageStats:
    damage: int = 0
    penetration: int = 0
    shredding: float = 0


@dataclass
class Damage:
    physic: DamageStats = field(default_factory=DamageStats)
    magic: DamageStats = field(default_factory=DamageStats)
    true: int = 0


@dataclass
class DefenseStats:
    hp: int = 0
    protection: int = 0
    barrier: int = 0
    resistance: float = 0


@dataclass
class BasicAtkStats:
    dps_damage: dict[DamageType, int] = field(
        default_factory=lambda: {
            DamageType.PHYSICAL: 0,
            DamageType.MAGIC: 0,
            DamageType.TRUE: 0,
        }
    )
    atk_speed: float = 0.0
    effect: float = 0.0


def get_price_str(craft_items: dict[str, dict[str, int]], additional_price: int) -> str:
    result_str: str = ""

    for ingredient, info in craft_items.items():
        for _ in range(info["amount"]):
            result_str += f"*{ingredient}* ({info['price']} J$) + "

    result_str += f"{additional_price} J$"

    return result_str


def get_stat_price(stat: str, value: float) -> float:
    stat_df = stats_df[stats_df["name"] == stat]

    return int(stat_df["price"].values[0]) * value


def get_percent_protection(protection: float) -> float:
    if protection < 0:
        protection = abs(protection)

        return -(protection / (100 + protection))

    return protection / (100 + protection)


def get_effective_hp(hp: int, protection: int) -> int:
    if protection < 0:
        protection = abs(protection)

        return round(hp * (0.5 + 25 / (protection + 50)))

    return round(hp * (1 + protection / 100))


def get_effective_protection(
    protection: int, penetration: int, shredding: float
) -> float:
    return (protection * (1 - shredding)) - penetration


def get_dps(
    dps_stats: BasicAtkStats,
    types: list[DamageType] = [DamageType.PHYSICAL, DamageType.MAGIC, DamageType.TRUE],
) -> int:
    dps_total: int = 0

    if DamageType.PHYSICAL in types:
        dps_total += dps_stats.dps_damage[DamageType.PHYSICAL]
    if DamageType.MAGIC in types:
        dps_total += dps_stats.dps_damage[DamageType.MAGIC]
    if DamageType.TRUE in types:
        dps_total += dps_stats.dps_damage[DamageType.TRUE]

    return round(dps_total * dps_stats.atk_speed * dps_stats.effect)


def get_damages(
    damage_stats: Damage, defense_stats: DefenseStats, dps_stats: BasicAtkStats
) -> tuple[float, float, float]:
    phys_damage = (
        (damage_stats.physic.damage + get_dps(dps_stats, [DamageType.PHYSICAL]))
        * (
            1
            - get_percent_protection(
                get_effective_protection(
                    defense_stats.protection,
                    damage_stats.physic.penetration,
                    damage_stats.physic.shredding,
                )
            )
        )
        * (1 - defense_stats.resistance)
    )

    mag_damage = (
        (damage_stats.magic.damage + get_dps(dps_stats, [DamageType.MAGIC]))
        * (
            1
            - get_percent_protection(
                get_effective_protection(
                    defense_stats.barrier,
                    damage_stats.magic.penetration,
                    damage_stats.magic.shredding,
                )
            )
        )
        * (1 - defense_stats.resistance)
    )
    
    true_damage = damage_stats.true + get_dps(dps_stats, [DamageType.TRUE])

    return round(phys_damage), round(mag_damage), round(true_damage)


if __name__ == "__main__":
    damage = Damage(
        physic=DamageStats(damage=1000, penetration=0, shredding=0),
        magic=DamageStats(damage=0, penetration=0, shredding=0),
        true=0,
    )

    defense = DefenseStats(hp=3000, protection=0, barrier=0, resistance=0)
    
    dps = BasicAtkStats(
        dps_damage= {
            DamageType.PHYSICAL: 100,
            DamageType.MAGIC: 0,
            DamageType.TRUE: 10
        },
        atk_speed=2,
        effect=1
    )

    print(get_damages(damage, defense, dps))
