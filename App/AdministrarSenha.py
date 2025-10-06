from cryptography.fernet import Fernet

class AdministrarSenha:


    # 1) gerar uma chave (faça uma vez e guarde em local seguro/ENV)
    key = Fernet.generate_key()
    print(key.decode())  # copie e guarde

    # 2) criar o objeto com a chave
    f = Fernet(key) 

    # 3) criptografar (bytes → token)
    dados = b"segredo simples"
    token = f.encrypt(dados)
    print(token)  # base64 seguro p/ salvar no BD

    # 4) descriptografar (token → bytes)
    original = f.decrypt(token)
    print(original)  # b"segredo simples"
