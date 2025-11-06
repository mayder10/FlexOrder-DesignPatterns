from abc import ABC, abstractmethod

# ==========================================================
# ESTRATÉGIA DE PAGAMENTO
# ==========================================================

class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor):
        pass


class PagamentoCredito(EstrategiaPagamento):
    def processar_pagamento(self, valor):
        print(f"Processando R${valor:.2f} via Cartão de Crédito...")
        if valor < 1000:
            print("   -> Pagamento com Crédito APROVADO.")
            return True
        else:
            print("   -> Pagamento com Crédito REJEITADO (limite excedido).")
            return False
    

class PagamentoPix(EstrategiaPagamento):
    def processar_pagamento(self, valor):
        print(f"Processando R${valor:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True


class PagamentoMana(EstrategiaPagamento):    
    def processar_pagamento(self, valor):
        print(f"Processando R${valor:.2f} via Transferência de Mana...") 
        print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
        return True


# ==========================================================
# ESTRATÉGIA DE FRETE
# ==========================================================

class EstrategiaFrete(ABC):
    @abstractmethod
    def calcular_frete(self, valor):
        pass


class FreteNormal(EstrategiaFrete):
    def calcular_frete(self, valor):
        custo = valor * 0.00
        print(f"Frete Normal: R${custo:.2f}")
        return custo


class FreteExpresso(EstrategiaFrete): 
    def calcular_frete(self, valor):
        custo = valor * 0.10 + 15.00
        print(f"Frete Expresso (com taxa): R${custo:.2f}")
        return custo


class FreteTeletransporte(EstrategiaFrete):
    def calcular_frete(self, valor):
        custo = 50.00
        print(f"Frete Teletransporte: R${custo:.2f}")
        return custo


# ==========================================================
# DECORATOR - DESCONTO E EXTRAS
# ==========================================================

class PedidoBase(ABC):
    @abstractmethod
    def calcular_total(self):
        pass


class PedidoSimples(PedidoBase):
    def __init__(self, itens):
        self.itens = itens

    def calcular_total(self):
        return sum(item['valor'] for item in self.itens)


class PedidoDecorator(PedidoBase):
    def __init__(self, pedido):
        self.pedido = pedido


class DescontoPix(PedidoDecorator):
    def calcular_total(self):
        valor_base = self.pedido.calcular_total()
        print("Aplicando 5% de desconto PIX.")
        return valor_base * 0.95


class EmbalagemPresente(PedidoDecorator):
    def calcular_total(self):
        valor = self.pedido.calcular_total()
        print("Adicionando custo de embalagem para presente: R$10.00")
        return valor + 10.00


# ==========================================================
# FACHADA DO CHECKOUT
# ==========================================================

class CheckoutFacade:
    def __init__(self):
        self.pagamentos = {
            'Credito': PagamentoCredito(),
            'Pix': PagamentoPix(),
            'Mana': PagamentoMana()
        }

        self.fretes = {
            'Normal': FreteNormal(),
            'Expresso': FreteExpresso(),
            'Teletransporte': FreteTeletransporte()
        }

    def concluir_transacao(self, itens, metodo_pagamento, tipo_frete, tem_embalagem_presente=False):
        print("=========================================")
        print("INICIANDO CHECKOUT MODULARIZADO...")

        # Etapa 1 - Pedido base
        pedido = PedidoSimples(itens)

        # Etapa 2 - Regras de desconto
        if metodo_pagamento == 'Pix':
            pedido = DescontoPix(pedido)

        # Etapa 3 - Embalagem presente
        if tem_embalagem_presente:
            pedido = EmbalagemPresente(pedido)

        # Etapa 4 - Total + Frete
        valor_com_desconto = pedido.calcular_total()
        custo_frete = self.fretes[tipo_frete].calcular_frete(valor_com_desconto)
        valor_final = valor_com_desconto + custo_frete

        print(f"\nValor final com frete: R${valor_final:.2f}")

        # Etapa 5 - Processar pagamento
        sucesso = self.pagamentos[metodo_pagamento].processar_pagamento(valor_final)

        # Etapa 6 - Conclusão
        if sucesso:
            print("Transação concluída com SUCESSO!")
            print("Nota fiscal emitida com sucesso.\n")
        else:
            print("Transação FALHOU. Por favor, tente novamente.")
            print("=========================================\n")


# ==========================================================
# EXEMPLOS DE USO
# ==========================================================

if __name__ == "__main__":
    loja = CheckoutFacade()

    # Pedido 1 - PIX + Frete Normal
    itens1 = [
        {'nome': 'Capa da Invisibilidade', 'valor': 150.0},
        {'nome': 'Poção de Voo', 'valor': 80.0}
    ]
    loja.concluir_transacao(itens1, 'Pix', 'Normal')

    print("\n--- Próximo Pedido ---")

    # Pedido 2 - Crédito + Expresso + Presente
    itens2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    loja.concluir_transacao(itens2, 'Credito', 'Expresso', tem_embalagem_presente=True)
