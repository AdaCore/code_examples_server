Concurrency
***********

.. todo::

  *Update with comparison to new C++11 concurrency features*

Tasks
=====

Java and Ada both provide support for concurrency in the language. The C++ language has added a concurrency facility in its most recent revision, C++11, but we are assuming that most C++ programmers are not (yet) familiar with these new features. We thus provide the following mock API for C++ which is similar to the Java *Thread* class:

.. code-block:: cpp

   class Thread {
      public:
         virtual void run (); // code to execute
         void start (); // starts a thread and then call run ()
         void join (); // waits until the thread is finished
   };

Each of the following examples will display the 26 letters of the alphabet twice, using two concurrent threads/tasks. Since there is no synchronization between the two threads of control in any of the examples, the output may be interspersed.

[Ada]

.. code-block:: ada

   procedure Main is -- implicitly called by the environment task
      task My_Task;

      task body My_Task is
      begin
         for I in 'A' .. 'Z' loop
            Put_Line (I);
         end loop;
      end My_Task;
   begin
      for I in 'A' .. 'Z' loop
         Put_Line (I);
      end loop;
   end Main;

[C++]

.. code-block:: cpp

   class MyThread : public Thread {
      public:

      void run () {
         for (char i = 'A'; i <= 'Z'; ++i) {
            cout << i << endl;
         }
      }
   };

   int main (int argc, char ** argv) {
      MyThread myTask;
      myTask.start ();

      for (char i = 'A'; i <= 'Z'; ++i) {
         cout << i << endl;
      }

      myTask.join ();

      return 0;
   }

[Java]

.. code-block:: java

   public class Main {
      static class MyThread extends Thread {
         public void run () {
            for (char i = 'A'; i <= 'Z'; ++i) {
               System.out.println (i);
            }
         }
      }

      public static void main (String args) {
         MyThread myTask = new MyThread ();
         myTask.start ();

         for (char i = 'A'; i <= 'Z'; ++i) {
            System.out.println (i);
         }
         myTask.join ();
      }
   }
Any number of Ada tasks may be declared in any declarative region. A task declaration is very similar to a procedure or package declaration. They all start automatically when control reaches the **begin**. A block will not exit until all sequences of statements defined within that scope, including those in tasks, have been completed.

A task type is a generalization of a task object; each object of a task type has the same behavior. A declared object of a task type is started within the scope where it is declared, and control does not leave that scope until the task has terminated.

An Ada task type is somewhat analogous to a Java *Thread* subclass, but in Java the instances of such a subclass are always dynamically allocated.  In Ada an instance of a task type may either be declared or dynamically allocated.

Task types can be parametrized; the parameter serves the same purpose as an argument to a constructor in Java. The following example creates 10 tasks, each of which displays a subset of the alphabet contained between the parameter and the 'Z' Character.  As with the earlier example, since there is no synchronization among the tasks, the output may be interspersed depending on the implementation's task scheduling algorithm.


[Ada]

.. code-block:: ada

   task type My_Task (First : Character);

   task body My_Task (First : Character) is
   begin
      for I in First .. 'Z' loop
         Put_Line (I);
      end loop;
   end My_Task;

   procedure Main is
      Tab : array (0 .. 9) of My_Task ('G');
   begin
      null;
   end Main;

[C++]

.. code-block:: cpp

   class MyThread : public Thread {
      public:

      char first;

      void run () {
         for (char i = first; i <= 'Z'; ++i) {
            cout << i << endl;
         }
      }
   };

   int main (int argc, char ** argv) {
      MyThread tab [10];

      for (int i = 0; i < 9; ++i) {
         tab [i].first = 'G';
         tab [i].start ();
      }

      for (int i = 0; i < 9; ++i) {
         tab [i].join ();
      }

      return 0;
   }

[Java]

.. code-block:: java

   public class MyThread extends Thread {
      public char first;

      public MyThread (char first){
         this.first = first;
      }

      public void run () {
         for (char i = first; i <= 'Z'; ++i) {
            cout << i << endl;
         }
      }
   }

   public class Main {
      public static void main (String args) {
         MyThread [] tab = new MyThread [10];

         for (int i = 0; i < 9; ++i) {
            tab [i] = new MyThread ('G');
            tab [i].start ();
         }

         for (int i = 0; i < 9; ++i) {
            tab [i].join ();
         }
      }
   }

In Ada a task may be allocated on the heap as opposed to the stack. The task will then start as soon as it has been allocated, and terminates when its work is completed. This model is probably the one that's the most similar to Java:


[Ada]

.. code-block:: ada

   type Ptr_Task is access My_Task;

   procedure Main is
      T : Ptr_Task;
   begin
      T := new My_Task ('G');
   end Main;

[C++]

.. code-block:: cpp

   int main (int argc, char ** argv) {
      MyThread * t = new MyThread ();
      t->first = 'G';
      t->start ();
      return 0;
   }

[Java]

.. code-block:: java

   public class Main {
      public static void main (String args) {
         MyThread t = new MyThread ('G');

         t.start ();
      }
   }
