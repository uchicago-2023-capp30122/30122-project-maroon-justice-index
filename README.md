<!-- [![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9875283&assignment_repo_type=AssignmentRepo) -->

# Cook County Period Poverty Index 

### Authors: Betty Fang, Ivanna Rodriguez, Jimena Salinas, Diamon Dunlap

Period poverty is defined as “limited or inadequate access to menstrual products or menstrual health education as a result of financial constraints or negative socio-cultural stigmas associated with menstruation.” Period poverty can be harmful to one’s health, such as using products longer than recommended, and emotional well-being, such as missing work or school due to period leaks, pain and shame. Period poverty is disproportionately affecting those who are impoverished or experiencing homelessness. 
 
We wanted to understand this disparity geographically in Cook County, IL. We focused on factors such as income, public assistance usage, number of menstruating people, percent of income spent on rent, and proximity to community-based services. Using these variables, we created an index at the census tract level and visualized it on a map. We found that the risk of period poverty was concentrated in three areas – west side, south side and far south side. We also found that the number of community centers was correlated with our index- areas with less access to community-based services were, on average, at higher risk of period poverty. From this analysis, we were able to identify neighborhoods that would benefit the most from greater access to free menstrual care resources.

## How to run the Dash application:

Setting up virtual environment using poetry

Once the repo is cloned, in the root directory 30122-project-maroon-justice-index:
1.	Run *poetry install* to install the necessary packages
2.	Run *poetry shell* to activate the virtual environment
3.	Run *python -m ppindex* to open the webapp


## Period Poverty Cook County Map

Below is a map illustrating our resulting index for each census tract in Chicago. Hover over each census tract to view the index value, and the neighborhood each tract is located within.

![Mapping Period Poverty across Cook County](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/map_image.png)


## Map of Neighbourhood Resources and Retail Centers

It was important for us to incorporate existing community services and commercial retailers providing period products into our index. For people in need, having a community service nearby could ameliorate their lack of access to period products. To find existing resources around Chicago, we built a webscraper to compile the addresses for community-based services and commercial retailers, and reached out to period poverty alleviation organizations in Chicago to understand the services offered and restrictions (if any) to access period products.

The map below includes all the resources we scraped, and the organizations that consented to being added to the map. Choose your neighborhood from the dropdown on the left to find the resources closest to you.

![Mapping Community Services and Retail Centers by Census Tract](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/community%20centers_image.png)


## Data Insights

In the process of working on creating our period poverty index and community resources and retailers map, we realized that some of the Census Tracts with the highest period poverty index were also some of the tracks with the least resources at walking distance. The scatter plot below shows the relationship between the period poverty index we calculated and the number of service centers and retailers at walking distance. We see that a lot of period resources are concentrated in areas with low period poverty levels. Our ultimate hope is to use data to inform policymakers on the areas where resources are most needed.

![Period Poverty, Services, and Commercial Retailers](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/income_pop.png)


It is especially important to consider areas with high period poverty rates and large numbers of menstruating people. The graph below helped us identify tracts with a high number of menstruating people and low monthly disposable incomes. For instance, the graph below highlights a few tracts within neighbourhoods like Riverdale, Washington Park, South Deering, Chatham, Humbolt Park, and Englewood, where additional resources could be greatly  beneficial.

![Menstruating People and Disposable Income](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/community_centers_index.png)


