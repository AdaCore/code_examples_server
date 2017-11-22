Selective Rendezvous
====================

The accept statement by itself can only wait for a single event (call) at a time. The **select** statement allows a task to listen for multiple events simultaneously, and then to deal with the first event to occur. This feature is illustrated by the task below, which maintains an integer value that is modified by other tasks that call *Increment*, *Decrement*, and *Get*:

.. code-block:: ada

   task Counter is
      entry Get (Result : out Integer);
      entry Increment;
      entry Decrement;
   end Counter;

   task body Counter is
      Value : Integer := 0;
   begin
      loop
         select
            accept Increment do
               Value := Value + 1;
            end Increment;
         or
            accept Decrement do
               Value := Value - 1;
            end Decrement;
         or
            accept Get (Result : out Integer) do
               Result := Value;
            end Get;
         or
            delay 1.0 * Minute;
            exit;
         end select;
      end loop;
   end Counter;

When the task's statement flow reaches the **select**, it will wait for all four events---three entries and a delay---in parallel. If the delay of one minute is exceeded, the task will execute the statements following the **delay** statement (and in this case will exit the loop, in effect terminating the task). The accept bodies for the *Increment*, *Decrement*, or *Get* entries will be otherwise executed as they're called. These four sections of the **select** statement are mutually exclusive: at each iteration of the loop, only one will be invoked. This is a critical point; if the task had been written as a package, with procedures for the various operations, then a "race condition" could occur where multiple tasks simultaneously calling, say, *Increment*, cause the value to only get incremented once. In the tasking version, if multiple tasks simultaneously call *Increment* then only one at a time will be accepted, and the value will be incremented by each of the tasks when it is accepted.

More specifically, each entry has an associated queue of pending callers.  If a task calls one of the entries and *Counter* is not ready to accept the call (i.e., if *Counter* is not suspended at the **select** statement) then the calling task is suspended, and placed in the queue of the entry that it is calling.  From the perspective of the *Counter* task, at any iteration of the loop there are several possibilities:

* There is no call pending on any of the entries.  In this case *Counter* is suspended.  It will be awakened by the first of two events: a call on one of its entries (which will then be immediately accepted), or the expiration of the one minute delay (whose effect was noted above).

* There is a call pending on exactly one of the entries.  In this case control passes to the **select** branch with an **accept** statement for that entry.  The choice of which caller to accept, if more than one, depends on the queuing policy, which can be specified via a pragma defined in the Real-Time Systems Annex of the Ada standard; the default is First-In First-Out.

* There are calls pending on more than one entry.  In this case one of the entries with pending callers is chosen, and then one of the callers is chosen to be de-queued (the choices depend on the queueing policy).
