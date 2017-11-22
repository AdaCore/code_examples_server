Conditions
==========

The use of the **if** statement:

[Ada]

.. code-block:: ada

   if Variable > 0 then
      Put_Line (" > 0 ");
   elsif Variable < 0 then
      Put_Line (" < 0 ");
   else
      Put_Line (" = 0 ");
   end if;

[C++]

.. code-block:: cpp

   if (Variable > 0)
      cout << " > 0 " << endl;
   else if (Variable < 0)
      cout << " < 0 " << endl;
   else
      cout << " = 0 " << endl;

[Java]

.. code-block:: java

   if (Variable > 0)
      System.out.println (" > 0 ");
   else if (Variable < 0)
      System.out.println (" < 0 ");
   else
      System.out.println (" = 0 ");

In Ada, everything that appears between the **if** and **then** keywords is the conditional expression---no parentheses required. Comparison operators are the same, except for equality (**=**) and inequality (**/=**). The english words **not**, **and**, and **or** replace the symbols **!**, **&**, and **|**, respectively, for performing boolean operations.

It's more customary to use **&&** and **||** in C++ and Java than **&** and **|** when writing boolean expressions. The difference is that **&&** and **||** are short-circuit operators, which evaluate terms only as necessary, and **&** and **|** will unconditionally evaluate all terms. In Ada, **and** and **or** will evaluate all terms; **and then** and **or else** direct the compiler to employ short circuit evaluation.

Here are what switch/case statements look like:

[Ada]

.. code-block:: ada

   case Variable is
      when 0 =>
         Put_Line ("Zero");
      when 1 .. 9 =>
         Put_Line ("Positive Digit");
      when 10 | 12 | 14 | 16 | 18 =>
         Put_Line ("Even Number between 10 and 18");
      when others =>
         Put_Line ("Something else");
   end case;

[C++]

.. code-block:: cpp

   switch (Variable) {
      case 0:
         cout << "Zero" << endl;
         break;
      case 1: case 2: case 3: case 4: case 5:
      case 6: case 7: case 8: case 9:
         cout << "Positive Digit" << endl;
         break;
      case 10: case 12: case 14: case 16: case 18:
         cout << "Even Number between 10 and 18" << endl;
         break;
      default:
         cout << "Something else";
   }

[Java]

.. code-block:: java

   switch (Variable) {
      case 0:
         System.out.println ("Zero");
         break;
      case 1: case 2: case 3: case 4: case 5:
      case 6: case 7: case 8: case 9:
         System.out.println ("Positive Digit");
         break;
      case 10: case 12: case 14: case 16: case 18:
         System.out.println ("Even Number between 10 and 18");
         break;
      default:
         System.out.println ("Something else");
   }

In Ada, the **case** and **end case** lines surround the whole case statement, and each case starts with **when**. So, when programming in Ada, replace **switch** with **case**, and replace **case** with **when**.

Case statements in Ada require the use of discrete types (integers or enumeration types), and require all possible cases to be covered by **when** statements. If not all the cases are handled, or if duplicate cases exist, the program will not compile. The default case, **default:** in C++ and Java, can be specified using **when others =>** in Ada.

In Ada, the **break** instruction is implicit and program execution will never fall through to subsequent cases. In order to combine cases, you can specify ranges using **..** and enumerate disjoint values using **|** which neatly replaces the multiple **case** statements seen in the C++ and Java versions.
