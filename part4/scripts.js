document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    setupPriceFiltering();
    setupLoginForm();
  });
  
  function checkAuthentication() {
    const token = getCookie('token');
    const loginButton = document.getElementById('login-link');
    const reviewForm = document.getElementById('review-form');
    
    if (loginButton) {
      loginButton.style.display = token ? 'none' : 'block';
    }
    
    if (reviewForm) {
      reviewForm.style.display = token ? 'block' : 'none';
    }
    
    const currentUrl = window.location.pathname;
    
    if (currentUrl.includes('index.html') || currentUrl.endsWith('/')) {
      if (document.getElementById('accommodations-container')) {
        loadAccommodations(token);
      }
    } else if (currentUrl.includes('accommodation.html')) {
      const accommodationId = new URLSearchParams(window.location.search).get('id');
      if (accommodationId) {
        loadAccommodationDetails(token, accommodationId);
        loadAccommodationReviews(accommodationId);
      }
    }
  }
  
  function setupPriceFiltering() {
    const priceSelector = document.getElementById('price-filter');
    if (!priceSelector) return;
    
    priceSelector.addEventListener('change', function() {
      const selectedPrice = this.value;
      
      const accommodationCards = document.querySelectorAll('.accommodation-item');
      
      accommodationCards.forEach(card => {
        const accommodationPrice = parseInt(card.getAttribute('data-price'));
        
        if (selectedPrice === 'all' || accommodationPrice <= parseInt(selectedPrice)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
  
  function setupLoginForm() {
    const authForm = document.getElementById('login-form');
    if (!authForm) return;
    
    authForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const formData = new FormData(authForm);
      const credentials = {
        email: formData.get('email'),
        password: formData.get('password')
      };
      
      try {
        const authResponse = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials),
          credentials: 'include'
        });
        
        if (!authResponse.ok) {
          throw new Error(`Authentication failed: ${authResponse.status}`);
        }
        
        const authData = await authResponse.json();
        
        if (authData.access_token) {
          storeToken(authData.access_token);
          window.location.href = 'index.html';
        } else {
          showError('Login failed. Check your credentials.');
        }
      } catch (error) {
        showError(`Login error: ${error.message}`);
      }
    });
  }
  
  async function loadAccommodations(token) {
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      
      const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
        method: 'GET',
        headers: headers,
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error(`Failed to load accommodations: ${response.status}`);
      }
      
      const accommodations = await response.json();
      displayAccommodations(accommodations);
    } catch (error) {
      console.error('Error loading accommodations:', error);
      showError('Unable to load accommodations. Try again later.');
    }
  }
  
  function displayAccommodations(accommodations) {
    const container = document.getElementById('accommodations-container') || document.getElementById('places-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    accommodations.forEach(item => {
      const card = document.createElement('div');
      card.className = 'accommodation-item';
      card.setAttribute('data-price', item.price);
      
      card.innerHTML = `
        <div class="accommodation-card">
          <h3 class="title">${item.title}</h3>
          <div class="info-section">
            <p class="description">${trimText(item.description, 100)}</p>
            <p class="location"><i class="location-icon"></i> ${item.location}</p>
            <p class="price-tag"><strong>€${item.price}</strong> per night</p>
            ${item.rooms ? `<p class="rooms-info">${item.rooms} rooms</p>` : ''}
            ${item.bathrooms ? `<p class="bathroom-info">${item.bathrooms} bathrooms</p>` : ''}
          </div>
          <a href="accommodation.html?id=${item.id}" class="view-button">See details</a>
        </div>
      `;
      
      container.appendChild(card);
    });
  }
  
  function trimText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
  }
  
  async function loadAccommodationDetails(token, accommodationId) {
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      
      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${accommodationId}`, {
        method: 'GET',
        headers: headers,
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error(`Failed to load details: ${response.status}`);
      }
      
      const accommodationData = await response.json();
      displayAccommodationDetails(accommodationData);
    } catch (error) {
      console.error('Error loading accommodation details:', error);
      showError('Unable to load accommodation details. Try again later.');
    }
  }
  
  function displayAccommodationDetails(accommodation) {
    const detailsContainer = document.getElementById('accommodation-details') || document.getElementById('place-details');
    if (!detailsContainer) return;
    
    detailsContainer.innerHTML = `
      <h1 class="accommodation-title">${accommodation.title}</h1>
      <div class="host-info">Hosted by ${accommodation.owner.first_name} ${accommodation.owner.last_name}</div>
      <div class="pricing">€${accommodation.price} per night</div>
      <div class="full-description">${accommodation.description}</div>
      <div class="features">
        <h3>Amenities</h3>
        <ul class="amenities-list">
          ${accommodation.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
        </ul>
      </div>
    `;
    
    const locationContainer = document.getElementById('location-info') || document.getElementById('place-info');
    if (locationContainer) {
      locationContainer.innerHTML = `
        <h2>Location</h2>
        <p class="coordinates">Coordinates: ${accommodation.latitude}, ${accommodation.longitude}</p>
      `;
    }
  }
  
  async function loadAccommodationReviews(accommodationId) {
    try {
      const token = getCookie('token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      
      const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${accommodationId}/reviews`, {
        method: 'GET',
        headers: headers,
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error(`Failed to load reviews: ${response.status}`);
      }
      
      const reviewsData = await response.json();
      displayReviews(reviewsData);
      
      setupReviewSubmission(token, accommodationId);
    } catch (error) {
      console.error('Error loading reviews:', error);
    }
  }
  
  function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews');
    if (!reviewsContainer) return;
    
    reviewsContainer.innerHTML = '<h2>Guest Reviews</h2>';
    
    if (reviews.length === 0) {
      reviewsContainer.innerHTML += '<p class="no-reviews">No reviews for this accommodation yet.</p>';
      return;
    }
    
    const reviewsList = document.createElement('div');
    reviewsList.className = 'reviews-list';
    
    reviews.forEach(review => {
      const reviewElement = document.createElement('div');
      reviewElement.className = 'review-item';
      
      const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
      
      reviewElement.innerHTML = `
        <div class="review-header">
          <div class="reviewer-name">${review.user.first_name} ${review.user.last_name}</div>
          <div class="review-rating">${stars}</div>
        </div>
        <div class="review-body">${review.text}</div>
      `;
      
      reviewsList.appendChild(reviewElement);
    });
    
    reviewsContainer.appendChild(reviewsList);
  }
  
  function setupReviewSubmission(token, accommodationId) {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;
    
    reviewForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      if (!token) {
        showError('You must be logged in to submit a review.');
        return;
      }
      
      const formData = new FormData(reviewForm);
      const reviewText = formData.get('review') || formData.get('review-text');
      const rating = formData.get('rating');
      
      try {
        const result = await submitReviewToServer(token, accommodationId, reviewText, rating);
        
        if (result.success) {
          showSuccess('Your review has been submitted successfully!');
          loadAccommodationReviews(accommodationId);
          reviewForm.reset();
        } else {
          showError(result.message || 'Failed to submit review. Please try again.');
        }
      } catch (error) {
        showError(`Error submitting review: ${error.message}`);
      }
    });
  }
  
  async function submitReviewToServer(token, accommodationId, reviewText, rating) {
    try {
      if (!token || !accommodationId || !reviewText || !rating) {
        return { success: false, message: 'Missing required information for review submission.' };
      }
      
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      };
      
      const tokenData = parseJWT(token);
      const userId = tokenData.sub.id;
      
      if (!userId) {
        return { success: false, message: 'Unable to identify user. Please log in again.' };
      }
      
      const reviewData = {
        text: reviewText,
        rating: parseInt(rating),
        user_id: userId,
        place_id: accommodationId
      };
      
      const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(reviewData),
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      return { success: true };
    } catch (error) {
      console.error('Error in review submission:', error);
      return { success: false, message: error.message };
    }
  }
  
  function parseJWT(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(atob(base64));
    } catch (error) {
      console.error('Error parsing JWT token:', error);
      return {};
    }
  }
  
  function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [cookieName, cookieValue] = cookie.trim().split('=');
      if (cookieName === name) {
        return cookieValue;
      }
    }
    return null;
  }
  
  function storeToken(token) {
    document.cookie = `token=${token}; path=/`;
  }
  
  function showError(message) {
    console.error(message);
    alert(message);
  }
  
  function showSuccess(message) {
    console.log(message);
    alert(message);
  }