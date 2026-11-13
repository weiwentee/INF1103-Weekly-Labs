# UML Class Diagram (Lab 8)

The rendered version is in `UML_class_diagram.png`. Types use language-independent UML names
(`String`, `float`, `int`, `Product [0..*]`) so the design reads the same in Python, Java or C#.

```
+----------------------------------------+                 +-----------------------------------------+
|               Supplier                 |                 |             <<interface>>               |
+----------------------------------------+                 |              CanBeShipped               |
| - supplier_id : String                 |                 +-----------------------------------------+
| - name : String                        |                 | + calculate_shipping_cost() : float     |
| - contact_email : String               |                 |                           {abstract}    |
+----------------------------------------+                 +-----------------------------------------+
| + Supplier(supplier_id : String,       |                                      ^
|     name : String,                     |                                      :  realisation
|     contact_email : String)            |                                      :  (dashed line,
| + get_supplier_id() : String           |                                      :   hollow triangle)
| + get_name() : String                  |                                      :
| + get_contact_email() : String         |                                      :
| + display_information() : void         |                                      :
| + to_dict() : Map<String, String>      |                                      :
+----------------------------------------+                                      :
                  | 1                                                           :
                  |  supplies   (association: solid line, no diamond)           :
                  | 0..*                                                        :
+----------------------------------------+   0..1 <>-------- 0..*   +---------------------------------------+
|             <<abstract>>               |  (aggregation, hollow    |              Inventory                |
|               Product                  |   diamond at Inventory)  +---------------------------------------+
+----------------------------------------+<-------------------------| - name : String                       |
| - product_id : String                  |                          | - products : Product [0..*]           |
| - name : String                        |                          +---------------------------------------+
| - price : float                        |                          | + Inventory(name : String)            |
| - stock : int                          |                          | + get_name() : String                 |
| - supplier : Supplier                  |                          | + add_product(product : Product)      |
+----------------------------------------+                          |                         : bool        |
| + Product(product_id : String,         |                          | + remove_product(product_id : String) |
|     name : String, price : float,      |                          |                   : Product | null    |
|     stock : int, supplier : Supplier)  |                          | + find_product(product_id : String)   |
| + get_product_id() : String            |                          |                   : Product | null    |
| + get_name() : String                  |                          | + get_all_products() : Product [0..*] |
| + get_price() : float                  |                          | + display_all_products() : void       |
| + get_stock() : int                    |                          +---------------------------------------+
| + get_supplier() : Supplier            |
| + update_stock(quantity : int) : void  |        0..*  +---------------------------------------+
| + display_information() : void         |<-------------|              OrderLine                |
| + to_dict() : Map<String, Object>      |   refers to  +---------------------------------------+
| + get_fulfilment_info() : String       |   1          | - product : Product                   |
|                          {abstract}    |  (association| - quantity : int                      |
+----------------------------------------+   no diamond)+---------------------------------------+
                  ^                                     | + OrderLine(product : Product,        |
                  |  generalisation                     |     quantity : int)                   |
                  |  (solid line, hollow triangle)      | + get_product() : Product             |
       +----------+--------------------+                | + get_quantity() : int                |
       |                               |                | + calculate_subtotal() : float        |
+------------------------------+ +------------------------------+ | + display_information() : void |
|        DigitalProduct        | |       PhysicalProduct        | +---------------------------------------+
+------------------------------+ +------------------------------+                  | 0..*
| - download_size : float      | | - weight : float             |                  |
+------------------------------+ | + BASE_SHIPPING_FEE : float  |                  | (composition: filled
| + DigitalProduct(product_id, | | + RATE_PER_KG : float        |                  |  diamond at Order)
|   name, price, stock,        | +------------------------------+                  | 1
|   supplier : Supplier,       | | + PhysicalProduct(product_id,|        <#>-------+
|   download_size : float)     | |   name, price, stock,        | +---------------------------------------+
| + get_download_size() : float| |   supplier : Supplier,       | |                Order                  |
| + display_information():void | |   weight : float)            | +---------------------------------------+
| + get_fulfilment_info()      | | + get_weight() : float       | | - order_id : String                   |
|                    : String  | | + display_information():void | | - order_lines : OrderLine [0..*]      |
| + to_dict()                  | | + get_fulfilment_info()      | +---------------------------------------+
|        : Map<String, Object> | |                    : String  | | + Order(order_id : String)            |
+------------------------------+ | + calculate_shipping_cost()  | | + get_order_id() : String             |
                                 |                    : float   | | + add_order_line(product : Product,   |
                                 | + to_dict()                  | |     quantity : int) : void            |
                                 |        : Map<String, Object> | | + remove_order_line(product_id :      |
                                 +------------------------------+ |     String) : bool                    |
                                     PhysicalProduct realises     | + get_order_lines() : OrderLine [0..*]|
                                     CanBeShipped (dashed ^ above)| + calculate_total() : float           |
                                                                  | + display_order() : void              |
                                                                  +---------------------------------------+
```

## Relationships and multiplicities

| Relationship | Notation | Multiplicity | Why |
|---|---|---|---|
| `PhysicalProduct`, `DigitalProduct` → `Product` | Generalisation (solid line, hollow triangle at `Product`) | – | Both *are-a* `Product`. |
| `PhysicalProduct` → `CanBeShipped` | Realisation (dashed line, hollow triangle) | – | Only physical products are shipped. |
| `Supplier` — `Product` | **Association** (plain solid line) | `Supplier 1 —— 0..* Product` | Each product has one supplier; a supplier supplies any number. Neither owns the other. |
| `Inventory` ◇— `Product` | **Aggregation** (hollow diamond at `Inventory`) | `Inventory 0..1 ◇—— 0..* Product` | Products exist before/after being in an inventory and can be transferred. The `0` means a product can be in no inventory. |
| `Order` ◆— `OrderLine` | **Composition** (filled diamond at `Order`) | `Order 1 ◆—— 0..* OrderLine` | `Order.add_order_line()` creates each line; a line belongs to exactly one order and is never transferred. |
| `OrderLine` — `Product` | **Association** (plain solid line) | `OrderLine 0..* —— 1 Product` | A line refers to a product but does not own it. |

Main program (`inventory_manager.py`, not a class): menu, user input, creating the right `Product`
subclass, and loading/saving `inventory.json` (the `"type"` field picks physical or digital; products
with the same supplier ID share one `Supplier` object).
