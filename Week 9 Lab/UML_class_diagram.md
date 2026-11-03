# UML Class Diagram (Lab 7)

```
                                                     +-----------------------------------------+
                                                     |            <<interface>>                |
                                                     |             CanBeShipped                |
                                                     +-----------------------------------------+
                                                     |                                         |
+-----------------------------------------+          +-----------------------------------------+
|                Inventory                |          | + calculate_shipping_cost() : float     |
+-----------------------------------------+          |                          {abstract}     |
| - __products : List<Product>            |          +-----------------------------------------+
+-----------------------------------------+                              ^
| + __init__()                            |                              :  (realisation:
| + add_product(product : Product) : bool |                              :   dashed line,
| + search_product(product_id : String)   |                              :   hollow triangle)
|                       : Product | None  |                              :
| + get_all_products() : List<Product>    |                              :
| + display_all() : void                  |                              :
+-----------------------------------------+                              :
                 <> 1                                                    :
                  |                                                      :
                  | contains                                             :
                  | 0..*                                                 :
                  v                                                      :
+-----------------------------------------+                              :
|              <<abstract>>               |                              :
|                 Product                 |                              :
+-----------------------------------------+                              :
| - __product_id : String                 |                              :
| - __name : String                       |                              :
| - __price : float                       |                              :
| - __stock : int                         |                              :
+-----------------------------------------+                              :
| + __init__(product_id, name,            |                              :
|            price, stock)                |                              :
| + get_product_id() : String             |                              :
| + get_name() : String                   |                              :
| + get_price() : float                   |                              :
| + get_stock() : int                     |                              :
| + update_stock(quantity : int) : void   |                              :
| + display_information() : void          |                              :
| + to_dict() : dict                      |                              :
| + get_fulfilment_info() : String        |                              :
|                          {abstract}     |                              :
+-----------------------------------------+                              :
                    ^                                                    :
                    |  (generalisation: solid line, hollow triangle)     :
          +---------+-----------------------------+                      :
          |                                       |                      :
+-----------------------------------------+  +-----------------------------------------+
|              DigitalProduct             |  |             PhysicalProduct             |
+-----------------------------------------+  +-----------------------------------------+
| - __download_size : float               |  | - __weight : float                      |
+-----------------------------------------+  | + BASE_SHIPPING_FEE : float = 5.00      |
| + __init__(product_id, name, price,     |  | + RATE_PER_KG : float = 2.00            |
|            stock, download_size)        |  +-----------------------------------------+
| + get_download_size() : float           |  | + __init__(product_id, name, price,     |
| + display_information() : void          |  |            stock, weight)               |
| + get_fulfilment_info() : String        |  | + get_weight() : float                  |
| + to_dict() : dict                      |  | + display_information() : void          |
+-----------------------------------------+  | + get_fulfilment_info() : String        |
                                             | + calculate_shipping_cost() : float     |
                                             | + to_dict() : dict                      |
                                             +-----------------------------------------+
```

Relationships:
- `PhysicalProduct` and `DigitalProduct` **inherit from** `Product` (solid line, hollow triangle to `Product`).
- `PhysicalProduct` **realises** the `CanBeShipped` interface (dashed line, hollow triangle to `CanBeShipped`).
  `DigitalProduct` does not, because digital products are never shipped.
- `Inventory` **contains** 0..* `Product` objects (aggregation, hollow diamond on `Inventory`).

Main program (`inventory_manager.py`, not a class): displays the menu, gets user input,
creates the right `Product` subclass, and handles loading/saving `inventory.json`
using the `"type"` field (`"physical"` / `"digital"`).
