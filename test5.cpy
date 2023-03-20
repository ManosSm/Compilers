def main_odd_even():
#{
    #declare x
    #declare y
    #declare z
    #declare even, odd


    #$ body of main_odd_even #$
    x = int(input());
    y = x // 2;
    z = x - 2 * y;

    even = 0;
    odd = 1;


    if (z == 0):
        print(even);
    else:
        print(odd);
#}




if __name__ == "__main__":
    #$ call of main functions #$
    main_odd_even();