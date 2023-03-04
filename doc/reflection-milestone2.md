# Mile Stone 1 Reflection

### Implemented Features:    
We have implemented all proposed features.   

**Panel 1:**  

**Graphs:**
- A line chart visualizing the top five player's rating and the changes in the selected data range
- A kernel density chart outlining the distribution of player ratings
- A histogram outlining the count of player ratings at each rating level
- A boxplot demonstrating the distribution of player ratings in different years

**Data filter:**
- User can select the year range of data on the slider. The graphs will update to reflect the data in the selected year range.
- League and team can be selected. By default the graphs will reflect data data of all leagues and all teams.

**Panel 2:**  

**Graphs:**
- Line chart visualizing the change of the selected stats over the selected year range. Each graph shows one stat. Stat of multiple players can be overlayed on the same graph.

**Data filter:**
- User can select the year range of data on the slider. 
- League and team can be selected. 
- Multiple players can be selected and there stats will be overlayed to the grahps.

**Panel 3:**

**Graph:**
- Line chart that shows the prediction of selected player's rating according to the data from previous years in the selected year range. 

**Data filter:**
- User can select the year range of data on the slider. 
- League and team can be selected. 
- Multiple players can be selected and there stats will be overlayed to the grahps.

## Limitation
- The graphs are very slow to load. This might be due to the tremendous size of our data set. 
- There are some strange data in our data set that result in strange phenomena on our graphs. Sometimes the line charts have disconnected lines. Some players' data are incomplete since they may have transferred to another league or team and then transferred back. Occasionally there are points on the line charts. This could be due to the player only playing in the selected league for one season. There are many NA data throughout the data set that might affect visualization. This is because the data set includes many players that are on professional teams but have never had a chance to play. 

## Future Improvement
- Explore the possibility of implementing an age slider.
- Consider adding more gunicorn workers or threads to load the graphs faster.
