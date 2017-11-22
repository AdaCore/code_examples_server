Heterogeneous Data Structures
=============================

In Ada, there's no distinction between **struct** and **class** as there is in C++. All heterogeneous data structures are **record**\s. Here are some simple records:

[Ada]

.. code-block:: ada

   declare
      type R is record
         A, B : Integer;
         C    : Float;
      end record;

      V : R;
   begin
      V.A := 0;
   end;


[C++]

.. code-block:: cpp

   struct R {
      int A, B;
      float C;
   };

   R V;
   V.A = 0;

[Java]

.. code-block:: java

   class R {
      public int A, B;
      public float C;
   }

   R V = new R ();
   V.A = 0;

Ada allows specification of default values for fields just like C++ and Java. The values specified can take the form of an ordered list of values, a named list of values, or an incomplete list followed by **others** => <> to specify that fields not listed will take their default values. For example:

.. code-block:: ada

   type R is record
      A, B : Integer := 0;
      C    : Float := 0.0;
   end record;

   V1 : R => (1, 2, 1.0);
   V2 : R => (A => 1, B => 2, C => 1.0);
   V3 : R => (C => 1.0, A => 1, B => 2);
   V3 : R => (C => 1.0, others => <>);
