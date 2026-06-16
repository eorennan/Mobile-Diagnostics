import os
import json
import subprocess
from datetime import datetime
from pyfiglet import Figlet


DESENVOLVEDOR = "eorennan"
LINKEDIN = "linkedin.com/in/renan-costa-pereira-5354ab3b9"
CAMINHO_RELATORIO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "diagnostic_report.txt"
)


def executar(comando):
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True
        )
        return resultado.stdout.strip()

    except Exception as erro:
        return f"Erro: {erro}"


def limpar():
    os.system("clear")


def titulo():

    limpar()

    banner = Figlet(font="big")

    print(banner.renderText("Mobile"))
    print(banner.renderText("Toolkit"))

    print("╔══════════════════════════════════════╗")
    print("║  MOBILE DIAGNOSTICS TOOLKIT v1.0     ║")
    print(f"║  Dev: {DESENVOLVEDOR:<31}║")
    print("╚══════════════════════════════════════╝")


# =============================
# COLETA DOS DADOS
# =============================

def bateria():
    try:
        dados = json.loads(
            executar(["termux-battery-status"])
        )
        return dados
    except:
        return {}


def wifi():
    try:
        dados = json.loads(
            executar(["termux-wifi-connectioninfo"])
        )
        return dados
    except:
        return {}


def modelo_dispositivo():
    return executar(["getprop", "ro.product.model"])


def versao_android():
    return executar(["getprop", "ro.build.version.release"])


def armazenamento():
    return executar(["df", "-h"])


def memoria():
    return executar(["cat", "/proc/meminfo"])


def cpu():
    return executar(["cat", "/proc/cpuinfo"])



def calcular_score():

    score = 100

    try:

        bat = bateria()

        porcentagem = bat.get("percentage", 100)

        if porcentagem < 50:
            score -= 10

        if porcentagem < 20:
            score -= 20

        temperatura = bat.get("temperature", 30)

        if temperatura > 40:
            score -= 15

    except:
        pass

    return max(score, 0)


# ==========================
# RELATÓRIO
# =============================

def gerar_relatorio():

    titulo()

    print("\nColetando dados do dispositivo...\n")

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    bat = bateria()
    rede = wifi()
    score = calcular_score()

    relatorio = f"""
==================================
MOBILE DIAGNOSTICS TOOLKIT v1.0
==================================

Data: {data}

------------------------------------------------------------
HEALTH SCORE
------------------------------------------------------------

Pontuação Geral: {score}/100

------------------------------------------------------------
DISPOSITIVO
------------------------------------------------------------

Modelo:
{modelo_dispositivo()}

Android:
{versao_android()}

------------------------------------------------------------
BATERIA
------------------------------------------------------------

Porcentagem:
{bat.get('percentage', 'N/A')} %

Temperatura:
{bat.get('temperature', 'N/A')} °C

Status:
{bat.get('status', 'N/A')}

Saúde:
{bat.get('health', 'N/A')}

------------------------------------------------------------
WI-FI
------------------------------------------------------------

SSID:
{rede.get('ssid', 'N/A')}

IP:
{rede.get('ip', 'N/A')}

------------------------------------------------------------
CPU
------------------------------------------------------------

{cpu()[:2000]}

------------------------------------------------------------
MEMÓRIA
------------------------------------------------------------

{memoria()[:2000]}

------------------------------------------------------------
ARMAZENAMENTO
------------------------------------------------------------

{armazenamento()}

============================
FIM DA AUDITORIA
============================
"""

    with open(CAMINHO_RELATORIO, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)

    print(" Relatório gerado com sucesso!")
    print(f"\nArquivo salvo em:\n{CAMINHO_RELATORIO}")

    input("\nPressione ENTER para voltar ao menu...")



def live_overview():

    titulo()

    bat = bateria()
    rede = wifi()

    print("\nSYSTEM OVERVIEW\n")

    print("=" * 50)

    print(f"Modelo       : {modelo_dispositivo()}")
    print(f"Android      : {versao_android()}")

    print("=" * 50)

    print(f"Bateria      : {bat.get('percentage', 'N/A')}%")
    print(f"Temperatura  : {bat.get('temperature', 'N/A')}°C")
    print(f"Status       : {bat.get('status', 'N/A')}")

    print("=" * 50)

    print(f"WiFi         : {rede.get('ssid', 'N/A')}")
    print(f"IP           : {rede.get('ip', 'N/A')}")

    print("=" * 50)

    print("\nHEALTH SCORE")
    print(f"Score        : {calcular_score()}/100")

    input("\nPressione ENTER para voltar ao menu...")



def localizar_relatorio():

    titulo()

    if not os.path.exists(CAMINHO_RELATORIO):
        print("\n Nenhum relatório encontrado.")
        print("  Gere um relatório primeiro (opção 1).")
        input("\nPressione ENTER para voltar ao menu...")
        return

    data_modificacao = os.path.getmtime(CAMINHO_RELATORIO)
    data_formatada = datetime.fromtimestamp(data_modificacao).strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    caminho_completo = CAMINHO_RELATORIO
    pasta_pai = os.path.basename(os.path.dirname(caminho_completo))
    tamanho = os.path.getsize(caminho_completo)

    print("\nRELATÓRIO LOCALIZADO\n")
    print("=" * 50)
    print(f"Arquivo      : diagnostic_report.txt")
    print(f"Pasta        : {pasta_pai}/")
    print(f"Caminho      : {caminho_completo}")
    print(f"Gerado em    : {data_formatada}")
    print(f"Tamanho      : {tamanho} bytes")
    print("=" * 50)
    print("\nPara abrir, acesse o gerenciador de")
    print(f"arquivos e navegue até a pasta '{pasta_pai}'.")

    input("\nPressione ENTER para voltar ao menu...")


# =============================
# MENU PRINCIPAL
# =============================

while True:

    titulo()

    print("""
[1] Gerar Relatório
    Coleta dados e salva em arquivo TXT.

[2] Live System Overview
    Exibe as informações na tela sem gerar arquivos.

[3] Localizar Último Relatório
    Exibe o caminho e a pasta onde o arquivo está salvo.

[0] Exit
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        gerar_relatorio()

    elif opcao == "2":

        live_overview()

    elif opcao == "3":

        localizar_relatorio()

    elif opcao == "0":

        print("\nEncerrando...")
        break

    else:

        input("\nOpção inválida. Pressione ENTER...")
