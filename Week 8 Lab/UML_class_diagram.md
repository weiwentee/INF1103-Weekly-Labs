# UML Class Diagram

```
+-----------------------------------------+
|                 Product                 |
+-----------------------------------------+
| - __product_id : String                 |
| - __name : String                       |
| - __price : float                       |
| - __stock : int                         |
+-----------------------------------------+
| + __init__(product_id, name,            |
|            price, stock)                |
| + get_product_id() : String             |
| + get_name() : String                   |
| + get_price() : float                   |
| + get_stock() : int                     |
| + update_stock(quantity : int) : void   |
| + display_information() : void          |
+-----------------------------------------+
                    ^
                    | 0..*
                    |
                    <> 1   (Inventory contains Products)
+-----------------------------------------+
|                Inventory                |
+-----------------------------------------+
| - __products : List<Product>            |
+-----------------------------------------+
| + __init__()                            |
| + add_product(product : Product) : bool |
| + search_product(product_id : String)   |
|                       : Product | None  |
| + get_all_products() : List<Product>    |
| + display_all() : void                  |
+-----------------------------------------+
```

Main program (`inventory_manager.py`, not a class): displays the menu, gets user input,
calls Inventory methods, and handles loading/saving `inventory.json`.
