Application-Defined Types
=========================

Ada's type system encourages programmers to think about data at a high level of abstraction. The compiler will at times output a simple efficient machine instruction for a full line of source code (and some instructions can be eliminated entirely). The careful programmer's concern that the operation really makes sense in the real world would be satisfied, and so would the programmer's concern about performance.

The next example below defines two different metrics: area and distance. Mixing these two metrics must be done with great care, as certain operations do not make sense, like adding an area to a distance. Others require knowledge of the expected semantics; for example, multiplying two distances. To help avoid errors, Ada requires that each of the binary operators "+", "-", "*", and "/" for integer and floating-point types take operands of the same type and return a value of that type.

.. code-block:: ada

   procedure Main is
      type Distance is new Float;
      type Area is new Float;

      D1 : Distance := 2.0;
      D2 : Distance := 3.0;
      A  : Area;
   begin
      D1 := D1 + D2;        -- OK
      D1 := D1 + A;         -- NOT OK: incompatible types for "+" operator
      A  := D1 * D2;        -- NOT OK: incompatible types for ":=" assignment
      A  := Area (D1 * D2); -- OK
   end Main;

Even though the **Distance** and **Area** types above are just **Float**\s, the compiler does not allow arbitrary mixing of values of these different types. An explicit conversion (which does not necessarily mean any additional object code) is necessary.

The predefined Ada rules are not perfect; they admit some problematic cases (for example multiplying two **Distance**\s yields a **Distance**) and prohibit some useful cases (for example multiplying two **Distance**\s should deliver an **Area**). These situations can be handled through other mechanisms. A predefined operation can be identified as **abstract** to make it unavailable; overloading can be used to give new interpretations to existing operator symbols, for example allowing an operator to return a value from a type different from its operands; and more generally, GNAT has introduced a facility that helps perform dimensionality checking.

Ada enumerations work similarly to C++ and Java's *enum*\s.

[Ada]

.. code-block:: ada

   type Day is
     (Monday,
      Tuesday,
      Wednesday,
      Thursday,
      Friday,
      Saturday,
      Sunday);

[C++]

.. code-block:: cpp

   enum Day {
      Monday,
      Tuesday,
      Wednesday,
      Thursday,
      Friday,
      Saturday,
      Sunday};

[Java]

.. code-block:: java

   enum Day {
      Monday,
      Tuesday,
      Wednesday,
      Thursday,
      Friday,
      Saturday,
      Sunday}

But even though such enumerations may be implemented using a machine word, at the language level Ada will not confuse the fact that *Monday* is a *Day* and is not an *Integer*. You can compare a *Day* with another *Day*, though. To specify implementation details like the numeric values that correspond with enumeration values in C++ you include them in the original *enum* statement:

[C++]

.. code-block:: cpp

   enum Day {
      Monday    = 10,
      Tuesday   = 11,
      Wednesday = 12,
      Thursday  = 13,
      Friday    = 14,
      Saturday  = 15,
      Sunday    = 16};

But in Ada you must use both a type definition for *Day* as well as a separate *representation clause* for it like:

[Ada]

.. code-block:: ada

   for Day use
     (Monday    => 10,
      Tuesday   => 11,
      Wednesday => 12,
      Thursday  => 13,
      Friday    => 14,
      Saturday  => 15,
      Sunday    => 16);
