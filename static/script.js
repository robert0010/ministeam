// Remove as mensagens de erro/sucesso após 4 segundos para a tela não ficar poluída
document.addEventListener("DOMContentLoaded", function() {
    const flashes = document.querySelectorAll('.flash');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(flash => {
                flash.style.opacity = '0';
                setTimeout(() => flash.remove(), 500);
            });
        }, 4000);
    }
});

// Função para simular o clique em "Finalizar Compra" do seu UC01
function checkout() {
    alert("Iniciando fluxo de pagamento... (Isso chamaria a próxima etapa do seu Caso de Uso!)");
}