function showImage(imgElement) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("largeImage");

    // Set the source of the modal image
    modalImg.src = imgElement.src;

    // Display the modal
    modal.style.display = "flex";
}

function closeImage() {
    document.getElementById("imageModal").style.display = "none";
}

// Get CSRF token for AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Add to cart functionality
function addToCart(productId, buttonElement) {
    fetch('/add-to-cart-ajax/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: `id=${productId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update cart count in navigation
            updateCartCount(data.cartCount);
            
            // Show success message
            showNotification('Item added to cart!', 'success');
            
            // Temporarily change button text
            const originalText = buttonElement.textContent;
            buttonElement.textContent = 'Added!';
            buttonElement.style.backgroundColor = '#28a745';
            
            setTimeout(() => {
                buttonElement.textContent = originalText;
                buttonElement.style.backgroundColor = '';
            }, 1500);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding item to cart', 'error');
    });
}

// Update quantity in cart
function updateQuantity(itemId, action, elementType = 'cart') {
    const url = elementType === 'cart' ? '/update-quantity-ajax/' : '/update-buy-quantity-ajax/';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: `id=${itemId}&action=${action}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.deleted) {
            // Remove the item from DOM
            document.getElementById(`${elementType}-item-${itemId}`).remove();
            showNotification('Item removed from cart', 'info');
        } else {
            // Update quantity and price displays
            document.getElementById(`${elementType}-qty-${itemId}`).textContent = data.qty;
            document.getElementById(`${elementType}-subtotal-${itemId}`).textContent = data.subtotal;
        }
        
        // Update total prices and cart count
        if (elementType === 'cart') {
            document.getElementById('cart-total').textContent = data.totalCart;
            updateCartCount(data.cartCount);
        } else {
            document.getElementById('order-total').textContent = data.totalOrder;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating quantity', 'error');
    });
}

// Remove item from cart
function removeFromCart(itemId, elementType = 'cart') {
    const url = elementType === 'cart' ? '/remove-from-cart-ajax/' : '/remove-from-buy-ajax/';
    
    if (confirm('Are you sure you want to remove this item?')) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: `id=${itemId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById(`${elementType}-item-${itemId}`).remove();
                
                if (elementType === 'cart') {
                    document.getElementById('cart-total').textContent = data.totalCart;
                    updateCartCount(data.cartCount);
                } else {
                    document.getElementById('order-total').textContent = data.totalOrder;
                }
                
                showNotification('Item removed successfully', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error removing item', 'error');
        });
    }
}

// Move item to buy list - FIXED VERSION
function buyItem(itemId) {
    fetch('/buy-item-ajax/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: `id=${itemId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Remove from cart section
            const cartItem = document.getElementById(`cart-item-${itemId}`);
            if (cartItem) {
                cartItem.remove();
            }
            
            // Create new buy item HTML using the correct item ID from response
            createBuyItemHTML(data.buyItem, data.buyItem.id);
            
            // Update totals
            document.getElementById('cart-total').textContent = data.totalCart;
            document.getElementById('order-total').textContent = data.totalOrder;
            updateCartCount(data.cartCount);
            
            showNotification('Item moved to order list', 'success');
        } else {
            showNotification(data.message || 'Error moving item to order', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error moving item to order', 'error');
    });
}
// Create buy item HTML dynamically - FIXED VERSION
function createBuyItemHTML(item, itemId) {
    const buyContainer = document.getElementById('buy-items-container');
    
    // Check if item already exists to avoid duplicates
    const existingItem = document.getElementById(`buy-item-${itemId}`);
    if (existingItem) {
        // Update existing item quantity and total
        const qtyElement = document.getElementById(`buy-qty-${itemId}`);
        const subtotalElement = document.getElementById(`buy-subtotal-${itemId}`);
        if (qtyElement) qtyElement.textContent = item.quantity;
        if (subtotalElement) subtotalElement.textContent = item.totalprice;
        return;
    }
    
    const buyItemHTML = `
        <div class="aa1" id="buy-item-${itemId}">
            <h2>${item.name}</h2>
            <h3>${item.desc}<sup>₹</sup>${item.price}
                <span>
                    <a href="#" onclick="updateQuantity('${itemId}', 'decrease', 'buy'); return false;">-</a>
                    <span id="buy-qty-${itemId}">${item.quantity}</span>
                    <a href="#" onclick="updateQuantity('${itemId}', 'increase', 'buy'); return false;">+</a>
                </span>
            </h3>
            <img src="${item.img}" alt="${item.name}" width="100px" height="50" onclick="showImage(this)">
            <h3><a href="#" onclick="removeFromCart('${itemId}', 'buy'); return false;">Delete</a></h3>
            <h3>total=<span id="buy-subtotal-${itemId}">${item.totalprice}</span></h3>
        </div><br>
    `;
    
    buyContainer.innerHTML += buyItemHTML;
}


// Update cart count in navigation - IMPROVED VERSION
function updateCartCount(count) {
    // Update all cart count elements (in case there are multiple)
    const cartCountElements = document.querySelectorAll('.cart-count, [id*="cart-count"]');
    cartCountElements.forEach(element => {
        element.textContent = count;
    });
    
    // Also update any cart links that show count in parentheses
    const cartLinks = document.querySelectorAll('a[href*="cart"]');
    cartLinks.forEach(link => {
        // Update text like "Cart(5)" or "Cart (5)"
        if (link.textContent.includes('Cart')) {
            link.textContent = link.textContent.replace(/Cart\s*\(\d+\)/, `Cart(${count})`);
        }
    });
    
    // Update navigation if it has cart count display
    const navCartElements = document.querySelectorAll('nav .cart-info, .nav-cart-count');
    navCartElements.forEach(element => {
        element.textContent = count > 0 ? `(${count})` : '';
    });
}


// Show notification messages
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        case 'info':
            notification.style.backgroundColor = '#17a2b8';
            break;
        default:
            notification.style.backgroundColor = '#6c757d';
    }
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add clear buy list function
function clearBuyList() {
    if (confirm('Are you sure you want to delete all order items?')) {
        fetch('/clear-buy-list-ajax/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('buy-items-container').innerHTML = '';
                document.getElementById('order-total').textContent = '0';
                showNotification('All order items deleted', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error deleting items', 'error');
        });
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
