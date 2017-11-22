Interfacing with C
==================

Much effort was spent making Ada easy to interface with other languages. The *Interfaces* package hierarchy and the pragmas *Convention*, *Import*, and *Export* allow you to make inter-language calls while observing proper data representation for each language.

Let's start with the following C code:

.. code-block:: c

   struct my_struct {
      int A, B;
   };

   void call (my_struct * p) {
      printf ("%d", p->A);
   }

To call that function from Ada, the Ada compiler requires a description of the data structure to pass as well as a description of the function itself. To capture how the C **struct** *my_struct* is represented, we can use the following record along with a **pragma** *Convention*. The pragma directs the compiler to lay out the data in memory the way a C compiler would.

.. code-block:: ada

   type my_struct is record
      A : Interfaces.C.int;
      B : Interfaces.C.int;
   end record;
   pragma Convention (C, my_struct);

Describing a foreign subprogram call to Ada code is called "binding" and it is performed in two stages. First, an Ada subprogram specification equivalent to the C function is coded. A C function returning a value maps to an Ada function, and a **void** function maps to an Ada procedure. Then, rather than implementing the subprogram using Ada code, we use a **pragma** *Import*:

.. code-block:: ada

   procedure Call (V : my_struct);
   pragma Import (C, Call, "call"); -- Third argument optional

The *Import* pragma specifies that whenever *Call* is invokeed by Ada code, it should invoke the *call* function with the C calling convention.

And that's all that's necessary. Here's an example of a call to *Call*:

.. code-block:: ada

   declare
      V : my_struct := (A => 1, B => 2);
   begin
      Call (V);
   end;

You can also make Ada subprograms available to C code, and examples of this can be found in the GNAT User's Guide. Interfacing with C++ and Java use implementation-dependent features that are also available with GNAT.
