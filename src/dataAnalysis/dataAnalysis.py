import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.dataStore.dao import *

data = read_from_db(TABLE_NAME)


def process_position():
    """
    Process the 'mainPosition' and 'subPosition' columns to create a new 'Position' column,
    where values are either the combination of 'mainPosition' and 'subPosition' or 'no' if 'subPosition' is 'no'.
    Drops the 'mainPosition' and 'subPosition' columns, explodes the 'Position' column, and returns the resulting DataFrame.
    """
    data['Position'] = data['mainPosition'] + '\n' + data['subPosition'].replace('no', 'no')
    temp = data.drop(['mainPosition', 'subPosition'], axis=1)
    result = temp.assign(Position=temp['Position'].str.split('\n')).explode('Position')
    return result


def count_hero_each_position():
    """
    Count the number of heroes for each 'Position' and return the result.
    """
    df = process_position()
    position_count = df['Position'].value_counts().drop('no')
    position_count = position_count.reset_index()
    position_count.columns = ['Position', 'Count']
    return position_count


def min_max_health_each_position():
    """
    Calculate the minimum and maximum health for each 'mainPosition' and 'subPosition'.
    Returns the resulting DataFrame.
    """
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


def average_health_each_position():
    """
    Calculate the average health for each 'Position' (combining 'mainPosition' and 'subPosition').
    Returns the resulting DataFrame.
    """
    df = process_position()
    average_health_position = df.groupby("Position")["MaximumHealth"].mean().reset_index()
    average_health_position.columns = ["Position", "AverageHealth"]
    average_health_position = average_health_position[average_health_position['Position'] != 'no']
    average_health_position.reset_index(drop=True, inplace=True)
    return average_health_position


def average_speed_each_position():
    """
    Calculate the average health for each 'Position' (combining 'mainPosition' and 'subPosition').
    Returns the resulting DataFrame.
    """
    df = process_position()
    average_speed_position = df.groupby("Position")["MovementSpeed"].mean().reset_index()
    average_speed_position.columns = ["Position", "MovementSpeed"]
    average_speed_position = average_speed_position[average_speed_position['Position'] != 'no']
    average_speed_position.reset_index(drop=True, inplace=True)
    return average_speed_position


def fast_slow_hero_each_position():
    """
    calculate the average speed for each 'Position' and return the resulting DataFrame.
    """
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


def median_damageReduction_for_phy_and_magic_each_position():
    """
    Calculate the median physical and magic damage reduction for each 'Position'.
    Return the resulting DataFrame.
    """
    df = process_position()
    mode_attack_both = df.groupby("Position")[
        ["PhysicalDamageReduction", "MagicDamageReduction"]].median().reset_index()
    mode_attack_both.columns = ["Position", "PhysicalDamageReduction", "MagicDamageReduction"]
    mode_attack_both = mode_attack_both[mode_attack_both['Position'] != 'no']
    mode_attack_both.reset_index(drop=True, inplace=True)
    return mode_attack_both


def health_kurtosis_each_position_and_all():
    """
    Calculate the kurtosis of the 'MaximumHealth' for each 'Position' and the overall kurtosis.
    Return the resulting kurtosis values.
    """
    df = process_position()

    def calculate_kurtosis(series):
        return pd.DataFrame({"Kurtosis": [series.kurtosis()]})

    max_health_kurtosis_by_position = df.groupby("Position")["MaximumHealth"].apply(calculate_kurtosis).reset_index()
    max_health_kurtosis_by_position.drop(
        max_health_kurtosis_by_position[max_health_kurtosis_by_position['Position'] == 'no'].index, inplace=True)
    max_health_kurtosis_by_position = max_health_kurtosis_by_position.drop("level_1", axis=1)
    max_health_kurtosis_all = data["MaximumHealth"].kurtosis()
    max_health_kurtosis_by_position.columns = ["Position", "Kurtosis"]
    max_health_kurtosis_by_position.reset_index(drop=True, inplace=True)

    all_row = pd.DataFrame({"Position": ["all"], "Kurtosis": [max_health_kurtosis_all]})
    max_health_kurtosis_by_position = pd.concat([max_health_kurtosis_by_position, all_row], ignore_index=True)
    return max_health_kurtosis_by_position


def maximumMana_each_position_and_all():
    """
    Find the maximum mana for each 'Position' and the overall maximum mana.
    Return the resulting values.
    """
    df = process_position()
    max_mana_by_position = df.groupby("Position")["MaximumMana"].max().reset_index()
    max_mana_by_position.drop(max_mana_by_position[max_mana_by_position['Position'] == 'no'].index, inplace=True)
    max_mana_by_position.columns = ["Position", "MaximumMana"]
    max_mana_by_position.reset_index(drop=True, inplace=True)
    max_mana_all = data["MaximumMana"].max()

    all_row = pd.DataFrame({"Position": ["all"], "MaximumMana": [max_mana_all]})
    max_mana_by_position = pd.concat([max_mana_by_position, all_row], ignore_index=True)
    return max_mana_by_position


def health_healthRegeneration_relative_each_position_and_all():
    """
    Calculate the correlation between 'MaximumHealth' and 'HealthRegeneration'.
    Return the resulting correlation.
    """
    df = process_position()
    correlation_matrix_by_position = df.groupby('Position')[['MaximumHealth', 'HealthRegeneration']].corr().iloc[0::2,
                                     -1].reset_index()
    all_row = pd.DataFrame(
        {"Position": ["all"], "HealthRegeneration": [df['HealthRegeneration'].corr(df['MaximumHealth'])]})
    correlation_matrix_by_position = pd.concat([correlation_matrix_by_position, all_row], ignore_index=True)
    correlation_matrix_by_position = correlation_matrix_by_position[correlation_matrix_by_position['Position'] != 'no']
    correlation_matrix_by_position.drop('level_1', axis=1, inplace=True)
    correlation_matrix_by_position.columns = ["Position", "Relative"]
    correlation_matrix_by_position.reset_index(drop=True, inplace=True)

    return correlation_matrix_by_position


def mana_ManaRegeneration_relative():
    """
    Calculate the covariance matrix of 'MaximumHealth' and 'HealthRegeneration'.
    Return the resulting covariance matrix.
    """
    covariance = data[['MaximumMana', 'ManaRegeneration']].cov()
    return covariance


def MAD_PhysicalAttack_each_position():
    """
    Calculate the median absolute deviation of 'PhysicalAttack' for each 'Position'.
    Return the resulting DataFrame.
    """

    def calculate_mad(column):
        median = np.median(column)
        mad = np.median(np.abs(column - median))
        return mad

    df = process_position()
    data_cleaned = df.dropna(subset=['PhysicalAttack'])

    mad_by_position = data_cleaned.groupby('Position')['PhysicalAttack'].agg(calculate_mad).reset_index()
    mad_by_position.columns = ['Position', 'MAD_PhysicalAttack']
    mad_by_position.drop(mad_by_position[mad_by_position['Position'] == 'no'].index, inplace=True)
    mad_by_position.reset_index(drop=True, inplace=True)

    return mad_by_position


def mode_movement_speed():
    """
    Calculate the mode of 'MovementSpeed'.
    Returns the mode value(s).
    """

    def custom_mode(series):
        return series.mode().iloc[0] if not series.mode().empty else None

    df = process_position()
    mode_by_group = df.groupby('Position')['MovementSpeed'].apply(custom_mode).reset_index()
    mode_by_group.drop(mode_by_group[mode_by_group['Position'] == 'no'].index, inplace=True)
    mode_by_group.columns = ['Position', 'Mode_MovementSpeed']
    mode_by_group.reset_index(drop=True, inplace=True)
    return mode_by_group


def skewness_attack_range_each_position():
    """
    Calculate the skewness of 'AttackRange' of each 'Position'.
    Returns the skewness value.
    """
    df = process_position()
    df['AttackRange'] = df['AttackRange'].apply(lambda x: 0 if x == 'short' else 1)
    skewness_values = df.groupby(['Position', 'AttackRange'])['AttackRange'].skew()
    skewness_values.replace(np.nan, 0, inplace=True)
    skewness_table = skewness_values.unstack(fill_value=0)
    skewness_table = skewness_table.rename(columns={0: 'short', 1: 'long'})
    skewness_table.reset_index(inplace=True)
    skewness_table.columns = ['Position', 'short', 'long']
    skewness_table.drop(skewness_table[skewness_table['Position'] == 'no'].index, inplace=True)
    skewness_table.reset_index(drop=True, inplace=True)

    return skewness_table


def coefficient_of_variation_max_mana_each_position():
    """
    Calculate the coefficient of variation for 'MaximumMana' of each 'Position'.
    Returns the coefficient of variation value for each 'Position'.
    """
    df = process_position()
    df = df.groupby('Position')['MaximumMana'].std() / df.groupby('Position')['MaximumMana'].mean()
    df = df.reset_index()
    df.columns = ['Position', 'CoefficientOfVariation']
    df.drop(df[df['Position'] == 'no'].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def covariance_physical_magic_attack():
    """
    Calculate the covariance between 'PhysicalAttack' and 'MagicAttack'.
    Returns the covariance value.
    """
    df = process_position()
    physical_defense = df['PhysicalDefense'].values
    physical_damage_reduction = df['PhysicalDamageReduction'].values
    total_covariance = np.cov(physical_defense, physical_damage_reduction)[0, 1]
    grouped_covariances = df.groupby('Position')[["PhysicalDefense", "PhysicalDamageReduction"]].cov().iloc[0::2,
                          1].reset_index(drop=True)
    result_df = pd.DataFrame({
        'Position': df['Position'].unique(),
        'GroupedCovariances': grouped_covariances.values
    })
    result_df = result_df[result_df['Position'] != 'no']
    result_df.reset_index(drop=True, inplace=True)

    return result_df


def covariance_physical_magic_attack_draw():
    """
        Calculate the covariance between 'PhysicalAttack' and 'MagicAttack' by linear regression.
        Returns the covariance value.
        """
    df = process_position()

    physical_defense = df['PhysicalDefense'].values
    physical_damage_reduction = df['PhysicalDamageReduction'].values

    covariance_value = np.cov(physical_defense, physical_damage_reduction)[0, 1]

    A = np.vstack([physical_defense, np.ones_like(physical_defense)]).T
    m, c = np.linalg.lstsq(A, physical_damage_reduction, rcond=None)[0]

    plt.scatter(physical_defense, physical_damage_reduction, label='Data Points')
    plt.plot(physical_defense, m * physical_defense + c, 'r', label='Linear Regression')

    plt.xlabel('Physical Defense')
    plt.ylabel('Physical Damage Reduction')
    plt.legend()
    plt.show()

    return covariance_value


def correlation_physical_defense_movement_speed():
    """
    Calculate the correlation between 'PhysicalDefense' and 'MovementSpeed'.
    Returns the correlation value.
    """
    return process_position().groupby('Position')[['PhysicalDefense', 'MovementSpeed']].corr().iloc[0, 1]


def chi2_test():
    """
    Perform a chi-square test for independence between 'mainPosition' and 'AttackRange'.
    Returns the chi-square statistic and p-value.
    """
    df = process_position()
    observed_values = dict()
    for _, row in df.iterrows():
        position = row['Position']
        attack_range = row['AttackRange']
        observed_values[(position, attack_range)] = observed_values.get((position, attack_range), 0) + 1

    positions = sorted(set(row[0] for row in observed_values))
    attack_ranges = sorted(set(row[1] for row in observed_values))

    observed_matrix = [[observed_values.get((position, attack_range), 0) for attack_range in attack_ranges] for position
                       in positions]

    row_totals = [sum(row) for row in observed_matrix]
    col_totals = [sum(row[i] for row in observed_matrix) for i in range(len(attack_ranges))]
    total = sum(row_totals)

    expected_matrix = [[(row_total * col_total) / total for col_total in col_totals] for row_total in row_totals]

    chi2_stat = sum(
        (observed_matrix[i][j] - expected_matrix[i][j]) ** 2 / expected_matrix[i][j] for i in range(len(positions)) for
        j in range(len(attack_ranges)))

    degrees_of_freedom = (len(positions) - 1) * (len(attack_ranges) - 1)

    def chi2_cdf(x, df):
        t = 0.5 * x
        s = np.exp(-t)
        cdf = s

        for i in range(1, df // 2):
            t *= x / (2.0 * i)
            s += t
            if s * (1.0 + 1.0 / (df - 2 * i)) >= 1.0:
                break

        return min(s, 1.0)

    p_value = 1 - chi2_cdf(chi2_stat, degrees_of_freedom)

    return chi2_stat, p_value


def t_statistic_damage_reduction():
    """
    Calculate the t-statistic for the difference between 'PhysicalDamageReduction' and 'MagicDamageReduction'.
    Returns the t-statistic value.
    """
    df = process_position()

    sample_physical = df['PhysicalDamageReduction'].dropna().to_numpy()
    sample_magic = df['MagicDamageReduction'].dropna().to_numpy()

    mean_physical = np.mean(sample_physical)
    mean_magic = np.mean(sample_magic)

    std_physical = np.std(sample_physical, ddof=1)
    std_magic = np.std(sample_magic, ddof=1)

    n_physical = len(sample_physical)
    n_magic = len(sample_magic)

    numerator = mean_physical - mean_magic
    denominator = np.sqrt((std_physical**2 / n_physical) + (std_magic**2 / n_magic))
    t_statistic = numerator / denominator

    return t_statistic


def effect_size_max_health():
    """
    Calculate the effect size for the difference in 'MaximumHealth'.
    Returns the effect size value.
    """
    df = process_position()
    df = (df.groupby('Position')['MaximumHealth'].mean() - df.groupby('Position')['MaximumHealth'].min()) / df.groupby('Position')['MaximumHealth'].std()
    df = df.reset_index()
    df.columns = ['Position', 'EffectSize']
    df.drop(df[df['Position'] == 'no'].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def mean_difference_attack_range():
    """
    Calculate the mean difference in 'AttackRange' between 'mainPosition' categories.
    Returns the mean difference value.
    """
    df = process_position()
    df = df.groupby('Position')['AttackRange'].apply(
        lambda x: x.apply(lambda y: 0 if y == 'short' else 1).mean()).diff().iloc[-1]
    return df


def percentage_difference_max_health():
    """
    Calculate the percentage difference in 'MaximumHealth' between 'assassin' and 'tank' categories.
    Returns the percentage difference value.
    """
    return ((data[data['mainPosition'] == 'assassin']['MaximumHealth'].mean() - data[data['mainPosition'] == 'tank'][
        'MaximumHealth'].mean()) / data['MaximumHealth'].mean()) * 100

