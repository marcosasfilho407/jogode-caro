import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Retro Racing: Legends", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing: Legends")
st.markdown("Pilote sua **Ferrari Vermelha**, desvie das **Combes Brancas** (lentas) e dos **Bugattis Verdes** (rápidos)!")

# Inicializa o estado do jogo na memória do Streamlit
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False

# MENU INICIAL (Só aparece antes do jogo começar)
if not st.session_state.jogo_iniciado:
    st.subheader("⚙️ Configurações da Corrida")
    dificuldade = st.select_slider(
        "Selecione a Dificuldade antes de ir para a pista:",
        options=["Fácil", "Médio", "Difícil", "Modo Ico"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🏁 Ligar os Motores (Começar Jogo)", use_container_width=True):
        # Salva a escolha e muda o estado para iniciado
        st.session_state.dificuldade_escolhida = dificuldade
        st.session_state.jogo_iniciado = True
        st.rerun()

# TELA DO JOGO (Só aparece após clicar em começar)
if st.session_state.jogo_iniciado:
    
    # Botão para parar e voltar ao menu
    if st.button("🛑 Parar Jogo / Voltar ao Menu"):
        st.session_state.jogo_iniciado = False
        st.rerun()
        
    dificuldade = st.session_state.dificuldade_escolhida
    
    # Física do jogo baseada na dificuldade
    if dificuldade == "Fácil":
        vel_pista = 4
        chance_spawn = 0.012
    elif dificuldade == "Médio":
        vel_pista = 6
        chance_spawn = 0.025
    elif dificuldade == "Difícil":
        vel_pista = 10
        chance_spawn = 0.045
    else:  # Modo Ico (Extremo)
        vel_pista = 18
        chance_spawn = 0.090

    # Código do Jogo em HTML/JS com Gráficos Melhorados
    # Usamos .replace() no final para injetar as variáveis sem quebrar as chaves do JavaScript
    codigo_do_jogo = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #111; display: flex; justify-content: center; }
        canvas { background-color: #333; box-shadow: 0 0 30px rgba(0,0,0,1); border-radius: 5px; mt-2}
    </style>
    </head>
    <body>
    <canvas id="gameCanvas" width="500" height="600"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Variáveis injetadas pelo Python
        const baseSpeed = __VEL_PISTA__;
        const spawnChance = __CHANCE_SPAWN__;

        // Jogador (Ferrari Vermelha)
        let player = { x: 230, y: 480, width: 40, height: 75, speed: 7, dx: 0 };
        let obstacles = [];
        let score = 0;
        let distance = 0;
        let gameOver = false;

        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") player.dx = -player.speed;
            if (e.key === "ArrowRight") player.dx = player.speed;
        });
        document.addEventListener("keyup", (e) => {
            if (e.key === "ArrowLeft" || e.key === "ArrowRight") player.dx = 0;
        });

        // DESENHO: FERRARI VERMELHA
        function drawFerrari(x, y, w, h) {
            ctx.save();
            ctx.translate(x, y);
            // Sombra
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(-5, 5, w+10, h);
            // Pintura Metálica Vermelha
            let grad = ctx.createLinearGradient(0, 0, w, 0);
            grad.addColorStop(0, "#800000"); grad.addColorStop(0.5, "#ff1a1a"); grad.addColorStop(1, "#800000");
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.roundRect(0, 0, w, h, 8); // Corpo aerodinâmico
            ctx.fill();
            // Para-brisa e Teto
            ctx.fillStyle = "rgba(10, 10, 10, 0.9)";
            ctx.beginPath(); ctx.moveTo(6, 25); ctx.lineTo(w-6, 25); ctx.lineTo(w-2, 45); ctx.lineTo(2, 45); ctx.fill(); // Vidro frente
            ctx.fillRect(6, 55, w-12, 10); // Vidro traseiro
            // Aerofólio Traseiro
            ctx.fillStyle = "#cc0000"; ctx.fillRect(0, h-8, w, 5);
            // Faróis
            ctx.fillStyle = "#ffff99";
            ctx.fillRect(4, 2, 8, 4); ctx.fillRect(w-12, 2, 8, 4);
            ctx.restore();
        }

        // DESENHO: COMBE BRANCA (Mais larga, quadrada e lenta)
        function drawCombe(x, y, w, h) {
            ctx.save();
            ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(-3, 3, w+6, h); // Sombra
            // Pintura
            let grad = ctx.createLinearGradient(0, 0, w, 0);
            grad.addColorStop(0, "#cccccc"); grad.addColorStop(0.5, "#ffffff"); grad.addColorStop(1, "#cccccc");
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, w, h);
            // Detalhe V da frente da Kombi
            ctx.strokeStyle = "#999"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(0, 20); ctx.lineTo(w/2, 35); ctx.lineTo(w, 20); ctx.stroke();
            // Para-brisa plano
            ctx.fillStyle = "rgba(40, 60, 80, 0.9)";
            ctx.fillRect(2, 2, w-4, 18);
            // Faróis redondos
            ctx.fillStyle = "#fffacd";
            ctx.beginPath(); ctx.arc(8, 28, 5, 0, Math.PI*2); ctx.arc(w-8, 28, 5, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        // DESENHO: BUGATTI VERDE (Mais redondo e rápido)
        function drawBugatti(x, y, w, h) {
            ctx.save();
            ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(-4, 5, w+8, h);
            // Pintura Verde Metálica
            let grad = ctx.createLinearGradient(0, 0, w, 0);
            grad.addColorStop(0, "#003300"); grad.addColorStop(0.5, "#00e600"); grad.addColorStop(1, "#003300");
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.ellipse(w/2, h/2, w/2, h/2, 0, 0, Math.PI*2);
            ctx.fill();
            // Grade em ferradura (Marca registrada)
            ctx.fillStyle = "#000"; ctx.fillRect(w/2 - 6, 0, 12, 12);
            // Para-brisa curvado
            ctx.fillStyle = "rgba(0,0,0,0.9)";
            ctx.beginPath(); ctx.ellipse(w/2, h/3 + 5, w/2 - 6, 12, 0, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        function drawTrack() {
            // Grama
            ctx.fillStyle = "#2e8b57";
            ctx.fillRect(0, 0, 40, canvas.height);
            ctx.fillRect(canvas.width - 40, 0, 40, canvas.height);
            
            // Asfalto
            ctx.fillStyle = "#333";
            ctx.fillRect(40, 0, canvas.width - 80, canvas.height);

            // Animação da pista (Zebras e Faixas)
            distance += baseSpeed;
            let offset = distance % 60;

            for(let y = -60 + offset; y < canvas.height; y += 60) {
                // Zebras laterais
                ctx.fillStyle = (Math.floor(y / 60) % 2 === 0) ? "#cc0000" : "#ffffff";
                ctx.fillRect(30, y, 10, 60); // Esquerda
                ctx.fillRect(canvas.width - 40, y, 10, 60); // Direita
                
                // Faixas centrais pontilhadas
                ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                ctx.fillRect(canvas.width/2 - 3, y + 15, 6, 30);
            }
        }

        function spawnObstacle() {
            let types = ["combe", "bugatti"];
            let type = types[Math.floor(Math.random() * types.length)];
            
            // Combe é mais larga e devagar; Bugatti é menor e bem mais rápido
            let w = type === "combe" ? 48 : 42;
            let h = type === "combe" ? 90 : 70;
            let spdModifier = type === "combe" ? -2 : 3; 

            // Mantém os inimigos dentro do asfalto
            let xPos = 50 + Math.random() * (canvas.width - 100 - w);
            
            obstacles.push({ x: xPos, y: -100, width: w, height: h, speed: baseSpeed + spdModifier, type: type });
        }

        function update() {
            if (gameOver) return;

            // Movimento do jogador
            player.x += player.dx;
            // Impede a Ferrari de sair do asfalto
            if (player.x < 40) player.x = 40;
            if (player.x + player.width > canvas.width - 40) player.x = canvas.width - 40 - player.width;

            // Movimento dos obstáculos
            for (let i = 0; i < obstacles.length; i++) {
                obstacles[i].y += obstacles[i].speed;
                
                // Sistema de Colisão (Hitbox um pouco menor para ser mais justo)
                let margin = 5;
                if (player.x + margin < obstacles[i].x + obstacles[i].width - margin &&
                    player.x + player.width - margin > obstacles[i].x + margin &&
                    player.y + margin < obstacles[i].y + obstacles[i].height - margin &&
                    player.y + player.height - margin > obstacles[i].y + margin) {
                    gameOver = true;
                }
            }

            // Aumentar score e remover carros antigos
            if (obstacles.length > 0 && obstacles[0].y > canvas.height) {
                obstacles.shift();
                score += 100; // 100 pontos por ultrapassagem
            }

            if (Math.random() < spawnChance) spawnObstacle();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawTrack();
            
            drawFerrari(player.x, player.y, player.width, player.height);
            
            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                if(obs.type === "combe") drawCombe(obs.x, obs.y, obs.width, obs.height);
                else drawBugatti(obs.x, obs.y, obs.width, obs.height);
            }

            // HUD / Placar
            ctx.fillStyle = "white";
            ctx.font = "bold 24px Arial";
            ctx.shadowColor = "black";
            ctx.shadowBlur = 5;
            ctx.fillText("Score: " + score, 50, 40);
            ctx.shadowBlur = 0; // reset

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(0, canvas.height/2 - 60, canvas.width, 120);
                ctx.fillStyle = "red";
                ctx.font = "bold 40px Arial";
                ctx.textAlign = "center";
                ctx.fillText("ACIDENTE!", canvas.width / 2, canvas.height / 2);
                ctx.font = "20px Arial";
                ctx.fillStyle = "white";
                ctx.fillText("Pare o jogo pelo menu acima para tentar de novo", canvas.width / 2, canvas.height / 2 + 35);
            }
        }

        function loop() {
            update();
            draw();
            if (!gameOver) requestAnimationFrame(loop);
        }
        
        loop();
    </script>
    </body>
    </html>
    """

    # Aplica as variáveis Python no HTML/JS
    codigo_do_jogo = codigo_do_jogo.replace("__VEL_PISTA__", str(vel_pista)).replace("__CHANCE_SPAWN__", str(chance_spawn))

    # Renderiza o jogo
    components.html(codigo_do_jogo, height=650)
