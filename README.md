# OptiLivraison
A Python script that calculates the lower carbon footprint path among n&lt;12 points. Has a setting tu run random multitests, or you can enter the payload and points by hand. Compares the shortest path (computed dynamically) to the lower carbon footprint path. The carbon footprint is in average 10% better with the lower carbon footprint path

Imagine a truck, loaded with a m0 mass. Its emissions are proportionnal to the mass transported times the distance.
Algorithmes are good at estimation the shortest path for the truck to take, but it's not always the one that has the lowest carbon footprint.
If a mass M_i is unloaded from the truck at point i, we need to calculate the carbon footprint of every segment.

Provided with the script is a few plots that the program outputs.
The blue paths are following the shortest distance (computed dynamically with mlalevic's method:https://gist.github.com/mlalevic/6222750)
The green paths are resulting of the brute force approach to find the bestpath and the right order in which to unload the mass M_i
The thickness of the line is proportionnal to the load the truck has

The carbon footprint is calculated using ADEME method and data.
The estimated route is calculated using trigonometry and a 1.4 factor supposed to represent the longer path a truck drives in real life.

This code is a bit sketchy because it's a prototype, to maybe use to lower the carbon footprint at Florentaise.
