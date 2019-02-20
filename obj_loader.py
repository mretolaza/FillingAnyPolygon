class obj_loader(object):
    def __init__(self, filename):
        self.vertices = []
        self.faces = []

        with open(filename) as f:
            self.documentLines = f.read().splitlines()

        self.read()

    def read(self):
        for line in self.documentLines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v':
                    self.vertices.append(list(map(int, value.split(' '))))                