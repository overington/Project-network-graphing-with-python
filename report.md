# Method
On first look at the dataset, I cam to the understanding that we needed to create a network graph, with the following arrangements:

  a. Graph type: `Undirected Simple`, therefore useing NetworkX `Graph` class. To begin analysing, and to simplify the start prcess, I have decided not to make use of directional information (`StartJunction` --> `EndJunction`), and focus only on the analysis of :
    - measuring link utilisation per year for each category of transport
    - average speed of the road, and change over years
    - latency (delay) - when looking through the whole road - where are the slow sections, and how does this change each year 
    - path bandwidth (overall traffic / per vehicle category)/ reliability
 

The dataset contains data about each road segment over a 17 year period. All of the data is together, so we need a way of being able to distinguish the same segment of road each year, in order to analyse relevent information, like traffic type changes over year...etc.

Creating a NetworkX Graph object, it takes in a hashable node. In graph theory, a node is an intersecting point, or vertex, where 0 or more edges  meet.

## Splitting the dataset

Using this information, and relating it to the dataset; each road can be seen as an `edge`; and the entry in the table `StartJunction` and `EndJunction` are the correstponding $v$ and $w$ nodes.

This picture does not give an exact representation, as it means that the individual junction entries often have more than one junction listed eg: an entry junction `'A124/A1083'` which means that it is linked to two roads; but for the time being, this is enough to begin analysing.

Each row entry in the dataset is the information about that particular year, so we can also split up the data for that particular road segment over years: structuring the data like so:






# Findings

# how you would extend your solution and perform further improvements given more time

# how you have designed your analysis to be scalable on larger datasets, identifying relevant limits and workaroundsYou have 10 days to complete and return your submission in a compressed file.