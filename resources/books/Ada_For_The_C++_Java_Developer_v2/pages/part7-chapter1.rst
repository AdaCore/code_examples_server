Generics
********

Ada, C++, and Java all have support for generics or templates, but on different sets of language entities. A C++ template can be applied to a class or a function. So can a Java generic. An Ada generic can be either a package or a subprogram.

Generic Subprograms
===================

A feature that is similar across all three languages is the subprogram. To swap two objects:

[Ada]

.. code-block:: ada

   generic
      type A_Type is private;
   procedure Swap (Left, Right : in out A_Type) is
      Temp : A_Type := Left;
   begin
      Left  := Right;
      Right := Temp;
   end Swap;

[C++]

.. code-block:: cpp

   template <class AType>
   AType swap (AType & left, AType & right) {
      AType temp = left;
      left  = right;
      right = temp;
   }

[Java]

.. code-block:: java

   public <AType> void swap (AType left, AType right) {
      AType temp = left;
      left  = right;
      right = temp;
   }

And examples of using these:

[Ada]

.. code-block:: ada

   declare
      type R is record
         F1, F2 : Integer;
      end record;

      procedure Swap_R is new Swap (R);
      A, B : R;
   begin
      ...
      Swap_R (A, B);
   end;

[C++]

.. code-block:: cpp

   class R {
      public:
         int f1, f2;
   };

   R a, b;
   ...
   swap (a, b);

[Java]

.. code-block:: java

   public class R {
      public int f1, f2;
   }

   R a = new R(), b = new R();
   ...
   swap (a, b);

The C++ template and Java generic both become usable once defined. The Ada generic needs to be explicitly instantiated using a local name and the generic's parameters.
