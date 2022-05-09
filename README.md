
# PySM
##To do:
- add way to select multiple items and modify their prop in batch

- Work on import
    - confirmationWidget, add props vs add part (merge, remplacer)
    - standard import for parts and props
    - import for orders dates and qte
    - reload partModel in treePropertiesEditor not only on program starup

## where I am:
# TODO bugs in containerInspector
  - placement_cb not updating
  - placement not good
  - shelfContent not updating on delete
  - dimensions not updating on change
  - 


  - add way to store and restore placement in xml_store file
  - add drag and drop for container group

  - Store element:
      - add wall to storeObject element
        - *integration of geometry as parent class is good should continue on that, maybe add integration of shapely
      - **transformations matrices for coordinates between store, racking and shelves
  - 
    

- drag to place containers in shelfviewer (on shelf)


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
