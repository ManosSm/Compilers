def main_test_6():
#{
    #$ declarations #$
    #declare x
    #declare i,j

    x = int(input());
    j = 1;
    i = 2;
    while (i<=x):
    #{
        j = j * 2;
        i = i + 1;
    #}
    print(j);
#}


if __name__ == "__main__":
    #$ call of main functions #$
    main_test_6();
