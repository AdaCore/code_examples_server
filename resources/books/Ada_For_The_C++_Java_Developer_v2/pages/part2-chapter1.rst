Statements and Declarations
===========================

The following code samples are all equivalent, and illustrate the use of comments and working with integer variables:

[Ada]

.. code-block:: ada

   --
   --  Ada program to declare and modify Integers
   --
   procedure Main is
      --  Variable declarations
      A, B : Integer := 0;
      C    : Integer := 100;
      D    : Integer;
   begin
      --  Ada uses a regular assignment statement for incrementation.
      A := A + 1;

      --  Regular addition
      D := A + B + C;
   end Main;

[C++]

.. code-block:: cpp

   /*
    *  C++ program to declare and modify ints
    */
   int main(int argc, const char* argv[]) {
      //  Variable declarations
      int a = 0, b = 0, c = 100, d;

      //  C++ shorthand for incrementation
      a++;

      //  Regular addition
      d = a + b + c;
   }

[Java]

.. code-block:: java

   /*
    *  Java program to declare and modify ints
    */
   public class Main {
      public static void main(String [] argv) {
         //  Variable declarations
         int a = 0, b = 0, c = 100, d;

         //  Java shorthand for incrementation
         a++;

         //  Regular addition
         d = a + b + c;
      }
   }

Statements are terminated by semicolons in all three languages. In Ada, blocks of code are surrounded by the reserved words **begin** and **end** rather than by curly braces.  We can use both multi-line and single-line comment styles in the C++ and Java code, and only single-line comments in the Ada code.

Ada requires variable declarations to be made in a specific area called the *declarative part*, seen here before the **begin** keyword. Variable declarations start with the identifier in Ada, as opposed to starting with the type as in C++ and Java (also note Ada's use of the **:** separator). Specifying initializers is different as well: in Ada an initialization expression can apply to multiple variables (but will be evaluated separately for each), whereas in C++ and Java each variable is initialized individually. In all three languages, if you use a function as an initializer and that function returns different values on every invocation, each variable will get initialized to a different value.

Let's move on to the imperative statements. Ada does not provide **++** or ``--`` shorthand expressions for increment/decrement operations; it is necessary to use a full assignment statement. The **:=** symbol is used in Ada to perform value assignment. Unlike C++'s and Java's **=** symbol, **:=** can not be used as part of an expression. So, a statement like *A* **:=** *B* **:=** *C;* doesn't make sense to an Ada compiler, and neither does a clause like "**if** *A* **:=** *B* **then** ...." Both are compile-time errors.

You can nest a block of code within an outer block if you want to create an inner scope:

.. code-block:: ada

   with Ada.Text_IO; use Ada.Text_IO;

   procedure Main is
   begin
      Put_Line ("Before the inner block");

      declare
         Alpha : Integer := 0;
      begin
         Alpha := Alpha + 1;
         Put_Line ("Now inside the inner block");
      end;

      Put_Line ("After the inner block");
   end Main;

It is OK to have an empty declarative part or to omit the declarative part entirely---just start the inner block with **begin** if you have no declarations to make. However it is not OK to have an empty sequence of statements. You must at least provide a **null;** statement, which does nothing and indicates that the omission of statements is intentional.
