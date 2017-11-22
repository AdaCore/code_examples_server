Declaration Protection
======================

The package is the basic modularization unit of the Ada language, as is the class for Java and the header and implementation pair for C++. An Ada package contains three parts that, for GNAT, are separated into two files: *.ads* files contain public and private Ada specifications, and *.adb* files contain the implementation, or Ada bodies.

Java doesn't provide any means to cleanly separate the specification of methods from their implementation: they all appear in the same file. You can use interfaces to emulate having separate specifications, but this requires the use of OOP techniques which is not always practical.

Ada and C++ do offer separation between specifications and implementations out of the box, independent of OOP.

.. code-block:: ada

   package Package_Name is
      -- public specifications
   private
      -- private specifications
   end Package_Name;

   package body Package_Name is
      -- implementation
   end Package_Name;

Private types are useful for preventing the users of a package's types from depending on the types' implementation details. The **private** keyword splits the package spec into "public" and "private" parts. That is somewhat analogous to C++'s partitioning of the class construct into different sections with different visibility properties. In Java, the encapsulation has to be done field by field, but in Ada the entire definition of a type can be hidden. For example:

.. code-block:: ada

   package Types is
      type Type_1 is private;
      type Type_2 is private;
      type Type_3 is private;
      procedure P (X : Type_1);
      ...
   private
      procedure Q (Y : Type_1);
      type Type_1 is new Integer range 1 .. 1000;
      type Type_2 is array (Integer range 1 .. 1000) of Integer;
      type Type_3 is record
         A, B : Integer;
      end record;
   end Types;

Subprograms declared above the **private** separator (such as *P*) will be visible to the package user, and the ones below (such as *Q*) will not. The body of the package, the implementation, has access to both parts.
