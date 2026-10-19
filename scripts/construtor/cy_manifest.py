import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # trace_python.py
from bld import *

PASTA = "ciberseguranca"
TITULO = "Cibersegurança"
S = ["demos/cyber.js"]
# O cap. 7 (Kill Chain) fica fora até depois do prazo do CP03 de Cyber (26/10/2026 23:59): vira True depois disso.
PUBLICAR_KILL_CHAIN = False
CAPS = [
 dict(n=1, file="cap-1-modelo-osi.html", titulo="Redes e o modelo OSI", aula="Aula 1", tempo=35,
      resumo="As sete camadas, o encapsulamento, e MAC address, NIC.br e sistemas autônomos.",
      pergunta="O OSI organiza as camadas. Como cada dispositivo é endereçado e como os dados viajam de fato?"),
 dict(n=2, file="cap-2-ip-tcp-udp.html", titulo="IP, TCP e UDP", aula="Aula 1", tempo=40,
      resumo="IPv4 e IPv6, máscara de rede, o handshake de três vias e quando usar TCP ou UDP.",
      pergunta="Ninguém decora números de IP. Como um nome como google.com vira um endereço?"),
 dict(n=3, file="cap-3-dns.html", titulo="DNS: a agenda da internet", aula="Aula 2", tempo=40,
      resumo="A hierarquia raiz, TLD e autoritativo, os tipos de registro, o cache, ARP e traceroute.",
      pergunta="O DNS confia em quem responde. O que acontece se alguém mentir?"),
 dict(n=4, file="cap-4-ataques-a-rede.html", titulo="Ataques à rede e ao DNS", aula="Aulas 2 e 6", tempo=40,
      resumo="DNS spoofing, DNS tunneling, ARP spoofing e man in the middle, com HTTP x HTTPS.",
      pergunta="Esses ataques miram a rede. Quais miram a pessoa, a máquina e a aplicação?"),
 dict(n=5, file="cap-5-catalogo-de-ataques.html", titulo="Catálogo de ataques", aula="Aula 6", tempo=45,
      resumo="Phishing, engenharia social, malware, DDoS, força bruta, SQL injection e XSS, organizados por alvo.",
      pergunta="Conhecer o ataque é metade do caminho. Como me defendo?"),
 dict(n=6, file="cap-6-defesa.html", titulo="Defesa: criptografia, hash e camadas", aula="Complemento", tempo=45,
      resumo="Tríade CIA, criptografia simétrica e assimétrica, hash de senhas, 2FA, HTTPS e defesa em profundidade.",
      pergunta="Cada defesa cobre uma parte. Como enxergo um ataque inteiro, do começo ao fim?"),
 dict(n=7, file="cap-7-kill-chain.html", titulo="A cadeia do ataque (Kill Chain)", aula="Complemento", tempo=35,
      resumo="As sete etapas de um ataque segundo a Cyber Kill Chain e onde cada defesa o interrompe.",
      pergunta=""),
]
if not PUBLICAR_KILL_CHAIN:
    CAPS = CAPS[:6]
    CAPS[-1]["pergunta"] = ""


if __name__ == "__main__":
    manifest(PASTA, "ciberseguranca", TITULO, CAPS)
    hub(PASTA, TITULO, "Cognitive Cybersecurity", "Apostila de Cibersegurança",
        "Como a internet funciona por dentro e como ela é atacada e defendida: camadas, IP, DNS, o catálogo de ataques e as defesas, com demos para mexer.",
        ["<b>%d</b> capítulos" % len(CAPS), "<b>~%s</b> de estudo ativo" % ("4h30" if PUBLICAR_KILL_CHAIN else "4h05"), "demos de rede, DNS e hash"],
        '<p>Não dá para se defender do que não se entende. Por isso a apostila segue o caminho do dado: primeiro <mark class="hl">como ele viaja</mark> (camadas, IP, TCP, DNS), depois <mark class="hl p">como é atacado</mark> em cada ponto do caminho, e por fim <mark class="hl g">como se defender</mark>. Cada capítulo responde à pergunta que o anterior deixou.</p>',
        'Os ataques são explicados com <b>finalidade educativa e defensiva</b>: o objetivo é reconhecer e prevenir. Nada aqui ensina a invadir sistemas de terceiros, e quase todas as demos rodam só no seu navegador (a consulta DNS do Capítulo 3 envia o domínio que você digitar ao DNS público do Google, e as de SQL baixam a biblioteca sql.js de um CDN).')
    print("manifest ok")
