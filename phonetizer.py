import re

class Phonetizer():

    # Define shorthands for phonological classes
    ph_classes = {
    'C' : 'p|t|k|b|d|g',
    'V' : 'a|e|i|o|u|y'
    }

    def __init__(self, mappings_filename):
        with open(mappings_filename) as mfile:
            self.read_mfile(mfile)

    def read_mfile(self, mfile):
        """
        """
        self.ortho_maps = []
        self.phone_maps = []
        for line in mfile:
            sline = line[:-1].split('\t')   # fix this using csv so the user doesn't have to have an extra blank line!
            if len(sline) == 2:
                self.ortho_maps.append((sline[0],sline[1]))
            elif len(sline) == 3:
                self.phone_maps.append((sline[0],sline[1]))
        self.ortho_maps.sort(key=lambda x: len(x[0]))
        self.ortho_maps.reverse()

    def read_wfile(self, ttfilename):
        with open(ttfilename) as ttfile:
            return [(line[:-1].split('\t')[0],line[:-1].split('\t')[1]) for line in ttfile]

    def run_tests(self, ttfilename):
        cases = self.read_wfile(ttfilename)
        for c in cases:
            transcription = self.phonetize(c[0])
            if transcription != c[1]:
                print('Output [{}] should have been [{}].'.format(transcription, c[1]))

    def phonetize(self, ortho):
        result = ['' for character in ortho]

        # go from ortho to initial transcription
        for om in self.ortho_maps:
            hits = re.finditer(om[0], ortho)
            for hit in hits:
                result[hit.start()] = om[1]
                ortho = ''.join(['*' if i in range(hit.start(), hit.end()) else c for i,c in enumerate(ortho)])
        for i,character in enumerate(ortho):
            if character != '*':
                result[i] = character
        result = ''.join(result)

        # apply "phonology"
        loop_input_str = ''.join(result)
        new_result = ['' for character in result]
        while True:
            loop_input = loop_input_str
            new_result = [c for c in loop_input_str]
            for pm in self.phone_maps:
                hits = re.finditer(pm[0], loop_input_str)
                for hit in hits:
                    new_result[hit.start()] = pm[1]
                    for i in range(hit.start()+1, hit.end()):
                        new_result[i] = ''
                    loop_input = ''.join(['*' if i in range(hit.start(), hit.end()) else c for i,c in enumerate(loop_input)])

            if ''.join(new_result) == loop_input_str:
                return loop_input_str
            else:
                loop_input_str = ''.join(new_result)




#### Quick, temp lines for testing
p = Phonetizer('test_mappings.txt')
p.run_tests('test_ortho.txt')