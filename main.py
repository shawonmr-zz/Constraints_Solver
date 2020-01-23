#./main.py input_filename  output_file_name  nresults

from constraints import Constraint
from genetic import Genetic
import sys, getopt



def main(argv):

    if len(sys.argv) < 3 :
        print('Please provide 3 command line arguments (e.g. input_filename, output_filename, n_results')
        exit(-1)

    in_filename = ''
    out_filename = ''
    niteration = 0


    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    niteration = int(sys.argv[3])

    c = Constraint(in_filename)
    v = c.get_example()
    print(v)
    n = c.get_ndim()  #this is the chromosome size for each population
    print(n)
    # print(c.apply([0.5, 1.0, 0.0, 0.5]))

    s = 300  #population size

    ga = Genetic(s, n, in_filename)  #initializes ga type object with populaton size, chromosome size, input file name

    p = ga.get_population()
    print(p)
    print(ga.cal_pop_fitness())

    temp_solution = ga.eval_ga(niteration)
    # print(temp_solution)
    # write result to the output
    with open(out_filename, 'w') as filehandle:
        for item in temp_solution:
            s = "   ".join(str(e) for e in item)
            # print(s)
            l = s
            # l = item
            print(l)
            filehandle.write('%s\n' % l)

    filehandle.close()


if __name__ == '__main__':
    main(sys.argv[1:])
