#### 前言
数据集来自Kaggle (<https://www.kaggle.com/drgilermo/nba-players-stats>)，其中包含了1950-1951赛季至2017-2018赛季的球员基本信息以及赛季技术统计。本文旨在通过对这些数据的简单整理归纳，从几个不同的角度，以图表的形式简单分析NBA自1982年以来的一些发展趋势。数据整理清洗主要使用Pandas，可视化工具用到Tableau。<br>
##### I. 各个位置球员的身高和体重分析
首先来看球员基本信息。<br>
![image.png](https://upload-images.jianshu.io/upload_images/16711962-5a7ce743020e2d80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
其中球员位置（position）中除了中锋（C）、前锋（F）、后卫（G）以外，还有许多球员位置是摇摆不定的，比如F-C, G-F。因此需要把这些位置信息进行处理。 此外，球员身高单位是英尺/英寸，需要对其进行转换。
```Python
#transform postions
def transform_position(value):
    if value=='F-C':
        return 'F'
    elif value=='G-F':
        return 'G'
    elif value =='C-F':
        return 'C'
    elif value =='F-G':
        return 'F'
    else:
        return value
print('initial position distribution')
print(player_data['position'].value_counts())
player_data['position'] = player_data['position'].apply(transform_position)
print('transformed position distribution')
print(player_data['position'].value_counts())
```
![image.png](https://upload-images.jianshu.io/upload_images/16711962-10d0b02465ca0e9f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
转换之后，一共有1932个后卫，1893个前锋，719个中锋。下面是将球员身高数据转换成以米为单位。<br>
```Python
def transform_height(height):
    h = height.split('-')
    feet = float(h[0])
    inch = float(h[1])
    meters = 0.3048*feet+0.0254*inch
    return meters
player_data['height_in_meters'] = player_data['height'].apply(transform_height)
```
接下来我们来看一下每一年进入联盟的球员的**身高体重**的变化趋势。<br>
![Average Height Over 5-Year Bins - V2.png](https://upload-images.jianshu.io/upload_images/16711962-7b78d6ae3a44112d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
不论是中锋、前锋还是后卫，球员的平均身高都处于一个上升的趋势，篮球仍旧是一项高个子的运动。各个位置的球员身高差距也在不断变化。 联盟早期，后卫、前锋、中锋之间的平均身高差距几乎是一样的， 逐渐地，前锋的身高在不断向中锋靠拢，同时与后卫拉大了差距。在1947-1948赛季，进入联盟的前锋的平均身高只有只有1米92，后卫的平均身高也有1米84。而在2017-2018赛季， 前锋的平均身高来到了2米06，就算是NBA历史上最高的后卫之一的本西蒙斯（2米08）也只是刚刚过了前锋的平均线。近几年NBA掀起的小球风使得比赛节奏不断加快，超级中锋逐渐没落，大家潜意识里可能会觉得球员的身高似乎不再那么重要。但是数据告诉我们，每个位置的球员身高还在不断提高，现在的联盟可能更看重球员的运动能力和投射能力， 但是身高仍旧是一项重要的指标。 <br>
![Average Weight Over 5-Year Bins - V2.png](https://upload-images.jianshu.io/upload_images/16711962-2148aa75fc1e5c10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
小球时代到来给人的另外一个印象就是大吨位的球员可能会越来越少。在小球风盛行的今天，可能很难再看到像西姆布拉尔一样的球员。作为首位进入NBA打球的印度裔球员，360磅（约163公斤）的西姆布拉尔在2014年进入联盟的那一刻不知不觉已经打破了联盟的体重记录，成为联盟历史上最重的球员。虽然球员的体重一直也处于一个上升的趋势，其实这和之前看到的球员身高的不断增加也不无关系，强壮程度差不多，身高变高了体重也自然会增加，但是自2000年开始逐渐趋于平稳，尤其是中锋和前锋的体重，近几年还有下降的趋势。根据联盟一直以来的发展趋势，体重大的球员在身体对抗方面有一定的优势，但当体重增加到一定水平以后，球员的速度和机动性也会受到影响，尤其是内线球员，过高的体重使得移动速度和外线防守成为短板，参见那几年让姚明吃了不少苦头的奥库和布泽尔。从图表上来看，球员体重的增加似乎在1996-2000年已经达到了一个潜在的临界值，各个位置的平均体重没有继续增长。加上小球风的推波助澜，平均体重还有一些下降的趋势。<br><br>
##### II. 球队/球员赛季数据分析
接下来分析球员/球队的技术统计。由于1982年之前的技术统计不够全面，存在太多的缺失值，所以我们主要来看1982年之后的球员数据。我们还在原有的数据基础上对每一个赛季的每一支球队增加了一个Id字段，并对每一个赛季的冠军球队进行了标注。同时，我们也创建了一个表，抓取了每个赛季场均助攻前十名的球员的数据。
```Python
#Read data
season_data = pd.read_csv(r'Seasons_Stats.csv')
season_data.head()
champion_data = pd.read_csv(r'Champion_Record.csv')
champion_data.head()
champion_data.dtypes
#Start from 1982
filtered_season_data = season_data[season_data['Year']>=1982].copy()
#Create unique Id for each team each season
champion_data['Id'] = champion_data['Year'].astype(str)+champion_data['Champion_Team']
filtered_season_data['Id'] = filtered_season_data['Year'].astype(str)+filtered_season_data['Tm']
filtered_season_data['Id'] = filtered_season_data['Id'].apply(lambda Id:Id.split('.0')[0]+Id.split('.0')[1])
filtered_season_data.to_csv(r'filtered_season_data.csv')
#Gather Top 10 assiting player data
ast_pts = filtered_season_data.loc[:,['Year','Player','Pos','G','AST','PTS']].copy()
ast_pts['Avg_Ast'] = ast_pts['AST']/ast_pts['G']
ast_pts['Avg_Pts'] = ast_pts['PTS']/ast_pts['G']
topAst_df = pd.DataFrame(columns = ast_pts.columns)
for year in range(1982,2018):
    part = ast_pts[ast_pts['Year']==year].nlargest(10,columns='AST')
    topAst_df = pd.concat([topAst_df,part])
topAst_df.to_csv(r'topAst.csv')
#Mark champion team for each season    
def is_champion(value):
    if value in list(champion_data['Id']):
        return 1
    return 0
filtered_season_data['Champion'] = filtered_season_data['Id'].apply(is_champion)
champion_teams = filtered_season_data[filtered_season_data['Champion']==1].copy()
champion_teams.to_csv(r'champion_teams.csv')
```
<br>
下面是自1982年以来，球队获得**总冠军次数**的情况。
![Number of Championships.png](https://upload-images.jianshu.io/upload_images/16711962-1e5af106a4867392.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)<br>
伪球迷都不知道费城76人在1982-1983赛季还拿过总冠军吧（1954-55，1966-67赛季还拿过两次）。
<br>
以下是联盟**平均两分命中率和三分命中率**。
![League Avg 2P% and 3P%.png](https://upload-images.jianshu.io/upload_images/16711962-6372c01341bfa041.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)<br>
从标注的趋势线上来看，平均两分命中率基本保持在一个相对稳定的水准，除了1997至2004赛季相对较低以外，其他时期联盟的平均两分命中率大多保持在48%以上。而联盟的平均三分命中率则有一个明显的上升趋势。其中1982至1988赛季，平均三分命中率上升尤为明显，然后在之后的八个赛季增速逐渐放缓，在1996赛季之后开始有些回落并稳定在35%上下。NBA1979-80赛季正式引入三分球机制，1980-81赛季NBA完全接受了三分球制度。这解释了1981-1982赛季开始联盟平均三分命中率迅速提高的原因，而如今球队的三分能力也越来越作为一支球队实力的重要指标，而有的球队甚至有意识地放弃中投专注三分球，参见休斯顿火箭队的“魔球理论”。<br>
下面是每个赛季联盟**场均助攻数TOP10球员**的位置分布情况。
![TOP10 Assiting Player Position.png](https://upload-images.jianshu.io/upload_images/16711962-992669b385207b19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
不出所料，控球后卫（PG）几乎包揽了每个赛季的助攻王竞争人选。只能零星地看到几个“组织前锋”进入榜单，实际上1981-1982赛季以来只有5位前锋进入过助攻TOP10，他们是保罗普莱西、斯科蒂皮蓬、格兰特希尔、勒布朗詹姆斯和德雷蒙德格林。<br>
接下来我们来看一下这些助攻TOP10球员们的得分能力如何，以下是每个赛季场均助攻前十的球员的场均助攻和场均得分情况。
![Avg AST_PTS.png](https://upload-images.jianshu.io/upload_images/16711962-9a6c5161a7658747.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
由于每个赛季只取了10位球员的数据，这两项数据的变化会受某一两个球员的数据的影响。从趋势线上来看，助攻TOP10球员的场均助攻数基本稳定在8-10的区间内，自1981-1982赛季以来有些许下滑。而助攻TOP10球员的得分能力在逐渐提高。这从一定程度上说明球员的得分能力越来越成为其助攻能力的一个保证，得分能力强的球员往往能够吸引足够的防守从而得到助攻队友的机会。<br>

以下是每个赛季**冠军球队**的场均出手数和三分出手数的直方图。
![3 Point Attempts and Total Attempts - Champion Teams.png](https://upload-images.jianshu.io/upload_images/16711962-3071e4f145e1d960.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
不难看出，1998-1999赛季和2011-2012赛季这两项数据明显低于平均水平，因为1998-1999赛季和2011-2012赛季是两个缩水赛季，分别只打了50场和66场比赛，导致在计算场均数据的时候出现了错误。下面是更正后的直方图。
![3 Point Attempts and Total Attempts (Modified) - Champion Teams.png](https://upload-images.jianshu.io/upload_images/16711962-421d90fbb0387ecb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240
<br>
自1979-1980赛季NBA引入三分球机制以来，每个赛季冠军球队的三分出手的比重基本保持一个稳定上升的趋势。当然三分出手比重并不能说明球队的三分能力，只是从一个方面说明球队对三分球的重视程度。<br>
为了比较冠军球队与非冠军球队一些技术统计上的差别，我们需要对每个赛季的每支球队进行分组汇总。注意两个缩水赛季场均数据的计算。
```Python
#Group by team, both champion and non-champion
stats = filtered_season_data[['Id','Champion','FG','FGA','3P','3PA','2P','2PA','FT','FTA','ORB','DRB','AST','STL','BLK','TOV','PF','PTS']].copy()
stats_by_team = stats.groupby('Id').sum()
stats_by_team.head()
stats_by_team['Champion'] = stats_by_team['Champion'].apply(lambda c:1 if c!=0 else c)
stats_by_team.reset_index(inplace=True)
stats_by_team.columns
stats_by_team['Year'] = stats_by_team['Id'].apply(lambda i:i[0:4])

champion_stats = stats_by_team[stats_by_team['Champion']==1].copy()
non_champion_stats = stats_by_team[stats_by_team['Champion']==0].copy().groupby('Year').mean()
#non_champion_stats.reset_index(inplace=True)
champion_stats.drop(['Id'],axis=1,inplace=True)
champion_stats.set_index('Year',inplace=True)
champion_stats.columns
non_champion_stats.columns
#Create dataframe calculating the difference between champion and non-champion team
df = pd.DataFrame(columns=champion_stats.columns)
for year in range(1982,2018):
    value = []
    for column in champion_stats.columns:
        v = (champion_stats[column][f'{year}']-non_champion_stats[column][f'{year}'])
        if year==1999:
            v=v/50
        elif year==2012:
            v=v/66
        else:
            v=v/82
        value.append(v)
    df2 = pd.DataFrame([value],index=[f'{year}'],columns=champion_stats.columns)
    df = pd.concat([df,df2])
df.drop(['Champion'],axis=1,inplace=True)
df.reset_index(inplace=True)
df.rename(columns={'index':'Year'},inplace=True)
df.to_csv(r'champion_subtract_non.csv')
```
<br>
下面的直方图显示了冠军球队与非冠军球队在两分出手数、三分出手数、罚球数上的差别。
![Champion Teams and League Avg.png](https://upload-images.jianshu.io/upload_images/16711962-9c51959e9dace652.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<br>
从2000-2001赛季开始，与其余29支非冠军球队的平均两分出手数相比，所有冠军球队都有更少的两分球出手数，而其中有一半的球队有更多的三分出手数，其中大多数冠军球队场均获得更少的罚球数。这说明了这段时期内的冠军球队与其他非冠军球队相比，他们相对更重视三分球的得分能力。与之相伴的影响是，由于两分出手比重的降低，内线博得罚球的机会也相应减少了。当然，这一图表平均了整个赛季的数据，而且是以其余29支球队的平均数据作为参考，并不能说明冠军球队在赛季某一时段（比如总决赛期间）的球队风格，只是一个粗略模糊的数据比较。更客观的冠军球队分析需要更详细的技术统计数据。<br>
