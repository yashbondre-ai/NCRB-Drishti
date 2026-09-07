document.addEventListener('DOMContentLoaded', () => {
    const triageChips = document.querySelectorAll('.triage-chip');
    const incidentCards = document.querySelectorAll('.incident-card');
    const alertSearchInput = document.getElementById('alertSearchInput');

    function filterIncidents() {
        const query = alertSearchInput ? alertSearchInput.value.toLowerCase().trim() : '';
        const activeChip = document.querySelector('.triage-chip.active');
        const selectedType = activeChip ? activeChip.getAttribute('data-filter') : 'all';

        incidentCards.forEach(card => {
            const cardType = card.getAttribute('data-type');
            const cardContent = card.textContent.toLowerCase();

            const matchesType = (selectedType === 'all' || cardType === selectedType);
            const matchesQuery = (!query || cardContent.includes(query));

            if (matchesType && matchesQuery) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    triageChips.forEach(chip => {
        chip.addEventListener('click', () => {
            triageChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            filterIncidents();
        });
    });

    if (alertSearchInput) {
        alertSearchInput.addEventListener('input', filterIncidents);
    }

    const incidentModal = document.getElementById('incidentModal');
    const modalIncidentHeading = document.getElementById('modalIncidentHeading');
    const modalIncidentCode = document.getElementById('modalIncidentCode');
    const modalFieldDocket = document.getElementById('modalFieldDocket');
    const modalFieldTime = document.getElementById('modalFieldTime');
    const modalFieldFile = document.getElementById('modalFieldFile');
    const modalFieldStation = document.getElementById('modalFieldStation');
    const modalFieldDetails = document.getElementById('modalFieldDetails');

    document.querySelectorAll('.btn-inspect-docket').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.incident-card');
            if (!card) return;

            const code = card.getAttribute('data-code');
            const docket = card.getAttribute('data-docket');
            const file = card.getAttribute('data-file');
            const station = card.getAttribute('data-station');
            const time = card.getAttribute('data-time');
            const details = card.getAttribute('data-details');
            const title = card.querySelector('h4') ? card.querySelector('h4').textContent : 'Incident Report';

            if (modalIncidentHeading) modalIncidentHeading.textContent = title;
            if (modalIncidentCode) modalIncidentCode.textContent = `Incident ID: ${code}`;
            if (modalFieldDocket) modalFieldDocket.textContent = docket;
            if (modalFieldTime) modalFieldTime.textContent = time;
            if (modalFieldFile) modalFieldFile.textContent = file;
            if (modalFieldStation) modalFieldStation.textContent = station;
            if (modalFieldDetails) modalFieldDetails.textContent = details;

            if (incidentModal) incidentModal.classList.add('active');
        });
    });

    document.querySelectorAll('.btn-ack-sign').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.incident-card');
            btn.innerHTML = '<i class="ph-fill ph-check-circle"></i> Acknowledged';
            btn.style.borderColor = 'var(--success, #22C55E)';
            btn.style.color = '#4ADE80';
            btn.disabled = true;

            if (card) {
                const badge = card.querySelector('.status-indicator span');
                if (badge) {
                    badge.className = 'badge-resolved font-mono';
                    badge.innerHTML = '<i class="ph-fill ph-shield-check"></i> Officer Acknowledged';
                }
            }
        });
    });

    const btnConfirmQuarantine = document.getElementById('btnConfirmQuarantine');
    if (btnConfirmQuarantine) {
        btnConfirmQuarantine.addEventListener('click', () => {
            btnConfirmQuarantine.innerHTML = '<i class="ph-fill ph-lock-key"></i> State Locked';
            btnConfirmQuarantine.style.background = '#22C55E';
            btnConfirmQuarantine.style.color = '#FFFFFF';

            setTimeout(() => {
                if (incidentModal) incidentModal.classList.remove('active');
                btnConfirmQuarantine.innerHTML = '<i class="ph-fill ph-lock-key"></i> Lock Quarantine State';
                btnConfirmQuarantine.style.background = 'rgba(220, 38, 38, 0.18)';
                btnConfirmQuarantine.style.color = '#EF4444';
            }, 800);
        });
    }

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });
});