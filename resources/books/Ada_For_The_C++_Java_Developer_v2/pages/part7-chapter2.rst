Generic Packages
================

Next, we're going to create a generic unit containing data and subprograms. In Java or C++, this is done through a class, while in Ada, it's a `generic package'. The Ada and C++ model is fundamentally different from the Java model. Indeed, upon instantiation, Ada and C++ generic data are duplicated; that is, if they contain global variables (Ada) or static attributes (C++), each instance will have its own copy of the variable, properly typed and independent from the others. In Java, generics are only a mechanism to have the compiler do consistency checks, but all instances are actually sharing the same data where the generic parameters are replaced by *java.lang.Object*. Let's look at the following example:

[Ada]

.. code-block:: ada

     generic
        type T is private;
     package Gen is
        type C is tagged record
           V : T;
        end record;

        G : Integer;
     end Gen;

[C++]

.. code-block:: cpp

   template <class T>
   class C{
      public:
        T v;
        static int G;
   };


[Java]

.. code-block:: java

   public class C <T> {
        public T v;
        public static int G;
   }

In all three cases, there's an instance variable (*v*) and a static variable (*G*). Let's now look at the behavior (and syntax) of these three instantiations:


[Ada]

.. code-block:: ada

   declare
      package I1 is new Gen (Integer);
      package I2 is new Gen (Integer);
      subtype Str10 is String (1..10);
      package I3 is new Gen (Str10);
   begin
      I1.G := 0;
      I2.G := 1;
      I3.G := 2;
   end;

[C++]

.. code-block:: cpp

   C <int>::G = 0;
   C <int>::G = 1;
   C <char *>::G = 2;


[Java]

.. code-block:: java

   C.G = 0;
   C.G = 1;
   C.G = 2;

In the Java case, we access the generic entity directly without using a parametric type. This is because there's really only one instance of *C*, with each instance sharing the same global variable *G*. In C++, the instances are implicit, so it's not possible to create two different instances with the same parameters. The first two assignments are manipulating the same global while the third one is manipulating a different instance. In the Ada case, the three instances are explicitly created, named, and referenced individually.
