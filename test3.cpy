def bigger_smaller_of_3():
#{
    #declare x
    #declare y
    #declare z
    #declare biggest
    #declare smallest
    
    def bigger(a,b):
    #{   
        if (a>b):
            return (a);
        else:
            return (b);  
    #}

    def smaller(a,b):
    #{
          
        if  (    a   <  b    )    :

            return (    a   )  ;

        else    :

            return   (  b   )  ;
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
    bigger_smaller_of_3();