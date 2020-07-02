//========================================================================
// ubmark-quicksort
//========================================================================
// This version (v1) is brought over directly from Fall 15.

#include "common.h"
#include "ubmark-quicksort.dat"

//------------------------------------------------------------------------
// quicksort-scalar
//------------------------------------------------------------------------

// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Add functions you may need
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
typedef struct{
  int *dest;
  int *src;
  int first;
  int last;
}arg_t;
//void swap( int *src,int a, int b)
//{
//  int temp=src[a];
//  src[a]=src[b];
//  src[b]=temp;
//}

__attribute__ ((noinline))
void quicksort_scalar( void *arg_vptr )
{
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement main function of serial quicksort
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  arg_t* arg_ptr=(arg_t*) arg_vptr;
  int *dest=arg_ptr->dest;
  int *src =arg_ptr->src;
  int first=arg_ptr->first;
  int last =arg_ptr->last;
  
  int pivot=last;
  int left=first;
  int right=last;
  if (first<last)
  {
    while(left<right)
    {
      while(src[right]>src[pivot] && right>first)
      {
        right-=1;
      }
      while(src[left]<=src[pivot] && left<last)
      {
        left+=1;
      }
      //swap(src,left,right);
      if (left < right)
      {
        int temp=src[left];
        src[left]=src[right];
        src[right]=temp;
      }

    }
    //swap(src,pivot,right);
    int temp2=src[pivot];
    src[pivot]=src[right];
    src[right]=temp2;
    arg_t arg0={dest,src,first,right-1};
    arg_t arg1={dest,src,right+1,last};
    quicksort_scalar(&arg0);
    quicksort_scalar(&arg1);
   // quicksort_scalar(dest, src, right-1,first);
    //quicksort_scalar(dest, src, last, right+1);
  }
    // implement quicksort algorithm here
    int i;
    // dummy copy src into dest
    for ( i = 0; i < size; i++ )
    {
      dest[i] = src[i];
    }
}

//------------------------------------------------------------------------
// verify_results
//------------------------------------------------------------------------

void verify_results( int dest[], int ref[], int size )
{
  int i;
  for ( i = 0; i < size; i++ ) {
    if ( !( dest[i] == ref[i] ) ) {
      test_fail( i, dest[i], ref[i] );
    }
  }
  test_pass();
}

//------------------------------------------------------------------------
// Test Harness
//------------------------------------------------------------------------

int main( int argc, char* argv[] )
{
  int dest[size];

  int i;
  for ( i = 0; i < size; i++ )
    dest[i] = 0;

  test_stats_on(); 
  arg_t arg2={dest,src,0,size-1};
  quicksort_scalar(&arg2);     //change original code
  test_stats_off();

  verify_results( dest, ref, size );

  return 0;
}
