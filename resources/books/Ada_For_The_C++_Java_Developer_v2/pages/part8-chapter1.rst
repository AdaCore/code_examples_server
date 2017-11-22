Exceptions
**********

Exceptions are a mechanism for dealing with run-time occurrences that are rare, that usually correspond to errors (such as improperly formed input data), and whose occurrence causes an unconditional transfer of control.

.. todo::

   *This chapter needs some additional material, for example on how exception propagation works.  Or at least just say that it is similar to Java and C++*

Standard Exceptions
===================

Compared with Java and C++, the notion of an Ada exception is very simple. An exception in Ada is an object whose "type" is **exception**, as opposed to classes in Java or any type in C++. The only piece of user data that can be associated with an Ada exception is a String.  Basically, an exception in Ada can be raised, and it can be handled; information associated with an occurrence of an exception can be interrogated by a handler.

Ada makes heavy use of exceptions especially for data consistency check failures at run time. These include, but are not limited to, checking against type ranges and array boundaries, null pointers, various kind of concurrency properties, and functions not returning a value.  For example, the following piece of code will raise the exception *Constraint_Error*:

.. code-block:: ada

   procedure P is
      V : Positive;
   begin
      V := -1;
   end P;

In the above code, we're trying to assign a negative value to a variable that's declared to be positive. The range check takes place during the assignment operation, and the failure raises the *Constraint_Error* exception at that point. (Note that the compiler may give a warning that the value is out of range, but the error is manifest as a run-time exception.) Since there is no local handler, the exception is propagated to the caller; if *P* is the main procedure, then the program will be terminated.

Java and C++ **throw** and **catch** exceptions when **try**\ing code. All Ada code is already implicitly within **try** blocks, and exceptions are **raise**\d and handled.

[Ada]

.. code-block:: ada

   begin
      Some_Call;
   exception
      when Exception_1 =>
         Put_Line ("Error 1");
      when Exception_2 =>
         Put_Line ("Error 2");
      when others =>
         Put_Line ("Unknown error");
   end;

[C++]

.. code-block:: cpp

   try {
      someCall ();
   } catch (Exception1) {
      cout << "Error 1" << endl;
   } catch (Exception2) {
      cout << "Error 2" << endl;
   } catch (...) {
      cout << "Unknown error" << endl;
   }

[Java]

.. code-block:: java

   try {
      someCall ();
   } catch (Exception1 e1) {
      System.out.println ("Error 1");
   } catch (Exception2 e2) {
      System.out.println ("Error 2");
   } catch (Throwable e3) {
      System.out.println ("Unknown error");
   }

Raising and throwing exceptions while within an exception handler is permissible in all three languages.
