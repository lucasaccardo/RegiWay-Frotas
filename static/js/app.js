// Funcao: scripts globais de comportamento da interface.
// Responsável: Kenny.
document.addEventListener("DOMContentLoaded", () => {
    console.log("RegiWay Frotas Front-End Inicializado com Sucesso!");

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => {
                alert.style.display = 'none';
            }, 400);
        }, 5000);
    });
    // Isso garante que os inputs do Kenzo/Lucas peguem seu CSS do app.css
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        if (input.type !== 'submit' && input.type !== 'checkbox') {
            input.classList.add('form-control');
        }
    });
});
