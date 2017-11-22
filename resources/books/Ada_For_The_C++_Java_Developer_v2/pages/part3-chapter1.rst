Strong Typing
=============

One of the main characteristics of Ada is its strong typing (i.e., relative absence of implicit type conversions). This may take some getting used to. For example, you can't divide an integer by a float. You need to perform the division operation using values of the same type, so one value must be explicitly converted to match the type of the other (in this case the more likely conversion is from integer to float). Ada is designed to guarantee that what's done by the program is what's meant by the programmer, leaving as little room for compiler interpretation as possible. Let's have a look at the following example:

[Ada]

.. code-block:: ada

   procedure Strong_Typing is
      Alpha  : Integer := 1;
      Beta   : Integer := 10;
      Result : Float;
   begin
      Result := Float (Alpha) / Float (Beta);
   end Strong_Typing;

[C++]

.. code-block:: cpp

   void weakTyping (void) {
      int   alpha = 1;
      int   beta = 10;
      float result;

      result = alpha / beta;
   }

[Java]

.. code-block:: java


   void weakTyping () {
      int   alpha = 1;
      int   beta = 10;
      float result;

      result = alpha / beta;
   }

Are the three programs above equivalent? It may seem like Ada is just adding extra complexity by forcing you to make the conversion from Integer to Float explicit. In fact it significantly changes the behavior of the computation. While the Ada code performs a floating point operation **1.0 / 10.0** and stores 0.1 in *Result*, the C++ and Java versions instead store 0.0 in *result*. This is because the C++ and Java versions perform an integer operation between two integer variables: **1 / 10** is **0**. The result of the integer division is then converted to a *float* and stored. Errors of this sort can be very hard to locate in complex pieces of code, and systematic specification of how the operation should be interpreted helps to avoid this class of errors. If an integer division was actually intended in the Ada case, it is still necessary to explicitly convert the final result to *Float*:

.. code-block:: ada

   -- Perform an Integer division then convert to Float
   Result := Float (Alpha / Beta);

In Ada, a floating point literal must be written with both an integral and decimal part. **10** is not a valid literal for a floating point value, while **10.0** is.
