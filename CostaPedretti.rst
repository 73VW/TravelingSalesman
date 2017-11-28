``Traveling salesman problem solver.``
======================================

The following code is used to try to find a solution to the TSP. Using City and Individual (path) class it is possible to find a possible solution approaching the real result. This code is optimized to take less time to execute not to find the absolute shortest path.

Modules
-------

+--------------------------------+-----------------------------+------------------------------+------------------------+
| `argparse <argparse.html>`__   | `pygame <pygame.html>`__    | `secrets <secrets.html>`__   | `time <time.html>`__   |
|  `math <math.html>`__          |  `random <random.html>`__   |  `sys <sys.html>`__          |                        |
+--------------------------------+-----------------------------+------------------------------+------------------------+

Classes
-------


- `builtins.object <builtins.html#object>`__

- `City <CostaPedretti.html#City>`__

- `Individual <CostaPedretti.html#Individual>`__

class **City**(`builtins.object <builtins.html#object>`__)
##########################################################

``Object that take the name of the city and it's coordonates. ``


Methods defined here:
+++++++++++++++++++++


**\_\_eq\_\_**\ (self, other)
    ``Compare two cities.``

**\_\_init\_\_**\ (self, name, x, y)
    ``Init city object.``

**\_\_repr\_\_**\ (self)
    ``Represent object.   Commonly used when printing a list of objects.``

**\_\_str\_\_**\ (self)
    ``Print object in a human readle way.``

**distance\_to**\ (self, other)

Data descriptors defined here:
++++++++++++++++++++++++++++++

**\_\_dict\_\_**
    ``dictionary for instance variables (if defined)``

**\_\_weakref\_\_**
    ``list of weak references to the object (if defined)``

Data and other attributes defined here:
+++++++++++++++++++++++++++++++++++++++

**\_\_hash\_\_** = None

class **Individual**\ (`builtins.object <builtins.html#object>`__)
####################################################################

``Class that take a possible path as value. ``


Methods defined here:
+++++++++++++++++++++

**\_\_contains\_\_**\ (self, city)
    ``Return if city is in path.``

**\_\_eq\_\_**\ (self, other)
    ``Compare two individuals.``

**\_\_getitem\_\_**\ (self, i)
    ``Return city at i.``

**\_\_init\_\_**\ (self, path)
    ``Init Individual object.``

**\_\_len\_\_**\ (self)
    ``Return path length.``

**\_\_lt\_\_**\ (self, other)
    ``Compare objects.``

**\_\_repr\_\_**\ (self)
    ``Represent object.   Commonly used when printing a list of objects.``

**\_\_setitem\_\_**\ (self, i, value)
    ``Set value for city at i.``

**\_\_str\_\_**\ (self)
    ``Print object in a human readle way.``

**extend**\ (self, datas)
    ``Extend path.``

**fitness**\ (self)
    ``Compute fitness value in order to choose who lives.   In this case we want to keep only the shortest path so we have to invert the result.``

**index**\ (self, value)
    ``Return index of value in self.path.``

**insert**\ (self, i, value)
    ``Insert value in self.path at i.``

**p\_length**\ (self)
    ``Compute path length according to cities order.``

--------------


Data descriptors defined here:
++++++++++++++++++++++++++++++

**\_\_dict\_\_**
    ``dictionary for instance variables (if defined)``

**\_\_weakref\_\_**
    ``list of weak references to the object (if defined)``

--------------

Data and other attributes defined here:
+++++++++++++++++++++++++++++++++++++++

**\_\_hash\_\_** = None

Functions
---------


**collect\_cities**\ (screen, font, cities)
    ``Collect cities from user input.``

**create\_random\_individual**\ (cities, solutions)
    ``Create random individual from cities list.``

**draw**\ (screen, font, positions)
    ``Draw cities on window.``

**draw\_line**\ (screen, font, cities, text)
    ``Draw lines from cities list.``

**extended\_two\_opt**\ (solution, gui, screen, font, text)
    ``Peforms 2-opt.   Source : https://github.com/rellermeyer/99tsp/blob/master/python/2opt/TSP2opt.py``

**fillArrayWithData**\ (fileName, cities)
    ``Fill city list with datas from [filename].``

**ga\_solve**\ (filename=None, gui=True, maxtime=0)
    ``Solve using Genetic Algorithm.``

**greedy\_subtour\_crossover**\ (ga, gb)
    ``Multiply individuals according to Greedy Subtour Crossover.   Source: http://www.gcd.org/sengoku/docs/arob98.pdf``

**init\_game**\ ()
    ``Init pygame interface.``

**init\_solutions**\ (cities, solutions, M)
    ``Init first random solutions.``

**multiply\_using\_gSC**\ (solutions, number\_of\_multiplication)
    ``Multiply using greedy_subtour_crossover function.``

**swap\_two\_opt**\ (solution, i, k)
    ``Swap cities between i and k in solution.``

**two\_opt**\ (solution)
    ``Peforms 2-opt.   Source : https://github.com/rellermeyer/99tsp/blob/master/python/2opt/TSP2opt.py``

Data
----
 

**KEYDOWN** = 2

**K\_RETURN** = 13

**MOUSEBUTTONDOWN** = 5

**QUIT** = 12

**app\_desc** = 'Traveling salesman problem'

**city\_color** = [255, 0, 127]

**city\_radius** = 3

**font\_color** = [255, 255, 255]

**screen\_x** = 510

**screen\_y** = 510
