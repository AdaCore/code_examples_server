Embedded Assembly Code
======================

When performing low-level development, such as at the kernel or hardware driver level, there can be times when it is necessary to implement functionality with assembly code.

Every Ada compiler has its own conventions for embedding assembly code, based on the hardware platform and the supported assembler(s). Our examples here will work with GNAT and GCC on the x86 architecture.

All x86 processors since the Intel Pentium offer the *rdtsc* instruction, which tells us the number of cycles since the last processor reset. It takes no inputs and places an unsigned 64 bit value split between the *edx* and *eax* registers.

GNAT provides a subprogram called *System.Machine_Code.Asm* that can be used for assembly code insertion. You can specify a string to pass to the assembler as well as source-level variables to be used for input and output:

.. code-block:: ada

   with System.Machine_Code; use System.Machine_Code;
   with Interfaces;          use Interfaces;

   function Get_Processor_Cycles return Unsigned_64 is
      Low, High : Unsigned_32;
      Counter   : Unsigned_64;
   begin
      Asm ("rdtsc",
           Outputs =>
             (Unsigned_32'Asm_Output ("=a", High),
              Unsigned_32'Asm_Output ("=d", Low)),
           Volatile => True);

      Counter :=
        Unsigned_64 (High) * 2 ** 32 +
        Unsigned_64 (Low);

      return Counter;
   end Get_Processor_Cycles;

The *Unsigned_32'Asm_Output* clauses above provide associations between machine registers and source-level variables to be updated. "=a" and "=d" refer to the *eax* and *edx* machine registers, respectively. The use of the *Unsigned_32* and *Unsigned_64* types from package *Interfaces* ensures correct representation of the data. We assemble the two 32-bit values to form a single 64 bit value.

We set the *Volatile* parameter to *True* to tell the compiler that invoking this instruction multiple times with the same inputs can result in different outputs. This eliminates the possibility that the compiler will optimize multiple invocations into a single call.

With optimization turned on, the GNAT compiler is smart enough to use the *eax* and *edx* registers to implement the *High* and *Low* variables, resulting in zero overhead for the assembly interface.

The machine code insertion interface provides many features beyond what was shown here. More information can be found in the GNAT User's Guide, and the GNAT Reference manual.
