Generalized Type Contracts: Subtype Predicates
==============================================

Range checks are a special form of type contracts; a more general method is provided by Ada subtype predicates, introduced in Ada 2012. A subtype predicate is a boolean expression defining conditions that are required for a given type or subtype. For example, the *Dice_Throw* subtype shown above can be defined in the following way:

.. code-block:: ada

   subtype Dice_Throw is Integer
      with Dynamic_Predicate => Dice_Throw in 1 .. 6;

The clause beginning with **with** introduces an Ada `aspect', which is additional information provided for declared entities such as types and subtypes. The *Dynamic_Predicate* aspect is the most general form. Within the predicate expression, the name of the (sub)type refers to the current value of the (sub)type. The predicate is checked on assignment, parameter passing, and in several other contexts. There is a "Static_Predicate" form which introduce some optimization and constrains on the form of these predicates, outside of the scope of this document.

Of course, predicates are useful beyond just expressing ranges. They can be used to represent types with arbitrary constraints, in particular types with discontinuities, for example:

.. code-block:: ada

   type Not_Null is new Integer
      with Dynamic_Predicate => Not_Null /= 0;

   type Even is new Integer
      with Dynamic_Predicate => Even mod 2 = 0;

