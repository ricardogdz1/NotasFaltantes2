// analisador/static/analisador/js/resultado.js
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Funcionalidade de cópia
    const botaoCopiar = document.getElementById('copiarFaltantes');
    const listaFaltantes = document.getElementById('listaFaltantes');
    const toast = new bootstrap.Toast(document.getElementById('toastCopia'));
    
    if (botaoCopiar) {
        botaoCopiar.addEventListener('click', async function() {
            try {
                const texto = this.getAttribute('data-lista') || listaFaltantes.textContent.trim();
                
                if (navigator.clipboard && window.isSecureContext) {
                    // API moderna de clipboard
                    await navigator.clipboard.writeText(texto);
                    mostrarSucesso();
                } else {
                    // Fallback para navegadores mais antigos
                    const textArea = document.createElement('textarea');
                    textArea.value = texto;
                    textArea.style.position = 'fixed';
                    textArea.style.opacity = '0';
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    
                    try {
                        document.execCommand('copy');
                        mostrarSucesso();
                    } catch (err) {
                        console.error('Erro ao copiar:', err);
                        alert('Erro ao copiar. Tente selecionar e copiar manualmente.');
                    }
                    
                    document.body.removeChild(textArea);
                }
            } catch (err) {
                console.error('Erro ao copiar:', err);
                alert('Erro ao copiar. Tente selecionar e copiar manualmente.');
            }
        });
        
        function mostrarSucesso() {
            // Mudar ícone do botão temporariamente
            const icone = botaoCopiar.querySelector('i');
            const textoOriginal = botaoCopiar.innerHTML;
            
            botaoCopiar.innerHTML = '<i class="bi bi-check"></i> Copiado!';
            botaoCopiar.classList.remove('btn-light');
            botaoCopiar.classList.add('btn-success');
            
            // Mostrar toast
            toast.show();
            
            // Restaurar botão após 2 segundos
            setTimeout(() => {
                botaoCopiar.innerHTML = textoOriginal;
                botaoCopiar.classList.remove('btn-success');
                botaoCopiar.classList.add('btn-light');
            }, 2000);
        }
    }
});