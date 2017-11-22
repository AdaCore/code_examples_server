Generic Parameters
==================

Ada offers a wide variety of generic parameters which is difficult to translate into other languages. The parameters used during instantiation---and as a consequence those on which the generic unit may rely on---may be variables, types, or subprograms with certain properties. For example, the following provides a sort algorithm for any kind of array:

.. code-block:: ada

   generic
      type Component is private;
      type Index is (<>);
      with function "<" (Left, Right : Component) return Boolean;
      type Array_Type is array (Index range <>) of Component;
   procedure Sort (A : in out Array_Type);

The above declaration states that we need a type (*Component*), a discrete type (*Index*), a comparison subprogram (*"<"*), and an array definition (*Array_Type*). Given these, it's possible to write an algorithm that can sort any *Array_Type*. Note the usage of the **with** reserved word in front of the function name, to differentiate between the generic parameter and the beginning of the generic subprogram.

Here is a non-exhaustive overview of the kind of constraints that can be put on types:

.. code-block:: ada

   type T is private; -- T is a constrained type, such as Integer
   type T (<>) is private; -- T can be an unconstrained type, such as String
   type T is tagged private; -- T is a tagged type
   type T is new T2 with private; -- T is an extension of T2
   type T is (<>); -- T is a discrete type
   type T is range <>; -- T is an integer type
   type T is digits <>; -- T is a floating point type
   type T is access T2; -- T is an access type, T2 is its designated type
