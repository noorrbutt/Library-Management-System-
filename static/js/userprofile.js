const profileState = {
    isEditing: false,
    hasChanges: false,
    originalData: {},
    currentData: {},
    photoPreview: null,
    hasExistingPhoto: false
};

$(document).ready(function() {
    // Set up jQuery AJAX to include CSRF token
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:/.test(settings.url) || /^https:/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            }
        }
    });
    
    initializeProfile();
    setupEventListeners();
    setupCollapsibleCards();
    displayAvatarInitials();
    checkForExistingPhoto();
});

function initializeProfile() {
    const fullNameValue = $.trim($('#fullName').val());
    const emailValue = $.trim($('#emailAddress').val());
    const phoneValue = $.trim($('#phoneNumber').val());
    const dobValue = $.trim($('#dateOfBirth').val());
    const addressValue = $.trim($('#address').val());

    profileState.originalData = {
        fullName: fullNameValue,
        email: emailValue,
        phone: phoneValue,
        dob: dobValue,
        address: addressValue
    };

    profileState.currentData = JSON.parse(JSON.stringify(profileState.originalData));
    
    setFieldsDisabled(true);
    updateButtonDisplay();
}

function setupEventListeners() {
    // Edit button click
    $('#editPersonalBtn').on('click', function(e) {
        e.preventDefault();
        if (profileState.isEditing) {
            savePersonalInfo();
        } else {
            enterEditMode();
        }
    });

    // Cancel button click
    $('#cancelPersonalBtn').on('click', function(e) {
        e.preventDefault();
        cancelEdit();
    });

    // Save button click
    $('#savePersonalBtn').on('click', function(e) {
        e.preventDefault();
        if (validatePersonalForm()) {
            savePersonalInfo();
        }
    });

    // Change password button
    $('#changePasswordBtn').on('click', function(e) {
        e.preventDefault();
        showPasswordChangeModal();
    });

    // Photo input change
    $('#photoInput').on('change', function(e) {
        handlePhotoUpload(e);
    });

    // Form field changes
    $('#fullName, #emailAddress, #phoneNumber, #dateOfBirth, #address').on('change input', function() {
        updateCurrentData();
        detectChanges();
        updateButtonState();
    });
}

function setupCollapsibleCards() {
    $('.collapsible-header').on('click', function() {
        const card = $(this).parent('.collapsible-card');
        card.toggleClass('active');
        
        // Optional: Close other cards
        // $('.collapsible-card').not(card).removeClass('active');
    });
}

function displayAvatarInitials() {
    const fullName = $.trim($('#fullName').val());
    const initials = getInitials(fullName);
    $('#avatarInitials').text(initials);
}

function getInitials(fullName) {
    if (!fullName) return 'U';
    
    const parts = fullName.trim().split(/\s+/);
    if (parts.length === 0) return 'U';
    if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
    
    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
}

function checkForExistingPhoto() {
    // Check if an image tag already exists in the avatar circle
    const $img = $('#avatarCircle').find('img.avatar-image');
    if ($img.length > 0 && $img.attr('src')) {
        profileState.hasExistingPhoto = true;
        $('#avatarCircle').addClass('has-photo');
    }
}

function enterEditMode() {
    profileState.isEditing = true;
    setFieldsDisabled(false);
    updateButtonDisplay();
    $('#fullName').focus();
}

function cancelEdit() {
    if (profileState.hasChanges) {
        if (!confirm('You have unsaved changes. Are you sure you want to discard them?')) {
            return;
        }
    }

    profileState.isEditing = false;
    profileState.hasChanges = false;
    
    $('#fullName').val(profileState.originalData.fullName);
    $('#emailAddress').val(profileState.originalData.email);
    $('#phoneNumber').val(profileState.originalData.phone);
    $('#dateOfBirth').val(profileState.originalData.dob);
    $('#address').val(profileState.originalData.address);

    profileState.currentData = JSON.parse(JSON.stringify(profileState.originalData));
    
    setFieldsDisabled(true);
    updateButtonDisplay();
}

function setFieldsDisabled(disabled) {
    const fields = ['#fullName', '#emailAddress', '#phoneNumber', '#dateOfBirth', '#address'];
    fields.forEach(selector => {
        $(selector).prop('readonly', disabled);
    });
}

function updateCurrentData() {
    profileState.currentData = {
        fullName: $.trim($('#fullName').val()),
        email: $.trim($('#emailAddress').val()),
        phone: $.trim($('#phoneNumber').val()),
        dob: $.trim($('#dateOfBirth').val()),
        address: $.trim($('#address').val())
    };
}

function detectChanges() {
    profileState.hasChanges = !isDataEqual(profileState.currentData, profileState.originalData);
}

function isDataEqual(data1, data2) {
    return JSON.stringify(data1) === JSON.stringify(data2);
}

function updateButtonDisplay() {
    const $editBtn = $('#editPersonalBtn');
    const $formActions = $('#personalActions');

    if (profileState.isEditing) {
        $editBtn.hide();
        $formActions.show();
    } else {
        $editBtn.show();
        $formActions.hide();
    }
}

function updateButtonState() {
    const $saveBtn = $('#savePersonalBtn');
    
    if (profileState.isEditing && profileState.hasChanges) {
        $saveBtn.prop('disabled', false).css('opacity', '1').css('cursor', 'pointer');
    } else if (profileState.isEditing && !profileState.hasChanges) {
        $saveBtn.prop('disabled', true).css('opacity', '0.5').css('cursor', 'not-allowed');
    }
}

function validatePersonalForm() {
    const fullName = $.trim($('#fullName').val());
    const email = $.trim($('#emailAddress').val());
    const phone = $.trim($('#phoneNumber').val());
    const dob = $.trim($('#dateOfBirth').val());

    if (!fullName) {
        showError('Full name is required.');
        return false;
    }

    if (fullName.length < 3) {
        showError('Full name must be at least 3 characters long.');
        return false;
    }

    if (!email) {
        showError('Email address is required.');
        return false;
    }

    if (!isValidEmail(email)) {
        showError('Please enter a valid email address.');
        return false;
    }

    if (phone && !isValidPhone(phone)) {
        showError('Please enter a valid phone number (10-15 digits).');
        return false;
    }

    if (dob) {
        if (!isValidDate(dob)) {
            showError('Invalid date of birth.');
            return false;
        }

        const dobDate = new Date(dob);
        const today = new Date();
        if (dobDate > today) {
            showError('Date of birth cannot be in the future.');
            return false;
        }

        const age = today.getFullYear() - dobDate.getFullYear();
        if (age < 13) {
            showError('You must be at least 13 years old.');
            return false;
        }
    }

    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^\d{10,15}$/;
    return phoneRegex.test(phone.replace(/\D/g, ''));
}

function isValidDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

function handlePhotoUpload(e) {
    const file = e.target.files[0];

    if (!file) {
        return;
    }

    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file.');
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        showError('Image size must be less than 5MB.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        profileState.photoPreview = event.target.result;
        
        // Update avatar to show the preview
        const $avatarCircle = $('#avatarCircle');
        let $img = $avatarCircle.find('img.avatar-image');
        
        if ($img.length > 0) {
            // Update existing image
            $img.attr('src', profileState.photoPreview);
        } else {
            // Create new image
            $avatarCircle.prepend(`<img src="${profileState.photoPreview}" alt="Profile Picture" class="avatar-image">`);
        }
        
        $avatarCircle.addClass('has-photo');
        uploadProfilePhoto(file);
    };
    reader.readAsDataURL(file);
}

function uploadProfilePhoto(file) {
    showLoading();

    const formData = new FormData();
    formData.append('photo', file);

    $.ajax({
        url: '/upload-profile-photo/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        timeout: 30000,
        success: function(response) {
            hideLoading();
            profileState.hasExistingPhoto = true;
            showSuccess('Profile photo updated successfully!');
            // Reset file input
            $('#photoInput').val('');
        },
        error: function(xhr, status, error) {
            hideLoading();
            let errorMsg = 'Failed to upload photo. Please try again.';
            
            if (xhr.status === 404) {
                errorMsg = 'Upload endpoint not found. Please contact support.';
            } else if (xhr.status === 403) {
                errorMsg = 'Permission denied. Please log in again.';
            } else if (xhr.status === 400) {
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMsg = xhr.responseJSON.message;
                } else {
                    errorMsg = 'Invalid file format or size. Please try again.';
                }
            } else if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMsg = xhr.responseJSON.message;
            }
            
            showError(errorMsg);
            
            // Revert avatar on error
            const $avatarCircle = $('#avatarCircle');
            if (!profileState.hasExistingPhoto) {
                $avatarCircle.find('img.avatar-image').remove();
                $avatarCircle.removeClass('has-photo');
            }
            profileState.photoPreview = null;
            $('#photoInput').val('');
            $avatarCircle.find('img').remove();
            $avatarCircle.removeClass('has-photo');
            profileState.photoPreview = null;
            $('#photoInput').val('');
        }
    });
}

function savePersonalInfo() {
    if (!validatePersonalForm()) {
        return;
    }

    showLoading();

    const fullNameParts = $.trim($('#fullName').val()).split(' ');
    const firstName = fullNameParts[0] || '';
    const lastName = fullNameParts.slice(1).join(' ') || '';

    const data = {
        first_name: firstName,
        last_name: lastName,
        email: $.trim($('#emailAddress').val()),
        phone: $.trim($('#phoneNumber').val()),
        date_of_birth: $.trim($('#dateOfBirth').val()),
        address: $.trim($('#address').val())
    };

    $.ajax({
        url: '/update-profile/',
        type: 'POST',
        data: data,
        timeout: 30000,
        success: function(response) {
            hideLoading();

            profileState.originalData = {
                fullName: $('#fullName').val(),
                email: data.email,
                phone: data.phone,
                dob: data.date_of_birth,
                address: data.address
            };

            profileState.currentData = JSON.parse(JSON.stringify(profileState.originalData));
            profileState.isEditing = false;
            profileState.hasChanges = false;

            setFieldsDisabled(true);
            updateButtonDisplay();
            updateButtonState();
            displayAvatarInitials();

            showSuccess('Profile information updated successfully!');
        },
        error: function(xhr, status, error) {
            hideLoading();
            let errorMsg = 'Failed to update profile. Please try again.';
            
            if (xhr.status === 404) {
                errorMsg = 'Update endpoint not found. Please contact support.';
            } else if (xhr.status === 403) {
                errorMsg = 'Permission denied. Please log in again.';
            } else if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMsg = xhr.responseJSON.message;
            }
            
            showError(errorMsg);
        }
    });
}

function showPasswordChangeModal() {
    alert('Password change feature coming soon!');
}

function showSuccess(message) {
    const $alert = $('#successAlert');
    $('#successMessage').text(message);
    
    $alert.stop(true, true).show().addClass('show');
    
    setTimeout(function() {
        $alert.fadeOut(function() {
            $alert.removeClass('show');
        });
    }, 5000);
}

function showError(message) {
    const $alert = $('#errorAlert');
    $('#errorMessage').text(message);
    
    $alert.stop(true, true).show().addClass('show');
    
    setTimeout(function() {
        $alert.fadeOut(function() {
            $alert.removeClass('show');
        });
    }, 5000);

    $('html, body').animate({ scrollTop: 0 }, 'smooth');
}

function showLoading() {
    $('#loadingSpinner').show();
}

function hideLoading() {
    $('#loadingSpinner').fadeOut();
}

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
    return cookieValue || '';
}

$(document).on('keydown', function(e) {
    if (e.key === 'Escape' && profileState.isEditing) {
        cancelEdit();
    }
});

$(window).on('beforeunload', function() {
    if (profileState.isEditing && profileState.hasChanges) {
        return 'You have unsaved changes. Are you sure you want to leave?';
    }
});
