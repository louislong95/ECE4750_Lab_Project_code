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

typedef struct{
  int *dest;
  int *src;
  int start;
  int len;
  int end;
}arg_m;

int cmpfunc(const void* a, const void* b)
{
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

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
      if (left<right)
      {
      int temp=src[left];
      src[left]=src[right];
      src[right]=temp;
      }
    }
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


int main( int argc, char* argv[] )
{
  int dest[size];
  int temp[size];
  int temp1[size];
  int block=size/4;

  //simple case
  int srcs[8]={1,2,3,4,5,6,7,0};
  arg_t arg2={temp,srcs,0,block-1};
  arg_t arg3={temp,srcs,block,2*block-1};
  arg_t arg4={temp,srcs,2*block,3*block-1};
  arg_t arg5={temp,srcs,3*block,size-1};
  quicksort_scalar(&arg2);
  quicksort_scalar(&arg3);
  quicksort_scalar(&arg4);
  quicksort_scalar(&arg5);
  arg_m arg6={temp1,temp,0,block,2*block};
  arg_m arg7={temp1,temp,2*block,block,size};
  merge(&arg6);
  merge(&arg7);
  arg_m arg8={dest,temp1,0,2*block,size};
  merge(&arg8);

  qsort(srcs, size, sizeof(int), cmpfunc);
  for (int i=0;i<size;i++)
  {
    assert(srcs[i]==dest[i]);
  }

  //large cases
  //positive
    int srcl[8]={INT_MAX, INT_MAX-1, INT_MAX-2, INT_MAX-3,
                 INT_MAX-4,INT_MAX-5,INT_MAX-6, INT_MAX-7};
    arg_t arg9 ={temp,srcl,0,block-1};
    arg_t arg10={temp,srcl,block,2*block-1};
    arg_t arg11={temp,srcl,2*block,3*block-1};
    arg_t arg12={temp,srcl,3*block,size-1};
    quicksort_scalar(&arg9);
    quicksort_scalar(&arg10);
    quicksort_scalar(&arg11);
    quicksort_scalar(&arg12);
    arg_m arg13={temp1,temp,0,block,2*block};
    arg_m arg14={temp1,temp,2*block,block,size};
    merge(&arg13);
    merge(&arg14);
    arg_m arg15={dest,temp1,0,2*block,size};
    merge(&arg15);
    qsort(srcl, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srcl[i]==dest[i]);
    }
    //negative
    int srcl2[8]={INT_MIN, INT_MIN+1, INT_MIN+2, INT_MIN+3,
                 INT_MIN+4,INT_MIN+5,INT_MIN+6, INT_MIN+7};
    arg_t arg16 ={temp,srcl2,0,block-1};
    arg_t arg17={temp,srcl2,block,2*block-1};
    arg_t arg18={temp,srcl2,2*block,3*block-1};
    arg_t arg19={temp,srcl2,3*block,size-1};
    quicksort_scalar(&arg16);
    quicksort_scalar(&arg17);
    quicksort_scalar(&arg18);
    quicksort_scalar(&arg19);
    arg_m arg20={temp1,temp,0,block,2*block};
    arg_m arg21={temp1,temp,2*block,block,size};
    merge(&arg20);
    merge(&arg21);
    arg_m arg22={dest,temp1,0,2*block,size};
    merge(&arg22);
    qsort(srcl2, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srcl2[i]==dest[i]);
    }
    //edge cases
    int srce[8]={9,9,9,9,9,9,9,9};
    arg_t arg23 ={temp,srce,0,block-1};
    arg_t arg24={temp,srce,block,2*block-1};
    arg_t arg25={temp,srce,2*block,3*block-1};
    arg_t arg26={temp,srce,3*block,size-1};
    quicksort_scalar(&arg23);
    quicksort_scalar(&arg24);
    quicksort_scalar(&arg25);
    quicksort_scalar(&arg26);
    arg_m arg27={temp1,temp,0,block,2*block};
    arg_m arg28={temp1,temp,2*block,block,size};
    merge(&arg27);
    merge(&arg28);
    arg_m arg29={dest,temp1,0,2*block,size};
    merge(&arg29);
    qsort(srce, size, sizeof(int), cmpfunc);
    for (int i=0;i<size;i++)
    {
    assert(srce[i]==dest[i]);
    }

    int srce2[8]={INT_MAX,INT_MIN,INT_MAX-1,INT_MIN+1,
                  INT_MAX-2,INT_MIN+2,INT_MAX-3,INT_MIN+3
    };
    arg_t arg30 ={temp,srce2,0,block-1};
    arg_t arg31={temp,srce2,block,2*block-1};
    arg_t arg32={temp,srce2,2*block,3*block-1};
    arg_t arg33={temp,srce2,3*block,size-1};
    quicksort_scalar(&arg30);
    quicksort_scalar(&arg31);
    quicksort_scalar(&arg32);
    quicksort_scalar(&arg33);
    arg_m arg34={temp1,temp,0,block,2*block};
    arg_m arg35={temp1,temp,2*block,block,size};
    merge(&arg34);
    merge(&arg35);
    arg_m arg36={dest,temp1,0,2*block,size};
    merge(&arg36);
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
      arg_t arg37 ={temp,srcr,0,block-1};
      arg_t arg38={temp,srcr,block,2*block-1};
      arg_t arg39={temp,srcr,2*block,3*block-1};
      arg_t arg40={temp,srcr,3*block,size-1};
      quicksort_scalar(&arg37);
      quicksort_scalar(&arg38);
      quicksort_scalar(&arg39);
      quicksort_scalar(&arg40);
      arg_m arg41={temp1,temp,0,block,2*block};
      arg_m arg42={temp1,temp,2*block,block,size};
      merge(&arg41);
      merge(&arg42);
      arg_m arg43={dest,temp1,0,2*block,size};
      merge(&arg43);
      qsort(srcr, size, sizeof(int), cmpfunc);
      for (int i=0;i<size;i++)
      {
      assert(srcr[i]==dest[i]);
      }
    }

    //Testing with array size of 128
    int dest2[size2];
    int temp_1[size2];
    int temp1_1[size2];
    int block_1=size2/4;
    int i2;
    for ( i2 = 0; i2 < size2; i2++ )
    {
      dest2[i2] = 0;
    }
    //simple cases
    int srcs_2[128];
    for (int i=0;i<size2;i++)
    {
      srcs_2[i]=i;
    }
    arg_t arg44={temp_1,srcs_2,0,block_1-1};
    arg_t arg45={temp_1,srcs_2,block_1,2*block_1-1};
    arg_t arg46={temp_1,srcs_2,2*block_1,3*block_1-1};
    arg_t arg47={temp_1,srcs_2,3*block_1,size2-1};
    quicksort_scalar(&arg44);
    quicksort_scalar(&arg45);
    quicksort_scalar(&arg46);
    quicksort_scalar(&arg47);
    for ( int i = 0; i < size2; i++ )
      {
        temp_1[i] = srcs_2[i];
      }
    arg_m arg48={temp1_1,temp_1,0,block_1,2*block_1};
    arg_m arg49={temp1_1,temp_1,2*block_1,block_1,size2};
    merge(&arg48);
    merge(&arg49);
    arg_m arg50={dest2,temp1_1,0,2*block_1,size2};
    merge(&arg50);
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
    arg_t arg51={temp_1,srcl_2,0,block_1-1};
    arg_t arg52={temp_1,srcl_2,block_1,2*block_1-1};
    arg_t arg53={temp_1,srcl_2,2*block_1,3*block_1-1};
    arg_t arg54={temp_1,srcl_2,3*block_1,size2-1};
    quicksort_scalar(&arg51);
    quicksort_scalar(&arg52);
    quicksort_scalar(&arg53);
    quicksort_scalar(&arg54);
    for ( int i = 0; i < size2; i++ )
      {
        temp_1[i] = srcs_2[i];
      }
    arg_m arg55={temp1_1,temp_1,0,block_1,2*block_1};
    arg_m arg56={temp1_1,temp_1,2*block_1,block_1,size2};
    merge(&arg55);
    merge(&arg56);
    arg_m arg57={dest2,temp1_1,0,2*block_1,size2};
    merge(&arg57);
    qsort(srcl_2, size2, sizeof(int), cmpfunc);
    for (int i=0;i<size2;i++)
    {
      assert(srcs_2[i]==dest2[i]);
    }
    //negative
    int srcl2_2[128];
    for (int i=0;i<size2;i++)
    {
      srcl2_2[i]=INT_MIN+i;
    }
    arg_t arg58={temp_1,srcl2_2,0,block_1-1};
    arg_t arg59={temp_1,srcl2_2,block_1,2*block_1-1};
    arg_t arg60={temp_1,srcl2_2,2*block_1,3*block_1-1};
    arg_t arg61={temp_1,srcl2_2,3*block_1,size2-1};
    quicksort_scalar(&arg58);
    quicksort_scalar(&arg59);
    quicksort_scalar(&arg60);
    quicksort_scalar(&arg61);
    for ( int i = 0; i < size2; i++ )
      {
        temp_1[i] = srcl2_2[i];
      }
    arg_m arg62={temp1_1,temp_1,0,block_1,2*block_1};
    arg_m arg63={temp1_1,temp_1,2*block_1,block_1,size2};
    merge(&arg62);
    merge(&arg63);
    arg_m arg64={dest2,temp1_1,0,2*block_1,size2};
    merge(&arg64);
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
    arg_t arg65={temp_1,srce_2,0,block_1-1};
    arg_t arg66={temp_1,srce_2,block_1,2*block_1-1};
    arg_t arg67={temp_1,srce_2,2*block_1,3*block_1-1};
    arg_t arg68={temp_1,srce_2,3*block_1,size2-1};
    quicksort_scalar(&arg65);
    quicksort_scalar(&arg66);
    quicksort_scalar(&arg67);
    quicksort_scalar(&arg68);
    for ( int i = 0; i < size2; i++ )
      {
        temp_1[i] = srce_2[i];
      }
    arg_m arg69={temp1_1,temp_1,0,block_1,2*block_1};
    arg_m arg70={temp1_1,temp_1,2*block_1,block_1,size2};
    merge(&arg69);
    merge(&arg70);
    arg_m arg71={dest2,temp1_1,0,2*block_1,size2};
    merge(&arg71);
    qsort(srcl2_2, size2, sizeof(int), cmpfunc);
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
    arg_t arg72={temp_1,srce2_2,0,block_1-1};
    arg_t arg73={temp_1,srce2_2,block_1,2*block_1-1};
    arg_t arg74={temp_1,srce2_2,2*block_1,3*block_1-1};
    arg_t arg75={temp_1,srce2_2,3*block_1,size2-1};
    quicksort_scalar(&arg72);
    quicksort_scalar(&arg73);
    quicksort_scalar(&arg74);
    quicksort_scalar(&arg75);
    for ( int i = 0; i < size2; i++ )
      {
        temp_1[i] = srce2_2[i];
      }
    arg_m arg76={temp1_1,temp_1,0,block_1,2*block_1};
    arg_m arg77={temp1_1,temp_1,2*block_1,block_1,size2};
    merge(&arg76);
    merge(&arg77);
    arg_m arg78={dest2,temp1_1,0,2*block_1,size2};
    merge(&arg78);
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
      arg_t arg79={temp_1,srcr_2,0,block_1-1};
      arg_t arg80={temp_1,srcr_2,block_1,2*block_1-1};
      arg_t arg81={temp_1,srcr_2,2*block_1,3*block_1-1};
      arg_t arg82={temp_1,srcr_2,3*block_1,size2-1};
      quicksort_scalar(&arg79);
      quicksort_scalar(&arg80);
      quicksort_scalar(&arg81);
      quicksort_scalar(&arg82);
      for ( int i = 0; i < size2; i++ )
        {
          temp_1[i] = srcr_2[i];
        }
      arg_m arg83={temp1_1,temp_1,0,block_1,2*block_1};
      arg_m arg84={temp1_1,temp_1,2*block_1,block_1,size2};
      merge(&arg83);
      merge(&arg84);
      arg_m arg85={dest2,temp1_1,0,2*block_1,size2};
      merge(&arg85);
      qsort(srcr_2, size2, sizeof(int), cmpfunc);
      for (int i=0;i<size2;i++)
      {
      assert(srcr_2[i]==dest2[i]);
      }
    }
  //test with array len not a multiple of 4
  int dest3[size3];
  int i3;
  int temp_2[size3];
  int temp1_2[size3];
  int block_2=size3/4;
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
  arg_t arg86={temp_2,srcs_3,0,block_2-1};
  arg_t arg87={temp_2,srcs_3,block_2,2*block_2-1};
  arg_t arg88={temp_2,srcs_3,2*block_2,3*block_2-1};
  arg_t arg89={temp_2,srcs_3,3*block_2,size3-1};
  quicksort_scalar(&arg86);
  quicksort_scalar(&arg87);
  quicksort_scalar(&arg88);
  quicksort_scalar(&arg89);
  for ( int i = 0; i < size3; i++ )
    {
      temp_2[i] = srcs_3[i];
    }
  arg_m arg90={temp1_2,temp_2,0,block_2,2*block_2};
  arg_m arg91={temp1_2,temp_2,2*block_2,block_2,size3};
  merge(&arg90);
  merge(&arg91);
  arg_m arg92={dest3,temp1_2,0,2*block_2,size3};
  merge(&arg92);
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
  arg_t arg93={temp_2,srcl_3,0,block_2-1};
  arg_t arg94={temp_2,srcl_3,block_2,2*block_2-1};
  arg_t arg95={temp_2,srcl_3,2*block_2,3*block_2-1};
  arg_t arg96={temp_2,srcl_3,3*block_2,size3-1};
  quicksort_scalar(&arg93);
  quicksort_scalar(&arg94);
  quicksort_scalar(&arg95);
  quicksort_scalar(&arg96);
  for ( int i = 0; i < size3; i++ )
    {
      temp_2[i] = srcl_3[i];
    }
  arg_m arg97={temp1_2,temp_2,0,block_2,2*block_2};
  arg_m arg98={temp1_2,temp_2,2*block_2,block_2,size3};
  merge(&arg97);
  merge(&arg98);
  arg_m arg99={dest3,temp1_2,0,2*block_2,size3};
  merge(&arg99);
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
  arg_t arg100={temp_2,srcl2_3,0,block_2-1};
  arg_t arg101={temp_2,srcl2_3,block_2,2*block_2-1};
  arg_t arg102={temp_2,srcl2_3,2*block_2,3*block_2-1};
  arg_t arg103={temp_2,srcl2_3,3*block_2,size3-1};
  quicksort_scalar(&arg100);
  quicksort_scalar(&arg101);
  quicksort_scalar(&arg102);
  quicksort_scalar(&arg103);
  for ( int i = 0; i < size3; i++ )
    {
      temp_2[i] = srcl2_3[i];
    }
  arg_m arg104={temp1_2,temp_2,0,block_2,2*block_2};
  arg_m arg105={temp1_2,temp_2,2*block_2,block_2,size3};
  merge(&arg104);
  merge(&arg105);
  arg_m arg106={dest3,temp1_2,0,2*block_2,size3};
  merge(&arg106);
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
  arg_t arg107={temp_2,srce_3,0,block_2-1};
  arg_t arg108={temp_2,srce_3,block_2,2*block_2-1};
  arg_t arg109={temp_2,srce_3,2*block_2,3*block_2-1};
  arg_t arg110={temp_2,srce_3,3*block_2,size3-1};
  quicksort_scalar(&arg107);
  quicksort_scalar(&arg108);
  quicksort_scalar(&arg109);
  quicksort_scalar(&arg110);
  for ( int i = 0; i < size3; i++ )
    {
      temp_2[i] = srce_3[i];
    }
  arg_m arg111={temp1_2,temp_2,0,block_2,2*block_2};
  arg_m arg112={temp1_2,temp_2,2*block_2,block_2,size3};
  merge(&arg111);
  merge(&arg112);
  arg_m arg113={dest3,temp1_2,0,2*block_2,size3};
  merge(&arg113);
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
  arg_t arg114={temp_2,srce2_3,0,block_2-1};
  arg_t arg115={temp_2,srce2_3,block_2,2*block_2-1};
  arg_t arg116={temp_2,srce2_3,2*block_2,3*block_2-1};
  arg_t arg117={temp_2,srce2_3,3*block_2,size3-1};
  quicksort_scalar(&arg114);
  quicksort_scalar(&arg115);
  quicksort_scalar(&arg116);
  quicksort_scalar(&arg117);
  for ( int i = 0; i < size3; i++ )
    {
      temp_2[i] = srce2_3[i];
    }
  arg_m arg118={temp1_2,temp_2,0,block_2,2*block_2};
  arg_m arg119={temp1_2,temp_2,2*block_2,block_2,size3};
  merge(&arg118);
  merge(&arg119);
  arg_m arg120={dest3,temp1_2,0,2*block_2,size3};
  merge(&arg120);
  qsort(srce2_3, size3, sizeof(int), cmpfunc);
  for (int i=0;i<size3;i++)
  {
   assert(srce2_3[i]==dest3[i]);
   //printf("srce %d ",srce2_3[i]);
   //printf("dest %d\n",dest3[i]);
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
    arg_t arg121={temp_2,srcr_3,0,block_2-1};
    arg_t arg122={temp_2,srcr_3,block_2,2*block_2-1};
    arg_t arg123={temp_2,srcr_3,2*block_2,3*block_2-1};
    arg_t arg124={temp_2,srcr_3,3*block_2,size3-1};
    quicksort_scalar(&arg121);
    quicksort_scalar(&arg122);
    quicksort_scalar(&arg123);
    quicksort_scalar(&arg124);
    for ( int i = 0; i < size3; i++ )
      {
        temp_2[i] = srcr_3[i];
      }
    arg_m arg125={temp1_2,temp_2,0,block_2,2*block_2};
    arg_m arg126={temp1_2,temp_2,2*block_2,block_2,size3};
    merge(&arg125);
    merge(&arg126);
    arg_m arg127={dest3,temp1_2,0,2*block_2,size3};
    merge(&arg127);
    qsort(srcr_3, size3, sizeof(int), cmpfunc);
    for (int i=0;i<size3;i++)
    {
    assert(srcr_3[i]==dest3[i]);
    }
  }

  printf("All tests have been passed!\n");
  return 0;
}
