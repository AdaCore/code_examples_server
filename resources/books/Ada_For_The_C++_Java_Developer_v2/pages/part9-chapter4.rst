Protected Objects
=================

Although the rendezvous may be used to implement mutually exclusive access to a shared data object, an alternative (and generally preferable) style is through a *protected object*, an efficiently implementable mechanism that makes the effect more explicit. A protected object has a public interface (its *protected operations*) for accessing and manipulating the object's components (its private part). Mutual exclusion is enforced through a conceptual lock on the object, and encapsulation ensures that the only external access to the components are through the protected operations.

Two kinds of operations can be performed on such objects: read-write operations by procedures or entries, and read-only operations by functions. The lock mechanism is implemented so that it's possible to perform concurrent read operations but not concurrent write or read/write operations.

Let's reimplement our earlier tasking example with a protected object called *Counter*:

.. code-block:: ada

   protected Counter is
      function Get return Integer;
      procedure Increment;
      procedure Decrement;
   private
      Value : Integer := 0;
   end Counter;

   protected body Counter is
      function Get return Integer is
      begin
         return Value;
      end Get;

      procedure Increment is
      begin
        Value := Value + 1;
      end Increment;

      procedure Decrement is
      begin
         Value := Value - 1;
      end Decrement;
   end Counter;

Having two completely different ways to implement the same paradigm might seem complicated. However, in practice the actual problem to solve usually drives the choice between an active structure (a task) or a passive structure (a protected object).

A protected object can be accessed through prefix notation:

.. code-block:: ada

   Counter.Increment;
   Counter.Decrement;
   Put_Line (Integer'Image (Counter.Get));

A protected object may look like a package syntactically, since it contains declarations that can be accessed externally using prefix notation. However, the declaration of a protected object is extremely restricted; for example, no public data is allowed, no types can be declared inside, etc. And besides the syntactic differences, there is a critical semantic distinction: a protected object has a conceptual lock that guarantees mutual exclusion; there is no such lock for a package.

Like tasks, it's possible to declare protected types that can be instantiated several times:

.. code-block:: ada

   declare
      protected type Counter is
         -- as above
      end Counter;

      protected body Counter is
         -- as above
      end Counter;

      C1 : Counter;
      C2 : Counter;
   begin
      C1.Increment;
      C2.Decrement;
      ...
   end;

Protected objects and types can declare a procedure-like operation known as an "entry". An entry is somewhat similar to a procedure but includes a so-called *barrier condition* that must be true in order for the entry invocation to succeed. Calling a protected entry is thus a two step process: first, acquire the lock on the object, and then evaluate the barrier condition.  If the condition is true then the caller will execute the entry body.  If the condition is false, then the caller is placed in the queue for the entry, and relinquishes the lock.  Barrier conditions (for entries with non-empty queues) are reevaluated upon completion of protected procedures and protected entries.

Here's an example illustrating protected entries: a protected type that models a binary semaphore / persistent signal.

.. code-block:: ada

  protected type Binary_Semaphore is
    entry Wait;
    procedure Signal;
  private
    Signaled : Boolean := False;
  end Binary_Semaphore;

  protected body Binary_Semaphore is
    entry Wait when Signaled is
    begin
      Signaled := False;
    end Wait;

    procedure Signal is
    begin
      Signaled := True;
    end Signal;
  end Binary_Semaphore;

Ada concurrency features provide much further generality than what's been presented here. For additional information please consult one of the works cited in the *References* section.

