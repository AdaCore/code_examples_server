Using Entities from Packages
============================

Entities declared in the visible part of a package specification can be made accessible using a **with** clause that references the package, which is similar to the C++ **#include** directive. Visibility is implicit in Java: you can always access all classes located in your *CLASSPATH*. After a **with** clause, entities needs to be prefixed by the name of their package, like a C++ namespace or a Java package. This prefix can be omitted if a **use** clause is employed, similar to a C++ **using namespace** or a Java **import**.

[Ada]

.. code-block:: ada

   -- pck.ads

   package Pck is
      My_Glob : Integer;
   end Pck;

   -- main.adb

   with Pck;

   procedure Main is
   begin
      Pck.My_Glob := 0;
   end Main;

[C++]

.. code-block:: cpp

   // pck.h

   namespace pck {
      extern int myGlob;
   }

   // pck.cpp

   namespace pck {
      int myGlob;
   }

   // main.cpp

   #include "pck.h"

   int main (int argc, char ** argv) {
      pck::myGlob = 0;
   }

[Java]

.. code-block:: java

   // Globals.java

   package pck;

   public class Globals {
      public static int myGlob;
   }

   // Main.java

   public class Main {
      public static void main (String [] argv) {
         pck.Globals.myGlob = 0;
      }
   }

