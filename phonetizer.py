import re

class Phonetizer():

    def __init__(self, mappings_filename, classes_filename):
        with open(classes_filename) as cfile:
            self.read_cfile(cfile)
        with open(mappings_filename) as mfile:
            self.read_mfile(mfile)

    def read_cfile(self, cfile):
        """
        """
        self.ortho_classes = {}
        self.phone_classes = {}
        for line in cfile:
            sline = line[:-1].split('\t')   # fix this using csv so the user doesn't have to have an extra blank line!
            if len(sline) == 2:
                self.ortho_classes[sline[0]] = sline[1]
            elif len(sline) == 3:
                self.phone_classes[sline[0]] = sline[1]

    def read_mfile(self, mfile):
        """
        """
        self.ortho_maps = []
        self.phone_maps = []
        for line in mfile:
            sline = line[:-1].split('\t')   # fix this using csv so the user doesn't have to have an extra blank line!
            if len(sline) == 3 and sline[2] == '*':
                self.phone_maps.append((sline[0],sline[1]))
            elif len(sline) > 1:
                ortho_input = sline[0]
                ortho_output = sline[1]
                try:
                    left_env = sline[2]
                except IndexError:
                    left_env = ''
                try:
                    right_env = sline[3]
                except IndexError:
                    right_env = ''
                self.ortho_maps.append((ortho_input, ortho_output, left_env, right_env))

        ## Sort by complexity of environment and length of input, e.g. L-xy-R > xy-R > L-x > xy > x
        self.ortho_maps.sort(key=lambda x: len(x[0]))
        self.ortho_maps.sort(key=lambda x: len(x))
        self.ortho_maps.reverse()

        self.phone_maps.sort(key=lambda x: len(x[0]))
        self.phone_maps.reverse()

    def translate_ortho_classes(self, expression):
        for c in self.ortho_classes:
            expression = expression.replace(c, self.ortho_classes[c])
        return expression

    def read_wfile(self, ttfilename):
        with open(ttfilename) as ttfile:
            return [(line[:-1].split('\t')[0],line[:-1].split('\t')[1]) for line in ttfile]

    def run_tests(self, ttfilename):
        cases = self.read_wfile(ttfilename)
        for c in cases:
            transcription = self.phonetize(c[0])
            if transcription != c[1]:
                print('Output [{}] for <{}> should have been [{}].'.format(transcription, c[0], c[1]))

    def phonetize(self, ortho):
        # go from ortho to initial transcription
        for om in self.ortho_maps:
            try:
                lookbehind = '(?<={})'.format(om[2])
            except IndexError:
                lookbehind = ''
            try:
                lookahead = '(?={})'.format(om[3])
            except IndexError:
                lookahead = ''
            ortho = re.sub(lookbehind+om[0]+lookahead, om[1], ortho)

        print(ortho)
        # apply "phonology"
        output = ortho
        for pm in self.phone_maps:
            output = re.sub(pm[0], pm[1], output)
            
        print(output)
        return output


    ### Old version, which keeps separate ortho and transcription tiers
    # def phonetize(self, ortho):
    #     result = ['' for character in ortho]
    #     # print()
    #     # print(ortho)

    #     # translate segment classes, add capture groups


    #     # go from ortho to initial transcription
    #     for om in self.ortho_maps:
    #         try:
    #             lookbehind = '(?<={})'.format(om[2])
    #         except IndexError:
    #             lookbehind = ''
    #         try:
    #             lookahead = '(?={})'.format(om[3])
    #         except IndexError:
    #             lookahead = ''
    #         hits = re.finditer(lookbehind+om[0]+lookahead, ortho)
    #         print()
    #         print(ortho)
    #         for hit in hits:
    #             result[hit.start()] = om[1]
    #             print(hit)
    #             print(hit.start())
    #             print(hit.end())
    #             ortho = ''.join(['*' if i in range(hit.start(), hit.end()) else c for i,c in enumerate(ortho)])
    #     for i,character in enumerate(ortho):
    #         if character != '*':
    #             result[i] = character
    #     result = ''.join(result)
    #     # print(result)

    #     # apply "phonology"
    #     loop_input_str = ''.join(result)
    #     new_result = ['' for character in result]
    #     while True:
    #         loop_input = loop_input_str
    #         new_result = [c for c in loop_input_str]
    #         for pm in self.phone_maps:
    #             hits = re.finditer(pm[0], loop_input_str)
    #             for hit in hits:
    #                 new_result[hit.start()] = pm[1]
    #                 for i in range(hit.start()+1, hit.end()):
    #                     new_result[i] = ''
    #                 loop_input = ''.join(['*' if i in range(hit.start(), hit.end()) else c for i,c in enumerate(loop_input)])

    #         if ''.join(new_result) == loop_input_str:
    #             # print(loop_input_str)
    #             return loop_input_str
    #         else:
    #             loop_input_str = ''.join(new_result)




#### Quick, temp lines for testing
p = Phonetizer('mappings.txt', 'segment_classes.txt')
p.run_tests('nouns_ortho_tiny.txt')
