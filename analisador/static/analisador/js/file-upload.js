// analisador/static/analisador/js/file-upload.js
(function() {
    'use strict';
    
    // Versão simplificada e mais robusta
    function initFileUpload() {
        const fileInput = document.getElementById('arquivo');
        const fileUploadArea = document.getElementById('fileUploadArea');
        const fileInfo = document.getElementById('fileInfo');
        const submitBtn = document.getElementById('submitBtn');
        const uploadForm = document.getElementById('uploadForm');
        
        // Garantir que os elementos existem
        if (!fileInput || !fileUploadArea || !fileInfo || !submitBtn || !uploadForm) {
            console.error('Elementos não encontrados');
            return;
        }
        
        let formSubmitted = false;
        
        // Evento de mudança no input de arquivo
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                handleFileSelect(this.files[0]);
            }
        });
        
        // Click na área de upload
        fileUploadArea.addEventListener('click', function(e) {
            // Se clicou no botão, não fazer nada (o onclick do botão já cuida)
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                return;
            }
            fileInput.click();
        });
        
        // Drag and drop
        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = '#28a745';
            this.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
        });
        
        fileUploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = '#007bff';
            this.style.backgroundColor = 'rgba(0, 123, 255, 0.05)';
        });
        
        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = '#007bff';
            this.style.backgroundColor = 'rgba(0, 123, 255, 0.05)';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                if (file.name.toLowerCase().endsWith('.txt')) {
                    // Criar um novo FileList
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    fileInput.files = dt.files;
                    
                    handleFileSelect(file);
                } else {
                    alert('Por favor, selecione apenas arquivos .txt');
                }
            }
        });
        
        function handleFileSelect(file) {
            const fileName = document.getElementById('fileName');
            const fileSize = document.getElementById('fileSize');
            
            if (fileName) fileName.textContent = file.name;
            if (fileSize) fileSize.textContent = `Tamanho: ${(file.size / 1024).toFixed(2)} KB`;
            
            // Mostrar informações do arquivo
            fileInfo.style.display = 'block';
            
            // Validar tamanho (5MB máximo)
            if (file.size > 5 * 1024 * 1024) {
                fileInfo.className = 'alert alert-danger';
                fileInfo.innerHTML = '<i class="bi bi-exclamation-triangle"></i> <strong>Erro:</strong> Arquivo muito grande (máximo 5MB)';
                submitBtn.disabled = true;
            } else {
                fileInfo.className = 'alert alert-info';
                fileInfo.innerHTML = `
                    <i class="bi bi-file-earmark-text"></i>
                    <strong>Arquivo selecionado:</strong> ${file.name}
                    <br><small class="text-muted">Tamanho: ${(file.size / 1024).toFixed(2)} KB</small>
                `;
                submitBtn.disabled = false;
            }
        }
        
        // Controle de submit
        uploadForm.addEventListener('submit', function(e) {
            if (formSubmitted) {
                e.preventDefault();
                return false;
            }
            
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Por favor, selecione um arquivo antes de continuar.');
                return false;
            }
            
            formSubmitted = true;
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Processando...';
            submitBtn.disabled = true;
            
            return true;
        });
    }
    
    // Inicializar quando a página carregar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFileUpload);
    } else {
        initFileUpload();
    }
    
    // Função global para o botão (fallback)
    window.selecionarArquivo = function() {
        const fileInput = document.getElementById('arquivo');
        if (fileInput) {
            fileInput.click();
        } else {
            console.error('Input de arquivo não encontrado');
        }
    };

})();