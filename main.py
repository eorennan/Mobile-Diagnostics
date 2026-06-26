import os
import json
import subprocess
import time
import speedtest
from datetime import datetime
from pyfiglet import Figlet

# =============================
# CONFIGURAÇÕES
# =============================

DESENVOLVEDOR = "eorennan"
LINKEDIN = "linkedin.com/in/renan-costa-pereira-5354ab3b9"
VERSAO = "v2.0"
HOST_PING = "8.8.8.8"
CAMINHO_RELATORIO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "reports"
)
HISTORICO_SCORE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "score_history.txt"
)

os.makedirs(CAMINHO_RELATORIO, exist_ok=True)



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


def barra_progresso(valor, maximo=100, tamanho=20):
    preenchido = int(tamanho * valor / maximo)
    barra = "█" * preenchido + "░" * (tamanho - preenchido)
    return f"[{barra}] {valor}/{maximo}"


def titulo():
    limpar()
    banner = Figlet(font="big")
    print(banner.renderText("Mobile"))
    print(banner.renderText("Toolkit"))
    print("╔══════════════════════════════════════╗")
    print(f"║  MOBILE DIAGNOSTICS TOOLKIT {VERSAO}    ║")
    print(f"║  Dev: {DESENVOLVEDOR:<31}║")
    print("╚══════════════════════════════════════╝")


# =============================
# COLETA DE DADOS
# =============================

def bateria():
    try:
        dados = json.loads(executar(["termux-battery-status"]))
        return dados
    except Exception as erro:
        print(f"[ERRO] Bateria: {erro}")
        return {}


def wifi():
    try:
        dados = json.loads(executar(["termux-wifi-connectioninfo"]))
        return dados
    except Exception as erro:
        print(f"[ERRO] Wi-Fi: {erro}")
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


def memoria_disponivel_mb():
    try:
        info = executar(["cat", "/proc/meminfo"])
        for linha in info.splitlines():
            if "MemAvailable" in linha:
                kb = int(linha.split()[1])
                return kb // 1024
        return None
    except Exception as erro:
        print(f"[ERRO] Memória: {erro}")
        return None


def teste_ping():
    try:
        resultado = executar(["ping", "-c", "4", HOST_PING])
        for linha in resultado.splitlines():
            if "avg" in linha or "rtt" in linha:
                avg = float(linha.split("/")[4])
                return avg
        return None
    except Exception as erro:
        print(f"[ERRO] Ping: {erro}")
        return None


def teste_velocidade():
    try:
        print("\n[INFO] Testando velocidade da internet...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        return round(download, 2), round(upload, 2)
    except Exception as erro:
        print(f"[ERRO] Speedtest: {erro}")
        return None, None


# =============================
# HEALTH SCORE
# =============================

def calcular_score(bat=None, ping=None, mem_mb=None):
    score = 100
    detalhes = []

    # Bateria — até 30 pontos
    try:
        porcentagem = bat.get("percentage", 100)
        temperatura = bat.get("temperature", 30)

        if porcentagem < 50:
            score -= 10
            detalhes.append("Bateria abaixo de 50%: -10pts")
        if porcentagem < 20:
            score -= 10
            detalhes.append("Bateria abaixo de 20%: -10pts")
        if temperatura > 40:
            score -= 10
            detalhes.append(f"Temperatura alta ({temperatura}°C): -10pts")
    except Exception as erro:
        print(f"[ERRO] Score bateria: {erro}")

    # Memória — até 20 pontos
    try:
        if mem_mb is not None:
            if mem_mb < 500:
                score -= 20
                detalhes.append("Memória crítica (<500MB): -20pts")
            elif mem_mb < 1000:
                score -= 10
                detalhes.append("Memória baixa (<1GB): -10pts")
    except Exception as erro:
        print(f"[ERRO] Score memória: {erro}")

    # Rede — até 30 pontos
    try:
        if ping is not None:
            if ping > 80:
                score -= 20
                detalhes.append(f"Latência alta ({ping}ms): -20pts")
            elif ping > 30:
                score -= 10
                detalhes.append(f"Latência moderada ({ping}ms): -10pts")
        else:
            score -= 30
            detalhes.append("Sem conexão detectada: -30pts")
    except Exception as erro:
        print(f"[ERRO] Score rede: {erro}")

    return max(score, 0), detalhes


def salvar_historico(score):
    try:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(HISTORICO_SCORE, "a", encoding="utf-8") as f:
            f.write(f"{data} | Score: {score}/100\n")
    except Exception as erro:
        print(f"[ERRO] Histórico: {erro}")


# =============================
# RELATÓRIO
# =============================

def gerar_relatorio():
    titulo()
    print("\nColetando dados do dispositivo...\n")

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_arquivo = f"diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    caminho_arquivo = os.path.join(CAMINHO_RELATORIO, nome_arquivo)

    bat = bateria()
    rede = wifi()
    mem_mb = memoria_disponivel_mb()
    ping = teste_ping()
    score, detalhes = calcular_score(bat=bat, ping=ping, mem_mb=mem_mb)

    # Alerta de temperatura
    temperatura = bat.get("temperature", 0)
    if temperatura > 40:
        print(f"ALERTA: Temperatura elevada! {temperatura}°C")

    salvar_historico(score)

    relatorio = f"""
==================================================
   MOBILE DIAGNOSTICS TOOLKIT {VERSAO}
==================================================
Data        : {data}
Desenvolvedor: {DESENVOLVEDOR}

--------------------------------------------------
HEALTH SCORE
--------------------------------------------------
{barra_progresso(score)}

Detalhes:
"""
    for d in detalhes:
        relatorio += f"  - {d}\n"

    relatorio += f"""
--------------------------------------------------
DISPOSITIVO
--------------------------------------------------
Modelo      : {modelo_dispositivo()}
Android     : {versao_android()}

--------------------------------------------------
BATERIA
--------------------------------------------------
Porcentagem : {bat.get('percentage', 'N/A')}%
Temperatura : {bat.get('temperature', 'N/A')}°C
Status      : {bat.get('status', 'N/A')}
Saúde       : {bat.get('health', 'N/A')}

--------------------------------------------------
REDE
--------------------------------------------------
SSID        : {rede.get('ssid', 'N/A')}
IP          : {rede.get('ip', 'N/A')}
Latência    : {f'{ping:.1f}ms' if ping else 'N/A'}

--------------------------------------------------
MEMÓRIA DISPONÍVEL
--------------------------------------------------
{f'{mem_mb} MB' if mem_mb else 'N/A'}

--------------------------------------------------
CPU
--------------------------------------------------
{cpu()[:1500]}

--------------------------------------------------
ARMAZENAMENTO
--------------------------------------------------
{armazenamento()}

==================================================
FIM DA AUDITORIA
==================================================
"""

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)

    print("\n Relatório gerado com sucesso!")
    print(f"Arquivo: {nome_arquivo}")
    print(f"Pasta  : {CAMINHO_RELATORIO}")
    input("\nPressione ENTER para voltar ao menu...")


# =============================
# LIVE OVERVIEW
# =============================

def live_overview():
    try:
        while True:
            titulo()
            bat = bateria()
            rede = wifi()
            mem_mb = memoria_disponivel_mb()
            ping = teste_ping()
            score, _ = calcular_score(bat=bat, ping=ping, mem_mb=mem_mb)
            temperatura = bat.get("temperature", 0)

            print("\nLIVE SYSTEM OVERVIEW\n")
            print("=" * 50)
            print(f"Modelo       : {modelo_dispositivo()}")
            print(f"Android      : {versao_android()}")
            print("=" * 50)
            print(f"Bateria      : {bat.get('percentage', 'N/A')}%")
            print(f"Temperatura  : {temperatura}°C {'ALTA!' if temperatura > 40 else ''}")
            print(f"Status       : {bat.get('status', 'N/A')}")
            print("=" * 50)
            print(f"WiFi         : {rede.get('ssid', 'N/A')}")
            print(f"IP           : {rede.get('ip', 'N/A')}")
            print(f"Latência     : {f'{ping:.1f}ms' if ping else 'N/A'}")
            print(f"Memória livre: {f'{mem_mb} MB' if mem_mb else 'N/A'}")
            print("=" * 50)
            print(f"\nHEALTH SCORE: {barra_progresso(score)}")
            print("\n[Atualizando a cada 10s — Ctrl+C para sair]")
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")
        input("\nPressione ENTER para voltar ao menu...")


# =============================
# TESTE DE VELOCIDADE
# =============================

def menu_velocidade():
    titulo()
    print("\nTESTE DE VELOCIDADE\n")
    print("Isso pode levar alguns segundos...\n")

    ping = teste_ping()
    download, upload = teste_velocidade()

    print("\n" + "=" * 50)
    print(f"Latência     : {f'{ping:.1f}ms' if ping else 'N/A'}")
    print(f"Download     : {f'{download} Mbps' if download else 'N/A'}")
    print(f"Upload       : {f'{upload} Mbps' if upload else 'N/A'}")
    print("=" * 50)

    if ping:
        if ping < 30:
            print("Rede         : Excelente")
        elif ping < 80:
            print("Rede         :  Boa")
        else:
            print("Rede         :  Ruim")

    input("\nPressione ENTER para voltar ao menu...")


# =============================
# HISTÓRICO DE SCORES
# =============================

def ver_historico():
    titulo()
    print("\nHISTÓRICO DE HEALTH SCORES\n")
    print("=" * 50)

    if not os.path.exists(HISTORICO_SCORE):
        print("Nenhum histórico encontrado.")
        print("Gere um relatório primeiro (opção 1).")
    else:
        with open(HISTORICO_SCORE, "r", encoding="utf-8") as f:
            linhas = f.readlines()
        for linha in linhas[-20:]:
            print(linha.strip())

    print("=" * 50)
    input("\nPressione ENTER para voltar ao menu...")


# =============================
# LOCALIZAR RELATÓRIO
# =============================

def localizar_relatorio():
    titulo()
    print("\nRELATÓRIOS SALVOS\n")
    print("=" * 50)

    if not os.path.exists(CAMINHO_RELATORIO):
        print("Nenhum relatório encontrado.")
        input("\nPressione ENTER para voltar ao menu...")
        return

    arquivos = sorted(os.listdir(CAMINHO_RELATORIO), reverse=True)

    if not arquivos:
        print("Nenhum relatório encontrado.")
    else:
        for i, arquivo in enumerate(arquivos[:10], 1):
            caminho = os.path.join(CAMINHO_RELATORIO, arquivo)
            tamanho = os.path.getsize(caminho)
            print(f"[{i}] {arquivo} — {tamanho} bytes")

        print(f"\nPasta: {CAMINHO_RELATORIO}")

    print("=" * 50)
    input("\nPressione ENTER para voltar ao menu...")


# =============================
# MENU PRINCIPAL
# =============================

def main():
    while True:
        titulo()
        print("""
[1] Gerar Relatório Completo
    Coleta dados, calcula score e salva em TXT.

[2] Live System Overview
    Monitoramento em tempo real (atualiza a cada 10s).

[3] Teste de Velocidade
    Mede latência, download e upload.

[4] Histórico de Health Scores
    Exibe os últimos scores registrados.

[5] Localizar Relatórios
    Lista os relatórios salvos.

[0] Sair
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerar_relatorio()
        elif opcao == "2":
            live_overview()
        elif opcao == "3":
            menu_velocidade()
        elif opcao == "4":
            ver_historico()
        elif opcao == "5":
            localizar_relatorio()
        elif opcao == "0":
            print("\nEncerrando...")
            break
        else:
            input("\nOpção inválida. Pressione ENTER...")


if __name__ == "__main__":
    main()
