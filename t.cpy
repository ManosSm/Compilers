def main_bigger_smaller_of_3():
#{
    #declare x
    #declare y
    #declare z
    #declare biggest
    #declare smallest

    def bigger(a,b):
    #{
        #declare f
        def asd(k):
        #{
            return (k);
        #}
        z= asd(42);
        z = 42;
        z= z*2;
        z= z//2;
        if (a>b):

            return (a);
        else:
            return (bigger(b-1,a));
    #}

    def smaller(a,b):
    #{

        if  (    a   <  b    )    :

            return (    a  );
      a = b - 1;
      a = 1 - b;
      a = a - b;
      a = 1 - 1;

      z = 42;

	  a = a + b;
	  a = 5 + b;
      a = a + 5;
      a = 5 + 5;
	#}



    #$ body of order_3_numbers #$
    x = int(input());
    y = int(input());
    z = int(input());

    biggest = bigger(x,y);
    biggest = bigger(biggest,z);

    smallest = smaller(x,y);
    smallest = smaller(smallest,z);

    print(biggest);
    print(smallest);

#}




if __name__ == "__main__":
    #$ call of main functions #$
    main_bigger_smaller_of_3();