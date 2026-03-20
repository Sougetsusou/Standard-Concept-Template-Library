# Duplicate Class Body Audit Results

Scanned 39 categories, 336 total class definitions, 252 unique class names.

---

## IDENTICAL duplicates (7 class names)

Same name, byte-for-byte identical body. Safe to consolidate in Pass 3.

Keep one canonical copy, delete the rest.

- `Cuboidal_Leg` — 2 copies: Box, Safe
- `Curve_Handle` — 4 copies: Dishwasher, Microwave, Oven, Refrigerator
- `Drawer_Like_Tray` — 3 copies: Dishwasher, Oven, Refrigerator
- `Flat_Tray` — 3 copies: Dishwasher, Oven, Refrigerator
- `Single_Cylinder` — 2 copies: Bucket, Mug
- `Sunken_Door` — 5 copies: Dishwasher, Microwave, Oven, Refrigerator, Safe
- `Trifold_Curve_Handle` — 4 copies: Dishwasher, Microwave, Oven, Refrigerator

## INCOMPATIBLE duplicates (30 class names)

Same name, different body. Rename the earlier (lost) class in Pass 2.


### `Controller_With_Button`
  - Variant 1 [00bc0629]: Microwave (line 375)
  - Variant 2 [e2d5e956]: Oven (line 566)
  - Variant 3 [c85c8381]: Washingmachine (line 273)

### `Cuboidal_Base`
  - Variant 1 [942c7fa1]: Display (line 105)
  - Variant 2 [874c9786]: Faucet (line 10)
  - Variant 3 [ada84291]: Globe (line 332)

### `Cuboidal_Body`
  - Variant 1 [4900f9e7]: Box (line 8)
  - Variant 2 [e9ecf9db]: Dishwasher (line 8), Microwave (line 8), Oven (line 8), Refrigerator (line 8), Safe (line 8)
  - Variant 3 [fa3c81eb]: Dispenser (line 55)
  - Variant 4 [087f44ca]: Gluestick (line 79)
  - Variant 5 [c6091e33]: Lighter (line 8)
  - Variant 6 [f6a560d5]: Washingmachine (line 114)

### `Cuboidal_Door`
  - Variant 1 [16a08286]: Dishwasher (line 135), Oven (line 135), Refrigerator (line 205), Safe (line 169)
  - Variant 2 [844d4ad7]: Microwave (line 65)
  - Variant 3 [56e33979]: Washingmachine (line 235)

### `Cuboidal_Handle`
  - Variant 1 [07f80ce5]: Dishwasher (line 228), Microwave (line 158), Oven (line 228), Refrigerator (line 298)
  - Variant 2 [9b9da6af]: Knife (line 8)
  - Variant 3 [ee78ef2a]: Scissors (line 1081)
  - Variant 4 [d3736381]: Window (line 533)

### `Curved_Blade`
  - Variant 1 [c18e0804]: Knife (line 412)
  - Variant 2 [997dd347]: Scissors (line 355)

### `Curved_Handle`
  - Variant 1 [d8634352]: Bucket (line 182)
  - Variant 2 [5489ef35]: Kettle (line 348)
  - Variant 3 [b92c9737]: Knife (line 117)
  - Variant 4 [4d1bc2b6]: Mug (line 248)

### `Curved_Spout`
  - Variant 1 [d3c7fcbd]: Faucet (line 543)
  - Variant 2 [96935744]: Kettle (line 668)

### `Cusp_Blade`
  - Variant 1 [1bfa43ae]: Knife (line 356)
  - Variant 2 [59edb630]: Scissors (line 295)

### `Cylindrical_Base`
  - Variant 1 [5588ab66]: Faucet (line 59)
  - Variant 2 [debdc775]: Globe (line 282)

### `Cylindrical_Body`
  - Variant 1 [413cf18d]: Bucket (line 8), KitchenPot (line 8), Mug (line 8), Trashcan (line 8)
  - Variant 2 [bacd8bb1]: Gluestick (line 9)

### `Cylindrical_Cover`
  - Variant 1 [8c90181a]: Gluestick (line 168)
  - Variant 2 [e9c25b95]: KitchenPot (line 54), Trashcan (line 176)

### `Cylindrical_Handle`
  - Variant 1 [2c2a73a5]: Door (line 560)
  - Variant 2 [f0bc918c]: Kettle (line 420)
  - Variant 3 [4655047c]: Knife (line 85)

### `Double_Layer_Body`
  - Variant 1 [0c09f1f3]: Dishwasher (line 65), Oven (line 65), Refrigerator (line 65)
  - Variant 2 [6bf2b860]: Lighter (line 103)

### `Flat_U_Handle`
  - Variant 1 [c67591b8]: Bucket (line 282)
  - Variant 2 [997bf8bb]: Kettle (line 520)

### `Lever_Switch`
  - Variant 1 [80246954]: Faucet (line 1313)
  - Variant 2 [91928375]: Switch (line 321)

### `Multilevel_Body`
  - Variant 1 [11a51281]: Bottle (line 8)
  - Variant 2 [7e1005f8]: Dispenser (line 8)
  - Variant 3 [b635c0f9]: Kettle (line 123)
  - Variant 4 [25c8f7ec]: Mug (line 102)

### `Multilevel_Leg`
  - Variant 1 [e4d35c9c]: Dishwasher (line 604)
  - Variant 2 [0e035974]: Oven (line 774), Refrigerator (line 650)

### `Prismatic_Body`
  - Variant 1 [e9d219e3]: Bucket (line 55), Mug (line 54)
  - Variant 2 [79be3f7b]: Trashcan (line 54)

### `Regular_Body`
  - Variant 1 [daeda97f]: Shaver (line 9)
  - Variant 2 [0510226a]: USB (line 9)

### `Regular_Cover`
  - Variant 1 [5208d573]: Box (line 179)
  - Variant 2 [69efd6ea]: Lighter (line 568)

### `Regular_door`
  - Variant 1 [922b7319]: StorageFurniture (line 183)
  - Variant 2 [aed2308d]: Table (line 1151)

### `Regular_drawer`
  - Variant 1 [b500da27]: StorageFurniture (line 238)
  - Variant 2 [d04ea957]: Table (line 1052)

### `Regular_leg`
  - Variant 1 [1f42533b]: Chair (line 396)
  - Variant 2 [8eec9c9e]: Table (line 121)

### `Ring_Handle`
  - Variant 1 [064fb870]: Kettle (line 384)
  - Variant 2 [f13bb796]: Scissors (line 414)

### `Round_Base`
  - Variant 1 [7013c86e]: Display (line 147)
  - Variant 2 [8aaa37b1]: Faucet (line 305)

### `Round_U_Handle`
  - Variant 1 [cd87286f]: Bucket (line 218)
  - Variant 2 [1b303063]: Kettle (line 456)

### `Standard_Wheel`
  - Variant 1 [5a0b44d1]: Lighter (line 182)
  - Variant 2 [4581055a]: Trashcan (line 682)

### `Star_leg`
  - Variant 1 [b947c7a6]: Chair (line 580)
  - Variant 2 [2fced3f9]: Table (line 572)

### `Trifold_Handle`
  - Variant 1 [60f45c4d]: Bucket (line 104)
  - Variant 2 [da306395]: Dishwasher (line 266), Microwave (line 196), Oven (line 266), Refrigerator (line 336)
  - Variant 3 [0ee7afbb]: Kettle (line 270)
  - Variant 4 [13800ebb]: Mug (line 170)
  - Variant 5 [1beda11e]: Safe (line 441)

## UNIQUE classes (215 class names)

Only one definition. No action needed.

- `Arched_Handle` — Window
- `Asymmetric_Straight_Handle` — Pliers
- `Asymmetrical_Window` — Window
- `Asymmetrical_body` — Ruler
- `Bar_cuboid_leg` — Table
- `Bar_cylindrical_leg` — Table
- `Barstool_leg` — Chair
- `Behind_Double_Layer_Door` — Safe
- `Bistratal_Button` — Pen
- `C_shaped_office_leg` — Chair
- `Cable_stayed_leg` — Table
- `Cambered_Body` — Lighter
- `Cambered_Nozzle` — Lighter
- `Carved_Cover` — Stapler
- `Carved_Cylindrical_Cover` — KitchenPot
- `Carved_Magazine` — Stapler
- `Claw_Handle` — Safe
- `Complex_Magazine` — Stapler
- `CuboidalRear_Support` — Display
- `Cuboidal_Baffle` — Oven
- `Cuboidal_Blade` — Knife
- `Cuboidal_Connector` — Laptop
- `Cuboidal_Cover` — Trashcan
- `Cuboidal_Hollow_Cover` — Trashcan
- `Cuboidal_Nozzle` — Lighter
- `Cuboidal_Plug` — Switch
- `Cuboidal_Ring_Handle` — Scissors
- `Cuboidal_Shaft` — Scissors
- `Cuboidal_Shell` — Trashcan
- `Cuboidal_Sidehandle` — KitchenPot
- `Cuboidal_Spout` — Faucet
- `Cuboidal_Support` — Display
- `Cuboidal_Switch` — Faucet
- `Cuboidal_Topcover` — Dishwasher
- `Cuboidal_Tophandle` — KitchenPot
- `Cuboidal_Vessel` — Refrigerator
- `Cuboidal_body` — Shampoo
- `Curved_Baffle` — Pliers
- `Curved_Base` — Faucet
- `Curved_Clip` — Pen
- `Curved_Gripper` — Pliers
- `Curved_jaw` — Clip
- `Curved_rack` — Foldingrack
- `Cusp_Gripper` — Pliers
- `Cylindrical_Barrel` — Pen
- `Cylindrical_Button` — Pen
- `Cylindrical_Connecter` — Safe
- `Cylindrical_Connector` — Laptop
- `Cylindrical_Dial` — Safe
- `Cylindrical_Hollow_Cover` — Trashcan
- `Cylindrical_Lid` — Bottle
- `Cylindrical_Plug` — Switch
- `Cylindrical_Refill` — Pen
- `Cylindrical_Shaft` — Scissors
- `Cylindrical_Shell` — Trashcan
- `Cylindrical_Spout` — Faucet
- `Cylindrical_Tray` — Microwave
- `Cylindrical_body` — Shampoo
- `Cylindrical_cap` — Shampoo
- `Cylindrical_desktop` — Table
- `Cylindrical_sublayer` — Table
- `Desk_type_leg` — Table
- `Domed_Cover` — Gluestick
- `Double_Cambered_Button` — Lighter
- `Double_Cuboidal_Shaft` — Scissors
- `Double_Curved_Handle` — Scissors
- `Double_Layer_Barrel` — Pen
- `Double_Layer_Cuboidal_Cover` — Trashcan
- `Dual_Connector` — Eyeglasses
- `Enclosed_Bracket` — Globe
- `Enclosed_leg` — StorageFurniture
- `Enveloping_Handle` — Knife
- `Enveloping_Nozzle` — Lighter
- `Flat_Top` — Oven
- `FlipX_Switch` — Switch
- `FlipY_Switch` — Switch
- `Fourfold_Cover` — Box
- `Frame_Base` — Switch
- `Front_Double_Layer_Door` — Safe
- `Front_Facing_Roller_Body` — Washingmachine
- `Frustum_Screen` — Display
- `Half_Ring_Handle` — Scissors
- `HandleY_Switch` — Faucet
- `HandleZ_Switch` — Faucet
- `Holed_Cuboidal_Cover` — Trashcan
- `Holed_Cylindrical_Cover` — Trashcan
- `Knob_Switch` — Faucet
- `Knob_handle` — Doorhandle
- `LShape_Handle` — Door
- `LShaped_Handle` — Window
- `L_Shaped_Button` — Lighter
- `L_Shaped_Sidehandle` — KitchenPot
- `L_type_desktop` — Table
- `Ladder_back` — Chair
- `Latice_back` — Chair
- `Left_Right_Double_Layer_Body` — Refrigerator
- `Middle_Curved_Handle` — Pliers
- `Multideck_Handle` — Knife
- `Multilevel_Tophandle` — KitchenPot
- `Mutiple_Layer_Body` — Safe
- `Office_armrest` — Chair
- `Parallel_Base` — Switch
- `PiShape_Handle` — Door
- `Press_Nozzle` — Dispenser
- `Quadfold_Spout` — Faucet
- `Rear_Curved_Handle` — Pliers
- `Rectangular_Baffle` — Pliers
- `Rectangular_Shaft` — Pliers
- `RegularX_Switch` — Faucet
- `RegularY_Switch` — Faucet
- `RegularZ_Switch` — Faucet
- `Regular_Base` — Laptop
- `Regular_Blade` — Shaver
- `Regular_Button` — Knife
- `Regular_Cap` — USB
- `Regular_Connector` — USB
- `Regular_Controller` — Safe
- `Regular_Leg` — Eyeglasses
- `Regular_Screen` — Laptop
- `Regular_backboard` — Table
- `Regular_cabinet` — Table
- `Regular_cap` — Shampoo
- `Regular_desktop` — Table
- `Regular_front_panel` — StorageFurniture
- `Regular_handle` — Doorhandle
- `Regular_hook` — Foldingrack
- `Regular_jaw` — Clip
- `Regular_leg_with_splat` — Chair
- `Regular_lever` — Clip
- `Regular_nozzle` — Shampoo
- `Regular_partition` — Table
- `Regular_rack` — Foldingrack
- `Regular_seat` — Chair
- `Regular_shaft` — Ruler
- `Regular_sublayer` — Table
- `Regular_with_splat_leg` — Table
- `Roller_Door` — Washingmachine
- `RotaryX_Switch` — Faucet
- `RotaryY_Switch` — Faucet
- `RotaryZ_Switch` — Faucet
- `RoundEnded_Body` — USB
- `RoundEnded_Cap` — USB
- `RoundFrame_Glasses` — Eyeglasses
- `Round_Glasses` — Eyeglasses
- `Round_Handle` — Safe
- `Round_Shaft` — Pliers
- `Round_Switch` — Switch
- `Round_seat` — Chair
- `Semi_Ring_Bracket` — Globe
- `Semi_Ring_Tophandle` — KitchenPot
- `Semi_Spherical_Body` — Kettle
- `Semi_Spherical_Cover` — KitchenPot
- `Separated_Cylindrical_Body` — Trashcan
- `ShowerRose_Spout` — Faucet
- `Simplied_Connector` — USB
- `SimplifiedZ_Switch` — Faucet
- `Simplified_Cover` — Stapler
- `Simplified_Wheel` — Lighter
- `Single_Cap` — Pen
- `Single_Leg` — Dishwasher
- `Slat_back` — Chair
- `Solid_armrest` — Chair
- `Solid_back` — Chair
- `Special_Base` — Globe
- `Spherical_Cylindrical_Body` — Kettle
- `Spherical_Handle` — Door
- `Splat_back` — Chair
- `Spray_Nozzle` — Dispenser
- `SquareEnded_Cap` — USB
- `Standard_Base` — Switch
- `Standard_Body` — Stapler
- `Standard_Connector` — Eyeglasses
- `Standard_Cover` — Kettle
- `Standard_Door` — Door
- `Standard_Doorframe` — Door
- `Standard_Guard` — Knife
- `Standard_Hinge` — Door
- `Standard_Knob` — Switch
- `Standard_Plug` — Switch
- `Standard_Screen` — Display
- `Standard_Sphere` — Globe
- `Standard_Support` — Eyeglasses
- `Standard_Wick` — Lighter
- `Standard_Windowframe` — Window
- `Star_Shaped_Base` — Globe
- `Storagefurniture_body` — StorageFurniture
- `Straight_Handle` — Pliers
- `Straight_Spout` — Kettle
- `Symmetrical_Window` — Window
- `Symmetrical_body` — Ruler
- `TShaped_Base` — Display
- `TShaped_Support` — Display
- `TShaped_Switch` — Faucet
- `TShaped_handle` — Doorhandle
- `T_Shaped_Connecter` — Safe
- `T_Shaped_Handle` — Knife
- `Table_Like_Base` — Globe
- `Tilted_Bracket` — Globe
- `Toothpaste_Body` — Gluestick
- `Toothpaste_body` — Shampoo
- `Top_With_Burner` — Oven
- `TrapezoidalFrame_Glasses` — Eyeglasses
- `Trapezoidal_Glasses` — Eyeglasses
- `Trifold_Clip` — Pen
- `Trifold_Leg` — Eyeglasses
- `Trifold_Sidehandle` — KitchenPot
- `Trifold_Spout` — Faucet
- `Trifold_Support` — Display
- `Trifold_Tophandle` — KitchenPot
- `Triple_Curved_Handle` — Scissors
- `UShapedXZ_Base` — Faucet
- `UShapedYZ_Base` — Faucet
- `Upright_Roller_Body` — Washingmachine
- `VerticalSlid_Window` — Window
- `Vshaped_Base` — Display