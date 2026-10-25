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
            options=["Ferrari Vermelha", "Bugatti Verde", "Combe Branca", "Moto Roxa", "Quadriciclo Rosa"]
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
    
    if st.button("🛑 Voltar à Garagem (Trocar Veículo/Nível)"):
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

        // Define as dimensões do veículo baseado na escolha do jogador
        let pWidth = 40, pHeight = 75, pSpeed = 7;
        if (myCarType === "Combe Branca") { pWidth = 48; pHeight = 90; pSpeed = 5; }
        else if (myCarType === "Bugatti Verde") { pWidth = 42; pHeight = 70; pSpeed = 8; }
        else if (myCarType === "Moto Roxa") { pWidth = 30; pHeight = 65; pSpeed = 9; }
        else if (myCarType === "Quadriciclo Rosa") { pWidth = 45; pHeight = 60; pSpeed = 6; }

        // Variáveis de estado do jogo
        let player = { x: 230, y: 480, width: pWidth, height: pHeight, speed: pSpeed, dx: 0, dy: 0 };
        let obstacles = [];
        let score = 0;
        let distance = 0;
        let gameOver = false;
        let isPaused = false;
        let isMobileControl = false;

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

        // ================= CONTROLES =================
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
            let x = event.gamma; 
            let y = event.beta;  
            if (x > 10) player.dx = player.speed;
            else if (x < -10) player.dx = -player.speed;
            else player.dx = 0;

            if (y > 55) player.dy = player.speed;
            else if (y < 35) player.dy = -player.speed;
            else player.dy = 0;
        }

        canvas.addEventListener("touchstart", (e) => {
            e.preventDefault();
            if (gameOver) restartGame();
            else isPaused = !isPaused;
        });

        document.addEventListener("keydown", (e) => {
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight", " ", "Enter"].indexOf(e.key) > -1 || e.code === "Space") e.preventDefault();
            if (!gameOver && !isPaused && !isMobileControl) {
                if (e.key === "ArrowLeft") player.dx = -player.speed;
                if (e.key === "ArrowRight") player.dx = player.speed;
                if (e.key === "ArrowUp") player.dy = -player.speed;
                if (e.key === "ArrowDown") player.dy = player.speed;
            }
            if (e.key === " " || e.code === "Space") if (!gameOver) isPaused = !isPaused;
            if (e.key === "Enter" && gameOver) restartGame();
        });

        document.addEventListener("keyup", (e) => {
            if (!isMobileControl) {
                if (e.key === "ArrowLeft" || e.key === "ArrowRight") player.dx = 0;
                if (e.key === "ArrowUp" || e.key === "ArrowDown") player.dy = 0;
            }
        });

        // ================= DESENHOS DOS VEÍCULOS =================
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

        function drawMoto(x, y, w, h) {
            ctx.save(); ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(w/2 - 10, 5, 20, h);
            ctx.fillStyle = "#6600cc"; // Roxa
            ctx.beginPath(); ctx.roundRect(w/2 - 8, 10, 16, h - 20, 5); ctx.fill();
            ctx.fillStyle = "#111"; // Pneus
            ctx.fillRect(w/2 - 5, 0, 10, 15);
            ctx.fillRect(w/2 - 6, h - 15, 12, 15);
            ctx.fillStyle = "#ccc"; // Guidão
            ctx.fillRect(w/2 - 14, 20, 28, 4);
            ctx.fillStyle = "#ffff99"; // Farol
            ctx.beginPath(); ctx.arc(w/2, 5, 5, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        function drawQuadriciclo(x, y, w, h) {
            ctx.save(); ctx.translate(x, y);
            ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(-2, 5, w+4, h);
            ctx.fillStyle = "#111"; // Pneus
            ctx.fillRect(0, 5, 12, 15);
            ctx.fillRect(w-12, 5, 12, 15);
            ctx.fillRect(0, h-20, 12, 15);
            ctx.fillRect(w-12, h-20, 12, 15);
            ctx.fillStyle = "#ff66b2"; // Rosa
            ctx.beginPath(); ctx.roundRect(8, 10, w - 16, h - 20, 5); ctx.fill();
            ctx.fillStyle = "#333"; // Banco
            ctx.fillRect(12, h/2 - 5, w - 24, 20);
            ctx.fillStyle = "#ccc"; // Guidão
            ctx.fillRect(4, 20, w - 8, 4);
            ctx.fillStyle = "#ffff99"; // Farol
            ctx.fillRect(w/2 - 6, 8, 12, 6);
            ctx.restore();
        }

        // ================= MECÂNICAS DE PISTA E OBSTÁCULOS =================
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
            let types = ["Ferrari Vermelha", "Combe Branca", "Bugatti Verde", "Moto Roxa", "Quadriciclo Rosa"];
            let type = types[Math.floor(Math.random() * types.length)];
            
            let w = 40, h = 75, spdModifier = 0;
            if (type === "Combe Branca") { w = 48; h = 90; spdModifier = -2; }
            else if (type === "Bugatti Verde") { w = 42; h = 70; spdModifier = 3; }
            else if (type === "Moto Roxa") { w = 30; h = 65; spdModifier = 4; }
            else if (type === "Quadriciclo Rosa") { w = 45; h = 60; spdModifier = -1; }

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
            
            let pTypes = {
                "Ferrari Vermelha": drawFerrari, "Combe Branca": drawCombe, 
                "Bugatti Verde": drawBugatti, "Moto Roxa": drawMoto, "Quadriciclo Rosa": drawQuadriciclo
            };
            
            pTypes[myCarType](player.x, player.y, player.width, player.height);
            
            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                pTypes[obs.type](obs.x, obs.y, obs.width, obs.height);
            }

            ctx.fillStyle = "white"; ctx.font = "bold 24px Arial";
            ctx.shadowColor = "black"; ctx.shadowBlur = 5;
            ctx.fillText("Score: " + score, 50, 40);
            ctx.shadowBlur = 0; 

            if (isPaused && !gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.5)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "yellow"; ctx.font = "bold 40px Arial"; ctx.textAlign = "center";
                ctx.fillText("PAUSADO", canvas.width / 2, canvas.height / 2);
                ctx.font = "20px Arial"; ctx.fillText("Toque na tela para voltar", canvas.width / 2, canvas.height / 2 + 35);
            }

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)"; ctx.fillRect(0, canvas.height/2 - 60, canvas.width, 120);
                ctx.fillStyle = "red"; ctx.font = "bold 40px Arial"; ctx.textAlign = "center";
                ctx.fillText("ACIDENTE!", canvas.width / 2, canvas.height / 2);
                ctx.font = "20px Arial"; ctx.fillStyle = "white";
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
