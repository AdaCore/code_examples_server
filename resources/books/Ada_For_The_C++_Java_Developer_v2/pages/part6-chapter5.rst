Abstract Types and Interfaces
=============================

Ada, C++ and Java all offer similar functionality in terms of abstract classes, or pure virtual classes. It is necessary in Ada and Java to explicitly specify whether a tagged type or class is **abstract**, whereas in C++ the presence of a pure virtual function implicitly makes the class an abstract base class. For example:

[Ada]

.. code-block:: ada

  package P is

      type T is abstract tagged private;

      procedure Method (Self : T) is abstract;
   private
      type T is abstract tagged record
         F1, F2 : Integer;
      end record;

   end P;

[C++]

.. code-block:: cpp

   class T {
      public:
         virtual void method () = 0;
      protected:
         int f1, f2;
   };


[Java]

.. code-block:: java

   public abstract class T {
      public abstract void method1 ();
      protected int f1, f2;
   };

All abstract methods must be implemented when implementing a concrete type based on an abstract type.

Ada doesn't offer multiple inheritance the way C++ does, but it does support a Java-like notion of interfaces. An interface is like a C++ pure virtual class with no attributes and only abstract members. While an Ada tagged type can inherit from at most one tagged type, it may implement multiple interfaces. For example:

[Ada]

.. code-block:: ada

   type Root is tagged record
      F1 : Integer;
   end record;
   procedure M1 (Self : Root);

   type I1 is interface;
   procedure M2 (Self : I1) is abstract;

   type I2 is interface;
   procedure M3 (Self : I2) is abstract;

   type Child is new Root and I1 and I2 with record
      F2 : Integer;
   end record;

   -- M1 implicitly inherited by Child
   procedure M2 (Self : Child);
   procedure M3 (Self : Child);

[C++]

.. code-block:: cpp

   class Root {
      public:
         virtual void M1();
         int f1;
   };

   class I1 {
      public:
         virtual void M2 () = 0;
   };

   class I2 {
      public:
         virtual void M3 () = 0;
   };

   class Child : public Root, I1, I2 {
      public:
         int f2;
         virtual void M2 ();
         virtual void M3 ();
   };

[Java]

.. code-block:: java

   public class Root {
      public void M1();
      public int f1;
   }

   public interface I1 {
      public void M2 () = 0;
   }

   public class I2 {
      public void M3 () = 0;
   }

   public class Child extends Root implements I1, I2 {
         public int f2;
         public void M2 ();
         public void M3 ();
   }
