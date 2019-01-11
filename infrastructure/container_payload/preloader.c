#include <unistd.h>
#include <stdio.h>
#include <unistd.h>

pid_t fork(void) {
  fprintf(stdout, "fork not allowed\n");  
  
   _exit(1);
}

pid_t vfork(void) {
   fprintf(stdout, "vfork not allowed\n");  
   _exit(1);
}

int execve(const char *filename, char *const argv[],
	   char *const envp[]) {
  fprintf(stdout, "execve not allowed\n");
  _exit(1);
}
