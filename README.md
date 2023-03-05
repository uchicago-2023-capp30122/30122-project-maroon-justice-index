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


![GitHub Project Structure](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/structure_diagram.jpeg)

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



### Project Takeaways

While working through this project we experienced a number of limitations and made several adaptations. The intent of the resource map was to create a resource for the community to use to locate affordable menstrual products and services since one does not currently exist. However, we found that many community organizations didn’t want their addresses published either because the resources they have are only for their clients and/or because their centers also act as domestic violence refuges. Thus, exposing their address would jeopardize the safety of many of the people seeking their services. Through our outreach, we compiled a small dataset of organizations that distribute free menstrual products to their clients and consented to having their service locations added to our map, and this was added to our map.

During our outreach, we also learned that homeless shelters, public schools and colleges/universities are now required by the State of Illinois to provide free menstrual products. Due to capacity and time constraints we did not scrape these because they were revealed to be high in complexity. The WIC offices and other community-based services we had already scraped mentioned either providing or not providing resources. Therefore, we used these centers as a proxy for access (defined by the number of these centers within a one-mile radius) within our index. If we had the data of who actually provides these services this would improve the quality of our resource in showing where one can go, but it is not necessarily the case here. In the end, we didn’t have the data to generate this resource map that we envisioned.

Moreover, an important population is missing from our index, which are those who are unhoused. The census recently enacted a program in 2020 that counts people receiving services from shelters and mobile vans, and from outdoor locations where people are known to sleep. Through this effort the counts are still inaccurate and attempting to triangulate population estimates continues to prove to be difficult without fixed housing. One study found that “On any given night, there are about 500,000-600,000 people experiencing homelessness in the United States, with about one-third sleeping on the streets and the rest in shelters.” That means about 500,000-600,000 people are not included in our index and this is a population we care greatly about. 

In summary, we used income and community center locations as proxies for estimating risk for period poverty at the census tract level. Before our analysis, we expected there to be variation in any given census tracts’ risk for period poverty based on whether we were factoring in residents’ income or proximity to community-services. Instead, we found that the two were largely correlated. We were surprised to find that the locations of Illinois Department of Health Services’ community-based services, which serve high-need or low-income populations, were lacking in the areas with high concentrations of poverty because we expected there to be greater investment in the infrastructure of community-based services in these areas. Instead, the infrastructure and availability of community-based services appear to be lagging behind available data on poverty. We found these insights interesting, and we learned that there is much work to be done to completely understand the issue of period poverty and inform policy initiatives that aim to provide resources.