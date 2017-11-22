Constructors and Destructors
============================

Ada does not have constructors and destructors in quite the same way as C++ and Java, but there is analagous functionality in Ada in the form of default initialization and finalization.

Default initialization may be specified for a record component and will occur if a variable of the record type is not assigned a value at initialization. For example:

.. code-block:: ada

   type T is tagged record
      F : Integer := Compute_Default_F;
   end record;

   function Compute_Default_F return Integer is
   begin
      Put_Line ("Compute");
      return 0;
   end Compute_Default_F;

   V1 : T;
   V2 : T := (F => 0);

In the declaration of *V1*, *T.F* receives a value computed by the subprogram *Compute_Default_F*. This is part of the default initialization. *V2* is initialized manually and thus will not use the default initialization.

For additional expressive power, Ada provides a type called *Ada.Finalization.Controlled* from which you can derive your own type. Then, by overriding the *Initialize* procedure you can create a constructor for the type:

.. code-block:: ada

   type T is new Ada.Finalization.Controlled with record
      F : Integer;
   end record;

   procedure Initialize (Self : in out T) is
   begin
      Put_Line ("Compute");
      Self.F := 0;
   end Initialize;

   V1 : T;
   V2 : T := (V => 0);

Again, this default initialization subprogram is only called for *V1*; *V2* is initialized manually. Furthermore, unlike a C++ or Java constructor, *Initialize* is a normal subprogram and does not perform any additional initialization such as calling the parent's initialization routines.

When deriving from *Controlled*, it's also possible to override the subprogram *Finalize*, which is like a destructor and is called for object finalization. Like *Initialize*, this is a regular subprogram. Do not expect any other finalizers to be automatically invoked for you.

Controlled types also provide functionality that essentially allows overriding the meaning of the assignment operation, and are useful for defining types that manage their own storage reclamation (for example, implementing a reference count reclamation strategy).
