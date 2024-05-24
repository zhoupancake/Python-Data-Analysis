import numpy as np

from src.dataAnalysis.dataAnalysis import *

data = read_from_db(TABLE_NAME)


def min_max_speed_each_position():
    df = process_position()
    fastest_heroes = df.sort_values("MovementSpeed", ascending=False).groupby("Position").head(1)[
        ["Position", "MovementSpeed"]]
    slowest_heroes = df.sort_values("MovementSpeed", ascending=True).groupby("Position").head(1)[
        ["Position", "MovementSpeed"]]
    fastest_heroes.drop(fastest_heroes[fastest_heroes['Position'] == 'no'].index, inplace=True)
    slowest_heroes.drop(slowest_heroes[slowest_heroes['Position'] == 'no'].index, inplace=True)
    fastest_heroes.columns = ["Position", "Fastest"]
    slowest_heroes.columns = ["Position", "Slowest"]
    fastest_heroes.reset_index(drop=True, inplace=True)
    slowest_heroes.reset_index(drop=True, inplace=True)
    merged_df = pd.merge(fastest_heroes, slowest_heroes, how='inner', on='Position')
    merged_df.columns = ["Position", "Fastest", "Slowest"]
    return merged_df


def min_max_health_each_position():
    main_position_stats = data.groupby(['mainPosition'])['MaximumHealth'].agg(['min', 'max']).reset_index()
    sub_position_stats = data.groupby(['subPosition'])['MaximumHealth'].agg(['min', 'max']).reset_index()
    main_position_stats.columns = ['position', 'min_main', 'max_main']
    sub_position_stats.columns = ['position', 'min_sub', 'max_sub']
    merged_stats = pd.merge(main_position_stats, sub_position_stats, how='outer', on='position',
                            suffixes=('_main', '_sub'))
    merged_stats['min_combined'] = merged_stats.apply(lambda row: np.nanmin([row['min_main'], row['min_sub']]), axis=1)
    merged_stats['max_combined'] = merged_stats.apply(lambda row: np.nanmax([row['max_main'], row['max_sub']]), axis=1)
    merged_stats = merged_stats[['position', 'min_combined', 'max_combined']][
        merged_stats['position'] != 'no'].reset_index()
    merged_stats.drop(['index'], axis=1, inplace=True)
    merged_stats.columns = ['position', 'min', 'max']
    return merged_stats


def distribution_speed_each_position():
    x_data = []
    x_name = []
    x1 = process_position()[process_position()['Position'] != 'no']
    x1 = x1.groupby('Position')
    for name, group in x1:
        x_data.append(np.array(group['MovementSpeed']).tolist())
        x_name.append(name)
    return [x_name, x_data]


def distribution_health_each_position():
    x_data = []
    x_name = []
    x1 = process_position()[process_position()['Position'] != 'no']
    x1 = x1.groupby('Position')
    for name, group in x1:
        x_data.append(np.array(group['MaximumHealth']).tolist())
        x_name.append(name)
    return [x_name, x_data]


def type_count_each_position():
    df = process_position()
    position_hero_type_count = df.groupby(['Position', 'HeroType']).size().unstack().fillna(0).astype(int)
    position_hero_type_count = position_hero_type_count[position_hero_type_count.index != 'no']
    position_hero_type_count = position_hero_type_count.reset_index()
    position_hero_type_count.columns = ['Position', 'Magic', 'Physical']
    return position_hero_type_count


def attack_range_count_each_position():
    df = process_position()
    position_hero_attackRange_count = df.groupby(['Position', 'AttackRange']).size().unstack().fillna(0).astype(int)
    position_hero_attackRange_count = position_hero_attackRange_count[position_hero_attackRange_count.index != 'no']
    position_hero_attackRange_count = position_hero_attackRange_count.reset_index()
    position_hero_attackRange_count.columns = ['Position', 'Long', 'Short']
    print(position_hero_attackRange_count)
    return position_hero_attackRange_count


def relation_PhysicalDefense_PhysicalDamageReduction():
    df = process_position()
    mode_attack_both = df.groupby("Position")[
        ["PhysicalDefense", "PhysicalDamageReduction"]].median().reset_index()
    mode_attack_both.columns = ["Position", "PhysicalDefense", "PhysicalDamageReduction"]
    mode_attack_both = mode_attack_both[mode_attack_both['Position'] != 'no']
    mode_attack_both.reset_index(drop=True, inplace=True)
    return mode_attack_both


def relation_MaximumMana_ManaRegeneration():
    df = process_position()
    mode_attack_both = df.groupby("Position")[
        ["MaximumMana", "ManaRegeneration"]].median().reset_index()
    mode_attack_both.columns = ["Position", "MaximumMana", "ManaRegeneration"]
    mode_attack_both = mode_attack_both[mode_attack_both['Position'] != 'no']
    mode_attack_both.reset_index(drop=True, inplace=True)
    return mode_attack_both
