import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Retro Racing: Legends", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing: Legends")
st.markdown("Use as **Setas** para pilotar, **'Espaço'** para pausar e **'Enter'** para reiniciar em caso de acidente!")

# Inicializa o estado do jogo na memória
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False

# ================= MENU INICIAL =================
if not st.session_state.jogo_iniciado:
    st.subheader("⚙️ Garagem & Configurações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        carro_escolhido = st.selectbox(
            "Escolha seu Veículo:",
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
    <style>
        body { margin: 0; overflow: hidden; background-color: #111; display: flex; justify-content: center; }
        canvas { background-color: #333; box-shadow: 0 0 30px rgba(0,0,0,1); border-radius: 5px; margin-top: 10px; }
    </style>
    </head>
    <body>
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

        // Controles de Teclado
        document.addEventListener("keydown", (e) => {
            // Evita que botões rodem a página
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight", " ", "Enter"].indexOf(e.key) > -1 || e.code === "Space") {
                e.preventDefault();
            }
            
            // Movimentação
            if (!gameOver && !isPaused) {
                if (e.key === "ArrowLeft") player.dx = -player.speed;
                if (e.key === "ArrowRight") player.dx = player.speed;
                if (e.key === "ArrowUp") player.dy = -player.speed;
                if (e.key === "ArrowDown") player.dy = player.speed;
            }
            
            // Pausa na barra de espaço
            if (e.key === " " || e.code === "Space") {
                if (!gameOver) isPaused = !isPaused;
            }

            // Reiniciar no Enter
            if (e.key === "Enter" && gameOver) {
                restartGame();
            }
        });

        document.addEventListener("keyup", (e) => {
            if (e.key === "ArrowLeft" || e.key === "ArrowRight") player.dx = 0;
            if (e.key === "ArrowUp" || e.key === "ArrowDown") player.dy = 0;
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
            ctx.strokeStyle = "#99
