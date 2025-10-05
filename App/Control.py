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

    def atualizar_Reagente(self, id, nome, formula=None, cas=None, unidade=None, quantidade=None, armario=None, prateleira=None, posicao=None):
        return self.Model.atualizar_Reagente(id, nome, formula, cas, unidade, quantidade, armario, prateleira, posicao)
    
    
    def getNomeUsuario(self, cpf):
        return self.Model.getNomeUsuario(cpf)

    # Usuários (Tecnicos) CRUD
    def listar_tecnicos(self):
        return self.Model.listar_tecnicos()
    # FunçãoApenas para pegar o CPF
    def PegarCPF(self, cpf):
        return self.Model.PegarCPF(cpf)

    def inserir_tecnico(self, nome, cpf, senha, email=None):
        return self.Model.inserir_tecnico(nome, cpf, senha, email)

    def atualizar_tecnico(self, nome, cpf, senha, email, original_cpf):
        return self.Model.atualizar_tecnico(nome, cpf, senha, email, original_cpf)

    def deletar_tecnico(self, cpf):
        return self.Model.deletar_tecnico(cpf)