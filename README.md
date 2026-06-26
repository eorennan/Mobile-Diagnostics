# Mobile Diagnostics Toolkit

Ferramenta de diagnóstico e monitoramento para dispositivos Android desenvolvida em **Python**, projetada para execução no **Termux** com integração da **Termux:API**.

O projeto centraliza informações importantes do sistema em uma interface de linha de comando (CLI), permitindo acompanhar o estado do dispositivo em tempo real, gerar relatórios e manter um histórico da saúde do sistema.

---

## Sobre o projeto

O Mobile Diagnostics Toolkit foi desenvolvido com o objetivo de aplicar conceitos de automação, monitoramento e coleta de informações do sistema operacional Android utilizando Python.

A aplicação consulta dados do dispositivo por meio da **Termux:API** e de comandos nativos do sistema, apresentando informações sobre bateria, CPU, memória RAM, armazenamento, rede e velocidade da internet. Além disso, calcula um **Health Score** com base nas condições atuais do dispositivo.

---

## Funcionalidades

- Geração de relatórios completos em arquivos `.txt` com timestamp
- Monitoramento em tempo real com atualização automática
- Visualização de informações da bateria, CPU, memória RAM, armazenamento e rede
- Teste de velocidade da internet (Ping, Download e Upload)
- Cálculo do Health Score com barra de progresso
- Alerta automático para temperatura elevada da bateria
- Histórico dos Health Scores registrados
- Listagem dos relatórios gerados

---

## Arquitetura

- Python 3
- Termux
- Termux:API
- PyFiglet
- speedtest-cli

---

## Requisitos

- Dispositivo Android
- Termux e Termux:API instalados via **F-Droid**
- Python 3

---

## Instalação

```bash
pkg update
pkg install python termux-api
pip install pyfiglet speedtest-cli

python main.py
```

---

## Como usar

| Opção | Descrição |
|-------|-----------|
| `[1]` Gerar Relatório | Coleta as informações do dispositivo e gera um relatório `.txt` |
| `[2]` Monitoramento em Tempo Real | Exibe continuamente as informações do sistema com atualização automática |
| `[3]` Teste de Velocidade | Executa testes de Ping, Download e Upload da conexão |
| `[4]` Histórico de Health Scores | Exibe os registros anteriores da saúde do dispositivo |
| `[5]` Listar Relatórios | Exibe todos os relatórios armazenados |

---

## Conceitos aplicados

| Conceito | Ferramenta utilizada |
|----------|----------------------|
| Desenvolvimento de aplicações de linha de comando (CLI) | Python |
| Integração com APIs nativas do Android | Termux:API |
| Coleta de informações do sistema | Comandos do Termux, `subprocess` e Termux:API |
| Monitoramento em tempo real | Python (`time`) |
| Processamento e interpretação de dados | Python |
| Geração de relatórios automatizados | Manipulação de arquivos `.txt` |
| Registro e consulta de histórico | Sistema de arquivos e Python |
| Teste de conectividade e velocidade da rede | `speedtest-cli` |
| Estruturação e modularização da aplicação | Funções e módulos em Python |
| Interface em linha de comando | PyFiglet e recursos nativos do terminal |

---

## Desenvolvedor

**Renan Costa Pereira**

LinkedIn: <https://linkedin.com/in/renan-costa-pereira-5354ab3b9>
