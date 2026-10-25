import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Retro Racing: Legends", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing: Legends")
st.markdown("💻 **No PC:** Use as **Setas**. 📱 **No Celular:** Clique em **Ativar Movimento** e incline o aparelho!")

# Inicializa o estado do jogo na memória
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False

# ================= MENU INICIAL =================
if not st.session_state.jogo_iniciado:
    st.subheader("⚙️ Garagem & Configurações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        carro_escolhido = st.selectbox(
            "Escolha o seu Veículo:",
            options=["Ferrari Vermelha", "Bugatti Verde", "Combe Branca"]
        )
        
    with col2:
        dificuldade = st.select_slider(
            "Selecione a Dificuldade:",
            options=["Fácil", "Médio", "Difícil", "Modo Ico"]
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🏁 Ligar os Motores (Começar Jogo)", use_container_width=True):
        st.session_state.dificuldade_escolhida = dificuldade
        st.session_state.carro_escolhido = carro_escolhido
        st.session_state.jogo_iniciado = True
        st.rerun()

# ================= TELA DO JOGO =================
if st.session_state.jogo_iniciado:
    
    if st.button("🛑 Voltar à Garagem (Trocar Carro/Nível)"):
        st.session_state.jogo_iniciado = False
        st.rerun()
        
    dificuldade = st.session_state.dificuldade_escolhida
    carro_escolhido = st.session_state.carro_escolhido
    
    if dificuldade == "Fácil":
        vel_pista = 4
        chance_spawn = 0.012
    elif dificuldade == "Médio":
        vel_pista = 6
        chance_spawn = 0.025
    elif dificuldade == "Difícil":
        vel_pista = 10
        chance_spawn = 0.045
    else:
        vel_pista = 18
        chance_spawn = 0.090

    codigo_do_jogo = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; overflow: hidden; background-color: #111; display: flex; flex-direction: column; align-items: center; }
        canvas { background-color: #333; box-shadow: 0 0 30px rgba(0,0,0,1); border-radius: 5px; margin-top: 10px; max-width: 100%; height: auto;}
        #btn-movimento { 
            margin-top: 10px; padding: 10px 20px; font-size: 16px; font-weight: bold; 
            background-color: #ff9800; color: white; border: none; border-radius: 5px; cursor: pointer;
        }
    </style>
    </head>
    <body>
    <button id="btn-movimento">📱 Ativar Controle por Movimento (Celular)</button>
    <canvas id="gameCanvas" width="500" height="600"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const baseSpeed = __VEL_PISTA__;
        const spawnChance = __CHANCE_SPAWN__;
        const myCarType = "__CARRO_ESCOLHIDO__";

        // Define as dimensões do carro baseado na escolha do jogador
        let pWidth = 40, pHeight = 75, pSpeed = 7;
        if (myCarType === "Combe Branca") { pWidth = 48; pHeight = 90; pSpeed = 5; }
        if (myCarType === "Bugatti Verde") { pWidth = 42; pHeight = 70; pSpeed = 8; }

        // Variáveis de estado do jogo
        let player = { x: 230, y: 480, width: pWidth, height: pHeight, speed: pSpeed, dx: 0, dy: 0 };
        let obstacles = [];
        let score = 0;
        let distance = 0;
        let gameOver = false;
        let isPaused = false;
        let isMobileControl = false;

        // Função para reiniciar o jogo
        function restartGame() {
            player.x = 230;
            player.y = 480;
            player.dx = 0;
            player.dy = 0;
            obstacles = [];
            score = 0;
            distance = 0;
            gameOver = false;
            isPaused = false;
        }

        // ================= CONTROLE POR MOVIMENTO (Giroscópio) =================
        document.getElementById("btn-movimento").addEventListener("click", function() {
            if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
                DeviceOrientationEvent.requestPermission()
                    .then(permissionState => {
                        if (permissionState === 'granted') {
                            window.addEventListener("deviceorientation", handleOrientation);
                            document.getElementById("btn-movimento").style.display = "none";
                            isMobileControl = true;
                        }
                    })
                    .catch(console.error);
            } else {
                window.addEventListener("deviceorientation", handleOrientation);
                document.getElementById("btn-movimento").style.display = "none";
                isMobileControl = true;
            }
        });

        function handleOrientation(event) {
            if (gameOver || isPaused) {
                player.dx = 0; player.dy = 0;
                return;
            }

            let x = event.gamma; // Esquerda/Direita [-90, 90]
            let y = event.beta;  // Cima/Baixo [-180, 180]

            // Zonas neutras para não ser muito sensível
            if (x > 10) player.dx = player.speed;
            else if (x < -10) player.dx = -player.speed;
            else player.dx = 0;

            // Assumindo que a pessoa segura o celular inclinado a ~45 graus
            if (y > 55) player.dy = player.speed;
            else if (y < 35) player.dy = -player.speed;
            else player.dy = 0;
        }

        // Toque na tela para reiniciar ou pausar no celular
        canvas.addEventListener("touchstart", (e) => {
            e.preventDefault();
            if (gameOver) {
                restartGame();
            } else {
                isPaused = !isPaused;
            }
        });

        // ================= CONTROLES DE TECLADO (PC) =================
        document.addEventListener("keydown", (e) => {
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight", " ", "Enter"].indexOf(e.key) > -1 || e.code === "Space") {
                e.preventDefault();
            }
            
            if (!gameOver && !isPaused && !isMobileControl) {
                if (e.key === "ArrowLeft") player.dx = -player.speed;
                if (e.key === "ArrowRight") player.dx = player.speed;
                if (e.key === "ArrowUp") player.dy = -player.speed;
                if (e.key === "ArrowDown") player.dy = player.speed;
            }
            
            if (e.key === " " || e.code === "Space") {
                if (!gameOver) isPaused = !isPaused;
            }

            if (e.key === "Enter" && gameOver) {
                restartGame();
            }
        });

        document.addEventListener("keyup", (e) => {
            if (!isMobileControl) {
                if (e.key === "ArrowLeft" || e.key === "ArrowRight") player.dx = 0;
                if (e.key === "ArrowUp" || e.key === "ArrowDown") player.dy = 0;
            }
        });

        // DESENHO DOS VEÍCULOS
        function drawFerrari(x, y, w, h) {
            ctx.save(); ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(-5, 5, w+10, h);
            let grad = ctx.createLinearGradient(0, 0, w, 0);
            grad.addColorStop(0, "#800000"); grad.addColorStop(0.5, "#ff1a1a"); grad.addColorStop(1, "#800000");
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.roundRect(0, 0, w, h, 8); ctx.fill();
            ctx.fillStyle = "rgba(10, 10, 10, 0.9)";
            ctx.beginPath(); ctx.moveTo(6, 25); ctx.lineTo(w-6, 25); ctx.lineTo(w-2, 45); ctx.lineTo(2, 45); ctx.fill(); 
            ctx.fillRect(6, 55, w-12, 10);
            ctx.fillStyle = "#cc0000"; ctx.fillRect(0, h-8, w, 5);
            ctx.fillStyle = "#ffff99"; ctx.fillRect(4, 2, 8, 4); ctx.fillRect(w-12, 2, 8, 4);
            ctx.restore();
        }

        function drawCombe(x, y, w, h) {
            ctx.save(); ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(-3, 3, w+6, h); 
            let grad = ctx.createLinearGradient(0, 0, w, 0);
            grad.addColorStop(0, "#cccccc"); grad.addColorStop(0.5, "#ffffff"); grad.addColorStop(1, "#cccccc");
            ctx.fillStyle = grad; ctx.fillRect(0, 0, w, h);
            ctx.strokeStyle = "#999"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(0, 20); ctx.lineTo(w/2, 35); ctx.lineTo(w, 20); ctx.stroke();
            ctx.fillStyle = "rgba(40, 60, 80, 0.9)"; ctx.fillRect(2, 2, w-4, 18);
            ctx.fillStyle = "#fffacd";
            ctx.beginPath(); ctx.arc(8, 28, 5, 0, Math.PI*2); ctx.arc(w-8, 28, 5, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        function drawBugatti(x, y, w, h) {
            ctx.save(); ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(-4, 5, w+8, h);
            let grad = ctx.createLinearGradient(0, 0, w, 0);
            grad.addColorStop(0, "#003300"); grad.addColorStop(0.5, "#00e600"); grad.addColorStop(1, "#003300");
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.ellipse(w/2, h/2, w/2, h/2, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#000"; ctx.fillRect(w/2 - 6, 0, 12, 12);
            ctx.fillStyle = "rgba(0,0,0,0.9)";
            ctx.beginPath(); ctx.ellipse(w/2, h/3 + 5, w/2 - 6, 12, 0, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        function drawTrack() {
            ctx.fillStyle = "#2e8b57";
            ctx.fillRect(0, 0, 40, canvas.height);
            ctx.fillRect(canvas.width - 40, 0, 40, canvas.height);
            
            ctx.fillStyle = "#333";
            ctx.fillRect(40, 0, canvas.width - 80, canvas.height);

            if (!isPaused && !gameOver) distance += baseSpeed;
            let offset = distance % 60;

            for(let y = -60 + offset; y < canvas.height; y += 60) {
                ctx.fillStyle = (Math.floor(y / 60) % 2 === 0) ? "#cc0000" : "#ffffff";
                ctx.fillRect(30, y, 10, 60); 
                ctx.fillRect(canvas.width - 40, y, 10, 60); 
                ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                ctx.fillRect(canvas.width/2 - 3, y + 15, 6, 30);
            }
        }

        function spawnObstacle() {
            let types = ["Ferrari Vermelha", "Combe Branca", "Bugatti Verde"];
            let type = types[Math.floor(Math.random() * types.length)];
            
            let w = 40, h = 75, spdModifier = 0;
            if (type === "Combe Branca") { w = 48; h = 90; spdModifier = -2; }
            if (type === "Bugatti Verde") { w = 42; h = 70; spdModifier = 3; }

            let xPos = 50 + Math.random() * (canvas.width - 100 - w);
            obstacles.push({ x: xPos, y: -100, width: w, height: h, speed: baseSpeed + spdModifier, type: type });
        }

        function update() {
            if (gameOver || isPaused) return;

            player.x += player.dx;
            player.y += player.dy;

            if (player.x < 40) player.x = 40;
            if (player.x + player.width > canvas.width - 40) player.x = canvas.width - 40 - player.width;
            
            if (player.y < 0) player.y = 0; 
            if (player.y + player.height > canvas.height) player.y = canvas.height - player.height; 

            for (let i = 0; i < obstacles.length; i++) {
                obstacles[i].y += obstacles[i].speed;
                
                let margin = 5;
                if (player.x + margin < obstacles[i].x + obstacles[i].width - margin &&
                    player.x + player.width - margin > obstacles[i].x + margin &&
                    player.y + margin < obstacles[i].y + obstacles[i].height - margin &&
                    player.y + player.height - margin > obstacles[i].y + margin) {
                    gameOver = true;
                }
            }

            if (obstacles.length > 0 && obstacles[0].y > canvas.height) {
                obstacles.shift();
                score += 100; 
            }

            if (Math.random() < spawnChance) spawnObstacle();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawTrack();
            
            if(myCarType === "Ferrari Vermelha") drawFerrari(player.x, player.y, player.width, player.height);
            else if(myCarType === "Combe Branca") drawCombe(player.x, player.y, player.width, player.height);
            else if(myCarType === "Bugatti Verde") drawBugatti(player.x, player.y, player.width, player.height);
            
            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                if(obs.type === "Ferrari Vermelha") drawFerrari(obs.x, obs.y, obs.width, obs.height);
                else if(obs.type === "Combe Branca") drawCombe(obs.x, obs.y, obs.width, obs.height);
                else if(obs.type === "Bugatti Verde") drawBugatti(obs.x, obs.y, obs.width, obs.height);
            }

            ctx.fillStyle = "white"; ctx.font = "bold 24px Arial";
            ctx.shadowColor = "black"; ctx.shadowBlur = 5;
            ctx.fillText("Score: " + score, 50, 40);
            ctx.shadowBlur = 0; 

            if (isPaused && !gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "yellow";
                ctx.font = "bold 40px Arial";
                ctx.textAlign = "center";
                ctx.fillText("PAUSADO", canvas.width / 2, canvas.height / 2);
                ctx.font = "20px Arial";
                ctx.fillText("Toque na tela para voltar", canvas.width / 2, canvas.height / 2 + 35);
            }

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(0, canvas.height/2 - 60, canvas.width, 120);
                ctx.fillStyle = "red";
                ctx.font = "bold 40px Arial";
                ctx.textAlign = "center";
                ctx.fillText("ACIDENTE!", canvas.width / 2, canvas.height / 2);
                ctx.font = "20px Arial";
                ctx.fillStyle = "white";
                ctx.fillText("Toque na tela (ou Enter) para reiniciar", canvas.width / 2, canvas.height / 2 + 35);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }
        
        loop();
    </script>
    </body>
    </html>
    """

    codigo_do_jogo = codigo_do_jogo.replace("__VEL_PISTA__", str(vel_pista))
    codigo_do_jogo = codigo_do_jogo.replace("__CHANCE_SPAWN__", str(chance_spawn))
    codigo_do_jogo = codigo_do_jogo.replace("__CARRO_ESCOLHIDO__", carro_escolhido)

    components.html(codigo_do_jogo, height=700)
