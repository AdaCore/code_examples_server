General Form
============

Subroutines in C++ and Java are always expressed as functions (methods) which may or may not return a value. Ada explicitly differentiates between functions and procedures. Functions must return a value and procedures must not. Ada uses the more general term "subprogram" to refer to both functions and procedures.

Parameters can be passed in three distinct modes: **in**, which is the default, is for input parameters, whose value is provided by the caller and cannot be changed by the subprogram. **out** is for output parameters, with no initial value, to be assigned by the subprogram and returned to the caller. **in out** is a parameter with an initial value provided by the caller, which can be modified by the subprogram and returned to the caller (more or less the equivalent of a non-constant reference in C++). Ada also provides **access** parameters, in effect an explicit pass-by-reference indicator.

In Ada the programmer specifies how the parameter will be used and in general the compiler decides how it will be passed (i.e., by copy or by reference). (There are some exceptions to the "in general". For example, parameters of scalar types are always passed by copy, for all three modes.) C++ has the programmer specify how to pass the parameter, and Java forces primitive type parameters to be passed by copy and all other parameters to be passed by reference. For this reason, a 1:1 mapping between Ada and Java isn't obvious but here's an attempt to show these differences:

[Ada]

.. code-block:: ada

   procedure Proc
    (Var1 : Integer;
     Var2 : out Integer;
     Var3 : in out Integer);

   function Func (Var : Integer) return Integer;

   procedure Proc
    (Var1 : Integer;
     Var2 : out Integer;
     Var3 : in out Integer)
   is
   begin
      Var2 := Func (Var1);
      Var3 := Var3 + 1;
   end Proc;

   function Func (Var : Integer) return Integer
   is
   begin
      return Var + 1;
   end Func;

[C++]

.. code-block:: cpp

   void Proc
     (int Var1,
      int & Var2,
      int & Var3);

   int Func (int Var);

   void Proc
     (int Var1,
      int & Var2,
      int & Var3) {

      Var2 = Func (Var1);
      Var3 = Var3 + 1;
   }

   int Func (int Var) {
      return Var + 1;
   }

[Java]

.. code-block:: java

   public class ProcData {
      public int Var2;
      public int Var3;

      public void Proc (int Var1) {
         Var2 = Func (Var1);
         Var3 = Var3 + 1;
      }
   }

   int Func (int Var) {
      return Var + 1;
   }

The first two declarations for *Proc* and *Func* are specifications of the subprograms which are being provided later. Although optional here, it's still considered good practice to separately define specifications and implementations in order to make it easier to read the program. In Ada and C++, a function that has not yet been seen cannot be used. Here, *Proc* can call *Func* because its specification has been declared. In Java, it's fine to have the declaration of the subprogram later .

Parameters in Ada subprogram declarations are separated with semicolons, because commas are reserved for listing multiple parameters of the same type. Parameter declaration syntax is the same as variable declaration syntax, including default values for parameters. If there are no parameters, the parentheses must be omitted entirely from both the declaration and invocation of the subprogram.
