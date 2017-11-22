Encapsulation
=============

While done at the class level for C++ and Java, Ada encapsulation occurs at the package level and targets all entities of the language, as opposed to only methods and attributes. For example:

[Ada]

.. code-block:: ada

   package Pck is
      type T is tagged private;
      procedure Method1 (V : T);
   private
      type T is tagged record
         F1, F2 : Integer;
      end record;
      procedure Method2 (V : T);
   end Pck;

[C++]

.. code-block:: cpp

   class T {
      public:
         virtual void method1 ();
      protected:
         int f1, f2;
         virtual void method2 ();
   };

[Java]

.. code-block:: java

   public class T {
      public void method1 ();
      protected int f1, f2;
      protected void method2 ();
   }

The C++ and Java code's use of **protected** and the Ada code's use of **private** here demonstrates how to map these concepts between languages. Indeed, the private part of an Ada child package would have visibility of the private part of its parents, mimicking the notion of **protected**. Only entities declared in the package body are completely isolated from access.
