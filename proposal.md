# Project Proposal
FootballScout   
Members: Renghe Tang, Henry Luo, Xiaoxiao Fu, Sylvia Lyu
## Motivation and Purpose
**Our role**: Data science team of a football club   

**Target audience**: Management team of a club 

Professional football clubs spend a considerable amount of money on the transfer market each season to find the best players that suit their teams. Transfer decisions could significantly affect a team's performance both in the short term and in the long run. However, scouting for suitable players is a challenging task. Many factors need to be considered. We intend to build a data visualization dashboard to help with the scouting process. The dashboard would visualize detailed statistics of individual football players and the overall distribution of statistics of all players in a selected scope (e.g. several leagues, a league, or a team). Scouts or the management of clubs could use the dashboard to compare different candidates, access how their stats changed over time, and determine which player is more suitable for the team. With the help of statistical modeling, the dashboard could also provide a projection of player performance ratings based on a specific value of game stats.   

## Description of the data

We are visualizing the data of around 50,000 players in five major European football leagues from 2010 to 2022. Each player has about 50 columns of information, which contains their demographics (name, nationality, team, etc.),game performance (rating, goals, tackles, etc.), and their status (injury, captain, position, etc.). 

## Research questions and usage scenarios
**Research questions**:
1. How to determine which player is the best for the team
2. What factors affect player performance rating    

**Usage scenario:**   

A La Liga (Spanish league) football team is looking for a new player in this winter transfer window. The scouting team recommended five candidates, and the management team was having difficulty deciding which candidate to pick, so they opened the FootballScout dashboard. In the first panel, they selected the years from 2016 to 2022 on the slider. They examined the distribution of player game ratings across the five major European leagues in the past six years from the kernel density plot and the box plot, which gives them the insight that an average player should have a rating of around 6.0. Then they wondered whether the La Liga players have different rating distributions than the other leagues. They select La Liga in the 'league' dropdown box and found that La Liga players have an average rating of 6.4. Now they established that they should pick the player with a rating of at least 6.4 to gain the team an edge in La Liga games.     
After that, they navigated to the second panel, where they entered the names of the five candidates in the 'players' box, keeping the year range the same as before. The five players' game ratings, goals, assists, shots, and key passes in the past six years are displayed as line charts. It is obvious that 3 of the five candidates have game ratings consistently above 6.4, but one of them seems to fluctuate a lot over the years, so the management team decided to pick one of the other two players, John and Frank, who have more stable game ratings.Since the team is looking for a midfield player who can make key passes, the management team entered the stat 'passes_key' into the 'stats' box to visualize the number of key passes John and Frank made in the past six years. It appeared that they were on par with key passes. John has a slightly higher game rating, so the management decided to get John.   
However, John's club didn't want to sell him. Well, could Frank improve his game rating to be as good as Johns in a short time? The management team went to the third panel of FootballScout and inputted some values for the key stats that predict game rating and found that if Frank could just increase his 'shots_on' by 5, his rating would be as good as John's. After consulting with the coaches, who believed that it was possible to increase 'shots_on' after Frank arrived at the team, the management reached out to Frank and signed him. 




