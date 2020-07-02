#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>

int size=8;
int size2=128;
int size3=150;

int INT_MAX =2147483647;
int INT_MIN =-2147483648;

typedef struct{
  int *dest;
  int *src;
  int first;
  int last;
}arg_t;

int cmpfunc(const void* a, const void* b)
{
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

void quicksort_scalar( void *arg_vptr )
{
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
      if(left<right)
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

int main( int argc, char* argv[] )
{
  int dest[size];
  int i;
  for ( i = 0; i < size; i++ )
    dest[i] = 0;

  //simple case
  int srcs[8]={0,1,2,3,4,5,6,7};
  arg_t arg2={dest,srcs,0,size-1};
  quicksort_scalar(&arg2);
  qsort(srcs, size, sizeof(int), cmpfunc);
  for (int i=0;i<size;i++)
  {
    assert(srcs[i]==dest[i]);
  }
  //large cases
  //positive
    int srcl[8]={INT_MAX, INT_MAX-1, INT_MAX-2, INT_MAX-3,
                 INT_MAX-4,INT_MAX-5,INT_MAX-6, INT_MAX-7
           };
    arg_t arg3={dest,srcl,0,size-1};
    quicksort_scalar(&arg3);
    qsort(srcl, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srcl[i]==dest[i]);
    }
    //negative
    int srcl2[8]={INT_MIN, INT_MIN+1, INT_MIN+2, INT_MIN+3,
                 INT_MIN+4,INT_MIN+5,INT_MIN+6, INT_MIN+7
           };
    arg_t arg4={dest,srcl2,0,size-1};
    quicksort_scalar(&arg4);
    qsort(srcl2, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srcl2[i]==dest[i]);
    }

  //edge cases
    int srce[8]={9,9,9,9,9,9,9,9};
    arg_t arg5={dest,srce,0,size-1};
    quicksort_scalar(&arg5);
    qsort(srce, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srce[i]==dest[i]);
    }

    int srce2[8]={INT_MAX,INT_MIN,INT_MAX-1,INT_MIN+1,
                  INT_MAX-2,INT_MIN+2,INT_MAX-3,INT_MIN+3
    };
    arg_t arg6={dest,srce2,0,size-1};
    quicksort_scalar(&arg6);
    qsort(srce2, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
      assert(srce2[i]==dest[i]);
    }

  //random tests
  for (int ii=0;ii<1000;ii++)
  {
    int srcr[8];
    srand(time(0));
    for (int j=0;j<8;j++)
    {
      int r=rand();
      srcr[j]=r;
    }
    arg_t arg2={dest,srcr,0,size-1};
    quicksort_scalar(&arg2);
    qsort(srcr, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srcr[i]==dest[i]);
    }
  }

  int dest2[size2];
  int i2;
  for ( i2 = 0; i2 < size2; i2++ )
  {
    dest2[i2] = 0;
  }
  //simple case
  int srcs_2[128];
  for (int i=0;i<size2;i++)
  {
    srcs_2[i]=i;
  }
  arg_t arg7={dest2,srcs_2,0,size2-1};
  quicksort_scalar(&arg7);
  for ( i = 0; i < size2; i++ )
    {
      dest2[i] = srcs_2[i];
    }

  qsort(srcs_2, size2, sizeof(int), cmpfunc);
  for (int i=0;i<size2;i++)
  {
    assert(srcs_2[i]==dest2[i]);
  }

  //large cases
  //positive
    int srcl_2[128];
    for (int i=0;i<size2;i++)
    {
      srcl_2[i]=INT_MAX-1;
    }
    arg_t arg8={dest2,srcl_2,0,size2-1};
    quicksort_scalar(&arg8);
    for ( int i = 0; i < size2; i++ )
    {
      dest2[i] = srcl_2[i];
    }
    qsort(srcl_2, size2, sizeof(int), cmpfunc);
    for (int i=0;i<size2;i++)
    {
    assert(srcl_2[i]==dest2[i]);
    }
  //negative
  int srcl2_2[128];
  for (int i=0;i<size2;i++)
  {
    srcl2_2[i]=INT_MIN+i;
  }

  arg_t arg9={dest2,srcl2_2,0,size2-1};
  quicksort_scalar(&arg9);
  for ( int i = 0; i < size2; i++ )
  {
    dest2[i] = srcl2_2[i];
  }
  qsort(srcl2_2, size2, sizeof(int), cmpfunc);
  for (int i=0;i<size2;i++)
  {
  assert(srcl2_2[i]==dest2[i]);
  }

  //edge cases
  int srce_2[128];
  for (int i=0;i<size2;i++)
  {
    srce_2[i]=1024;
  }
  arg_t arg10={dest2,srce_2,0,size2-1};
  quicksort_scalar(&arg10);
  for ( int i = 0; i < size2; i++ )
  {
    dest2[i] = srce_2[i];
  }
  //quicksort_scalar(&arg10);
  qsort(srce_2, size2, sizeof(int), cmpfunc);
  for (int i=0;i<size2;i++)
  {
  assert(srce_2[i]==dest2[i]);
  }

  int srce2_2[128];
  for (int i=0;i<size2;i++)
  {
    if (i%2==0)
    {
     srce2_2[i]=INT_MAX-i;
    }
    else
    {
      srce2_2[i]=INT_MIN+i;
    }
  }
  arg_t arg11={dest2,srce2_2,0,size2-1};
  quicksort_scalar(&arg11);
  for (int i=0;i<size2;i++)
  {
    dest2[i]=srce2_2[i];
  }
  qsort(srce2_2, size2, sizeof(int), cmpfunc);
  for (int i=0;i<size2;i++)
  {
    assert(srce2_2[i]==dest2[i]);
  }

  //random tests
  for (int iii=0;iii<1000;iii++)
  {
    int srcr_2[128];
    srand(time(0));
    for (int j=0;j<128;j++)
    {
      int r=rand();
      srcr_2[j]=r;
    }
    arg_t arg12={dest2,srcr_2,0,size2-1};
    quicksort_scalar(&arg12);
    for (int i=0;i<size2;i++)
    {
      dest2[i]=srcr_2[i];
    }

    qsort(srcr_2, size2, sizeof(int), cmpfunc);
    for (int i=0;i<size2;i++)
    {
    assert(srcr_2[i]==dest2[i]);
    }
  }

  //test with array len not a multiple of 4
  int dest3[size3];
  int i3;
  for ( i3 = 0; i3 < size3; i3++ )
  {
    dest3[i3] = 0;
  }
  //simple case
  int srcs_3[150];
  for (int i=0;i<size3;i++)
  {
    srcs_3[i]=i;
  }
  arg_t arg13={dest3,srcs_3,0,size3-1};
  quicksort_scalar(&arg13);
  for ( i = 0; i < size3; i++ )
    {
      dest3[i] = srcs_3[i];
    }
  qsort(srcs_3, size3, sizeof(int), cmpfunc);
  for (int i=0;i<size3;i++)
  {
    assert(srcs_3[i]==dest3[i]);
  }
  //large cases
  //positive
  int srcl_3[150];
  for (int i=0;i<size3;i++)
  {
    srcl_3[i]=INT_MAX-i;
  }
  arg_t arg14={dest3,srcl_3,0,size3-1};
  quicksort_scalar(&arg14);
  for ( int i = 0; i < size3; i++ )
  {
    dest3[i] = srcl_3[i];
  }
  qsort(srcl_3, size3, sizeof(int), cmpfunc);
  for (int i=0;i<size3;i++)
  {
  assert(srcl_3[i]==dest3[i]);
  }
  //negative
  int srcl2_3[150];
  for (int i=0;i<size3;i++)
  {
    srcl2_3[i]=INT_MIN+i;
  }
  arg_t arg15={dest3,srcl2_3,0,size3-1};
  quicksort_scalar(&arg15);
  for ( int i = 0; i < size3; i++ )
  {
    dest3[i] = srcl2_3[i];
  }
  qsort(srcl2_3, size3, sizeof(int), cmpfunc);
  for (int i=0;i<size3;i++)
  {
  assert(srcl2_3[i]==dest3[i]);
  }
  //edge cases
  int srce_3[150];
  for (int i=0;i<size3;i++)
  {
    srce_3[i]=19841103;
  }
  arg_t arg16={dest3,srce_3,0,size3-1};
  quicksort_scalar(&arg16);
  for ( int i = 0; i < size3; i++ )
  {
    dest3[i] = srce_3[i];
  }
  qsort(srce_3, size3, sizeof(int), cmpfunc);
  for (int i=0;i<size3;i++)
  {
  assert(srce_3[i]==dest3[i]);
  }
  int srce2_3[150];
  for (int i=0;i<size3;i++)
  {
    if (i%2==0)
    {
     srce2_3[i]=INT_MAX-i;
    }
    else
    {
      srce2_3[i]=INT_MIN+i;
    }
  }
  arg_t arg17={dest3,srce2_3,0,size3-1};
  quicksort_scalar(&arg17);
  for (int i=0;i<size3;i++)
  {
    dest3[i]=srce2_3[i];
  }
  qsort(srce2_3, size3, sizeof(int), cmpfunc);
  for (int i=0;i<size3;i++)
  {
    assert(srce2_3[i]==dest3[i]);
  }
  //random tests
  for (int iiii=0;iiii<1000;iiii++)
  {
    int srcr_3[150];
    srand(time(0));
    for (int j=0;j<150;j++)
    {
      int r=rand();
      srcr_3[j]=r;
    }
    arg_t arg18={dest3,srcr_3,0,size3-1};
    quicksort_scalar(&arg18);
    for (int i=0;i<size3;i++)
    {
      dest3[i]=srcr_3[i];
    }
    qsort(srcr_3, size3, sizeof(int), cmpfunc);
    for (int i=0;i<size3;i++)
    {
    assert(srcr_3[i]==dest3[i]);
    }
  }

  printf("All tests have been passed!\n");
  return 0;
}
