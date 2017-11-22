Type Ranges
===========

Contracts can be associated with types and variables, to refine values and define what are considered valid values. The most common kind of contract is a *range constraint* introduced with the **range** reserved word, for example:

.. code-block:: ada

   procedure Main is
      type Grade is range 0 .. 100;

      G1, G2  : Grade;
      N       : Integer;
   begin
      ...                -- Initialization of N
      G1 := 80;          -- OK
      G1 := N;           -- Illegal (type mismatch)
      G1 := Grade (N);   -- Legal, run-time range check
      G2 := G1 + 10;     -- Legal, run-time range check
      G1 := (G1 + G2)/2; -- Legal, run-time range check
   end Main;

In the above example, *Grade* is a new integer type associated with a range check. Range checks are dynamic and are meant to enforce the property that no object of the given type can have a value outside the specified range. In this example, the first assignment to *G1* is correct and will not raise a run-time exceprion. Assigning *N* to *G1* is illegal since *Grade* is a different type than *Integer*. Converting *N* to *Grade* makes the assignment legal, and a range check on the conversion confirms that the value is within 0 .. 100.  Assigning *G1+10* to *G2* is legal since **+** for *Grade* returns a *Grade* (note that the literal *10* is interpreted as a *Grade* value in this context), and again there is a range check.

The final assignment illustrates an interesting but subtle point. The subexpression *G1 + G2* may be outside the range of *Grade*, but the final result will be in range. Nevertheless, depending on the representation chosen for *Grade*, the addition may overflow. If the compiler represents *Grade* values as signed 8-bit integers (i.e., machine numbers in the range -128 .. 127) then the sum *G1+G2* may exceed 127, resulting in an integer overflow. To prevent this, you can use explicit conversions and perform the computation in a sufficiently large integer type, for example:

.. code-block:: ada

      G1 := Grade (Integer (G1) + Integer (G2)) / 2);

Range checks are useful for detecting errors as early as possible. However, there may be some impact on performance. Modern compilers do know how to remove redundant checks, and you can deactivate these checks altogether if you have sufficient confidence that your code will function correctly.

Types can be derived from the representation of any other type. The new derived type can be associated with new constraints and operations. Going back to the *Day* example, one can write:

.. code-block:: ada

   type Business_Day is new Day range Monday .. Friday;
   type Weekend_Day is new Day range Saturday .. Sunday;

Since these are new types, implicit conversions are not allowed. In this case, it's more natural to create a new set of constraints for the same type, instead of making completely new ones. This is the idea behind `subtypes' in Ada. A subtype is a type with optional additional constraints. For example:

.. code-block:: ada

   subtype Business_Day is Day range Monday .. Friday;
   subtype Weekend_Day is Day range Saturday .. Sunday;
   subtype Dice_Throw is Integer range 1 .. 6;

These declarations don't create new types, just new names for constrained ranges of their base types.
