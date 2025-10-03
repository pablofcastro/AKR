from sys import argv
from num2words import num2words
from uplts import plts, perception, kh 

if __name__ == '__main__':

    doors         = len(argv)-3
    probabilities = list(map(float, argv[1:-1]))
    mode          = argv[-1]

    if doors > 0:

        fname = f'{mode}-' + num2words(doors) + '.kr'

        try:
            ffile = open(fname,'x')

            ffile.write(f"{plts(doors,probabilities)}")
            ffile.write(f"{perception(doors,mode)}")
            ffile.write(f"{kh(success=probabilities[0])}")

        except FileExistsError:
            print(f'the file {fname} already exists')

    else:
        print(f'error: incorrect number of arguments for {argv[0]}')
        print(f'  use: {argv[0]} <success:float> <prob1:float> <prob2:float> ... <probn:float> canyengue|salon|milonga')
