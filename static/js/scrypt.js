
// VALIDAÇÃO DE TELEFONE

const telefone = document.getElementById("telefone");

if (telefone) {

    telefone.addEventListener("input", function () {

        let numero = telefone.value.replace(/\D/g, "");

        numero = numero.substring(0, 11);

        if (numero.length > 10) {
            numero = numero.replace(
                /^(\d{2})(\d{5})(\d{4})$/,
                "($1) $2-$3"
            );
        } else if (numero.length > 6) {
            numero = numero.replace(
                /^(\d{2})(\d{4})(\d{0,4})$/,
                "($1) $2-$3"
            );
        } else if (numero.length > 2) {
            numero = numero.replace(
                /^(\d{2})(\d{0,5})$/,
                "($1) $2"
            );
        }

        telefone.value = numero;

    });

}


// VALIDAÇÃO DO FORMULÁRIO

const formulario = document.querySelector(".cadastro-card form");

if (formulario) {

    formulario.addEventListener("submit", function (event) {

        const email = document.getElementById("email").value.trim();

        const numero = telefone.value.replace(/\D/g, "");

        const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

        if (!emailValido) {
            event.preventDefault();
            alert("Digite um endereço de e-mail válido!");
            return;
        }

        if (numero.length !== 10 && numero.length !== 11) {
            event.preventDefault();
            alert("Digite um telefone válido com DDD!");
            return;
        }

    });

}
