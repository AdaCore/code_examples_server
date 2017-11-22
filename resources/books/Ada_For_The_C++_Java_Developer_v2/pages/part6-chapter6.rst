Invariants
==========

.. todo::
  *This section is not part of the OOP material and should be moved to a different chapter*


Any private type in Ada may be associated with a *Type_Invariant* contract. An invariant is a property of a type that must always be true after the return from of any of its primitive subprograms. (The invariant might not be maintained during the execution of the primitive subprograms, but will be true after the return.) Let's take the following example:

.. code-block:: ada

   package Int_List_Pkg is

      type Int_List (Max_Length : Natural) is private
        with Type_Invariant => Is_Sorted (Int_List);

      function Is_Sorted (List : Int_List) return Boolean;

      type Int_Array is array (Positive range <>) of Integer;

      function To_Int_List (Ints : Int_Array) return Int_List;

      function To_Int_Array (List : Int_List) return Int_Array;

      function "&" (Left, Right : Int_List) return Int_List;

      ... -- Other subprograms
   private

      type Int_List (Max_Length : Natural) is record
         Length : Natural;
         Data   : Int_Array (1..Max_Length);
      end record;


      function Is_Sorted (List : Int_List) return Boolean is
         (for all I in List.Data'First .. List.Length-1 =>
               List.Data (I) <= List.Data (I+1));

   end Int_List_Pkg;

   package body Int_List_Pkg is

      procedure Sort (Ints : in out Int_Array) is
      begin
         ... Your favorite sorting algorithm
      end Sort;

      function To_Int_List (Ints : Int_Array) return Int_List is
         List : Int_List :=
          (Max_Length => Ints'Length,
           Length     => Ints'Length,
           Data       => Ints);
      begin
         Sort (List.Data);
         return List;
      end To_Int_List;

      function To_Int_Array (List : Int_List) return Int_Array is
      begin
         return List.Data;
      end To_Int_Array;

      function "&" (Left, Right : Int_List) return Int_List is
         Ints : Int_Array := Left.Data & Right.Data;
      begin
         Sort (Ints);
         return To_Int_List (Ints);
      end "&";

      ... -- Other subprograms
   end Int_List_Pkg;

The *Is_Sorted* function checks that the type stays consistent. It will be called at the exit of every primitive above. It is permissible if the conditions of the invariant aren't met during execution of the primitive. In *To_Int_List* for example, if the source array is not in sorted order, the invariant will not be satisfied at the "begin",  but it will be checked at the end.
