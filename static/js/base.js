document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.sidebar-menu .menu-item');
    menuItems.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('.search-container input, #caseSearchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });

    function updateLiveClock() {
        const clockElement = document.getElementById('liveClock');
        if (!clockElement) return;
        
        const now = new Date();
        const day = String(now.getDate()).padStart(2, '0');
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const month = months[now.getMonth()];
        const year = now.getFullYear();
        
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        
        hours = hours % 12;
        hours = hours ? String(hours).padStart(2, '0') : '12';
        
        clockElement.textContent = `${day} ${month} ${year} | ${hours}:${minutes}:${seconds} ${ampm}`;
    }

    setInterval(updateLiveClock, 1000);
    updateLiveClock();
});