# UML Class Diagram (Lab 9)

Everything from the Lab 8 diagram is unchanged (`Supplier`, `Product`, `PhysicalProduct`,
`DigitalProduct`, `CanBeShipped`, `Inventory`, `OrderLine`), except:

- `Product` gains `+ set_price(price : float) : void` (validates price > 0).
- `Order` gains a `discount` attribute, `get_discount()`, `set_discount()` and `calculate_subtotal()`.
- New classes: `DiscountStrategy` (abstract) + 4 strategies, and `ProductFactory`.

```
                                         +---------------------------------------+
                                         |                Order                  |
                                         +---------------------------------------+
                                         | - order_id : String                   |
                                         | - order_lines : OrderLine [0..*]      |
                                         | - discount : DiscountStrategy         |
                                         +---------------------------------------+
                                         | + Order(order_id : String,            |
      (composition to OrderLine,         |     discount : DiscountStrategy       |
       unchanged from Lab 8)  <#>--------|              = NoDiscount)            |
                                         | + get_order_id() : String             |
                                         | + get_discount() : DiscountStrategy   |
                                         | + set_discount(discount :             |
                                         |     DiscountStrategy) : void          |
                                         | + add_order_line(product : Product,   |
                                         |     quantity : int) : void            |
                                         | + remove_order_line(product_id :      |
                                         |     String) : bool                    |
                                         | + get_order_lines() : OrderLine [0..*]|
                                         | + calculate_subtotal() : float        |
                                         | + calculate_total() : float           |
                                         | + display_order() : void              |
                                         +---------------------------------------+
                                                            | 0..*
                                                            |  uses  (association:
                                                            |  solid line, arrow,
                                                            v  no diamond)
                                                            | 1
                                         +---------------------------------------+
                                         |            <<abstract>>               |
                                         |          DiscountStrategy             |
                                         +---------------------------------------+
                                         | + apply(total : float) : float        |
                                         |                         {abstract}    |
                                         +---------------------------------------+
                                                            ^
                                                            | generalisation
                                                            | (solid line, hollow triangle)
          +-------------------------+-----------------------+---------------------------+
          |                         |                       |                           |
+-------------------+ +---------------------------+ +---------------------------+ +-----------------------+
|    NoDiscount     | |    PercentageDiscount     | |       BulkDiscount        | |    StudentDiscount    |
+-------------------+ +---------------------------+ +---------------------------+ +-----------------------+
|                   | | - percentage : float      | | - threshold : float       | | + RATE : float = 0.05 |
+-------------------+ +---------------------------+ | - amount : float          | +-----------------------+
| + apply(total :   | | + PercentageDiscount(     | +---------------------------+ | + apply(total : float)|
|   float) : float  | |   percentage : float)     | | + BulkDiscount(threshold :| |   : float             |
+-------------------+ | + get_percentage() : float| |   float, amount : float)  | +-----------------------+
                      | + apply(total : float)    | | + get_threshold() : float |
                      |   : float                 | | + get_amount() : float    |
                      +---------------------------+ | + apply(total : float)    |
                                                    |   : float                 |
                                                    +---------------------------+


+-----------------------------------------------+                    +---------------------------+
|                ProductFactory                 |      <<creates>>   |       <<abstract>>        |
+-----------------------------------------------+ - - - - - - - - - >|         Product           |
| (no attributes - stores nothing)              |   (dependency:     |  (see Lab 8 diagram;      |
+-----------------------------------------------+    dashed arrow)   |   + set_price(price :     |
| + create(product_type : String,               |                    |     float) : void)        |
|     product_id : String, name : String,       |                    +---------------------------+
|     price : float, stock_quantity : int,      |
|     supplier : Supplier, extra : float = 0)   |
|     : Product                     {static}    |
+-----------------------------------------------+
```

## New relationships and multiplicities

| Relationship | Notation | Multiplicity | Why |
|---|---|---|---|
| `NoDiscount`, `PercentageDiscount`, `BulkDiscount`, `StudentDiscount` → `DiscountStrategy` | Generalisation (solid line, hollow triangle) | – | Each *is-a* discount strategy and implements `apply()`. |
| `Order` → `DiscountStrategy` | **Association** (solid line with arrow, no diamond) | `Order 0..* —— 1 DiscountStrategy` | An order *uses* exactly one strategy at a time (defaults to `NoDiscount`). The strategy is not part of the order: it is passed in, can be swapped with `set_discount()`, and one strategy object can be shared by many orders. |
| `ProductFactory` ⇢ `Product` | **Dependency** (dashed arrow, `«creates»`) | – | The factory builds `PhysicalProduct`/`DigitalProduct` objects and returns them as `Product`, but never keeps a reference to them. |

Main program (`inventory_manager.py`, not a class): menu, input helpers (`get_positive_float`,
`get_non_negative_int`, `get_non_negative_float`), JSON load/save, and `load_products()` for CSV import.
All product creation goes through `ProductFactory.create()`.