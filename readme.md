# SensorDataFusion

Git link:
```shell
 https://git.hs-coburg.de/siv2871s/Grid_map_Ros2.git
```
##  Parameters of class Grid map :

g_map = Gridmap(20, 0.2, "hsc_map", 0.5, 0.8, 0.2)

|Parameters|	Description|	Type|	value|
|-----|------|------|-------|
|size|	size of the grid map in cells|	integer value|	20|
|resolution|	resolution of the grid map in meters per cell|	float value|	0.2|
|topic_name|	name of the topic on which the OccupancyGrid message will be published|	string value|	hsc_map
|p_0|	prior probability of a cell being occupied|	float value between 0 and 1|	0.5|
|p_occ|	probability of a cell being occupied given that it is observed to be occupied|	float value between 0 and 1|	0.8|
|p_free|	probability of a cell being free given that it is observed to be free|	float value between 0 and 1|	0.2|

## Different resolutions:

#### When you use different resolutions in the grid map, it changes how detailed the map is. 

#### If you choose a higher resolution, the map will have more small squares, showing more details.

####  On the other hand, if you choose a lower resolution, the squares will be larger, and the map may not show as much detail. 

#### It's like choosing between a very detailed picture and a simpler one In my situation.

#### I tried three different resolutions (0.1, 0.2, 0.6) to see how they make the map look different.
