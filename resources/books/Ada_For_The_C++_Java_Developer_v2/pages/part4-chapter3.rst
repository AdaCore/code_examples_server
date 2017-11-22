Subprogram Contracts
====================

You can express the expected inputs and outputs of subprograms by specifying subprogram contracts. The compiler can then check for valid conditions to exist when a subprogram is called and can check that the return value makes sense. Ada allows defining contracts in the form of *Pre* and *Post* conditions; this facility was introduced in Ada 2012. They look like:

.. code-block:: ada

   function Divide (Left, Right : Float) return Float
      with Pre  => Right /= 0.0,
           Post => Divide'Result * Right < Left + 0.0001
                   and then Divide'Result * Right > Left - 0.0001;

The above example adds a *Pre* condition, stating that *Right* cannot be equal to 0.0. While the IEEE floating point standard permits divide-by-zero, you may have determined that use of the result could still lead to issues in a particular application. Writing a contract helps to detect this as early as possible. This declaration also provides a *Post* condition on the result.

Postconditions can also be expressed relative to the value of the input:

.. code-block:: ada

   procedure Increment (V : in out Integer)
      with Pre  => V < Integer'Last,
           Post => V = V'Old + 1;

*V'Old* in the postcondition represents the value that *V* had before entering *Increment*.
