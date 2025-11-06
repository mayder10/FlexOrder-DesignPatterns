# FlexOrder-DesignPatterns
##  Objetivos do Refatoramento

O código legado possuía problemas como:
- Multiplicidade de regras condicionais (`if/else`) misturadas.
- Cálculo de frete, descontos e formas de pagamento escritos dentro de um único método.
- classes com responsabilidades múltiplas.
- era necessário alterar código existente para adicionar novos recursos.

A nova versão resolve esses problemas **separando responsabilidades e permitindo extensões sem modificações internas**.

## Arquitetura Aplicada

 Componente , Responsabilidade , Padrão Usado 

 `EstrategiaPagamento` + subclasses | Processar diferentes pagamentos | **Strategy Pattern** |
 `EstrategiaFrete` + subclasses | Cálculo de frete customizável | **Strategy Pattern** |
 `PedidoSimples` e Decoradores | Aplicação de descontos e extras | **Decorator Pattern** |
 `CheckoutFacade` | Orquestração do processo de compra | **Facade Pattern** |

 ##  Explicação dos Padrões Utilizados

### 1) **Strategia  (Pagamento e Frete)**

**Antes:**  
O método de checkout tinha vários `if`s para decidir *como pagar* e *como calcular frete*.

**Depois:**  
Cada tipo de pagamento e frete virou uma classe independente:

```python
class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor):
        pass

 Corrige SRP: cada classe faz apenas UMA coisa
 Atende OCP: para adicionar Boleto, basta criar outra classe sem alterar código existente.

 2) Decorator Pattern (Descontos e Adicionais)

Antes:
Descontos e extras eram feitos com ifs dentro do cálculo do pedido.

Depois:
Um pedido “básico” pode ser decorado dinamicamente com modificadores:

pedido = PedidoSimples(itens)
pedido = DescontoPix(pedido)
pedido = EmbalagemPresente(pedido)

Permite encadear várias regras de negócio

 Evita duplicação de código
 Facilita adicionar novos descontos

 Facade Pattern (CheckoutFacade)

A CheckoutFacade simplifica a chamada das operações internas:
loja.concluir_transacao(itens, 'Pix', 'Normal')

Sem expor ao usuário a complexidade das regras internas.

Fluxo da Compra

Criar pedido

Aplicar descontos (opcional)

Aplicar adicionais como embalagem

Calcular total + frete

Processar pagamento

Finalizar transação


# Esemplo de uso 

itens = [
    {'nome': 'Poção de Força', 'valor': 120.0}
]

loja = CheckoutFacade()
loja.concluir_transacao(itens, 'Pix', 'Expresso', tem_embalagem_presente=True)

Benefícios da Nova Arquitetura
Problema do Código Antigo	            Solução Aplicada
Código difícil de entender   	        Responsabilidades separadas
Uso de muitos if/else	                Strategy e Decorator
Difícil adicionar novos recursos	    OCP respeitado
Classes com várias funções misturadas	SRP respeitado