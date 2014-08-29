import re

class Transcriber():

    def __init__(self, mappings_filename):
        with open(mappings_filename) as mfile:
            self.map_list = self.read_mfile(mfile)

    def read_mfile(mfile):
        """Create mapping list of tuples from an opened text file.
        The mappings file should be tab-delimited and include the following 
        columns:
        orthography, corresponding transcription, environment
        Note that the order of mappings is important! Some mappings must be
        ordered before others.
        """
        map_list = []
        for line in mfile:
            if len(line) > 0:
                sline = line.split('\t')
                try:
                    environment = sline[2]
                except IndexError:
                    environment = None
                map_list.append((sline[0], sline[1], environment))

    def transcribe_file(ortho_filename):
        self.result = ''
        with open(ortho_filename) as ortho_file:
            for line in ortho_file:
                self.result += self.transcribe_line(line)

    def transcribe_line(line):
        line_result = line[:]
        for ortho, trans, env in self.map_list:
            env_left, env_right = '_'.split(re.sub('_+', '_', 
                                                   env.replace(' ','')))
            line_result = re.sub('(?<={}){}(?={})'.format(
                            env_left, ortho, env_right), trans, line_result)
