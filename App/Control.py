import Model  

class ControllerGeral:
    def __init__(self):
        # instancia a CLASSE Model de dentro do módulo Model
        self.Model = Model.Model()

    def login(self, cpf, senha):
        if cpf is None:
            cpf = ""
        else:
            cpf = str(cpf).strip()

        if senha is None:
            senha = ""
        else:
            senha = str(senha)

        return self.Model.validar_login(cpf, senha)

    def listar_reagentes_localizacao(self):
        return self.Model.listar_reagentes_localizacao()
    
    def cadastrar_Reagente(self,nome,formula=None,cas=None,unidade=None,quantidade=None,armario=None,prateleira=None,posicao=None, id=None):
        return self.Model.cadastrar_Reagente(nome, formula, cas, unidade, quantidade, armario, prateleira, posicao, id)
    
    def getNomeUsuario(self, cpf):
        return self.Model.getNomeUsuario(cpf)
