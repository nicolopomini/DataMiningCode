# DataMiningCode
Coding part for the data mining project

## Sum up of the meeting with Yannis

- we can assume every record has a field called _parent_ that indicates which record is the parent
- we can compare with any other thing. Yannis want to see how we sell our product
- big data: the data generator

### Idea

The starting idea can be the following:
- cluser the records, in order to group them by similarity
- count the occurences of singles
- prune those nodes that are under a certain score (e.g. the average of appearence)
- link a _survived_ node with its parent, if it is _survived_ too
- count the link importance
- go on with pruning / linking
