Pointers
========

Pointers, references, and access types differ in significant ways across the languages that we are examining. In C++, pointers are integral to a basic understanding of the language, from array manipulation to proper declaration and use of function parameters. Java goes a step further: everything is a reference, except for primitive types like scalars. Ada's design goes in the other direction: it makes more features available without requiring the explicit use of pointers.

We'll continue this section by explaining the difference between objects allocated on the stack and objects allocated on the heap using the following example:

[Ada]

.. code-block:: ada

   declare
      type R is record
         A, B : Integer;
      end record;

      V1, V2 : R;
   begin
      V1.A := 0;
      V2 := V1;
      V2.A := 1;
   end;

[C++]

.. code-block:: cpp

   struct R {
      int A, B;
   };

   R V1, V2;
   V1.A = 0;
   V2 = V1;
   V2.A = 1;

[Java]

.. code-block:: java

   public class R {
      public int A, B;
   }

   R V1, V2;
   V1 = new R ();
   V1.A = 0;
   V2 = V1;
   V2.A = 1;

There's a fundamental difference between the Ada and C++ semantics above and the semantics for Java. In Ada and C++, objects are allocated on the stack and are directly accessed. *V1* and *V2* are two different objects and the assignment statement copies the value of *V1* into *V2*. In Java, *V1* and *V2* are two `references' to objects of class *R*. Note that when *V1* and *V2* are declared, no actual object of class *R* yet exists in memory: it has to be allocated later with the **new** allocator operator. After the assignment *V2 = V1*, there's only one R object in memory: the assignment is a reference assignment, not a value assignment. At the end of the Java code, *V1* and *V2* are two references to the same objects and the *V2.A = 1* statement changes the field of that one object, while in the Ada and the C++ case *V1* and *V2* are two distinct objects.

To obtain similar behavior in Ada, you can use pointers. It can be done through Ada's `access type':

[Ada]

.. code-block:: ada

   declare
      type R is record
         A, B : Integer;
      end record;
      type R_Access is access R;

      V1 : R_Access;
      V2 : R_Access;
   begin
      V1 := new R;
      V1.A := 0;
      V2 := V1;
      V2.A := 1;
   end;

[C++]

.. code-block:: cpp

   struct R {
      int A, B;
   };

   R * V1, * V2;
   V1 = new R ();
   V1->A = 0;
   V2 = V1;
   V2->A = 0;

For those coming from the Java world: there's no garbage collector in Ada, so objects allocated by the **new** operator need to be expressly freed.

Dereferencing is performed automatically in certain situations, for instance when it is clear that the type required is the dereferenced object rather than the pointer itself, or when accessing record members via a pointer. To explicitly dereference an access variable, append **.all**. The equivalent of *V1->A* in C++ can be written either as *V1.A* or *V1.all.A*.

Pointers to scalar objects in Ada and C++ look like:

[Ada]

.. code-block:: ada

   procedure Main is
      type A_Int is access Integer;
      Var : A_Int := new Integer;
   begin
      Var.all := 0;
   end Main;

[C++]

.. code-block:: cpp

   int main (int argc, char *argv[]) {
     int * Var = new int;
     *Var = 0;
   }

An initializer can be specified with the allocation by appending *'(value)*:

.. code-block:: ada

   Var : A_Int := new Integer'(0);

When using Ada pointers to reference objects on the stack, the referenced objects must be declared as being **aliased**. This directs the compiler to implement the object using a memory region, rather than using registers or eliminating it entirely via optimization. The access type needs to be declared as either **access all** (if the referenced object needs to be assigned to) or **access constant** (if the referenced object is a constant). The *'Access* attribute works like the C++ & operator to get a pointer to the object, but with a "scope accessibility" check to prevent references to objects that have gone out of scope. For example:

[Ada]

.. code-block:: ada

   type A_Int is access all Integer;
   Var : aliased Integer;
   Ptr : A_Int := Var'Access;

[C++]

.. code-block:: cpp

   int Var;
   int * Ptr = &Var;

To deallocate objects from the heap in Ada, it is necessary to use a deallocation subprogram that accepts a specific access type. A generic procedure is provided that can be customized to fit your needs---it's called *Ada.Unchecked_Deallocation*. To create your customized deallocator (that is, to instantiate this generic), you must provide the object type as well as the access type as follows:

[Ada]

.. code-block:: ada

   with Ada.Unchecked_Deallocation;
   procedure Main is
      type Integer_Access is access all Integer;
      procedure Free is new Ada.Unchecked_Deallocation (Integer, Integer_Access);
      My_Pointer : Integer_Access := new Integer;
   begin
      Free (My_Pointer);
   end Main;

[C++]

.. code-block:: cpp

   int main (int argc, char *argv[]) {
     int * my_pointer = new int;
     delete my_pointer;
   }
