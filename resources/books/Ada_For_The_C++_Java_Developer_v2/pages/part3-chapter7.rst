Arrays and Strings
==================

C++ arrays are pointers with offsets, but the same is not the case for Ada and Java. Arrays in the latter two languages are not interchangable with operations on pointers, and array types are considered first-class citizens. Arrays in Ada have dedicated semantics such as the availability of the array's boundaries at run-time. Therefore, unhandled array overflows are impossible unless checks are suppressed. Any discrete type can serve as an array index, and you can specify both the starting and ending bounds---the lower bound doesn't necessarily have to be 0. Most of the time, array types need to be explicitly declared prior to the declaration of an object of that array type.

Here's an example of declaring an array of 26 characters, initializing the values from 'a' to 'z':

[Ada]

.. code-block:: ada

   declare
      type Arr_Type is array (Integer range <>) of Character;
      Arr : Arr_Type (1 .. 26);
      C : Character := 'a';
   begin
      for I in Arr'Range loop
         Arr (I) := C;
         C := Character'Succ (C);
      end loop;
   end;

[C++]

.. code-block:: cpp

   char Arr [26];
   char C = 'a';

   for (int I = 0; I < 26; ++I) {
      Arr [I] = C;
      C = C + 1;
   }

[Java]

.. code-block:: java

   char [] Arr = new char [26];
   char C = 'a';

   for (int I = 0; I < Arr.length; ++I) {
      Arr [I] = C;
      C = C + 1;
   }

In C++ and Java, only the size of the array is given during declaration. In Ada, array index ranges are specified using two values of a discrete type. In this example, the array type declaration specifies the use of Integer as the index type, but does not provide any constraints (use <>, pronounced `box', to specify "no constraints").  The constraints are defined in the object declaration to be 1 to 26, inclusive. Arrays have an attribute called *'Range*. In our example, *Arr'Range* can also be expressed as *Arr'First .. Arr'Last*; both expressions will resolve to *1 .. 26*. So the *'Range* attribute supplies the bounds for our **for** loop. There is no risk of stating either of the bounds incorrectly, as one might do in C++ where "I <= 26" may be specified as the end-of-loop condition.

As in C++, Ada *String*\s are arrays of *Character*\s. The C++ or Java *String* class is the equivalent of the Ada type *Ada.Strings.Unbounded_String* which offers additional capabilities in exchange for some overhead. Ada strings, importantly, are not delimited with the special character '\\0' like they are in C++. It is not necessary because Ada uses the array's bounds to determine where the string starts and stops.

Ada's predefined *String* type is very straighforward to use:

.. code-block:: ada

   My_String : String (1 .. 26);

Unlike C++ and Java, Ada does not offer escape sequences such as '\\n'. Instead, explicit values from the *ASCII* package must be concatenated (via the concatenation operator, &). Here for example, is how to initialize a line of text ending with a new line:

   My_String : String := "This is a line with a end of line" & ASCII.LF;

You see here that no constraints are necessary for this variable definition. The initial value given allows the automatic determination of *My_String*'s bounds.

Ada offers high-level operations for copying, slicing, and assigning values to arrays. We'll start with assignment. In C++ or Java, the assignment operator doesn't make a copy of the value of an array, but only copies the address or reference to the target variable. In Ada, the actual array contents are duplicated. To get the above behavior, actual pointer types would have to be defined and used.

[Ada]

.. code-block:: ada

   declare
      type Arr_Type is array (Integer range <>) of Integer
      A1 : Arr_Type (1 .. 2);
      A2 : Arr_Type (1 .. 2);
   begin
      A1 (1) = 0;
      A1 (2) = 1;

      A2 := A1;
   end;

[C++]

.. code-block:: cpp

   int A1 [2];
   int A2 [2];

   A1 [0] = 0;
   A1 [1] = 1;

   for (int i = 0; i < 2; ++i) {
      A2 [i] = A1 [i];
   }


[Java]

.. code-block:: java

   int [] A1 = new int [2];
   int [] A2 = new int [2];

   A1 [0] = 0;
   A1 [1] = 1;

   A2 = Arrays.copyOf(A1, A1.length);

In all of the examples above, the source and destination arrays must have precisely the same number of elements. Ada allows you to easily specify a portion, or slice, of an array. So you can write the following:

[Ada]

.. code-block:: ada

   declare
      type Arr_Type is array (Integer range <>) of Integer
      A1 : Arr_Type (1 .. 10);
      A2 : Arr_Type (1 .. 5);
   begin
      A2 (1 .. 3) := A1 (4 .. 6);
   end;

This assigns the 4th, 5th, and 6th elements of *A1* into the 1st, 2nd, and 3rd elements of *A2*. Note that only the length matters here: the values of the indexes don't have to be equal; they slide automatically.

Ada also offers high level comparison operations which compare the contents of arrays as opposed to their addresses:

[Ada]

.. code-block:: ada

   declare
      type Arr_Type is array (Integer range <>) of Integer;
      A1 : Arr_Type (1 .. 2);
      A2 : Arr_Type (1 .. 2);
   begin
      if A1 = A2 then

[C++]

.. code-block:: cpp

   int A1 [2];
   int A2 [2];

   bool eq = true;

   for (int i = 0; i < 2; ++i) {
      if (A1 [i] != A2 [i]) {
         eq = false;
      }
   }

   if (eq) {


[Java]

.. code-block:: java

   int [] A1 = new int [2];
   int [] A2 = new int [2];

   if (A1.equals (A2)) {

You can assign to all the elements of an array in each language in different ways. In Ada, the number of elements to assign can be determined by looking at the right-hand side, the left-hand side, or both sides of the assignment. When bounds are known on the left-hand side, it's possible to use the **others** expression to define a default value for all the unspecified array elements. Therefore, you can write:

.. code-block:: ada

   declare
      type Arr_Type is array (Integer range <>) of Integer;
      A1 : Arr_Type := (1, 2, 3, 4, 5, 6, 7, 8, 9);
      A2 : Arr_Type (-2 .. 42) := (others => 0);
   begin
      A1 := (1, 2, 3, others => 10);

      -- use a slice to assign A2 elements 11 .. 19 to 1
      A2 (11 .. 19) := (others => 1);
   end;
