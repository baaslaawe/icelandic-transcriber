import re

class Transcriber():

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
            if len(line.replace('\t','')) > 1:
                sline = line.split('\t')
                try:
                    environment = sline[2]
                except:
                    environment = ''
                self.map_list.append((sline[0], sline[1], environment))

    def transcribe_file(self, ortho_filename):
        self.result = ''
        with open(ortho_filename) as ortho_file:
            for line in ortho_file:
                self.result += self.transcribe_line(line)

    def transcribe_line(self, line):
        line_result = line[:]
        for ortho, trans, env in self.map_list:
            envs = re.sub('_+', '_',env.replace(' ',''))
            try:
                env_left, env_right = envs.split('_')
            except:
                env_left, env_right = '', ''
            line_result = re.sub('(?<={}){}(?={})'.format(
                            env_left, ortho, env_right), trans, line_result)
        print('{} --> {}'.format(line, line_result))
        return line_result


#### Quick, temp lines for testing
mt = Transcriber('test_mappings.csv')
mt.transcribe_file('test_ortho.txt')