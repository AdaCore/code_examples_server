Derivation and Dynamic Dispatch
===============================

Despite the syntactic differences, derivation in Ada is similar to derivation (inheritance) in C++ or Java. For example, here is a type hierarchy where a child class overrides a method and adds a new method:

[Ada]

.. code-block:: ada

   type Root is tagged record
      F1 : Integer;
   end record;

   procedure Method_1 (Self : Root);

   type Child is new Root with record
      F2 : Integer;
   end Child;

   overriding
   procedure Method_1 (Self : Child);

   procedure Method_2 (Self : Child);


[C++]

.. code-block:: cpp

   class Root {
      public:
         int f1;
         virtual void method1 ();
   };

   class Child : public Root {
      public:
         int f2;
         virtual void method1 ();
         virtual void method2 ();
   };

[Java]

.. code-block:: java

   public class Root {
      public int f1;
      public void method1 ();
   }

   public class Child extends Root {
      public int f2;
      @Override
      public void method1 ();
      public void method2 ();
   }

Like Java, Ada primitives on tagged types are always subject to dispatching; there is no need to mark them **virtual**. Also like Java, there's an optional keyword **overriding** to ensure that a method is indeed overriding something from the parent type.

Unlike many other OOP languages, Ada differentiates between a reference to a specific tagged type, and a reference to an entire tagged type hierarchy. While *Root* is used to mean a specific type, *Root'Class*---a class-wide type---refers to either that type or any of its descendants. A method using a parameter of such a type cannot be overridden, and must be passed a parameter whose type is of any of *Root*'s descendants (including *Root* itself).

Next, we'll take a look at how each language finds the appropriate method to call within an OO class hierarchy; that is, their dispatching rules. In Java, calls to non-private instance methods are always dispatching. The only case where static selection of an instance method is possible is when calling from a method to the **super** version.

In C++, by default, calls to virtual methods are always dispatching. One common mistake is to use a by-copy parameter hoping that dispatching will reach the real object. For example:

.. code-block:: cpp

   void proc (Root p) {
      p.method1 ();
   }

   Root * v = new Child ();

   proc (*v);


In the above code, *p.method1 ()* will not dispatch. The call to *proc* makes a copy of the *Root* part of *v*, so inside *proc*,  *p.method1*() refers to the *method1*() of the root object. The intended behavior may be specified by using a reference instead of a copy:

.. code-block:: cpp

   void proc (Root & p) {
      p.method1 ();
   }

   Root * v = new Child ();

   proc (*v);

In Ada, tagged types are always passed by reference but dispatching only occurs on class-wide types. The following Ada code is equivalent to the latter C++ example:

.. code-block:: ada

   declare
      procedure Proc (P : Root'Class) is
      begin
         P.Method_1;
      end;

      type Root_Access is access all Root'Class;
      V : Root_Access := new Child;
   begin
      Proc (V.all);
   end;

Dispatching from within primitives can get tricky. Let's consider a call to *Method_1* in the implementation of *Method_2*. The first implementation that might come to mind is:

.. code-block:: ada

   procedure Method_2 (P : Root) is
   begin
      P.Method_1;
   end;

However, *Method_2* is called with a parameter that is of the definite type *Root*. More precisely, it is a definite view of a child. So, this call is not dispatching; it will always call *Method_1* of *Root* even if the object passed is a child of *Root*. To fix this, a view conversion is necessary:

.. code-block:: ada

   procedure Method_2 (P : Root) is
   begin
      Root'Class (P).Method_1;
   end;

This is called "redispatching." Be careful, because this is the most common mistake made in Ada when using OOP. In addition, it's possible to convert from a class wide view to a definite view, and to select a given primitive, like in C++:

[Ada]

.. code-block:: ada

   procedure Proc (P : Root'Class) is
   begin
      Root (P).Method_1;
   end;

[C++]

.. code-block:: cpp

   void proc (Root & p) {
      p.Root::method1 ();
   }
