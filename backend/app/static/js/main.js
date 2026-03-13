// Custom JavaScript for Intern CRUD application

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 
                          'Are you sure you want to delete this? This action cannot be undone.';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // File upload validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = this.files[0];
            if (file) {
                // Check file size (2MB = 2097152 bytes)
                const maxSize = 2097152;
                if (file.size > maxSize) {
                    alert('File size must not exceed 2MB');
                    this.value = '';
                    return;
                }
                
                // Check file type (PDF only)
                const allowedTypes = ['application/pdf'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Only PDF files are allowed');
                    this.value = '';
                    return;
                }
                
                // Display file name
                const fileName = file.name;
                const fileInfo = this.parentElement.querySelector('.file-upload-info');
                if (fileInfo) {
                    fileInfo.textContent = `Selected: ${fileName}`;
                }
            }
        });
    });
    
    // Form submission loading state
    const forms = document.querySelectorAll('form[data-loading]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.classList.contains('loading')) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;
            }
        });
    });
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

