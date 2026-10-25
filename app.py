import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Retro Racing", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing")
st.markdown("Use as **Setas do Teclado (Esquerda/Direita)** para desviar dos outros carros!")

# Filtro de Dificuldade no Streamlit
dificuldade = st.select_slider(
    "Selecione a Dificuldade:",
    options=["Fácil", "Médio", "Difícil", "Modo Ico"]
)

# Configurando as variáveis do jogo baseado na dificuldade
if dificuldade == "Fácil":
    vel_obstaculo = 2
    chance_spawn = 0.010
elif dificuldade == "Médio":
    vel_obstaculo = 4
    chance_spawn = 0.025
elif dificuldade == "Difícil":
    vel_obstaculo = 7
    chance_spawn = 0.045
else:  # Modo Ico (Extremo)
    vel_obstaculo = 12
    chance_spawn = 0.080

st.markdown("---")

# Usamos f-string (f""") para injetar as variáveis do Python no JavaScript
codigo_do_jogo = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; overflow: hidden; background-color: #222; display: flex; justify-content: center; }}
    canvas {{ background-color: #555; border-left: 5px solid white; border-right: 5px solid white; box-shadow: 0 0 20px rgba(0,0,0,0.8); }}
</style>
</head>
<body>
<canvas id="gameCanvas" width="400" height="500"></canvas>
<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let car = {{ x: 175, y: 400, width: 40, height: 70, speed: 6, dx: 0 }};
    let obstacles = [];
    let score = 0;
    let lines = [0, 100, 200, 300, 400, 500];
    let gameOver = false;

    // Recebe as variáveis do Python
    const baseSpeed = {vel_obstaculo};
    const spawnChance = {chance_spawn};

    document.addEventListener("keydown", (e) => {{
        if (e.key === "ArrowLeft") car.dx = -car.speed;
        if (e.key === "ArrowRight") car.dx = car.speed;
    }});
    document.addEventListener("keyup", (e) => {{
        if (e.key === "ArrowLeft" || e.key === "ArrowRight") car.dx = 0;
    }});

    function drawCar(x, y, color) {{
        ctx.fillStyle = color;
        ctx.fillRect(x, y, car.width, car.height);
        ctx.fillStyle = "#000";
        ctx.fillRect(x + 5, y + 15, car.width - 10, 15);
        ctx.fillRect(x + 5, y + 45, car.width - 10, 10);
    }}

    function spawnObstacle() {{
        let xPos = Math.random() * (canvas.width - car.width);
        obstacles.push({{ x: xPos, y: -70, width: 40, height: 70, speed: baseSpeed + Math.random() * 2 }});
    }}

    function update() {{
        if (gameOver) return;

        car.x += car.dx;
        if (car.x < 0) car.x = 0;
        if (car.x + car.width > canvas.width) car.x = canvas.width - car.width;

        // A velocidade da pista acompanha a velocidade dos obstáculos
        for (let i = 0; i < lines.length; i++) {{
            lines[i] += baseSpeed;
            if (lines[i] > canvas.height) lines[i] = -50;
        }}

        for (let i = 0; i < obstacles.length; i++) {{
            obstacles[i].y += obstacles[i].speed;
            
            if (car.x < obstacles[i].x + obstacles[i].width &&
                car.x + car.width > obstacles[i].x &&
                car.y < obstacles[i].y + obstacles[i].height &&
                car.y + car.height > obstacles[i].y) {{
                gameOver = true;
            }}
        }}

        if (obstacles.length > 0 && obstacles[0].y > canvas.height) {{
            obstacles.shift();
            score += 10;
        }}

        if (Math.random() < spawnChance) spawnObstacle();
    }}

    function draw() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "white";
        for (let i = 0; i < lines.length; i++) {{
            ctx.fillRect(canvas.width / 2 - 5, lines[i], 10, 40);
        }}

        drawCar(car.x, car.y, "red");
        
        for (let i = 0; i < obstacles.length; i++) {{
            let color = baseSpeed > 10 ? "yellow" : "blue"; // Carros ficam amarelos no Modo Ico
            drawCar(obstacles[i].x, obstacles[i].y, color); 
        }}

        ctx.fillStyle = "white";
        ctx.font = "20px Arial";
        ctx.fillText("Score: " + score, 10, 30);

        if (gameOver) {{
            ctx.fillStyle = "red";
            ctx.font = "40px Arial";
            ctx.fillText("GAME OVER", 80, canvas.height / 2);
            ctx.font = "20px Arial";
            ctx.fillStyle = "white";
            ctx.fillText("Mude a dificuldade para reiniciar", 60, canvas.height / 2 + 30);
        }}
    }}

    function loop() {{
        update();
        draw();
        if (!gameOver) {{
            requestAnimationFrame(loop);
        }}
    }}
    
    loop();
</script>
</body>
</html>
"""

# Renderiza o jogo
components.html(codigo_do_jogo, height=550)
