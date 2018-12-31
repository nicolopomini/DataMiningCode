# DataMiningCode
Coding part for the data mining project

## Sum up of the meeting with Yannis

- we can assume every record has a field called _parent_ that indicates which record is the parent
- we can compare with any other thing. Yannis want to see how we sell our product
- big data: the data generator

### Idea

We have a list of trees, potentially large and irregular. We have to find frequent patterns among attributes (eg the field _a_ of the parent equal to _x_ implies the field _b_ of the child equal to _y_).
Ideas:
- prune single nodes that are not frequent, under a certain _threshold_;
- with the remaining nodes, create couples of attributes with distance 1 (means that the two attributes are in nodes with distance 1)
- prune again, excluding those couples less frequent than _threshold_;
- go on, every iteration increasing by 1 the distance
- stop when no more tuples survive from the pruning


### Note
Python >= 3.6 is necessary
