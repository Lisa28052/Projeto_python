import pygame
import sys
from random import choice

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Plataforma")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Fonte para texto
FONT = pygame.font.SysFont("Arial", 24)

# Carregar a imagem de fundo
background = pygame.image.load("Jogo_de_plataforma/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Redimensionar para caber na tela

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Jogo_de_plataforma/cavaleiro.png").convert_alpha()  # Carrega a imagem do personagem
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta o tamanho para 50x50
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 70)
        self.vel_y = 0
        self.jump_speed = -15
        self.gravity = 0.8
    

    def update(self, platforms):
        # Movimento horizontal
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Aplicar gravidade
        self.vel_y += self.gravity
        self.rect.y += self.vel_y



        # Checar colisão com plataformas
        if self.vel_y > 0:  # Apenas verificar colisão quando está caindo
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                self.rect.bottom = hits[0].rect.top
                self.vel_y = 0

    def jump(self):
        # Pulo somente se o jogador estiver em uma plataforma
        if self.vel_y == 0:
            self.vel_y = self.jump_speed
    

# Classe das plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Classe das moedas
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar a imagem da moeda
        self.image = pygame.image.load("Jogo_de_plataforma/moeda.png").convert_alpha()  # Carregar imagem com fundo transparente
        self.image = pygame.transform.scale(self.image, (30, 30))  # Ajustar o tamanho para 30x30 pixels
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# Função para exibir perguntas em um quadrado na tela principal
def show_question(question_data):
    # Dimensões do retângulo
    rect_width = 600
    rect_height = 200
    rect_x = (WIDTH - rect_width) // 2
    rect_y = (HEIGHT - rect_height) // 2

    # Fonte para perguntas e opções
    question_font = pygame.font.SysFont("Arial", 24)

    while True:
        # Desenhar o fundo e o quadrado
        SCREEN.blit(background, (0, 0))  # Redesenha o fundo
        all_sprites.draw(SCREEN)  # Redesenha os sprites
        pygame.draw.rect(SCREEN, WHITE, (rect_x, rect_y, rect_width, rect_height))  # Retângulo de fundo
        pygame.draw.rect(SCREEN, BLACK, (rect_x, rect_y, rect_width, rect_height), 5)  # Borda preta

        # Exibir a pergunta
        question_text = question_font.render(question_data["question"], True, BLACK)
        SCREEN.blit(question_text, (rect_x + 20, rect_y + 20))

        # Exibir as opções
        for i, option in enumerate(question_data["options"]):
            option_text = question_font.render(option, True, BLACK)
            SCREEN.blit(option_text, (rect_x + 20, rect_y + 60 + i * 30))

        # Atualizar a tela
        pygame.display.flip()

        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Verificar se a tecla pressionada corresponde à resposta
                if event.key == pygame.K_a and question_data["answer"] == "A":
                    return True
                if event.key == pygame.K_b and question_data["answer"] == "B":
                    return True
                if event.key == pygame.K_c and question_data["answer"] == "C":
                    return True
                return False


# Tela de transição entre níveis
def show_level_transition(level):
    SCREEN.fill(WHITE)
    text = FONT.render(f"Próximo Nível: {level + 1}", True, BLACK)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

# Função para carregar o nível
def load_level(level_data):
    # Limpar os grupos
    all_sprites.empty()
    platforms.empty()
    coins.empty()

    # Redefinir a posição do jogador no chão
    player.rect.midbottom = (WIDTH // 2, HEIGHT - 70)
    player.vel_y = 0  # Resetar a velocidade vertical do jogador
    all_sprites.add(player)

    # Adicionar plataformas
    for x, y, width, height in level_data["platforms"]:
        platform = Platform(x, y, width, height)
        all_sprites.add(platform)
        platforms.add(platform)

    # Adicionar moedas
    for x, y in level_data["coins"]:
        coin = Coin(x, y)
        all_sprites.add(coin)
        coins.add(coin)

    # Retornar as perguntas do nível
    return level_data["questions"]

# Lista de níveis (exemplo expandido)
levels = [
    # Nível 1 - Fácil
    {
        "platforms": [
            (0, HEIGHT - 20, WIDTH, 20),  # Chão
            (100, HEIGHT - 100, 200, 20),
            (350, HEIGHT - 200, 200, 20),
            (200, HEIGHT - 300, 200, 20),
            (400, HEIGHT - 400, 200, 20),
        ],
        "coins": [
            (150, HEIGHT - 120),
            (400, HEIGHT - 220),
            (250, HEIGHT - 320),
            (450, HEIGHT - 420),
        ],
        "questions": [
            {"question": "O que é uma poupança?", "options": ["A. Um tipo de investimento", "B. Um empréstimo", "C. Uma dívida"], "answer": "A"},
            {"question": "Qual é o objetivo de um orçamento?", "options": ["A. Gastar tudo", "B. Planejar despesas", "C. Ignorar receitas"], "answer": "B"},
        ],
    },
    # Nível 2 - Médio
    {
        "platforms": [
            (0, HEIGHT - 20, WIDTH, 20),  # Chão
            (150, HEIGHT - 150, 150, 20),
            (300, HEIGHT - 250, 150, 20),
            (100, HEIGHT - 350, 150, 20),
            (400, HEIGHT - 450, 150, 20),
        ],
        "coins": [
            (200, HEIGHT - 170),
            (350, HEIGHT - 270),
            (150, HEIGHT - 370),
            (450, HEIGHT - 470),
        ],
        "questions": [
            {"question": "O que é um investimento?", "options": ["A. Aplicar dinheiro para gerar mais", "B. Gastar sem controle", "C. Deixar o dinheiro parado"], "answer": "A"},
            {"question": "Qual é a vantagem da diversificação?", "options": ["A. Reduzir riscos", "B. Aumentar dívidas", "C. Concentrar ganhos"], "answer": "A"},
        ],
    },
    # Nível 3 - Difícil
    {
        "platforms": [
            (0, HEIGHT - 20, WIDTH, 20),  # Chão
            (50, HEIGHT - 150, 100, 20),
            (200, HEIGHT - 250, 120, 20),
            (400, HEIGHT - 350, 120, 20),
            (600, HEIGHT - 450, 80, 20),
        ],
        "coins": [
            (100, HEIGHT - 180),
            (250, HEIGHT - 270),
            (400, HEIGHT - 360),
            (500, HEIGHT - 480),
        ],
        "questions": [
            {"question": "O que significa liquidez de um ativo?", "options": ["A. A facilidade de vender um ativo rapidamente", "B. O tempo que leva para um ativo se valorizar", "C. A rentabilidade do ativo no longo prazo"], "answer": "A"},
            {"question": "Qual é a principal vantagem dos fundos imobiliários?", "options": ["A. Garantia de retorno fixo", "B. Diversificação e acesso ao mercado imobiliário", "C. Menor risco do mercado de ações"], "answer": "B"},
            {"question": "O que é a taxa de juros compostos?", "options": ["A. Juros sobre o valor original", "B. Juros sobre o valor original e sobre os juros acumulados", "C. Taxa fixa ao ano"], "answer": "B"},
        ],
    },
    # Nível 4 - Muito Difícil
    {
        "platforms": [
            (0, HEIGHT - 20, WIDTH, 20),  # Chão
            (150, HEIGHT - 150, 150, 20),
            (350, HEIGHT - 250, 120, 20),
            (200, HEIGHT - 350, 100, 20),
            (450, HEIGHT - 450, 200, 20),
        ],
        "coins": [
            (180, HEIGHT - 170),
            (300, HEIGHT - 270),
            (400, HEIGHT - 370),
            (500, HEIGHT - 470),
        ],
        "questions": [
            {"question": "O que significa o termo 'valor presente'?", "options": ["A. O valor de um ativo no futuro", "B. O valor de um ativo ajustado para o momento atual", "C. A soma de todos os fluxos de caixa futuros"], "answer": "B"},
            {"question": "Qual a principal característica dos títulos públicos?", "options": ["A. Rentabilidade fixa", "B. Garantia do governo", "C. Maior risco", "D. Liquidez diária"], "answer": "B"},
            {"question": "Qual o objetivo da análise técnica no mercado financeiro?", "options": ["A. Prever o movimento de preços com base em dados históricos", "B. Estudar as finanças das empresas", "C. Avaliar os impactos da economia global"], "answer": "A"},
        ],
    },
    # Nível 5 - Desafio Avançado
{
    "platforms": [
        (0, HEIGHT - 20, WIDTH, 20),  # Chão
        (100, HEIGHT - 100, 120, 20),
        (250, HEIGHT - 200, 100, 20),
        (400, HEIGHT - 300, 100, 20),
        (550, HEIGHT - 400, 80, 20),
        (700, HEIGHT - 500, 150, 20),
    ],
    "coins": [
        (120, HEIGHT - 120),
        (270, HEIGHT - 220),
        (420, HEIGHT - 320),
        (580, HEIGHT - 420),
        (750, HEIGHT - 520),
    ],
    "questions": [
        {"question": "O que é alavancagem financeira?", "options": ["A. Usar recursos próprios", "B. Utilizar recursos de terceiros para aumentar os retornos", "C. Reduzir os riscos financeiros"], "answer": "B"},
        {"question": "O que é a diversificação internacional?", "options": ["A. Investir apenas no mercado nacional", "B. Alocar recursos em diferentes países para diluir riscos", "C. Comprar ativos apenas de empresas multinacionais"], "answer": "B"},
        {"question": "O que é o índice de Sharpe?", "options": ["A. Uma medida de retorno ajustado ao risco", "B. A variação de preços de um ativo", "C. O total de lucros acumulados por uma empresa"], "answer": "A"},
    ],
},

# Nível 6 - Experiente
{
    "platforms": [
        (0, HEIGHT - 20, WIDTH, 20),  # Chão
        (50, HEIGHT - 150, 100, 20),
        (200, HEIGHT - 250, 120, 20),
        (350, HEIGHT - 350, 100, 20),
        (500, HEIGHT - 450, 150, 20),
        (650, HEIGHT - 550, 120, 20),
    ],
    "coins": [
        (70, HEIGHT - 170),
        (220, HEIGHT - 270),
        (370, HEIGHT - 370),
        (520, HEIGHT - 470),
        (700, HEIGHT - 570),
    ],
    "questions": [
        {"question": "O que é o preço/lucro (P/L)?", "options": ["A. Relação entre preço da ação e lucro por ação", "B. Valor total de uma empresa", "C. Taxa de crescimento anual"], "answer": "A"},
        {"question": "Qual a diferença entre ativo fixo e circulante?", "options": ["A. Fixo é imobilizado, circulante é líquido", "B. Fixo é dinheiro em caixa, circulante são bens físicos", "C. Não há diferença"], "answer": "A"},
        {"question": "O que é o mercado de derivativos?", "options": ["A. Mercado de compra e venda de commodities", "B. Mercado de ativos que derivam seu valor de outro ativo", "C. Mercado de títulos públicos"], "answer": "B"},
    ],
},

# Nível 7 - Mestre em Finanças
{
    "platforms": [
        (0, HEIGHT - 20, WIDTH, 20),  # Chão
        (100, HEIGHT - 100, 150, 20),
        (300, HEIGHT - 200, 100, 20),
        (450, HEIGHT - 300, 120, 20),
        (600, HEIGHT - 400, 100, 20),
        (750, HEIGHT - 500, 80, 20),
    ],
    "coins": [
        (150, HEIGHT - 120),
        (320, HEIGHT - 220),
        (470, HEIGHT - 320),
        (620, HEIGHT - 420),
        (780, HEIGHT - 520),
    ],
    "questions": [
        {"question": "O que significa volatilidade?", "options": ["A. Variação nos preços de um ativo", "B. Taxa de crescimento de um ativo", "C. Rentabilidade acumulada"], "answer": "A"},
        {"question": "O que é um fundo de hedge?", "options": ["A. Fundo com estratégias de alto risco", "B. Fundo que investe em ações de empresas pequenas", "C. Fundo exclusivo de títulos públicos"], "answer": "A"},
        {"question": "O que significa beta em finanças?", "options": ["A. Medida de sensibilidade de um ativo em relação ao mercado", "B. Taxa de crescimento de uma empresa", "C. Rendimento de um título público"], "answer": "A"},
    ],
},

# Nível 8 - Lendário
{
    "platforms": [
        (0, HEIGHT - 20, WIDTH, 20),  # Chão
        (50, HEIGHT - 120, 100, 20),
        (200, HEIGHT - 240, 150, 20),
        (400, HEIGHT - 360, 120, 20),
        (600, HEIGHT - 480, 100, 20),
        (750, HEIGHT - 600, 80, 20),
    ],
    "coins": [
        (80, HEIGHT - 140),
        (250, HEIGHT - 260),
        (420, HEIGHT - 380),
        (620, HEIGHT - 500),
        (780, HEIGHT - 620),
    ],
    "questions": [
        {"question": "O que é custo de oportunidade?", "options": ["A. Custo de abrir mão de algo para escolher outra coisa", "B. Valor total de uma oportunidade perdida", "C. Juros sobre investimentos"], "answer": "A"},
        {"question": "O que é valuation?", "options": ["A. Processo de avaliação do valor de uma empresa", "B. Taxa de juros de um título público", "C. Retorno líquido de uma ação"], "answer": "A"},
        {"question": "O que é risco sistêmico?", "options": ["A. Risco que afeta todo o mercado", "B. Risco de uma empresa específica", "C. Risco associado a mudanças no governo"], "answer": "A"},
    ],
},

]

# Criar o jogador e grupos de sprites
player = Player()
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites.add(player)

# Lógica principal do jogo
# Lógica principal do jogo
def main():
    level = 0
    score = 0

    while True:
        # Iniciar o nível
        if level < len(levels):  # Certifica-se de que há mais níveis disponíveis
            level_data = levels[level]
            questions = load_level(level_data)

            # Transição para o próximo nível (exibe mensagem apenas se não for o primeiro nível)
            if level > 0:
                show_level_transition(level)
        else:
            # Se todos os níveis foram completados
            SCREEN.fill(WHITE)
            victory_text = FONT.render("Você completou todos os níveis! Parabéns!", True, BLACK)
            SCREEN.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()

        # Loop do nível
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()

            # Atualizações do jogador
            player.update(platforms)

            # Verificar colisões com moedas
            for coin in coins:
                if player.rect.colliderect(coin.rect):
                    coin.kill()
                    score += 10  # Incrementar a pontuação

                    # Mostrar pergunta sobre educação financeira
                    question = choice(questions)
                    if show_question(question):
                        score += 20  # Resposta correta, pontuação extra
                    else:
                        score -= 20  # Resposta errada, perde mais pontos

            # Atualizar a tela
            SCREEN.blit(background, (0, 0))
            all_sprites.draw(SCREEN)

            # Exibir pontuação
            score_text = FONT.render(f"Pontuação: {score}", True, BLACK)
            SCREEN.blit(score_text, (10, 10))

            pygame.display.flip()

            # Checar se todas as moedas foram coletadas
            if len(coins) == 0:
                running = False  # Sai do loop do nível

            clock.tick(FPS)

        # Passa para o próximo nível
        level += 1

if __name__ == "__main__":
    main()

