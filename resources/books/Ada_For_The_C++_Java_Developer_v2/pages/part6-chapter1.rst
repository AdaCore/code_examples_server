Primitive Subprograms
=====================

Primitive subprograms in Ada are basically the subprograms that are eligible for inheritance / derivation. They are the equivalent of C++ member functions and Java instance methods. While in C++ and Java these subprograms are located within the nested scope of the type, in Ada they are simply declared in the same scope as the type. There's no syntactic indication that a subprogram is a primitive of a type.

The way to determine whether *P* is a primitive of a type *T* is if (1) it is declared in the same scope as *T*, and (2) it contains at least one parameter of type *T*, or returns a result of type *T*.

In C++ or Java, the self reference **this** is implicitly declared. It may need to be explicitly stated in certain situations, but usually it's omitted. In Ada the self-reference, called the `controlling parameter', must be explicitly specified in the subprogram parameter list. While it can be any parameter in the profile with any name, we'll focus on the typical case where the first parameter is used as the `self' parameter. Having the controlling parameter listed first also enables the use of OOP prefix notation which is convenient.

A **class** in C++ or Java corresponds to a **tagged type** in Ada. Here's an example of the declaration of an Ada tagged type with two parameters and some dispatching and non-dispatching primitives, with equivalent examples in C++ and Java:

[Ada]

.. code-block:: ada

   type T is tagged record
      V, W : Integer;
   end record;

   type T_Access is access all T;

   function F (V : T) return Integer;

   procedure P1 (V : access T);

   procedure P2 (V : T_Access);

[C++]

.. code-block:: cpp

   class T {
      public:
         int V, W;

         int F (void);

         void P1 (void);
   };

   void P2 (T * v);

[Java]

.. code-block:: java

   public class T {
         public int V, W;

         public int F (void) {};

         public void P1 (void) {};

         public static void P2 (T v) {};
   }

Note that *P2* is not a primitive of *T*---it does not have any parameters of type *T*. Its parameter is of type *T_Access*, which is a different type.

Once declared, primitives can be called like any subprogram with every necessary parameter specified, or called using prefix notation.  For example:

[Ada]

.. code-block:: ada

   declare
      V : T;
   begin
      V.P1;
   end;

[C++]

.. code-block:: cpp

   {
     T v;
     v.P1 ();
   }

[Java]

.. code-block:: java

   {
     T v = new T ();
     v.P1 ();
   }
