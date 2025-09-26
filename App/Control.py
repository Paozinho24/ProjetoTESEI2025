import Model

class ControllerLogin:
    def __init__(self):
        # model deve ser uma instância de Model
        self.Model = Model.Model()

    def login(self, cpf, senha):
        # Normaliza entradas de forma explícita
        if cpf is None:
            cpf = ""
        else:
            cpf = str(cpf)
            cpf = cpf.strip()

        if senha is None:
            senha = ""
        else:
            senha = str(senha)

        resultado = self.Model.validar_login(cpf, senha)
        return resultado
