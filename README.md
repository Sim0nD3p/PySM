
# PySM
##To do:
- add way to select multiple items and modify their prop in batch

- Work on import
    - confirmationWidget, add props vs add part (merge, remplacer)
    - standard import for parts and props
    - import for orders dates and qte
    - reload partModel in treePropertiesEditor not only on program starup

## where I am:
- Store element:
    - add wall to storeObject element
      - *integration of geometry as parent class is good should continue on that, maybe add integration of shapely
    - **transformations matrices for coordinates between store, racking and shelves
- Shelf and container
  - Actions and toolbar for shelf, act on containers
    - *integration of shapely in geometry for shape (postponed)
    - **add way to find place for container in shelf
      - shelfPanel
        - way to save shelf to racking
        - check shelf properties
        - add way to add container (container selector for part, select part and container)
    - ***add way to find best shelf according to place available (later)
    - bug when drawing new racking when racking already selected

## Mid term
- StoreFloor writer loader will be broken by the addition of geometry as a parent class


## Long term
- nomenclature naming module
- add way to have hierarchy between part -> add class Subassembly and Assembly(final)
- add way to regroup parts with usage (which are used together and how often)
  - part A might be used with part B and part C but part A and C not used together



## STORE ALGO V2
- add optinos for how parts are placed in store
- what happens when targeted quantities changes? no broken store
- manually place part (before and after store generation) -> how to reorganize containers?
