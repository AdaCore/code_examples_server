Attributes
==========

Attributes start with a single apostrophe ("tick"), and they allow you to query properties of, and perform certain actions on, declared entities such as types, objects, and subprograms. For example, you can determine the first and last bounds of scalar types, get the sizes of objects and types, and convert values to and from strings. This section provides an overview of how attributes work. For more information on the many attributes defined by the language, you can refer directly to the Ada Language Reference Manual.

The *'Image* and *'Value* attributes allow you to transform a scalar value into a *String* and vice-versa. For example:

.. code-block:: ada

   declare
      A : Integer := 99;
   begin
      Put_Line (Integer'Image (A));
      A := Integer'Value ("99");
   end;

Certain attributes are provided only for certain kinds of types. For example, the *'Val* and *'Pos* attributes for an enumeration type associates a discrete value with its position among its peers. One circuitous way of moving to the next character of the ASCII table is:

[Ada]

.. code-block:: ada

   declare
      C : Character := 'a';
   begin
      C := Character'Val (Character'Pos (C) + 1);
   end;

A more concise way to get the next value in Ada is to use the *'Succ* attribute:

.. code-block:: ada

   declare
      C : Character := 'a';
   begin
      C := Character'Succ (C);
   end;

You can get the previous value using the *'Pred* attribute. Here is the equivalent in C++ and Java:

[C++]

.. code-block:: cpp

   char c = 'a';
   c++;

[Java]

.. code-block:: java

   char c = 'a';
   c++;

Other interesting examples are the *'First* and *'Last* attributes which, respectively, return the first and last values of a scalar type. Using 32-bit integers, for instance, *Integer'First* returns -2\ :superscript:`31` and *Integer'Last* returns 2\ :superscript:`31` - 1.
