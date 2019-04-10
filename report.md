# Method
On first look at the dataset, I cam to the understanding that we needed to create a network graph.

The dataset contains each road segment over 17 years. All of the data is together, so we need a way of being able to distinguish the same segment of road each year, in order to analyse relevent information, like traffic type changes over year...etc.

Creating a NetworkX Graph object, it takes in a hashable node. In graph theory, a node is an intersecting point, or vertex, where 0 or more edges  meet.

Using this information, and relating it to the dataset; each road can be seen as an `edge`; and the entry in the table `StartJunction` and `EndJunction` are the correstponding $v$ and $w$ nodes.

This picture does not give an exact representation, as it means that the individual junction entries often have more than one junction listed eg: an entry junction `'A124/A1083'` which means that it is linked 

Splitting the dataset

# Findings

# how you would extend your solution and perform further improvements given more time

# how you have designed your analysis to be scalable on larger datasets, identifying relevant limits and workaroundsYou have 10 days to complete and return your submission in a compressed file.