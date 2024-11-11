document.querySelector('.search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    
    try {
        const response = await fetch(`/search_user?username=${encodeURIComponent(username)}`);
        const data = await response.json();
        
        if (data.found) {
            window.location.href = `/profile/${encodeURIComponent(username)}`;
        } else {
            alert('User not found');
        }
    } catch (error) {
        console.error('Error searching for user:', error);
        alert('Error searching for user');
    }
}); 