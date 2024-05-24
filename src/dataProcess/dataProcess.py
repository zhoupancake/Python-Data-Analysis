import pandas as pd
from xpinyin import Pinyin

# readData
source1 = pd.read_csv("../data/source1.csv").fillna(0.0)
source2 = pd.read_csv("../data/source2.csv", sep="\t").fillna(0.0)

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
merged_df.to_csv("../../static/csv/data.csv", index=False)
