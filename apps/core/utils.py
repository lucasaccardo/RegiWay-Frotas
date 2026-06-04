# Funcao: funcoes utilitarias compartilhadas pelo projeto.
# Responsável: Lucas sureira.

def formatar_placa(placa):
    """Garante que as placas fiquem no padrão ABC-1234."""
    if placa and len(placa) == 7:
        return f"{placa[:3]}-{placa[3:]}".upper()
    return placa.upper() if placa else ""
