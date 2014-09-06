import re

class Transcriber():

    # Define shorthands for phonological classes
    ph_classes = {
    'C' : 'p|t|k|b|d|g',
    'V' : 'a|e|i|o|u|y'
    }

    def __init__(self, mappings_filename):
        with open(mappings_filename) as mfile:
            self.read_mfile(mfile)

    def read_mfile(self, mfile):
        """Create mapping list of tuples from an opened text file.
        The mappings file should be tab-delimited and include the following 
        columns:
        orthography, corresponding transcription, environment
        Note that the order of mappings is important! Some mappings must be
        ordered before others.
        """
        self.map_list = []
        for line in mfile:
            sline = line.split('\t')
            try:
                env_l = self.replace_sets(sline[2])
            except IndexError:
                env_l = ''
            try:
                env_r = self.replace_sets(sline[3])
            except IndexError:
                env_r = ''
            try:
                self.map_list.append((sline[0],sline[1],env_l,env_r))
            except IndexError:
                pass

    def replace_sets(self, env):
        # Remove all input set syntax (spaces, braces, and straggling newlines) and create a list:
        all_envs = env.replace(' ', '').replace('{', '').replace('}', '').strip().split(',')
        for n,i in enumerate(all_envs):
            if i in self.ph_classes.keys(): # If environment contains a set
                all_envs[n] = self.ph_classes[i]  # Replace shorthand with set
        # Return a regex formatted set of environments
        return '({})'.format('|'.join(all_envs))

    def transcribe_file(self, ortho_filename):
        self.result = ''
        with open(ortho_filename) as ortho_file:
            for line in ortho_file:
                self.result += self.transcribe_line(line.strip())

    def transcribe_line(self, line):
        # Load input line and surround by word boundaries
        line_result = '#{}#'.format(line[:])
        for ortho, trans, env_l, env_r in self.map_list:
            line_result = re.sub('(?<={}){}(?={})'.format(
                            env_l, ortho, env_r), trans, line_result)
        print('{} --> {}'.format(line, line_result.replace('#', '')))
        return line_result


#### Quick, temp lines for testing
mt = Transcriber('test_mappings.txt')
mt.transcribe_file('test_ortho.txt')