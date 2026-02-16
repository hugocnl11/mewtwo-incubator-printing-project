"""
Animación de monitoreo de Mewtwo - Pantalla vertical estilo laboratorio
"""
import pygame
import math
import random
import os

# Configuración - Pantalla horizontal (landscape)
WIDTH = 854
HEIGHT = 480
FPS = 60

# Colores
BG_COLOR = (10, 22, 40)      # Azul oscuro #0a1628
NEON_BLUE = (56, 189, 248)   # #38bdf8
NEON_LIGHT = (125, 211, 252) # #7dd3fc
BUBBLE_COLOR = (125, 211, 252, 80)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Subject #151 - Mewtwo")
    clock = pygame.time.Clock()

    # Fuentes
    font_mono = pygame.font.SysFont("Consolas", 24)
    font_title = pygame.font.SysFont("Consolas", 32)

    # Cargar imagen de Mewtwo si existe
    assets_path = os.path.join(os.path.dirname(__file__), "assets")
    mewtwo_path = os.path.join(assets_path, "mewtwo.png")
    mewtwo_img = None
    if os.path.exists(mewtwo_path):
        mewtwo_img = pygame.image.load(mewtwo_path).convert_alpha()

    # Estado de animación
    time = 0.0
    dna_angle = 0.0
    ecg_offset = 0.0
    heart_scale = 1.0

    # Burbujas
    num_bubbles = 20
    bubbles = []
    for _ in range(num_bubbles):
        bubbles.append({
            "x": random.uniform(0, WIDTH),
            "y": random.uniform(0, HEIGHT),
            "radius": random.uniform(2, 8),
            "speed": random.uniform(0.3, 1.2),
        })

    # Patrón ECG: 100% segmentos rectos, estilo robótico/digital
    def generate_ecg_points(length=200):
        points = []
        for i in range(length):
            t = i / length
            # Solo líneas rectas, sin curvas
            if t < 0.05:
                y = 0
            elif t < 0.075:
                y = 0.2 * (t - 0.05) / 0.025   # P subida
            elif t < 0.10:
                y = 0.2 - 0.2 * (t - 0.075) / 0.025  # P bajada
            elif t < 0.15:
                y = 0
            elif t < 0.18:
                y = -0.6 * (t - 0.15) / 0.03   # Q bajada
            elif t < 0.22:
                y = -0.6 + 1.8 * (t - 0.18) / 0.04  # R subida
            elif t < 0.26:
                y = 1.2 - 1.5 * (t - 0.22) / 0.04   # S bajada
            elif t < 0.35:
                y = 0.35 * (t - 0.26) / 0.09   # T subida
            elif t < 0.45:
                y = 0.35 - 0.35 * (t - 0.35) / 0.10  # T bajada
            else:
                y = 0
            points.append((i * 3, y * 35))
        return points

    ecg_template = generate_ecg_points()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar animaciones
        dna_angle += 45 * dt
        ecg_offset += 120 * dt
        if ecg_offset > 600:
            ecg_offset -= 600

        # Latido del corazón ~72 BPM (ciclo ~0.83s)
        heart_phase = (time % 0.83) / 0.83
        if heart_phase < 0.15:
            heart_scale = 1.0 + 0.2 * (heart_phase / 0.15)
        elif heart_phase < 0.3:
            heart_scale = 1.2 - 0.2 * ((heart_phase - 0.15) / 0.15)
        else:
            heart_scale = 1.0

        # Actualizar burbujas
        for b in bubbles:
            b["y"] -= b["speed"]
            if b["y"] < -b["radius"]:
                b["y"] = HEIGHT + b["radius"]
                b["x"] = random.uniform(0, WIDTH)

        # Dibujar fondo
        screen.fill(BG_COLOR)

        # Dibujar burbujas
        for b in bubbles:
            size = int(b["radius"] * 4)
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(s, (*NEON_LIGHT, 60), (size // 2, size // 2), int(b["radius"]))
            screen.blit(s, (b["x"] - size // 2, b["y"] - size // 2))

        # Dibujar ADN (derecha)
        draw_dna(screen, WIDTH - 80, HEIGHT // 2, dna_angle)

        # Dibujar etiquetas (abajo izquierda)
        label1 = font_mono.render("SUBJECT #151", True, NEON_BLUE)
        label2 = font_title.render("MEWTWO", True, NEON_LIGHT)
        screen.blit(label1, (30, HEIGHT - 80))
        screen.blit(label2, (30, HEIGHT - 50))

        # Dibujar corazón (arriba izquierda)
        draw_heart(screen, 50, 60, heart_scale)

        # Dibujar ECG (junto al corazón)
        draw_ecg(screen, 100, 55, ecg_offset, ecg_template)

        # Dibujar Mewtwo (centro) con efecto respirar + flotar
        draw_mewtwo(screen, mewtwo_img, WIDTH // 2, HEIGHT // 2, time)

        pygame.display.flip()

    pygame.quit()


def draw_dna(surface, cx, cy, angle_deg):
    """Dibuja símbolo de ADN con rotación."""
    segments = 20
    height_span = 320
    radius = 25
    node_radius = 4

    s = pygame.Surface((120, height_span), pygame.SRCALPHA)
    s.set_alpha(140)

    for i in range(segments):
        theta = (i / segments) * 2 * math.pi + math.radians(angle_deg)
        x1 = 60 + radius * math.cos(theta)
        y1 = (i / segments) * height_span
        x2 = 60 - radius * math.cos(theta)
        y2 = y1

        pygame.draw.circle(s, NEON_LIGHT, (int(x1), int(y1)), node_radius)
        pygame.draw.circle(s, NEON_LIGHT, (int(x2), int(y2)), node_radius)
        if i < segments - 1:
            theta_next = ((i + 1) / segments) * 2 * math.pi + math.radians(angle_deg)
            x1n = 60 + radius * math.cos(theta_next)
            y1n = ((i + 1) / segments) * height_span
            x2n = 60 - radius * math.cos(theta_next)
            pygame.draw.line(s, NEON_BLUE, (x1, y1), (x1n, y1n), 2)
            pygame.draw.line(s, NEON_BLUE, (x2, y2), (x2n, y1n), 2)
        pygame.draw.line(s, NEON_BLUE, (x1, y1), (x2, y2), 1)

    surface.blit(s, (cx - 60, cy - height_span // 2))


def draw_heart(surface, cx, cy, scale):
    """Dibuja corazón con escala para animación de latido."""
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        x = 16 * (math.sin(rad) ** 3)
        y = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)
        points.append((cx + x * scale, cy - y * scale))

    if len(points) > 1:
        pygame.draw.polygon(surface, NEON_LIGHT, points)
        pygame.draw.aalines(surface, NEON_BLUE, True, points, 1)


def draw_ecg(surface, start_x, center_y, offset, template):
    """Dibuja línea ECG con scroll horizontal."""
    points = []
    pattern_len = len(template) * 3
    for x in range(380):
        pattern_x = (offset + x) % pattern_len
        i = min(int(pattern_x / 3), len(template) - 1)
        dy = template[i][1]
        points.append((start_x + x, center_y - dy))
    if len(points) >= 2:
        pygame.draw.lines(surface, NEON_BLUE, False, points, 2)


def draw_mewtwo(surface, img, cx, cy, time=0.0):
    """Dibuja Mewtwo centrado con efecto de respirar y flotar."""
    if img is not None:
        # Flotar: movimiento muy suave vertical y ligero horizontal
        float_y = math.sin(time * 1.2) * 6
        float_x = math.sin(time * 0.9 + 0.5) * 3
        cx_eff = cx + float_x
        cy_eff = cy + float_y

        # Respirar: escala suave ~4.5 s por ciclo
        breath = math.sin(time * 2 * math.pi / 4.5) * 0.025
        breath_scale = 1.0 + breath  # entre ~0.975 y 1.025

        rect = img.get_rect(center=(cx_eff, cy_eff))
        max_w, max_h = 200, 280
        scale = min(max_w / rect.width, max_h / rect.height, 1.0) * breath_scale
        new_size = (int(rect.width * scale), int(rect.height * scale))
        scaled = pygame.transform.smoothscale(img, new_size)
        rect = scaled.get_rect(center=(cx_eff, cy_eff))

        # Halo opcional (sigue al sprite)
        halo = pygame.Surface((250, 320), pygame.SRCALPHA)
        pygame.draw.ellipse(halo, (*NEON_BLUE, 40), halo.get_rect(), 2)
        surface.blit(halo, (cx_eff - 125, cy_eff - 160))

        surface.blit(scaled, rect)
    else:
        # Placeholder
        placeholder = pygame.Surface((180, 220))
        placeholder.set_alpha(80)
        placeholder.fill(BG_COLOR)
        pygame.draw.rect(placeholder, NEON_BLUE, placeholder.get_rect(), 2)
        font = pygame.font.SysFont("Consolas", 28)
        text = font.render("MEWTWO", True, NEON_BLUE)
        tr = text.get_rect(center=(90, 110))
        placeholder.blit(text, tr)
        surface.blit(placeholder, (cx - 90, cy - 110))


if __name__ == "__main__":
    main()
