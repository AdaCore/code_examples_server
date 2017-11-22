Custom Exceptions
=================

Custom exception declarations resemble object declarations, and they can be created in Ada using the **exception** keyword:

.. code-block:: ada

   My_Exception : exception;

Your exceptions can then be raised using a **raise** statement, optionally accompanied by a message following the **with** reserved word:

[Ada]

.. code-block:: ada

   raise My_Exception with "Some message";

[C++]

.. code-block:: cpp

   throw My_Exception ("Some message");

[Java]

.. code-block:: java

   throw new My_Exception ("Some message");

Language defined exceptions can also be raised in the same manner:

.. code-block:: ada

   raise Constraint_Error;
