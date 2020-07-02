//========================================================================
// mtbmark-sort-v1
//========================================================================
// This version (v1) is brought over directly from Fall 15. It uses
// quicksort to sort each fourth of the elements, and then run 3 times of
// two-way merge. The first two merge runs are parallelized.

#include "common.h"
#include "mtbmark-sort.dat"

// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Implement multicore sorting
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
//------------------------------------------------------------------------
// verify_results
//------------------------------------------------------------------------
typedef struct{
  int *dest;
  int *src;
  int first;
  int last;
}arg_t;

typedef struct{
  int *dest;
  int *src;
  int start;
  int len;
  int end;
}arg_m;

__attribute__ ((noinline))
void merge(void *arg_vptr)
{
  arg_m* arg_ptr=(arg_m*) arg_vptr;
  int *dest=arg_ptr->dest;
  int *src=arg_ptr->src;
  int start=arg_ptr->start;
  int len=arg_ptr->len;
  int end=arg_ptr->end;
  
  int i=start;
  int j=start+len;
  for (int t=start;t<end;t++)
  {
    if (i>len+start-1)
    {
      dest[t]=src[j];
      j++;
    }
    else if(j>end-1)
    {
      dest[t]=src[i];
      i++;
    }
    else if(src[i]<=src[j])
    {
      dest[t]=src[i];
      i++;
    }
    else if(src[i]>src[j])
    {
      dest[t]=src[j];
      j++;
    }
  }
}
  
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
    
  }
    // implement quicksort algorithm here
    int i;
    // dummy copy src into dest
    for ( i = 0; i < size; i++ )
    {
      dest[i] = src[i];
    }
}

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

  // Initialize the bthread (bare thread)

  bthread_init();

  // Initialize dest array, which stores the final result.

  int dest[size];

  //--------------------------------------------------------------------
  // Start counting stats
  //--------------------------------------------------------------------

  test_stats_on();

  //int i = 0;

  // Because we need in-place sorting, we need to create a mutable temp
  // array.
  int temp[size];
  int temp1[size];
  int block=size/4;
  
  
  arg_t arg2={temp,src,0,block-1};
  arg_t arg3={temp,src,block,2*block-1};
  arg_t arg4={temp,src,2*block,3*block-1};
  arg_t arg5={temp,src,3*block,size-1};

  bthread_spawn(1, &quicksort_scalar, &arg3);
  bthread_spawn(2, &quicksort_scalar, &arg4);
  bthread_spawn(3, &quicksort_scalar, &arg5);
  quicksort_scalar(&arg2);
  
  bthread_join(1);
  bthread_join(2);
  bthread_join(3);
  
  arg_m arg6={temp1,temp,0,block,2*block};
  arg_m arg7={temp1,temp,2*block,block,size};
  
  bthread_spawn(1, &merge,&arg7);
  merge(&arg6);
  bthread_join(1);
  
  arg_m arg8={dest,temp1,0,2*block,size};
  merge(&arg8);
  
  //for ( i = 0; i < size; i++ ) {
  //  temp0[i] = src[i];
    
  //}

  
  //bthread_spawn(1, &quicksort_scalar, &arg3);
  //bthread_join(1);
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: distribute work and call sort_scalar()
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: do bthread_join(), do the final reduction step here
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  //--------------------------------------------------------------------
  // Stop counting stats
  //--------------------------------------------------------------------

  test_stats_off();

  // verifies solution

  //verify_results( dest, ref, size );
    if ( bthread_get_core_id() == 0 )
      verify_results( dest, ref, size );

  return 0;
}
