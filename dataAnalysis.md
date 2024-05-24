# The Assignment of Python Data Analysis on 8th Dec

## Dataset Analysis

### Dataset Source

The dataset I use is BasedDataforHeroInHonorOfKing.csv with 106 rows and 26 columns. This dataset is crawled from the data analysis website for the game *Honor of Kings*, whose url is https://db.18183.com/wzry/hero/16364.html. The tools I use is spider and the basis request tools provided by *lxml* package. The tools is included in the back-end codes I provide in the zip file. The executing file is placed in the folder dataScrapy named crawlExecution.py. The initial datasets I crawl are stored in the folder 'data' named 'source1.csv' and 'source2.csv'.  

### Data PreProcess

In this project, I crawl two datasets to check the correctness of the datasets. After comparison, I draw the conclusion that the difference in data values between the two data sets is acceptable, but both datasets have problem that missing some values. So I merge two datasets by the heroes' names and transmit it into one table. Based on it, I process the original data table by the following steps.

1. Adapt the 'fillna' function to fill the 'null' or 'NaN' values with '0'.  
2. Adapt the 'xpinyin' package to transmit the Chinese characters into letter form in order to avoid the decodering errors.
3. Adapt the 'split' function to divide the 'HeroType' into two part if the value of 'HeroType' contains two positions.

After the processing, I store the processed data into the .csv file named 'data.csv' in the folder data. Here comes the preprocess source codes that deal with the data table.

```python
import pandas as pd
from xpinyin import Pinyin

# readData
source1 = pd.read_csv("../../static/csv/source1.csv").fillna(0.0)
source2 = pd.read_csv("../../static/csv/source2.csv", sep="\t").fillna(0.0)

# data process
merged_df = pd.merge(source1, source2, how='inner', left_on='name', right_on='HeroName', suffixes=('_x', '_y'))
column_to_exclude = 'position'
columns_except_one = [col for col in source1.columns if col != column_to_exclude]
merged_df = merged_df.drop(columns=columns_except_one, axis=1)


def analyze_and_translate_hero_type(hero_type):
    if '物理' in hero_type:
        return 'Physical'
    elif '魔法' in hero_type:
        return 'Magic'
    else:
        return 'Unknown'


def analyze_and_translate_attack_range(AttackRange):
    if '远程' in AttackRange:
        return 'long'
    elif '近程' in AttackRange:
        return 'short'
    else:
        return 'Unknown'


def chinese_to_pinyin(chinese_str):
    p = Pinyin()
    s = p.get_pinyin(chinese_str).split('-')
    result = ''.join([word.capitalize() for word in s])
    return result


# transmit the Chinese to Pinyin
merged_df['HeroType'] = merged_df['HeroType'].apply(analyze_and_translate_hero_type)
merged_df['AttackRange'] = merged_df['AttackRange'].apply(analyze_and_translate_attack_range)
merged_df["HeroName"] = merged_df["HeroName"].apply(lambda x: chinese_to_pinyin(str(x)) if isinstance(x, str) else x)

# divide the position
merged_df[['mainPosition', 'subPosition']] = merged_df['position'].str.split(',', expand=True)
merged_df.drop(columns=['position'], inplace=True)

# fill the null
merged_df['subPosition'].fillna("no", inplace=True)
merged_df.replace(0, '0/0', regex=True)

# export
merged_df.to_csv("../data/data1.csv", index=False)
```

 Here come the screenshots of the dataset before and after the process.

![image-20231211054316716](./src/dataAnalysis/dataAnalysis_files/process_before1.png)

The datasets before process (The row named '嫦娥' has null values)

![image-20231211061602605](./src/dataAnalysis/dataAnalysis_files/process_before2.png)

The datasets before process (The row named '嫦娥' has '点' in some values)

![image-20231211060448858](./src/dataAnalysis/dataAnalysis_files/process_after.png)

The dataset after process

### Dataset description

The dataset describes the basis data describing the parameters when the heroes in level 1. To better explain the analysis questions and formulas in the following parts, here comes the short descriptions of the column names in the following tables.

| Parameter                | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| HeroName                 | Name of the hero                                       |
| HeroType                 | Type of the hero (Physical or Magic)                   |
| MaximumHealth            | Maximum health points of the hero                      |
| MaximumMana              | Maximum mana points of the hero                        |
| PhysicalAttack           | Physical attack power of the hero                      |
| MagicAttack              | Magical attack power of the hero                       |
| PhysicalDefense          | Physical defense power of the hero                     |
| PhysicalDamageReduction  | Reduction in physical damage inflicted on the hero     |
| MagicDefense             | Magical defense power of the hero                      |
| MagicDamageReduction     | Reduction in magical damage inflicted on the hero      |
| MovementSpeed            | Speed of movement of the hero                          |
| PhysicalArmorPenetration | Penetration of physical armor by the hero              |
| MagicArmorPenetration    | Penetration of magical armor by the hero               |
| AttackSpeedBonus         | Bonus to attack speed of the hero                      |
| CriticalStrikeRate       | Rate of critical strikes by the hero                   |
| CriticalStrikeDamage     | Damage multiplier for critical strikes by the hero     |
| PhysicalLifeSteal        | Life steal for physical damage by the hero             |
| MagicLifeSteal           | Life steal for magical damage by the hero              |
| CooldownReduction        | Reduction in cooldown time for abilities by the hero   |
| AttackRange              | Range of attack for the hero                           |
| Tenacity                 | Resistance to crowd control effects by the hero        |
| HealthRegeneration       | Rate of health regeneration for the hero               |
| ManaRegeneration         | Rate of mana regeneration for the hero                 |
| mainPosition             | Main position or role of the hero in the game          |
| subPosition              | Sub position or secondary role of the hero in the game |

Because these values describe the basis data of the heroes when they are in level 1, the columns like PhysicalArmorPenetration, AttackSpeedBonus and so on are with the value 0.0. So my data analysis will concentrate on the value like MaxMumHealth with meaningful numbers.

##<center>Basis Part: Data Analysis & Description</center>

Based on the data table I generate in the previous part, I will analysis the data to mine the valuable data by using 'numpy' package and 'pandas' package. I will introduce the 20 questions and the solutions of the corresponding questions one by one.

1.  **Read the data from the .csv file and define the shared function to process the data**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("../data/data.csv")
```


```python
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
```

When playing the game, the players might use the heroes with 'fighter' position to take responsibility to 'mage' (for example, ChangE), that is why there appear the mainPosition and subPosition. Based on this theory, I will count this hero in two positions when calculate the data in different positions. The function named process_position is used for generating the tables I need when  finishing the above operation.

2. **Count the numbers of the heroes in different positions**

In this question, I want to count the numbers of the heroes in different positions and acquire the percentage of them. Based on the descriptions, I can adapt the 'groupby' to generate the tables only contains the heroes that belongs to corresponding positions, then I use 'value_count' to count the distinguishing values( the name of heroes) to count the number of the heroes that belong to this positions. As there are some heroes only belong to one position, so I use 'no' to fill up their 'subPosition', which should not be counted when calculating, that is why I need to drop the columns named 'no' after counting the heroes.  

```python
# Count the number of heroes for each 'Position' and print the result.
df = process_position()
position_count = df['Position'].value_counts().drop('no')
position_count = position_count.reset_index()
position_count.columns = ['Position', 'Count']
print(position_count)

plt.pie(position_count['Count'], labels=position_count['Position'], autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Heroes Across Positions')
plt.show()
```
       Position  Count
    0   fighter     35
    1      tank     30
    2      mage     30
    3  assassin     17
    4   support     14
    5  marksman     14

![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_2_1.png)
    Based on the result I get, the fighter and the tank occupy important positions in the composition of heroes in *Honor of King*, which shows the love from the players might focus on the tank and the fighter. It might be the developing policy in next generation of *Honor of King*.  

3. **Calculate the minimum and maximum of health points in different positions**

In this question, I want to acquire the minimum and maximum of the health points and know the distributions of the health points in different positions. In this question, I introduce another method to acquire the data. I use 'groupby' function first to generate the tables to see the minimum and maximum in main positions and sub positions. After that, I use lambda expression to compare the minimums in main positions and sub positions of the corresponding tables and acquire the final minimum and maximum. 

To know the distributions of the health points in different positions, I introduce the boxplot to display it. It analyses the quantiles of whole dataset and acquires the distributions of the data based on Gauss distributions Analysis.

```python
#Calculate the minimum and maximum health for each 'mainPosition' and 'subPosition'.
#Returns the resulting DataFrame.
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
print(merged_stats)

plt.subplot(1,1,1)
x_data = []
x_name = []
x1 = process_position()[process_position()['Position'] != 'no']
x1 = x1.groupby('Position')
for name, group in x1:
    x_data.append(np.array(group['MaximumHealth']))
    x_name.append(name)
plt.boxplot(x_data,labels=x_name,vert=True)
plt.title("Boxplot of Min and Max Values for Positions",loc="center")
plt.grid(visible=False)
plt.show()
```

       position     min     max
    0  assassin  2886.0  3483.0
    1   fighter  2862.0  3622.0
    2      mage  1600.0  3323.0
    3  marksman  2977.0  3401.0
    4   support  2958.0  3450.0
    5      tank   946.0  3622.0



![png](.\src\dataAnalysis\dataAnalysis_files/dataAnalysis_3_1.png)
    The result shows that the health points in fighter and so on is fair. But the health points of assassins are a little bit low because there are some exception points in assassins. But based on the attack powers of assassins(this will show in the following part), this design is fair in *Honor of King*.

4. **Calculate the average health for each position**

In this question, I try to discover the difference between different positions by the average health points in different positions. So I use 'groupby' function to generate the tables that contain the heroes belong to different positions. Based on them, I can use 'mean' function to get the average value of them. To better display the distance, I use bar chart to display the result.   

```python
# Calculate the average health for each 'Position' (combining 'mainPosition' and 'subPosition').
# Returns the resulting DataFrame.
df = process_position()
average_health_position = df.groupby("Position")["MaximumHealth"].mean().reset_index()
average_health_position.columns = ["Position", "AverageHealth"]
average_health_position = average_health_position[average_health_position['Position'] != 'no']
average_health_position.reset_index(drop=True, inplace=True)
print(average_health_position)

sns.barplot(x='Position', y='AverageHealth', data=average_health_position)
plt.title('Average Health for Each Position')
plt.xlabel('Position')
plt.ylabel('Average Health')
plt.show()
```
       Position  AverageHealth
    0  assassin    3208.882353
    1   fighter    3238.228571
    2      mage    3051.400000
    3  marksman    3149.857143
    4   support    3200.785714
    5      tank    3169.066667



![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_4_1.png)
    Based on this result, I draw the conclusion that the average health points can not show the distances between different positions completely cause they are almost same. To distinguishing different positions, we need to consider more parameters like attack powers and so on.

5. **Calculate the average moving speed for each Position**

In this question, I want to complete the comparison between different positions based on the difference on moving speed. To acquire the corresponding result, I generate the tables as before by 'groupby' function and use 'mean' function to get the average of the moving speeds of different positions.  For the same reason as the previous question, I adapt the bar chart to display the final result.

```python
 # Calculate the average moving speed for each 'Position' (combining 'mainPosition' and 'subPosition').
 # Returns the resulting DataFrame.
df = process_position()
average_speed_position = df.groupby("Position")["MovementSpeed"].mean().reset_index()
average_speed_position.columns = ["Position", "MovementSpeed"]
average_speed_position = average_speed_position[average_speed_position['Position'] != 'no']
average_speed_position.reset_index(drop=True, inplace=True)
print(average_speed_position)

sns.barplot(x='MovementSpeed', y='Position', data=average_speed_position, orient='h')
plt.title('Average Speed for Each Position')
plt.xlabel('Average Movement Speed')
plt.ylabel('Position')
plt.show()
```
       Position  MovementSpeed
    0  assassin     380.000000
    1   fighter     379.714286
    2      mage     368.900000
    3  marksman     354.285714
    4   support     372.857143
    5      tank     388.833333



![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_5_1.png)
    The result displays the difference between different positions. The average moving speed of markman is the lowest one among the six positions, which means that the characters can carry the whole competitions should be decrease to reduce impact of the competitions.

6. **calculate the heroes with highest speed for each Position**

This question is design for the same target as the previous question. In my point of view, the highest moving speeds can let the players know the heroes who can run away from the danger first. To get the corresponding result, use 'groupby' function to get the specific tables that contains the heroes belonging to this position. I use radio chart to display the result to show the clear distance between the fastest heroes in different positions. 

```python
# calculate the average speed for each 'Position'
# Return the resulting DataFrame.
df = process_position()
fastest_heroes = df.sort_values("MovementSpeed", ascending=False).groupby("Position").head(1)[
    ["Position", "HeroName", "MovementSpeed"]]
fastest_heroes.drop(fastest_heroes[fastest_heroes['Position'] == 'no'].index, inplace=True)
fastest_heroes.reset_index(drop=True, inplace=True)
print(fastest_heroes)

labels = fastest_heroes['Position']
x_data = fastest_heroes['MovementSpeed']
x_data=np.concatenate((x_data, [x_data[0]]))
angles=np.concatenate((labels, [labels[0]]))
plt.polar(angles,x_data,color='r',marker="o")
plt.title("The fastest Moving Speed in each Position")
```
       Position      HeroName  MovementSpeed
    0   support       DunShan            530
    1      tank        MengQi            530
    2      mage        MengQi            530
    3   fighter     YaDianNuo            410
    4  assassin   LanLingWang            400
    5  marksman  ChengJiSiHan            370


![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_6_2.png)
​    

The radio chart shows that the assassin, markman, fighter have close highest moving speeds (the hero named 'MengQi' should be recognized as the fighter rather than mage in this game version), but support and tank possess greater highest moving speeds, which can promises the supporting speed among the game. It is fair.

7. **Calculate the median physical and magic damage reduction for each Position**

In this question, I want to know the distributions of the physical and magic damage reduction in each positions to see which kind of the positions possess the highest attack power. So I generate the position tables by the 'groupby' function and acquire the median of different tables by the 'median' function. In this question, I adapt the stackplot to display the result to show the tends of the reduction changes between different positions.

```python
# Calculate the median physical and magic damage reduction for each 'Position'.
# Return the resulting DataFrame.
df = process_position()
mode_attack_both = df.groupby("Position")[
    ["PhysicalDamageReduction", "MagicDamageReduction"]].median().reset_index()
mode_attack_both.columns = ["Position", "PhysicalDamageReduction", "MagicDamageReduction"]
mode_attack_both = mode_attack_both[mode_attack_both['Position'] != 'no']
mode_attack_both.reset_index(drop=True, inplace=True)
print(mode_attack_both)

plt.subplot(1,1,1)

x = np.array(mode_attack_both['Position'])
y1=np.array(mode_attack_both['MagicDamageReduction'])
y2=np.array(mode_attack_both['PhysicalDamageReduction'] - mode_attack_both['MagicDamageReduction'])

labels = ['PhysicalDamageReduction','MagicDamageReduction']
plt.stackplot(x,y1,y2,labels=labels)

plt.title("Median Physical Damage Reduction for Each Position",loc="center")
plt.xlabel("Position")
plt.ylabel('PhysicalDamageReduction & MagicDamageReduction')
plt.legend()
plt.show()
```
       Position  PhysicalDamageReduction  MagicDamageReduction
    0  assassin                     12.9                   7.6
    1   fighter                     14.1                   7.6
    2      mage                     13.0                   7.6
    3  marksman                     12.8                   7.6
    4   support                     13.7                   7.6
    5      tank                     14.3                   7.6

![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_7_1.png)
    The result show that the tank and the fighter possess the highest Physical Damage Reduction, which is fair because they are the characters who bear the most damage among six positions. But it is unfair to set the initial Magic Damage Reduction among six positions cause different position will receive different types of the damages, which requires the Magic Damage Reduction should be in different levels in different positions. 

8. **Calculate the kurtosis of the Maximum Health for each Position and the overall kurtosis**

This part I consider the fairness among different positions. The kurtosis can shows the data concentration among the dataset,which can shows that if the data distribute surround a specific value. To get the kurtosis in different positions, I use the 'groupby' function to acquire the  tables that contains the corresponding heroes. Based on them, I define a function named 'calculate_kurtosis' because the dataframe can not calculate the kurtosis directly. Here I use internal function named 'apply' to apply the self-define function to single column or row of the dataframe. With the help of the self-define function, I can calculate the kurtosis and get the final result.  

```python
 # Calculate the kurtosis of the 'MaximumHealth' for each 'Position' and the overall kurtosis.
 # Return the resulting kurtosis values.
 
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
print(max_health_kurtosis_by_position)

sns.barplot(x='Position', y='Kurtosis', data=max_health_kurtosis_by_position, palette='viridis')
plt.title('Kurtosis of Maximum Health for Each Position')
plt.xlabel('Position')
plt.ylabel('Kurtosis')
plt.show()
```

       Position   Kurtosis
    0  assassin   0.160075
    1   fighter  -0.546453
    2      mage  22.205071
    3  marksman   0.003690
    4   support  -0.842863
    5      tank  10.287253
    6       all  27.662755



![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_8_2.png)
    The values of the kurtosis shows the distances between the real distributions of values in dataset and the standard Gauss distribution. So the distributions of max health points of the assassin, fighter and markman are close to the Gauss distribution, but the mage and the tank appear great offset to the Gauss distribution, which refers to the unfair design in these positions heroes. 

9. **Find the maximum mana for each Position and the overall maximum mana**

The goal to design this question is to check the different between the maximum of the magic attack power between different positions. To get this result, I use 'groupby' to generate the specific data tables and use the 'max' function to get the maximum.  To better compare the data in single position and the whole data, I introduce the maximum magic attack power named 'all' in the point chart.

```python
# Find the maximum mana for each 'Position' and the overall maximum mana.
# Return the resulting values.
df = process_position()
max_mana_by_position = df.groupby("Position")["MaximumMana"].max().reset_index()
max_mana_by_position.drop(max_mana_by_position[max_mana_by_position['Position'] == 'no'].index, inplace=True)
max_mana_by_position.columns = ["Position", "MaximumMana"]
max_mana_by_position.reset_index(drop=True, inplace=True)
max_mana_all = data["MaximumMana"].max()

all_row = pd.DataFrame({"Position": ["all"], "MaximumMana": [max_mana_all]})
max_mana_by_position = pd.concat([max_mana_by_position, all_row], ignore_index=True)
print(max_mana_by_position)

sns.pointplot(x='Position', y='MaximumMana', data=max_mana_by_position, color='blue', linestyles='dashdot')
plt.title('Maximum Mana for Each Position')
plt.xlabel('Position')
plt.ylabel('Maximum Mana')
for a,b in zip(max_mana_by_position['Position'],max_mana_by_position['MaximumMana']):
    plt.text(a,b,b,ha="center",va="bottom",fontsize=10)
plt.show()
```

       Position  MaximumMana
    0  assassin          490
    1   fighter          490
    2      mage          490
    3  marksman          490
    4   support          490
    5      tank          490
    6       all          490



![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_9_1.png)
    The result shows a reticular fact: all the positions acquire the same highest maximum magic attack power. For the same reason (different positions show use different levels and types attack to keep the balance of the game), this value should be various in different positions. But considering the growing of the heroes, I can accept this design partly. (To simple the basis data design)  

10. **Calculate the correlation between Maximum Health and Health Regeneration**

This analysis delves into the correlation between maximum health points and health regeneration across different hero positions in the game "Honor of Kings." Utilizing the 'groupby' function, I organized the data and calculated correlation matrices for each position. The resulting DataFrame, named ‘correlation_matrix_by_position', showcases correlation strength and direction. An aggregate row labeled "all" provides an overall correlation across positions. After data refinement, correlation values are rounded to two decimal places for clarity. The scatter plot visually depicts these correlations for each position, aiding in a succinct interpretation of health attribute patterns in the game. This analytical approach sheds light on the intricate relationships between health-related attributes, offering insights for strategic gameplay considerations.

```python
# Calculate the correlation between 'MaximumHealth' and 'HealthRegeneration'.
# Print the resulting correlation.
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

print(correlation_matrix_by_position)


correlation_matrix_by_position['Relative'] = np.round(correlation_matrix_by_position['Relative'], 2) 
sns.scatterplot(y='Relative', x='Position', data=correlation_matrix_by_position, color='blue')
plt.title('Correlations for Each Position')
plt.xlabel('Position')
plt.ylabel('Relative')

for a,b in zip(np.array(correlation_matrix_by_position['Position']),np.array(correlation_matrix_by_position['Relative'])):
    plt.text(a,b,b,ha="center",va="bottom",fontsize=10)
plt.show()
```

       Position  Relative
    0  assassin  0.283657
    1   fighter  0.052049
    2      mage  0.061957
    3  marksman  0.163065
    4   support  0.561379
    5      tank  0.214219
    6       all  0.197600

![image-20231211083701186](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_10_1.png)
    The result shows that the relation between the Maximum Health and Health Regeneration are almost same. But their is a exception: the support. This design might concerning the function of the support is the protect the  markman or the mage, which requires the higher health regeneration to satisfy the corresponding goal.

11. Calculate the covariance matrix of Maximum Magic Attack Power and Magic Regeneration

This question is design to test whether the Maximum Magic Attack Power and Magic Regeneration have relationship. As we all know, the attributes will always link to the regeneration attributes with the same attributes. As the 'numpy' package has the function 'cov' to calculate the covariance between two arrays with same dimensions, so I use this function to calculate the covariance. Because the covariance matrix can display the result directly, I use no graphic to display it.

```python
# Calculate the covariance matrix of 'MaximumHealth' and 'HealthRegeneration'.
#     Return the resulting covariance matrix.
covariance = data[['MaximumMana', 'ManaRegeneration']].cov()
covariance
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MaximumMana</th>
      <th>ManaRegeneration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>MaximumMana</th>
      <td>39657.708895</td>
      <td>954.716981</td>
    </tr>
    <tr>
      <th>ManaRegeneration</th>
      <td>954.716981</td>
      <td>89.593890</td>
    </tr>
  </tbody>
</table>
This matrix depicts the correlations between hero attributes. The correlation coefficient between Maximum Mana and Mana Regeneration is 39657.71, indicating a significant positive correlation. The self-correlation of Mana Regeneration is 89.59, relatively weaker compared to its correlation with Maximum Mana. These findings offer insights into the relationships among hero attributes, particularly concerning mana-related aspects.

12. **Calculate the median absolute deviation of Physical Attack for each Position**

This code aims to reveal the variability of heroes in terms of physical attack by calculating the Median Absolute Deviation (MAD) of 'Physical Attack' for each 'Position'. Firstly, the hero's position data is processed to ensure data integrity. Then, a custom function, 'calculate_mad', is employed to compute the MAD of physical attack for heroes at each position. Finally, the resulting MAD values are visualized using a scatter plot, illustrating the distribution of physical attack MAD across different positions.


```python
# Calculate the median absolute deviation of 'PhysicalAttack' for each 'Position'.
# Return the resulting DataFrame.
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
print(mad_by_position)

plt.subplot(1,1,1)

x=np.array(mad_by_position['Position'])
y=np.array(mad_by_position['MAD_PhysicalAttack'])

colors = y*10 - 20
area = y*100
plt.scatter(x,y,c=colors,marker="o",s=area)

plt.title("Correlation between Maximum Health and Health Regeneration for Each Position",loc="center")

for a,b in zip(x,y):
    plt.text(a,b,b,ha="center",va="center",fontsize=10,color="white")

plt.xlabel("Position")
plt.ylabel("MAD_PhysicalAttack")
# plt.grid(b=False)
```

       Position  MAD_PhysicalAttack
    0  assassin                 3.0
    1   fighter                 5.0
    2      mage                 5.0
    3  marksman                 7.5
    4   support                 6.5
    5      tank                 7.5


![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_12_2.png)
    The provided data presents the Median Absolute Deviation (MAD) of 'PhysicalAttack' for heroes in different positions. MAD measures the dispersion of individual data points from the median, providing insights into the variability of physical attack within each position. Analyzing the MAD values across positions reveals how consistent or varied the physical attack values are for different hero roles. In the presented results, 'marksman,' 'support,' and 'tank' positions exhibit higher MAD values, suggesting greater variability in physical attack among heroes in these roles. This analysis aids in understanding the diversity of physical attack strengths within distinct hero positions in the game.

13. **Calculate the mode of Movement Speed**

The purpose of the provided code is to calculate the mode of the 'MovementSpeed' attribute for heroes in different positions. The 'custom_mode' function is defined to handle the calculation of the mode, considering cases where there might be no mode (empty series). The 'process_position' function retrieves the dataset, and the main calculation is performed within the 'groupby' operation. The implementation strategy involves grouping the dataset by the 'Position' column and applying the 'custom_mode' function to the 'MovementSpeed' values within each group. The resulting dataFrame, 'mode_by_group,' contains the calculated mode of 'MovementSpeed' for each hero position. The 'drop' method is then used to remove rows where the 'Position' is 'no,' and the dataFrame is structured with columns 'Position' and 'Mode_MovementSpeed.'

```python
# Calculate the mode of 'MovementSpeed'.
# Returns the mode value(s).
def custom_mode(series):
    return series.mode().iloc[0] if not series.mode().empty else None

df = process_position()
mode_by_group = df.groupby('Position')['MovementSpeed'].apply(custom_mode).reset_index()
mode_by_group.drop(mode_by_group[mode_by_group['Position'] == 'no'].index, inplace=True)
mode_by_group.columns = ['Position', 'Mode_MovementSpeed']
mode_by_group.reset_index(drop=True, inplace=True)
mode_by_group
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Position</th>
      <th>Mode_MovementSpeed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>assassin</td>
      <td>380</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fighter</td>
      <td>380</td>
    </tr>
    <tr>
      <th>2</th>
      <td>mage</td>
      <td>350</td>
    </tr>
    <tr>
      <th>3</th>
      <td>marksman</td>
      <td>350</td>
    </tr>
    <tr>
      <th>4</th>
      <td>support</td>
      <td>360</td>
    </tr>
    <tr>
      <th>5</th>
      <td>tank</td>
      <td>380</td>
    </tr>
  </tbody>
</table>
The data displays the mode of 'MovementSpeed' for heroes in different positions. Notably, assassins and fighters share a mode of 380, mages and marksmen have a mode of 350, while supports prefer 360. Tanks align with assassins and fighters, having a mode of 380. The information highlights distinct movement speed preferences across hero positions.

14. **Calculate the skewness of AttackRange of each Position**

The purpose of this code is to calculate the skewness values of the 'AttackRange' for each 'Position' and visualize the skewness comparison between short and long attack ranges in different professions. Firstly, the values of 'AttackRange' are processed by transforming 'short' and 'long' into 0 and 1, respectively. Then, the 'groupby' function is used to group the data by 'Position' and 'AttackRange', calculating the skewness values for each profession's attack range. The processed results are organized into a table where 'Position' represents the profession, and 'short' and 'long' represent the skewness values for short and long attack ranges. Finally, a point plot is created with professions on the x-axis, skewness on the y-axis, and different colors indicating short and long attack ranges, providing a visual comparison of skewness differences. The overall implementation involves data cleaning, group-based skewness calculation, result organization, and visualization.


```python
# Calculate the skewness of 'AttackRange' of each 'Position'.
# Returns the skewness value.
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
print(skewness_table)

skewness_table_long = skewness_table.melt(id_vars='Position', var_name='AttackRange', value_name='Skewness')

# Plot the bar graph
sns.pointplot(x='Position', y='Skewness', hue='AttackRange', data=skewness_table_long)

plt.xlabel('Position')
plt.ylabel('Skewness')
plt.title('Skewness of Attack Range by Position')
plt.legend(title='Attack Range')
plt.show()
```

       Position  short  long
    0  assassin    0.0   0.0
    1   fighter    0.0   0.0
    2      mage    0.0   0.0
    3  marksman    0.0   0.0
    4   support    0.0   0.0
    5      tank    0.0   0.0

![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_14_1.png)
    The data analysis reveals that for each position, both short and long attack ranges exhibit zero skewness. This indicates a symmetric distribution in the attack range data for all professions, suggesting that the majority of heroes within each category have similar characteristics in terms of attack range. The skewness values of 0.0 imply that the data distribution is centered and balanced, without a significant tail on either side. Overall, the results suggest uniformity in the attack range distribution across different positions, with no apparent skewness towards short or long attack ranges.

15. **Calculate the coefficient of variation for Maximum Mana of each Position**

The purpose of this code is to calculate and visualize the coefficient of variation for the 'MaximumMana' attribute across various hero positions. It processes the data, computes the coefficient of variation, creates a dataFrame, cleans the data, and generates a scatter plot to depict the variability of 'MaximumMana' relative to the mean across different hero positions.

```python
# Calculate the coefficient of variation for 'MaximumMana' of each 'Position'.
# Returns the coefficient of variation value for each 'Position'.
df = process_position()
df = df.groupby('Position')['MaximumMana'].std() / df.groupby('Position')['MaximumMana'].mean()
df = df.reset_index()
df.columns = ['Position', 'CoefficientOfVariation']
df.drop(df[df['Position'] == 'no'].index, inplace=True)
df.reset_index(drop=True, inplace=True)
print(df)

plt.subplot(1,1,1)

x=np.array(df['Position'])
y=np.array(np.round(df['CoefficientOfVariation'], 2))

colors = y*10 - 20
area = y*1000
plt.scatter(x,y,c=colors,marker="o",s=area)

plt.title("Coefficient of MaximumMana for Each Position",loc="center")

for a,b in zip(x,y):
    plt.text(a,b,b,ha="center",va="center",fontsize=10,color="white")

plt.xlabel("Position")
plt.ylabel("CoefficientOfVariation")
```

       Position  CoefficientOfVariation
    0  assassin                0.695338
    1   fighter                1.018233
    2      mage                0.237354
    3  marksman                0.372277
    4   support                0.313917
    5      tank                0.728669


![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_15_2.png)
    The provided data displays the coefficient of variation for the 'MaximumMana' attribute across distinct hero positions. This statistical measure assesses the relative variability of 'MaximumMana' concerning its mean. The values indicate the degree of dispersion within each position. The coefficients range from approximately 0.24 to 1.02, suggesting varying levels of dispersion across hero categories. Specifically, 'fighter' exhibits the highest variation, exceeding 1, while 'mage' shows the lowest variability with a coefficient around 0.24. Overall, the coefficients provide insights into the diversity of 'MaximumMana' within different hero positions in the analyzed dataset.

16. **Calculate the covariance between Physical Attack and Magic Attack**

The purpose of the provided code is to calculate the covariances between 'PhysicalDefense' and 'PhysicalDamageReduction' for heroes in different positions ('Position'). This is achieved by utilizing NumPy's `np.cov` function to calculate the overall covariance and then applying `groupby` to compute the covariances for each position. The resulting covariances are stored in a DataFrame named `result_df`. Finally, a Seaborn bar plot is generated to visually represent the covariances between 'PhysicalDefense' and 'PhysicalDamageReduction' for each position. The code aims to provide insights into the relationships between these two attributes across different hero positions.

```python
# Calculate the covariance between 'PhysicalAttack' and 'MagicAttack'.
# Returns the covariance value.
df = process_position()
physical_defense = df['PhysicalDefense'].values
physical_damage_reduction = df['PhysicalDamageReduction'].values
total_covariance = np.cov(physical_defense, physical_damage_reduction)[0, 1]
grouped_covariances = df.groupby('Position')[["PhysicalDefense", "PhysicalDamageReduction"]].cov().iloc[0::2,
                      1].reset_index(drop=True)
result_df = pd.DataFrame({
    'Position': df['Position'].unique(),
    'Covariances': grouped_covariances.values
})
result_df = result_df[result_df['Position'] != 'no']
result_df.reset_index(drop=True, inplace=True)
print(result_df)

sns.barplot(x='Position', y='Covariances', data=result_df, palette='viridis')
plt.title('Covariances between PhysicalDefense & PhysicalDamageReduction for Each Position')
plt.xlabel('Position')
plt.ylabel('Covariances')
plt.show()
```

       Position  Covariances
    0   fighter     3.290809
    1      tank     4.714713
    2      mage     1.506593
    3   support    15.702347
    4  assassin    40.784615
    5  marksman    39.853563


![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_16_2.png)
    

17. **Calculate the covariance between Physical Attack and Magic Attack by linear regression**

```python
# Calculate the covariance between 'PhysicalAttack' and 'MagicAttack' by linear regression.
# Returns the covariance value.
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

covariance_value
```

![png](./src/dataAnalysis/dataAnalysis_files/dataAnalysis_17_0.png)
​

    18.94738442278458

The 18.94738442278458 corresponds to the covariances between 'PhysicalDefense' and 'PhysicalDamageReduction' for a specific hero position. This value represents the degree of linear association or correlation between these two attributes for heroes belonging to that particular position. In the context of the code, this covariance value is part of the DataFrame result_df and contributes to the Seaborn bar plot. The bar plot visually displays the covariances for each hero position, providing a comparative view of the relationships between 'PhysicalDefense' and 'PhysicalDamageReduction' across different positions. The higher the covariance, the stronger the linear relationship between the two attributes, and vice versa.

18. **Calculate the correlation between Physical Defense and Movement Speed**

The question aims to determine the correlation between 'PhysicalDefense' and 'MovementSpeed' for heroes based on their respective positions. The implemented logic involves obtaining a DataFrame of hero data through the ‘process_position’ function, grouping the data by hero position, and calculating the correlation matrix between the specified attributes within each group. The resulting correlation values indicate the strength and direction of the linear relationship between physical defense and movement speed for heroes in different positions. This analysis helps unveil potential patterns or associations in the data, shedding light on the interplay between these attributes across various hero roles.


```python
 # Calculate the correlation between 'PhysicalDefense' and 'MovementSpeed'.
 #    Returns the correlation value.
process_position().groupby('Position')[['PhysicalDefense', 'MovementSpeed']].corr().iloc[0, 1]
```


    0.024336227130506424

The correlation coefficient between 'PhysicalDefense' and 'MovementSpeed' is approximately 0.0243. This indicates a very weak positive linear relationship, suggesting that changes in physical defense are not strongly associated with changes in movement speed for the analyzed positions.

19. **Perform a chi-square test for independence between main Position and Attack Range**


```python
 # Perform a chi-square test for independence between 'mainPosition' and 'AttackRange'.
 # Returns the chi-square statistic and p-value.
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

chi2_stat, p_value
```


    (86.13169619813307, 0.0)

20. **Calculate the t-statistic for the difference between Physical Damage Reduction and Magic Damage Reduction**

The code performs a chi-square test to assess the independence between 'mainPosition' and 'AttackRange.' It calculates observed and expected frequencies, computes the chi-square statistic, and determines the p-value. This helps evaluate whether there's a significant association between the two categorical variables.


```python
# Calculate the t-statistic for the difference between 'PhysicalDamageReduction' and 'MagicDamageReduction'.
# Returns the t-statistic value.
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

t_statistic

```


    52.43056837851716

The value 52.43056837851716 is the chi-square statistic obtained from performing a chi-square test for independence between the 'mainPosition' and 'AttackRange' variables. In statistical terms, the chi-square statistic measures the discrepancy between the observed and expected frequencies in a contingency table.

21. **Calculate the effect size for the difference in Maximum Health**

The code calculates the effect size for the difference in 'MaximumHealth' across different positions. Effect size indicates the practical significance of observed differences. It involves computing the mean, minimum, and standard deviation of 'MaximumHealth' for each position group. The effect size is then calculated using (mean - min) / std. The result is a DataFrame with effect sizes for each position, excluding 'no'. This provides insights into the practical significance of health differences among positions.


```python
# Calculate the effect size for the difference in 'MaximumHealth'.
# Returns the effect size value.
df = process_position()
df = (df.groupby('Position')['MaximumHealth'].mean() - df.groupby('Position')['MaximumHealth'].min()) / df.groupby('Position')['MaximumHealth'].std()
df = df.reset_index()
df.columns = ['Position', 'EffectSize']
df.drop(df[df['Position'] == 'no'].index, inplace=True)
df.reset_index(drop=True, inplace=True)
df
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Position</th>
      <th>EffectSize</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>assassin</td>
      <td>2.080381</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fighter</td>
      <td>1.931060</td>
    </tr>
    <tr>
      <th>2</th>
      <td>mage</td>
      <td>4.950004</td>
    </tr>
    <tr>
      <th>3</th>
      <td>marksman</td>
      <td>1.471812</td>
    </tr>
    <tr>
      <th>4</th>
      <td>support</td>
      <td>1.492000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>tank</td>
      <td>3.999410</td>
    </tr>
  </tbody>
</table>
The effect size data, such as 2.08 for the assassin, 1.93 for the fighter, 4.95 for the mage, 1.47 for the marksman, 1.49 for the support, and 3.99 for the tank, indicates significant differences in 'MaximumHealth' among various in-game roles. This suggests varying levels of survivability, influencing the game dynamics. Game designers can leverage this information to fine-tune the balance between different roles, ensuring each class has distinctive strengths and contributing to an enhanced overall gaming experience. Analyzing these effect sizes helps the design team understand the nuances in survivability among different roles, facilitating more precise adjustments for a well-balanced and enjoyable game.

22. **Calculate the mean difference in Attack Range**

This code calculates the mean difference in 'AttackRange' between 'mainPosition' categories. It first processes the dataset using the process_position() function. Then, it groups the data by the 'Position' column and applies a lambda function to calculate the mean difference in 'AttackRange' for each group. The lambda function converts 'short' to 0 and 'long' to 1 before calculating the mean. Finally, it computes the difference between consecutive values and extracts the last element using `iloc[-1]`. The result, stored in the variable 'df', represents the mean difference in 'AttackRange' between the 'mainPosition' categories.


```python
 # Calculate the mean difference in 'AttackRange' between 'mainPosition' categories.
 # Returns the mean difference value.
df = process_position()
df = df.groupby('Position')['AttackRange'].apply(
    lambda x: x.apply(lambda y: 0 if y == 'short' else 1).mean()).diff().iloc[-1]
df
```


    -0.4380952380952381

The value -0.438 indicates a mean decrease in 'AttackRange' between different 'mainPosition' categories. This suggests that, on average, certain positions tend to have shorter attack ranges compared to others in the game. Game designers could leverage this information to balance character roles, diversify gameplay mechanics, or enhance strategic elements within the game.

23. **Calculate the percentage difference in Maximum Health between assassin and tank categories**

The code aims to calculate the percentage difference in 'MaximumHealth' between the 'assassin' and 'tank' categories. The implementation logic involves extracting the mean 'MaximumHealth' for both 'assassin' and 'tank' main positions and then computing the percentage difference relative to the overall mean 'MaximumHealth'. This value provides insights into the relative health strength between assassins and tanks, aiding game designers in balancing character attributes and enhancing gameplay dynamics.


```python
 # Calculate the percentage difference in 'MaximumHealth' between 'assassin' and 'tank' categories.
 # Returns the percentage difference value.
((data[data['mainPosition'] == 'assassin']['MaximumHealth'].mean() - data[data['mainPosition'] == 'tank'][
        'MaximumHealth'].mean()) / data['MaximumHealth'].mean()) * 100
```


    3.2717410906266085

The result of 3.27% indicates the percentage difference in the mean 'MaximumHealth' between the 'assassin' and 'tank' main positions. This implies that, on average, assassins have approximately 3.27% higher 'MaximumHealth' compared to tanks in the game. The positive value suggests that, in terms of health points, assassins are slightly favored or stronger than tanks. Game designers may interpret this information to adjust or balance character attributes for better gameplay experience and fairness between different main positions.

## <center>Expanded Part: PythonWeb & data visualization</center>

In this project, I create a python website based on the Flask, mySQL and echarts to visualize the data I analysis in the previous part. To achieve this goal, I create a data centralized screen based on the data. Here comes the detail descriptions of the website. Moreover, as the project contains external packages functions, so please execute the following command after opening the project to install the required external packages.

```shell
pip install -r requirements.txt 
```

(The source codes is attached in the uploaded zip file) 

### Database operation

To satisfy the requirements that the project need to be deployed and tested in different platform, I implement this project based on MySQL database. Moreover, concerning the correctness of the data, I also provide the data in .csv form attached with the source codes I upload. Here comes the detail descriptions of them.

#### The .csv file

According to the requirements, I store the data I use in this project in .csv file inside the uploaded folder. There are three .csv file in the same folder named 'data.csv', 'source1.csv', 'source2.csv'. The main data source I use in the project is the 'data.csv' file, the file named 'source1.csv' and 'source2.csv' is the file that store the crawled result when I crawl the data. The data stored in the 'source1.csv' and 'source2.csv' are not be cleared, so the data can not be used in the whole project.

![image-20231212174208576](.\src\dataAnalysis\dataAnalysis_files\directotyStructure.png) 

 #### The database

To correct the correctness of the data and simplify the local operations, I set the .sql file together with the upload file. Moreover, The data source is also uploaded to the online Aliyun server, so if the project is only for testing or viewing, threre is no need to create the database locally, all the operations concerning the database are set to operated on online server.

#### The data operation

 I implement the data operation codes in the dataStore/dao.py file. Here comes the code of it.

```python
# dao.py
import pandas as pd
from sqlalchemy import create_engine
TABLE_NAME = 'heroes'

engine = create_engine('mysql+pymysql://root:Root123456@rm-cn-4xl3gmscg000cxpo.rwlb.rds.aliyuncs.com/python_db')


def read_from_db(name):
    df = None
    try:
        query = "SELECT * FROM " + name
        df = pd.read_sql(query, engine)
    except Exception as e:
        print("Error")
    return df


def read_from_csv(path):
    df = pd.read_csv(path)
    return df


def save_to_db(df, name):
    try:
        df.to_sql(name, engine, if_exists='replace')
    except Exception as e:
        print("Error")


def save_to_csv(df, path):
    df.to_csv(path, index=False)
```

Here I provide two possible ways to acquire the data. When acquiring or saving the data on database, I open the connection to the database first, then use the internal function 'read_sql' in pandas package to execute the query sentence and read the data to the prepared dataFrame. The pandas packages also provides the function 'read_csv' to read the data form the .csv file to the dataFrame.

### Website Implementation

As the website implementation is too complex to describe it in detail, so I will only introduce some key operations and implementations in this part to display the process to implement the Website.

#### Data process

I want to use the echarts tools to visualize the data, so I need to process the data to dig out the expected and valuable data and pass it from back-end to front-end. Here come the details to acquire the data from the source data.

1.  Get minimum and maximum speed in each positions

The purpose of the code is to identify the fastest and slowest heroes in terms of 'MovementSpeed' for each 'Position' in the game dataset. The implementation involves sorting the dataset based on 'MovementSpeed' in ascending and descending order separately, then extracting the fastest and slowest heroes for each position using the 'head(1)' function. After removing any entries with 'Position' labeled as 'no', the resulting data frames are formatted and merged into a single data frame containing the 'Position', 'Fastest', and 'Slowest' columns. Finally, the merged data frame is returned, providing a summary of the fastest and slowest heroes for each position in the game.

```python
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
```

2. Get minimum and maximum health points in each positions

The purpose of the code is to calculate the minimum and maximum values of 'MaximumHealth' for each hero position ('mainPosition' and 'subPosition') in the game dataset. The implementation involves grouping the data by 'mainPosition' and 'subPosition' separately, aggregating the minimum and maximum values for 'MaximumHealth', and merging these statistics into a single dataframe. The resulting dataframe includes columns for the hero position, the minimum health ('min'), and the maximum health ('max'). Entries with 'position' labeled as 'no' are excluded from the final dataframe. The calculated statistics are then returned in the 'merged_stats' dataframe.

```python
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
```

3. Get the whole speed grouped by positions

The purpose of the code is to create a list of speed distributions for each hero position in the game dataset. The implementation involves filtering out entries with 'Position' labeled as 'no', grouping the data by 'Position,' and then creating two lists: 'x_name' representing the hero positions and 'x_data' representing the corresponding speed distributions. The 'x_data' list is formed by converting the 'MovementSpeed' values for each position group into arrays. The resulting data structure is then returned as a list containing both the hero positions and their respective speed distributions.

```python
def distribution_speed_each_position():
    x_data = []
    x_name = []
    x1 = process_position()[process_position()['Position'] != 'no']
    x1 = x1.groupby('Position')
    for name, group in x1:
        x_data.append(np.array(group['MovementSpeed']).tolist())
        x_name.append(name)
    return [x_name, x_data]
```

4. Get the whole health points grouped by positions

The purpose of the code is to create a list of health distributions for each hero position in the game dataset. The implementation involves filtering out entries with 'Position' labeled as 'no', grouping the data by 'Position,' and then creating two lists: 'x_name' representing the hero positions and 'x_data' representing the corresponding health distributions. The 'x_data' list is formed by converting the 'MaximumHealth' values for each position group into arrays. The resulting data structure is intended to be used for further analysis or visualization.

```python
def distribution_health_each_position():
    x_data = []
    x_name = []
    x1 = process_position()[process_position()['Position'] != 'no']
    x1 = x1.groupby('Position')
    for name, group in x1:
        x_data.append(np.array(group['MaximumHealth']).tolist())
        x_name.append(name)
    return [x_name, x_data]
```

5. Count the heroes with different types belong to each position

The purpose of the code is to count the number of heroes for each hero type within different positions in the game dataset. The implementation involves grouping the data by both 'Position' and 'HeroType,' counting the occurrences of each combination, and then reshaping the result into a table with 'Position' as the index and separate columns for 'Magic' and 'Physical' hero types. The resulting table, named 'position_hero_type_count,' is intended to provide a summary of hero distribution across different positions and their respective hero types.

```python
def type_count_each_position():
    df = process_position()
    position_hero_type_count = df.groupby(['Position', 'HeroType']).size().unstack().fillna(0).astype(int)
    position_hero_type_count = position_hero_type_count[position_hero_type_count.index != 'no']
    position_hero_type_count = position_hero_type_count.reset_index()
    position_hero_type_count.columns = ['Position', 'Magic', 'Physical']
    return position_hero_type_count
```

6. Count the heroes with different attack ranges belong to each position

The purpose of the code is to count the number of heroes with different attack ranges within different positions in the game dataset. The implementation involves grouping the data by both 'Position' and 'AttackRange,' counting the occurrences of each combination, and then reshaping the result into a table with 'Position' as the index and separate columns for 'Long' and 'Short' attack ranges. The resulting table, named 'position_hero_attackRange_count,' is intended to provide a summary of hero distribution across different positions and their respective attack ranges. The function also prints the resulting table and returns it.

```python
def attack_range_count_each_position():
    df = process_position()
    position_hero_attackRange_count = df.groupby(['Position', 'AttackRange']).size().unstack().fillna(0).astype(int)
    position_hero_attackRange_count = position_hero_attackRange_count[position_hero_attackRange_count.index != 'no']
    position_hero_attackRange_count = position_hero_attackRange_count.reset_index()
    position_hero_attackRange_count.columns = ['Position', 'Long', 'Short']
    print(position_hero_attackRange_count)
    return position_hero_attackRange_count
```

7. Check the relation between Physical Defense and Physical Damage Reduction by compare the change trend

The purpose of the code is to calculate the median values of 'PhysicalDefense' and 'PhysicalDamageReduction' for each 'Position' in the game dataset. The implementation involves grouping the data by 'Position' and then calculating the median values for the specified columns. The resulting DataFrame, named 'mode_attack_both,' contains columns for 'Position,' 'PhysicalDefense,' and 'PhysicalDamageReduction.' Rows corresponding to the 'no' position are removed from the DataFrame before resetting the index and returning the result.

```python
def relation_PhysicalDefense_PhysicalDamageReduction():
    df = process_position()
    mode_attack_both = df.groupby("Position")[
        ["PhysicalDefense", "PhysicalDamageReduction"]].median().reset_index()
    mode_attack_both.columns = ["Position", "PhysicalDefense", "PhysicalDamageReduction"]
    mode_attack_both = mode_attack_both[mode_attack_both['Position'] != 'no']
    mode_attack_both.reset_index(drop=True, inplace=True)
    return mode_attack_both
```

8. Check the relation between Physical Defense and Physical Damage Reduction by compare the change trend

The purpose of this code is to calculate the median values of 'MaximumMana' and 'ManaRegeneration' for each 'Position' in the game dataset. The implementation involves grouping the data by 'Position' and then calculating the median values for the specified columns. The resulting DataFrame, named 'mode_attack_both,' contains columns for 'Position,' 'MaximumMana,' and 'ManaRegeneration.' Rows corresponding to the 'no' position are removed from the DataFrame before resetting the index and returning the result.

```python
def relation_MaximumMana_ManaRegeneration():
    df = process_position()
    mode_attack_both = df.groupby("Position")[
        ["MaximumMana", "ManaRegeneration"]].median().reset_index()
    mode_attack_both.columns = ["Position", "MaximumMana", "ManaRegeneration"]
    mode_attack_both = mode_attack_both[mode_attack_both['Position'] != 'no']
    mode_attack_both.reset_index(drop=True, inplace=True)
    return mode_attack_both
```

#### Data transmission

After preparing the data for the data visualization, I need to transmit the data from the back-end to front-end to create the charts. In this project, I use Flask as the back-end, based on the setting of the Flask framework, I use the annotation in app.py file to set the routing paths of the corresponding data generated functions. Moreover, to decrease the size of the transmitted data, I transform the original Dataframe form or numpy.array form data into the json object or json arrays by 'to_json' or 'json.dump'. It is worth to mention that to the original numpy.array is not serializable, so I have to transform it into list first.

```python
# app.py
from flask import Flask, render_template
import src.dataAnalysis.display as display
import json as JSON

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/min_max_speed_each_position')
def min_max_speed_each_position():
    return display.min_max_speed_each_position().to_json(orient='records')


@app.route('/min_max_health_each_position')
def min_max_health_each_position():
    return display.min_max_health_each_position().to_json(orient='records')


@app.route('/distribution_speed_each_position')
def distribution_speed_each_position():
    return JSON.dumps(display.distribution_speed_each_position(), indent=2)


@app.route('/distribution_health_each_position')
def distribution_health_each_position():
    return JSON.dumps(display.distribution_health_each_position(), indent=2)


@app.route('/type_count_each_position')
def type_count_each_position():
    return display.type_count_each_position().to_json(orient='records')


@app.route('/attack_range_count_each_position')
def attack_range_count_each_position():
    return display.attack_range_count_each_position().to_json(orient='records')


@app.route('/relation_PhysicalDefense_PhysicalDamageReduction')
def relation_PhysicalDefense_PhysicalDamageReduction():
    return display.relation_PhysicalDefense_PhysicalDamageReduction().to_json(orient='records')


@app.route('/relation_MaximumMana_ManaRegeneration')
def relation_MaximumMana_ManaRegeneration():
    return display.relation_MaximumMana_ManaRegeneration().to_json(orient='records')


if __name__ == '__main__':
    distribution_speed_each_position()
    app.run(debug=True)

```

In the front-end, I use fetch API to request and receive the data.

```javascript
document.addEventListener('DOMContentLoaded', function () {
    fetch('/type_count_each_position')
        .then(response => response.json())
        .then(data => {
            let processedData = processData_b2(data);
            createBarChart_b2(processedData);
        })
        .catch(error => console.error('Error fetching data:', error));
});
```

#### Data visualization

As I mentioned in the beginning, I use the echarts to create the interactive charts. It is too complex to introduce the detail setting of different charts based on echarts, so I will display a simple demonstration here to introduce how I get an echart-maked chart. 

```js
//bottom1.js
document.addEventListener('DOMContentLoaded', function () {
    fetch('/type_count_each_position')
        .then(response => response.json())
        .then(data => {
            let processedData = processData_b2(data);
            createBarChart_b2(processedData);
        })
        .catch(error => console.error('Error fetching data:', error));
});

function processData_b2(data) {
    let processedData = {
        departments: [],
        femaleCount: [],
        maleCount: []
    };

    for (let i = 0; i < data.length; i++) {
        processedData.departments.push(data[i].Position);
        processedData.femaleCount.push(data[i].Magic);
        processedData.maleCount.push(data[i].Physical);
    }

    return processedData;
}

function createBarChart_b2(data) {
    let chartContainer = document.getElementById('bottom1');
    let myChart = echarts.init(chartContainer);

   let option = {
        title: {
            text: 'Type Distribution in Positions',
            left: 'center',
            textStyle: {
                fontSize: 12
            },
            top: 5
        },
        legend: {
            data: ['Magic', 'Physical'],
            top: 25
        },
        xAxis: {
            type: 'category',
            data: data.departments,
            axisLabel: {
                interval: 0,
                rotate: 45,
                textStyle: {
                    fontSize: 10
                }
            },
            axisTick: {
                show: false
            },
            axisLine: {
                show: false
            },
            z: 10
        },
        yAxis: {
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                color: '#999'
            }
        },
        series: [
            {
                name: 'Magic',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: function (params) {
                        return params.value;
                    }
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.femaleCount
            },
            {
                name: 'Physical',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: function (params) {
                        return params.value;
                    }
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.maleCount
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function (params) {
                let tooltip = params[0].name + '<br>';
                for (let i = 0; i < params.length; i++) {
                    tooltip += params[i].seriesName + ': ' + params[i].value + '<br>';
                }
                return tooltip;
            }
        }
    };

    myChart.setOption(option);
}
```

In the front-end, the data will be pass into the function 'processData' to shape the data into the form that echarts accepts, then the data will be pass into the function 'createBarChart' to create a chart. In this function, the chart is  initialize  as the corresponding chart and banded to a specific container in the website first, then it generate the setting and the data it contains in the 'option' variable. After the generation, the chart will be banded with the set data and rendering to display.

### Final Result

![image-20231212192741129](.\src\dataAnalysis\dataAnalysis_files\finalResult.png)
