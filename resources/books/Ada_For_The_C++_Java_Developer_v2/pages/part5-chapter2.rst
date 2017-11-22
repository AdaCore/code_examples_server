Hierarchical Packages
=====================

Ada packages can be organized into hierarchies. A child unit can be declared in the following way:

.. code-block:: ada

   -- root-child.ads

   package Root.Child is
      --  package spec goes here
   end Root.Child;

   -- root-child.adb

   package body Root.Child is
      --  package body goes here
   end Root.Child;

Here, *Root.Child* is a child package of *Root*. The public part of *Root.Child* has access to the public part of *Root*. The private part of *Child* has access to the private part of *Root*, which is one of the main advantages of child packages. However, there is no visibility relationship between the two bodies. One common way to use this capability is to define subsystems around a hierarchical naming scheme.
