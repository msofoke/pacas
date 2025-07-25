// Main JavaScript for Pacas Management App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation and calculations
    initializeFormValidation();
    initializeCalculations();
    
    // Initialize tooltips and other Bootstrap components
    initializeBootstrapComponents();
    
    // Initialize edit form if present
    initializeEditForm();
});

function initializeFormValidation() {
    const form = document.getElementById('bundleForm') || document.getElementById('editBundleForm');
    if (!form) return;
    
    // Real-time validation for classification totals
    const typeInputs = document.querySelectorAll('.classification-type');
    const qualityInputs = document.querySelectorAll('.classification-quality');
    const totalPiecesInput = document.getElementById('total_pieces');
    
    // Update totals when inputs change
    typeInputs.forEach(input => {
        input.addEventListener('input', updateClassificationTotals);
    });
    
    qualityInputs.forEach(input => {
        input.addEventListener('input', updateClassificationTotals);
    });
    
    totalPiecesInput.addEventListener('input', updateClassificationTotals);
    
    // Form submission validation
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
}

function updateClassificationTotals() {
    // Calculate type total
    const typeInputs = document.querySelectorAll('.classification-type');
    let typeTotal = 0;
    typeInputs.forEach(input => {
        typeTotal += parseInt(input.value) || 0;
    });
    
    // Calculate quality total
    const qualityInputs = document.querySelectorAll('.classification-quality');
    let qualityTotal = 0;
    qualityInputs.forEach(input => {
        qualityTotal += parseInt(input.value) || 0;
    });
    
    // Update display
    const typeDisplay = document.getElementById('type-total');
    const qualityDisplay = document.getElementById('quality-total');
    
    if (typeDisplay) {
        typeDisplay.textContent = typeTotal;
        typeDisplay.className = typeTotal === getTotalPieces() ? 'text-success' : 'text-danger';
    }
    
    if (qualityDisplay) {
        qualityDisplay.textContent = qualityTotal;
        qualityDisplay.className = qualityTotal === getTotalPieces() ? 'text-success' : 'text-danger';
    }
    
    // Update input validation classes
    updateInputValidation(typeInputs, typeTotal);
    updateInputValidation(qualityInputs, qualityTotal);
}

function updateInputValidation(inputs, total) {
    const totalPieces = getTotalPieces();
    const isValid = total === totalPieces && totalPieces > 0;
    
    inputs.forEach(input => {
        if (isValid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else if (total > 0) {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-valid', 'is-invalid');
        }
    });
}

function getTotalPieces() {
    const totalPiecesInput = document.getElementById('total_pieces');
    return parseInt(totalPiecesInput?.value) || 0;
}

function validateForm() {
    const totalPieces = getTotalPieces();
    
    if (totalPieces <= 0) {
        showAlert('El número total de piezas debe ser mayor a 0', 'danger');
        return false;
    }
    
    // Validate type classification
    const typeInputs = document.querySelectorAll('.classification-type');
    let typeTotal = 0;
    typeInputs.forEach(input => {
        typeTotal += parseInt(input.value) || 0;
    });
    
    if (typeTotal !== totalPieces) {
        showAlert(`La suma de piezas por tipo (${typeTotal}) debe ser igual al total de piezas (${totalPieces})`, 'danger');
        return false;
    }
    
    // Validate quality classification
    const qualityInputs = document.querySelectorAll('.classification-quality');
    let qualityTotal = 0;
    qualityInputs.forEach(input => {
        qualityTotal += parseInt(input.value) || 0;
    });
    
    if (qualityTotal !== totalPieces) {
        showAlert(`La suma de piezas por calidad (${qualityTotal}) debe ser igual al total de piezas (${totalPieces})`, 'danger');
        return false;
    }
    
    return true;
}

function initializeCalculations() {
    // Auto-calculate costs when basic inputs change
    const costInput = document.getElementById('total_cost');
    const piecesInput = document.getElementById('total_pieces');
    const expenseInputs = document.querySelectorAll('input[name="transport"], input[name="cleaning"], input[name="other"]');
    
    [costInput, piecesInput, ...expenseInputs].forEach(input => {
        if (input) {
            input.addEventListener('input', debounce(calculatePreview, 300));
        }
    });
}

function calculatePreview() {
    const totalCost = parseFloat(document.getElementById('total_cost')?.value) || 0;
    const totalPieces = parseInt(document.getElementById('total_pieces')?.value) || 0;
    const transport = parseFloat(document.getElementById('transport')?.value) || 0;
    const cleaning = parseFloat(document.getElementById('cleaning')?.value) || 0;
    const other = parseFloat(document.getElementById('other')?.value) || 0;
    
    if (totalCost > 0 && totalPieces > 0) {
        const totalExpenses = transport + cleaning + other;
        const totalCostWithExpenses = totalCost + totalExpenses;
        const costPerPiece = totalCostWithExpenses / totalPieces;
        
        // You could display this preview somewhere if needed
        console.log(`Cost per piece: ${formatCurrency(costPerPiece)}`);
    }
}

function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="bi bi-${type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    if (main && main.firstChild) {
        main.insertBefore(alertDiv, main.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format currency for display
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

// Format percentage for display
function formatPercentage(percentage) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
    }).format(percentage / 100);
}

// Format number with thousand separators
function formatNumber(number) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(number);
}

// Utility function to handle form loading states
function setFormLoading(form, loading = true) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const inputs = form.querySelectorAll('input, select, textarea');
    
    if (loading) {
        form.classList.add('loading');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Procesando...';
        }
        inputs.forEach(input => input.disabled = true);
    } else {
        form.classList.remove('loading');
        if (submitBtn) {
            submitBtn.disabled = false;
            const isEdit = form.id === 'editBundleForm';
            submitBtn.innerHTML = isEdit ? '<i class="bi bi-check-circle me-1"></i>Actualizar Paca' : '<i class="bi bi-check-circle me-1"></i>Crear Paca';
        }
        inputs.forEach(input => input.disabled = false);
    }
}

function initializeEditForm() {
    // Initialize totals for edit form
    updateClassificationTotals();
}

// Export functions for use in other scripts if needed
window.PacasApp = {
    formatCurrency,
    formatPercentage,
    formatNumber,
    showAlert,
    setFormLoading
};
