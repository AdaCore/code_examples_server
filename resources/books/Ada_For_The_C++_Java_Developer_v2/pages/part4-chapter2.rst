Overloading
===========

Different subprograms may share the same name; this is called "overloading." As long as the subprogram signatures (subprogram name, parameter types, and return types) are different, the compiler will be able to resolve the calls to the proper destinations. For example:

.. code-block:: ada

   function Value (Str : String) return Integer;
   function Value (Str : String) return Float;

   V : Integer := Value ("8");

The Ada compiler knows that an assignment to *V* requires an *Integer*. So, it chooses the *Value* function that returns an *Integer* to satisfy this requirement.

Operators in Ada can be treated as functions too. This allows you to define local operators that override operators defined at an outer scope, and provide overloaded operators that operate on and compare different types. To express an operator as a function, enclose it in quotes:

[Ada]

.. code-block:: ada

   function "=" (Left : Day; Right : Integer) return Boolean;

[C++]

.. code-block:: cpp

   bool operator = (Day Left, int Right);
