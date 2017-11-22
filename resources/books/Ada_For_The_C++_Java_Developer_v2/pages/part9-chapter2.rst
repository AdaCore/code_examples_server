Rendezvous
==========

.. todo::

   *Check if rendezvous is supported in Java or C++ through an API*

A rendezvous is a synchronization between two tasks, allowing them to exchange data and coordinate execution. Ada's rendezvous facility cannot be modeled with C++ or Java without complex machinery. Therefore, this section will just show examples written in Ada.

Let's consider the following example:

.. code-block:: ada

   with Ada.Text_IO; use Ada.Text_IO;

   procedure Main is

      task After is
         entry Go;
      end After ;

      task body After is
      begin
         accept Go;
         Put_Line ("After");
      end After;

   begin
      Put_Line ("Before");
      After.Go;
   end;

The *Go* **entry** declared in *After* is the external interface to the task. In the task body, the **accept** statement causes the task to wait for a call on the entry. This particular **entry** and **accept** pair doesn't do much more than cause the task to wait until *Main* calls *After.Go*. So, even though the two tasks start simultaneously and execute independently, they can coordinate via *Go*. Then, they both continue execution independently after the rendezvous.

The **entry**\/**accept** pair can take/pass parameters, and the **accept** statement can contain a sequence of statements; while these statements are executed, the caller is blocked.

Let's look at a more ambitious example. The rendezvous below accepts parameters and executes some code:

.. code-block:: ada

   with Ada.Text_IO; use Ada.Text_IO;

   procedure Main is

      task After is
         entry Go (Text : String);
      end After ;

      task body After is
      begin
         accept Go (Text : String) do
            Put_Line ("After: " & Text);
         end Go;
      end After;

   begin
      Put_Line ("Before");
      After.Go ("Main");;
   end;

In the above example, the *Put_Line* is placed in the **accept** statement. Here's a possible execution trace, assuming a uniprocessor:

1. At the **begin** of *Main*, task *After* is started and the main procedure is suspended.

2. *After* reaches the **accept** statement and is suspended, since there is no pending call on the *Go* entry.

3. The main procedure is awakened and executes the *Put_Line* invocation, displaying the string "Before".

4. The main procedure calls the *Go* entry.  Since *After* is suspended on its **accept** statement for this entry, the call succeeds.

5. Tha main procedure is suspended, and the task *After* is awakened to execute the body of the **accept** statement. The actual parameter "Main" is passed to the **accept** statement, and the *Put_Line* invocation is executed. As a result, the string "After: Main" is displayed.

6. When the **accept** statement is completed, both the *After* task and the main procedure are ready to run.  Suppose that the *Main* procedure is given the processor. It reaches its **end**, but the local task *After* has not yet terminated.  The main procedure is suspended.

7. The *After* task continues, and terminates since it is at its **end**.  The main procedure is resumed, and it too can terminate since its dependent task has terminated.

The above description is a conceptual model; in practice the implementation can perform various optimizations to avoid unnecessary context switches.

