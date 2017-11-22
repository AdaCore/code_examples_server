Loops
=====

In Ada, loops always start with the **loop** reserved word and end with **end loop**. To leave the loop, use **exit**---the C++ and Java equivalent being **break**. This statement can specify a terminating condition using the **exit when** syntax. The **loop** opening the block can be preceded by a **while** or a **for**.

The **while** loop is the simplest one, and is very similar across all three languages:

[Ada]

.. code-block:: ada

   while Variable < 10_000 loop
      Variable := Variable * 2;
   end loop;

[C++]

.. code-block:: cpp

   while (Variable < 10000) {
      Variable = Variable * 2;
   }

[Java]

.. code-block:: java

  while (Variable < 10000) {
      Variable = Variable * 2;
  }

Ada's **for** loop, however, is quite different from that in C++ and Java. It always increments or decrements a loop index within a discrete range. The loop index (or "loop parameter" in Ada parlance) is local to the scope of the loop and is implicitly incremented or decremented at each iteration of the loop statements; the program cannot directly modify its value. The type of the loop parameter is derived from the range. The range is always given in ascending order even if the loop iterates in descending order. If the starting bound is greater than the ending bound, the interval is considered to be empty and the loop contents will not be executed. To specify a loop iteration in decreasing order, use the **reverse** reserved word. Here are examples of loops going in both directions:

[Ada]

.. code-block:: ada

   --  Outputs 0, 1, 2, ..., 9
   for Variable in 0 .. 9 loop
      Put_Line (Integer'Image (Variable));
   end loop;

   --  Outputs 9, 8, 7, ..., 0
   for Variable in reverse 0 .. 9 loop
      Put_Line (Integer'Image (Variable));
   end loop;

[C++]

.. code-block:: cpp

   //  Outputs 0, 1, 2, ..., 9
   for (int Variable = 0; Variable <= 9; Variable++) {
      cout << Variable << endl;
   }

   //  Outputs 9, 8, 7, ..., 0
   for (int Variable = 9; Variable >=0; Variable--) {
      cout << Variable << endl;
   }

[Java]

.. code-block:: java

   //  Outputs 0, 1, 2, ..., 9
   for (int Variable = 0; Variable <= 9; Variable++) {
      System.out.println (Variable);
   }

   //  Outputs 9, 8, 7, ..., 0
   for (int Variable = 9; Variable >= 0; Variable--) {
      System.out.println (Variable);
   }

Ada uses the *Integer* type's *'Image* attribute to convert a numerical value to a String. There is no implicit conversion between *Integer* and *String* as there is in C++ and Java. We'll have a more in-depth look at such attributes later on.

It's easy to express iteration over the contents of a container (for instance, an array, a list, or a map) in Ada and Java. For example, assuming that *Int_List* is defined as an array of Integer values, you can use:

[Ada]

.. code-block:: ada

   for I of Int_List loop
      Put_Line (Integer'Image (I));
   end loop;

[Java]

.. code-block:: java

   for (int i : Int_List) {
      System.out.println (i);
   }
