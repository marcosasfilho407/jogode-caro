import streamlit as st
import streamlit.components.v1 as components

# Configuração da página no Streamlit
st.set_page_config(page_title="Retro Racing", page_icon="🏎️", layout="centered")

st.title("🏎️ Retro Racing (Estilo Top Gear)")
st.markdown("Use as **Setas do Teclado (Esquerda/Direita)** para desviar dos outros carros!")
st.markdown("---")

# Código do jogo (HTML/CSS/JS) encapsulado no Python
codigo_do_jogo = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; overflow: hidden; background-color: #222; display: flex; justify-content: center; }
    canvas { background-color: #555; border-left: 5px solid white; border-right: 5px solid white; box-shadow: 0 0 20px rgba(0,0,0,0.8); }
</style>
</head>
<body>
<canvas id="gameCanvas" width="400" height="500"></canvas>
<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let car = { x: 175, y: 400, width: 40, height: 70, speed: 5, dx: 0 };
    let obstacles = [];
    let score = 0;
    let lines = [0, 100, 200, 300, 400, 500];
    let gameOver = false;

    // Controles
    document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft") car.dx = -car.speed;
        if (e.key === "ArrowRight") car.dx = car.speed;
    });
    document.addEventListener("keyup", (e) => {
        if (e.key === "ArrowLeft" || e.key === "ArrowRight") car.dx = 0;
    });

    function drawCar(x, y, color) {
        ctx.fillStyle = color;
        ctx.fillRect(x, y, car.width, car.height);
        // Vidros
        ctx.fillStyle = "#000";
        ctx.fillRect(x + 5, y + 15, car.width - 10, 15);
        ctx.fillRect(x + 5, y + 45, car.width - 10, 10);
    }

    function spawnObstacle() {
        let xPos = Math.random() * (canvas.width - car.width);
        obstacles.push({ x: xPos, y: -70, width: 40, height: 70, speed: 3 + Math.random() * 3 });
    }

    function update() {
        if (gameOver) return;

        // Movimento do jogador
        car.x += car.dx;
        if (car.x < 0) car.x = 0;
        if (car.x + car.width > canvas.width) car.x = canvas.width - car.width;

        // Animação da pista (linhas centrais)
        for (let i = 0; i < lines.length; i++) {
            lines[i] += 5;
            if (lines[i] > canvas.height) lines[i] = -50;
        }

        // Movimento dos obstáculos
        for (let i = 0; i < obstacles.length; i++) {
            obstacles[i].y += obstacles[i].speed;
            
            // Colisão
            if (car.x < obstacles[i].x + obstacles[i].width &&
                car.x + car.width > obstacles[i].x &&
                car.y < obstacles[i].y + obstacles[i].height &&
                car.y + car.height > obstacles[i].y) {
                gameOver = true;
            }
        }

        // Remover obstáculos que passaram e aumentar pontuação
        if (obstacles.length > 0 && obstacles[0].y > canvas.height) {
            obstacles.shift();
            score += 10;
        }

        if (Math.random() < 0.02) spawnObstacle();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Desenhar linhas da pista
        ctx.fillStyle = "white";
        for (let i = 0; i < lines.length; i++) {
            ctx.fillRect(canvas.width / 2 - 5, lines[i], 10, 40);
        }

        drawCar(car.x, car.y, "red"); // Carro do jogador
        
        for (let i = 0; i < obstacles.length; i++) {
            drawCar(obstacles[i].x, obstacles[i].y, "blue"); // Outros carros
        }

        // Placar
        ctx.fillStyle = "white";
        ctx.font = "20px Arial";
        ctx.fillText("Score: " + score, 10, 30);

        if (gameOver) {
            ctx.fillStyle = "red";
            ctx.font = "40px Arial";
            ctx.fillText("GAME OVER", 80, canvas.height / 2);
        }
    }

    function loop() {
        update();
        draw();
        if (!gameOver) {
            requestAnimationFrame(loop);
        }
    }
    
    loop();
</script>
</body>
</html>
"""

# Renderiza o jogo dentro do Streamlit
components.html(codigo_do_jogo, height=550)

st.markdown("---")
st.caption("Jogo renderizado em HTML5 Canvas dentro do Streamlit Cloud.")