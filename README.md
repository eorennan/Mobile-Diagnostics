# Mobile Diagnostics Toolkit

Ferramenta simples de diagnóstico mobile via linha de comando para dispositivos Android, desenvolvida em Python para rodar no **Termux** com integração do **Termux:API**.

---

## Sobre o projeto

Ele coleta e exibe informações do sistema em tempo real diretamente pelo terminal — bateria, Wi-Fi, CPU, memória, armazenamento e uma pontuação geral de saúde do dispositivo.

---

## Funcionalidades

- Gerar relatório completo em arquivo `.txt`
- Visualizar resumo do sistema em tempo real sem criar arquivos
- Localizar o caminho do último relatório gerado

---

## Requisitos

- Dispositivo Android
- Termux + Termux:API instalados via [F-Droid](https://f-droid.org)
- Python 3

---

## Instalação

```bash
pkg install termux-api
pip install pyfiglet
python mobile_toolkit.py
```

---

## Como usar

| Opção | Descrição |
|-------|-----------|
| `[1]` Gerar Relatório | Coleta os dados e salva um `.txt` |
| `[2]` Live System Overview | Exibe as informações na tela |
| `[3]` Localizar Último Relatório | Mostra onde o arquivo está salvo |

---

## Desenvolvedor

Desenvolvido por **eorennan**
[LinkedIn](https://linkedin.com/in/renan-costa-pereira-5354ab3b9)
