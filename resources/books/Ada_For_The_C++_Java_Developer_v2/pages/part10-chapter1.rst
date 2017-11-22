Low Level Programming
*********************

Representation Clauses
======================

We've seen in the previous chapters how Ada can be used to describe high level semantics and architecture. The beauty of the language, however, is that it can be used all the way down to the lowest levels of the development, including embedded assembly code or bit-level data management.

One very interesting feature of the language is that, unlike C, for example, there are no data representation constraints unless specified by the developer. This means that the compiler is free to choose the best trade-off in terms of representation vs. performance. Let's start with the following example:

[Ada]

.. code-block:: ada

   type R is record
      V  : Integer range 0 .. 255;
      B1 : Boolean;
      B2 : Boolean;
   end record
   with Pack;

[C++]

.. code-block:: cpp

   struct R {
      unsigned int v:8;
      bool b1;
      bool b2;
   };

[Java]

.. code-block:: java

   public class R {
      public byte v;
      public boolean b1;
      public boolean b2;
   }

The Ada and the C++ code above both represent efforts to create an object that's as small as possible. Controlling data size is not possible in Java, but the language does specify the size of values for the primitive types.

Although the C++ and Ada code are equivalent in this particular example, there's an interesting semantic difference. In C++, the number of bits required by each field needs to be specified. Here, we're stating that *v* is only 8 bits, effectively representing values from 0 to 255. In Ada, it's the other way around: the developer specifies the range of values required and the compiler decides how to represent things, optimizing for speed or size. The **Pack** aspect declared at the end of the record specifies that the compiler should optimize for size even at the expense of decreased speed in accessing record components.

Other representation clauses can be specified as well, along with compile-time consistency checks between requirements in terms of available values and specified sizes. This is particularly useful when a specific layout is necessary; for example when interfacing with hardware, a driver, or a communication protocol. Here's how to specify a specific data layout based on the previous example:

.. code-block:: ada

   type R is record
      V  : Integer range 0 .. 255;
      B1 : Boolean;
      B2 : Boolean;
   end record;

   for R use record
      --  Occupy the first bit of the first byte.
      B1 at 0 range 0 .. 0;

      --  Occupy the last 7 bits of the first byte,
      --  as well as the first bit of the second byte.
      V  at 0 range 1 .. 8;

      --  Occupy the second bit of the second byte.
      B2 at 1 range 1 .. 1;
   end record;

We omit the **with** *Pack* directive and instead use a record representation clause following the record declaration. The compiler is directed to spread objects of type *R* across two bytes. The layout we're specifying here is fairly inefficient to work with on any machine, but you can have the compiler construct the most efficient methods for access, rather than coding your own machine-dependent bit-level methods manually.
