
def main_add_4_NuMBerS():
#{
    #declare x
    #declare y
    #declare z
    #declare w
    #declare sum1
    #declare sum2
    #declare final_sum
    

    def add_2_numbers(a,b):
    #{
        return (a+b);
    #}

    
    #$ body of main_add_3_NuMBerS #$
    
    x = int(input());
    y = int(input());
    z = int(input());
    w = int(input());

    sum1 = add_2_numbers(x,y);
    sum2 = add_2_numbers(z,w);
    final_sum = add_2_numbers(sum1,sum2);

    print(final_sum);

#}




if __name__ == "__main__":
    #$ call of main functions #$
    main_add_4_NuMBerS();