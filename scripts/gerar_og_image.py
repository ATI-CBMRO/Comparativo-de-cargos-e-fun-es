"""Gera public/og-portal-cbm.png — a imagem do preview de link (Open Graph).

Por que um PNG gerado, e não um SVG: WhatsApp, Telegram e afins não renderizam
SVG em preview de link. E por que um script, e não um arquivo solto: assim a
imagem pode ser regerada quando a marca mudar, sem depender de ninguém reabrir
um editor.

Reproduz o bloco de marca da barra lateral (App.jsx, `.sidebar-logo-icon` com
`<Flame strokeWidth={2.5} color="#fff">`): chama branca sobre quadrado vermelho
arredondado, em fundo azul-marinho.

O traçado é o do ícone `Flame` do lucide, o MESMO que a barra lateral desenha,
transcrito abaixo em coordenadas absolutas. Tentar reaproveitar a silhueta de
public/favicon.svg não funciona: lá a chama só existe pela sobreposição de três
demãos coloridas, e a demão externa sozinha, preenchida, vira uma gota d'água.

Rodar:  python scripts/gerar_og_image.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

SAIDA = Path(__file__).parent.parent / "public" / "og-portal-cbm.png"

# Espelham as variáveis de src/index.css. Se mudarem lá, mude aqui e regere.
NAVY = "#121d3d"        # --navy-850, fundo da barra lateral
VERMELHO = "#c8102e"    # --cbm-red-700, fundo do selo
BRANCO = "#ffffff"

LADO = 1024             # imagem final, quadrada
SELO = 640              # lado do quadrado vermelho
RAIO = 160              # 25% do lado, mesma proporção do selo de 40px/raio 10px
CHAMA_ALTURA = 0.56     # fração do selo ocupada pela altura da chama
SUPER = 4               # supersampling: PIL não antialiasa polilinha nem cantos

# Ícone `Flame` do lucide, viewBox 24x24, traçado de 2.5 (o mesmo strokeWidth que
# App.jsx passa). Original:
#   M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6
#   .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3
#   a2.5 2.5 0 0 0 2.5 2.5z
# Convertido para absoluto aqui para não precisar de um parser de path completo.
VIEWBOX = 24.0
TRACO = 2.5
INICIO = (8.5, 14.5)
# ("A", rx, ry, rotacao, arco_grande, sentido, destino) | ("C", c1, c2, destino)
SEGMENTOS = [
    ("A", 2.5, 2.5, 0.0, 0, 0, (11.0, 12.0)),
    ("C", (11.0, 10.62), (10.5, 10.0), (10.0, 9.0)),
    ("C", (8.928, 6.857), (9.776, 4.946), (12.0, 3.0)),
    ("C", (12.5, 5.5), (14.0, 7.9), (16.0, 9.5)),
    ("C", (18.0, 11.1), (19.0, 13.0), (19.0, 15.0)),
    ("A", 7.0, 7.0, 0.0, 1, 1, (5.0, 15.0)),
    ("C", (5.0, 13.847), (5.433, 12.706), (6.0, 12.0)),
    ("A", 2.5, 2.5, 0.0, 0, 0, (8.5, 14.5)),
]
PASSOS = 220            # amostras por segmento; alto porque o traço é carimbado
                        # disco a disco (ver gerar()) e precisa de sobreposição


def _cubica(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
        u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1],
    )


def _pontos_do_arco(p0, rx, ry, rot_graus, arco_grande, sentido, p1, passos):
    """Amostra um arco elíptico do SVG (conversão endpoint→centro, spec F.6.5).

    Amostra a elipse direto em vez de convertê-la para Bézier: o resultado aqui
    só precisa virar polilinha, então o passo intermediário não paga o preço.
    """
    phi = math.radians(rot_graus)
    cos_p, sin_p = math.cos(phi), math.sin(phi)

    dx2 = (p0[0] - p1[0]) / 2.0
    dy2 = (p0[1] - p1[1]) / 2.0
    x1 = cos_p * dx2 + sin_p * dy2
    y1 = -sin_p * dx2 + cos_p * dy2

    rx, ry = abs(rx), abs(ry)
    # Raio pequeno demais para alcançar o destino: a spec manda escalar os dois.
    lamb = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry)
    if lamb > 1:
        escala = math.sqrt(lamb)
        rx *= escala
        ry *= escala

    num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    den = rx * rx * y1 * y1 + ry * ry * x1 * x1
    fator = math.sqrt(max(0.0, num / den))
    if arco_grande == sentido:
        fator = -fator
    cx1 = fator * rx * y1 / ry
    cy1 = -fator * ry * x1 / rx

    cx = cos_p * cx1 - sin_p * cy1 + (p0[0] + p1[0]) / 2.0
    cy = sin_p * cx1 + cos_p * cy1 + (p0[1] + p1[1]) / 2.0

    theta1 = math.atan2((y1 - cy1) / ry, (x1 - cx1) / rx)
    theta2 = math.atan2((-y1 - cy1) / ry, (-x1 - cx1) / rx)
    dtheta = theta2 - theta1
    if sentido == 0 and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sentido == 1 and dtheta < 0:
        dtheta += 2 * math.pi

    pontos = []
    for passo in range(1, passos + 1):
        t = theta1 + dtheta * (passo / passos)
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        pontos.append((cos_p * x - sin_p * y + cx, sin_p * x + cos_p * y + cy))
    return pontos


def pontos_da_chama():
    """Achata o traçado num anel fechado de pontos, no espaço original 24x24."""
    pontos = [INICIO]
    atual = INICIO
    for seg in SEGMENTOS:
        if seg[0] == "C":
            _, c1, c2, fim = seg
            for passo in range(1, PASSOS + 1):
                pontos.append(_cubica(atual, c1, c2, fim, passo / PASSOS))
        else:
            _, rx, ry, rot, grande, sentido, fim = seg
            pontos.extend(_pontos_do_arco(atual, rx, ry, rot, grande, sentido, fim, PASSOS))
        atual = seg[-1]
    pontos.append(INICIO)  # fecha o contorno (o `z` do path)
    return pontos


def gerar():
    lado = LADO * SUPER
    img = Image.new("RGB", (lado, lado), NAVY)
    draw = ImageDraw.Draw(img)

    selo = SELO * SUPER
    x0 = (lado - selo) / 2
    draw.rounded_rectangle(
        [x0, x0, x0 + selo, x0 + selo], radius=RAIO * SUPER, fill=VERMELHO
    )

    bruto = pontos_da_chama()
    minx = min(p[0] for p in bruto)
    maxx = max(p[0] for p in bruto)
    miny = min(p[1] for p in bruto)
    maxy = max(p[1] for p in bruto)

    escala = (selo * CHAMA_ALTURA) / (maxy - miny)
    # Centraliza pela CAIXA do desenho, não pelo viewBox: a chama não é simétrica
    # dentro dos 24x24 e sairia deslocada dentro do selo.
    dx = (lado - (maxx - minx) * escala) / 2 - minx * escala
    dy = (lado - (maxy - miny) * escala) / 2 - miny * escala
    pontos = [(p[0] * escala + dx, p[1] * escala + dy) for p in bruto]

    # Traço carimbado disco a disco, e não com draw.line(joint="curve"): o PIL
    # emenda cada segmento como um retângulo próprio e deixa farpas visíveis em
    # toda junção. Discos sobrepostos dão o mesmo resultado que um traço de ponta
    # e junção redondas, que é como o lucide desenha (stroke-linecap: round).
    raio = TRACO * escala / 2
    for x, y in pontos:
        draw.ellipse([x - raio, y - raio, x + raio, y + raio], fill=BRANCO)

    img = img.resize((LADO, LADO), Image.LANCZOS)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    img.save(SAIDA, "PNG", optimize=True)
    print(f"Gerado: {SAIDA} ({LADO}x{LADO}, {SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    gerar()
