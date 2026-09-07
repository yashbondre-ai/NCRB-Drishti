document.addEventListener('DOMContentLoaded', () => {
    const firSearchInput = document.getElementById('firSearchInput');
    const firChips = document.querySelectorAll('.fir-chip');
    const tableRows = document.querySelectorAll('#firsMasterTable tbody tr');
    const firRecordCounter = document.getElementById('firRecordCounter');

    function updateCounter(visible) {
        if (firRecordCounter) {
            firRecordCounter.textContent = `Showing ${visible} of ${tableRows.length} Records`;
        }
    }

    function filterFirsTable() {
        const query = firSearchInput ? firSearchInput.value.toLowerCase().trim() : '';
        const activeChip = document.querySelector('.fir-chip.active');
        const filterType = activeChip ? activeChip.getAttribute('data-filter') : 'all';

        let count = 0;
        tableRows.forEach(row => {
            const rowType = row.getAttribute('data-type');
            const rowStatus = row.getAttribute('data-status');
            const rowText = row.textContent.toLowerCase();

            let matchesChip = false;
            if (filterType === 'all') {
                matchesChip = true;
            } else if (filterType === 'pending') {
                matchesChip = (rowStatus === 'pending');
            } else {
                matchesChip = (rowType === filterType);
            }

            const matchesSearch = (!query || rowText.includes(query));

            if (matchesChip && matchesSearch) {
                row.style.display = '';
                count++;
            } else {
                row.style.display = 'none';
            }
        });

        updateCounter(count);
    }

    if (firSearchInput) {
        firSearchInput.addEventListener('input', filterFirsTable);
    }

    firChips.forEach(chip => {
        chip.addEventListener('click', () => {
            firChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            filterFirsTable();
        });
    });

    const gazetteModal = document.getElementById('firGazetteModal');
    const gazetteHeaderTitle = document.getElementById('gazetteHeaderTitle');
    const gazettePs = document.getElementById('gazettePs');
    const gazetteFirNumber = document.getElementById('gazetteFirNumber');
    const gazetteSections = document.getElementById('gazetteSections');
    const gazetteIo = document.getElementById('gazetteIo');
    const gazetteOccurTime = document.getElementById('gazetteOccurTime');
    const gazetteReportedTime = document.getElementById('gazetteReportedTime');
    const gazetteComplainant = document.getElementById('gazetteComplainant');
    const gazetteAccused = document.getElementById('gazetteAccused');
    const gazetteGistText = document.getElementById('gazetteGistText');
    const gazetteHash = document.getElementById('gazetteHash');
    const gazetteShoName = document.getElementById('gazetteShoName');
    const gazetteShoId = document.getElementById('gazetteShoId');

    document.querySelectorAll('.btn-view-gazette').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const row = e.target.closest('tr');
            if (!row) return;

            const fir = row.getAttribute('data-fir');
            const ps = row.getAttribute('data-ps');
            const district = row.getAttribute('data-district');
            const sections = row.getAttribute('data-sections');
            const complainant = row.getAttribute('data-complainant');
            const accused = row.getAttribute('data-accused');
            const occur = row.getAttribute('data-occurrence');
            const rep = row.getAttribute('data-reported');
            const io = row.getAttribute('data-io');
            const sho = row.getAttribute('data-sho');
            const shoId = row.getAttribute('data-sho-id');
            const hash = row.getAttribute('data-hash');
            const gist = row.getAttribute('data-gist');

            if (gazetteHeaderTitle) gazetteHeaderTitle.textContent = fir;
            if (gazettePs) gazettePs.textContent = `${ps}, ${district}`;
            if (gazetteFirNumber) gazetteFirNumber.textContent = fir;
            if (gazetteSections) gazetteSections.textContent = sections;
            if (gazetteIo) gazetteIo.textContent = io;
            if (gazetteOccurTime) gazetteOccurTime.textContent = occur;
            if (gazetteReportedTime) gazetteReportedTime.textContent = rep;
            if (gazetteComplainant) gazetteComplainant.textContent = complainant;
            if (gazetteAccused) gazetteAccused.textContent = accused;
            if (gazetteGistText) gazetteGistText.textContent = gist;
            if (gazetteHash) gazetteHash.textContent = hash;
            if (gazetteShoName) gazetteShoName.textContent = sho;
            if (gazetteShoId) gazetteShoId.textContent = shoId;

            if (gazetteModal) gazetteModal.classList.add('active');
        });
    });

    const lodgeModal = document.getElementById('lodgeFirModal');
    const btnOpenLodge = document.getElementById('btnLodgeFir');
    if (btnOpenLodge && lodgeModal) {
        btnOpenLodge.addEventListener('click', () => {
            lodgeModal.classList.add('active');
        });
    }

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const printFirBtn = document.getElementById('btnPrintFir');
    if (printFirBtn) {
        printFirBtn.addEventListener('click', () => {
            window.print();
        });
    }

    const lodgeForm = document.getElementById('lodgeFirForm');
    if (lodgeForm) {
        lodgeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('btnSubmitFir');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="ph ph-check"></i> FIR Logged & Synced to Ledger';
                submitBtn.style.background = 'var(--success)';
            }
            setTimeout(() => {
                if (lodgeModal) lodgeModal.classList.remove('active');
                lodgeForm.reset();
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="ph ph-lock-key"></i> Register & Dispatch to IO';
                    submitBtn.style.background = 'var(--primary-navy)';
                }
            }, 1200);
        });
    }
});