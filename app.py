import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Retro Racing: Legends", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing: Legends")
st.markdown("💻 **PC:** Setas para pilotar, Espaço para pausar, Enter para reiniciar.\n\n📱 **Celular:** Incline para pilotar, toque no topo para pausar, toque na tela para reiniciar.")

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

# ================= TELA DO JOGO =================Para fazer o jogo funcionar no telemóvel utilizando o giroscópio/acelerómetro (inclinando o aparelho), precisamos de adicionar um evento JavaScript chamado `deviceorientation`. 

Como os navegadores modernos (especialmente no iPhone) exigem que o utilizador dê permissão explicitamente para aceder a estes sensores, adicionei um botão **"Ativar Sensores de Movimento"** que aparecerá por cima do jogo no telemóvel. Além disso, adicionei controlos por **toque no ecrã**: tocar pausa/despausa o jogo e, se bater, tocar no ecrã reinicia a partida (em vez de precisar do botão Enter).

Copie o código abaixo (use o botão de copiar no canto superior direito para evitar cortes) e substitua todo o conteúdo do seu ficheiro `app.py`:

```python
import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Retro Racing: Legends", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing: Legends")
st.markdown("💻 **PC:** Use as **Setas**, **Espaço** (Pausar) e **Enter** (Reiniciar).")
st.markdown("📱 **Telemóvel:** Clique em **'Ativar Sensores'**, incline o telemóvel para conduzir e **Toque no ecrã** para pausar ou reiniciar!")

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
        body { margin: 0; overflow: hidden; background-color: #111; display: flex; justify-content: center; align-items: center; position: relative; flex-direction: column;}
        canvas { background-color: #333; box-shadow: 0 0 30px rgba(0,0,0,1); border-radius: 5px; margin-top: 10px; max-width: 100%; height: auto;}
        #motionBtn {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            padding: 15px 25px; font-size: 18px; font-weight: bold; background-color: #ffaa00;
            color: #000; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            z-index: 10;
        }
    </style>
    </head>
    <body>
    <button id="motionBtn" onclick="requestMotionPermission()">📱 Ativar Sensores de Movimento</button>
    <canvas id="gameCanvas" width="500" height="600"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const baseSpeed = __VEL_PISTA__;
        const spawnChance = __CHANCE_SPAWN__;
        const myCarType = "__CARRO_ESCOLHIDO__";

        let pWidth = 40, pHeight = 75, pSpeed = 7;
        if (myCarType === "Combe Branca") { pWidth = 48; pHeight = 90; pSpeed = 5; }
        if (myCarType === "Bugatti Verde") { pWidth = 42; pHeight = 70; pSpeed = 8; }

        let player = { x: 230, y: 480, width: pWidth, height: pHeight, speed: pSpeed, dx: 0, dy: 0 };
        let obstacles = [];
        let score = 0;
        let distance = 0;
        let gameOver = false;
        let isPaused = false;
        let motionEnabled = false;

        function restartGame() {
            player.x = 230; player.y = 480; player.dx = 0; player.dy = 0;
            obstacles = []; score = 0; distance = 0;
            gameOver = false; isPaused = false;
        }

        // ================= CONTROLES DE MOVIMENTO (MOBILE) =================
        function requestMotionPermission() {
            if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
                DeviceOrientationEvent.requestPermission()
                    .then(permissionState => {
                        if (permissionState === 'granted') {
                            window.addEventListener('deviceorientation', handleOrientation);
                            document.getElementById('motionBtn').style.display = 'none';
                        }
                    })
                    .catch(console.error);
            } else {
                window.addEventListener('deviceorientation', handleOrientation);
                document.getElementById('motionBtn').style.display = 'none';
            }
        }

        // Esconde o botão se não for mobile (tela de toque)
        if (!('ontouchstart' in window)) {
            document.getElementById('motionBtn').style.display = 'none';
        }

        function handleOrientation(event) {
            if (gameOver || isPaused) return;
            
            let beta = event.beta;  // Frente/Trás [-180,180]
            let gamma = event.gamma; // Esquerda/Direita [-90,90]

            if (beta === null || gamma === null) return;

            // Controle Esquerda / Direita
            if (gamma > 10) player.dx = player.speed;
            else if (gamma < -10) player.dx = -player.speed;
            else player.dx = 0;

            // Controle Cima / Baixo (Assumindo que seguramos o celular a ~40 graus)
            if (beta > 55) player.dy = player.speed; // Inclinar para trás (frear)
            else if (beta < 25) player.dy = -player.speed; // Inclinar para frente (acelerar)
            else player.dy = 0;
        }

        // ================= TOQUE NA TELA =================
        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault(); // Evita scroll ao tocar
            if (gameOver) {
                restartGame();
            } else {
                isPaused = !isPaused;
            }
        });

        // ================= CONTROLES TE
