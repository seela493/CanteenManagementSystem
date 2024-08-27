document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll('.item');
    const totalPriceElement = document.getElementById('total-price');

    function calculateTotal() {
        let total = 0;
        items.forEach(item => {
            const price = parseInt(item.querySelector('.item-price').textContent);
            const quantity = parseInt(item.querySelector('.item-quantity').value);
            total += price * quantity;
        });
        totalPriceElement.textContent = `Rs.${total}`;
    }

    items.forEach(item => {
        const decreaseBtn = item.querySelector('.decrease');
        const increaseBtn = item.querySelector('.increase');
        const quantityInput = item.querySelector('.item-quantity');

        decreaseBtn.addEventListener('click', function () {
            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantity--;
                quantityInput.value = quantity;
                calculateTotal();
            }
        });

        increaseBtn.addEventListener('click', function () {
            let quantity = parseInt(quantityInput.value);
            quantity++;
            quantityInput.value = quantity;
            calculateTotal();
        });
    });

    calculateTotal();
});
