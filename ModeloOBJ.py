
class ModeloOBJ(object):

    def __init__(self, filename):
        m = open(filename,'r')

        self.lineas = m.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texture = []
        self.faces = []

        self.traducir()


    def traducir(self):

        for line in self.lineas:
            if line:
                tipo, valor = line.split(' ', 1)

                #Vertices
                if tipo == 'v':
                    self.vertices.append(list(map(float,valor.split(' '))))
                # Normales
                elif tipo == 'vn':
                    self.normals.append(list(map(float,valor.split(' '))))
                # Texturas
                elif tipo == 'vt':
                    self.texture.append(list(map(float,valor.split(' '))))
                # Caras
                elif tipo == 'f':
                    caras =  valor.split(' ')
                    lista=[]
                    for cara in caras:
                        if cara!='':
                            c = cara.split('/')
                            vector=[]
                            for x in c:
                                try:
                                    vector.append(int(x))
                                except:
                                    print("no int")
                            lista.append(vector)
                    self.faces.append(lista)



