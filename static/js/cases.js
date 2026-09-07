document.addEventListener('DOMContentLoaded', () => {
    const caseSearchInput = document.getElementById('caseSearchInput');
    const caseChips = document.querySelectorAll('.case-chip');
    const tableRows = document.querySelectorAll('#casesMasterTable tbody tr');
    const recordCounter = document.getElementById('caseRecordCounter');

    function updateCounter(visible) {
        if (recordCounter) {
            recordCounter.textContent = `Showing ${visible} of ${tableRows.length} Records`;
        }
    }

    function filterMasterTable() {
        const query = caseSearchInput ? caseSearchInput.value.toLowerCase().trim() : '';
        const activeChip = document.querySelector('.case-chip.active');
        const filterType = activeChip ? activeChip.getAttribute('data-filter') : 'all';

        let count = 0;
        tableRows.forEach(row => {
            const rowStatus = row.getAttribute('data-status');
            const rowText = row.textContent.toLowerCase();

            const matchesFilter = (filterType === 'all' || rowStatus === filterType);
            const matchesSearch = (!query || rowText.includes(query));

            if (matchesFilter && matchesSearch) {
                row.style.display = '';
                count++;
            } else {
                row.style.display = 'none';
            }
        });

        updateCounter(count);
    }

    if (caseSearchInput) {
        caseSearchInput.addEventListener('input', filterMasterTable);
    }

    caseChips.forEach(chip => {
        chip.addEventListener('click', () => {
            caseChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            filterMasterTable();
        });
    });

    const dossierModal = document.getElementById('caseDossierModal');
    const dossierCaseId = document.getElementById('dossierCaseId');
    const dossierCaseTitle = document.getElementById('dossierCaseTitle');
    const dossierComplainant = document.getElementById('dossierComplainant');
    const dossierAccused = document.getElementById('dossierAccused');
    const dossierOfficer = document.getElementById('dossierOfficer');
    const dossierCourt = document.getElementById('dossierCourt');
    const dossierSections = document.getElementById('dossierSections');
    const dossierDate = document.getElementById('dossierDate');

    function updatePipelineTracker(status) {
        const nodeFir = document.getElementById('nodeFir');
        const nodeEvidence = document.getElementById('nodeEvidence');
        const nodeForensic = document.getElementById('nodeForensic');
        const nodeChargeSheet = document.getElementById('nodeChargeSheet');
        const nodeTrial = document.getElementById('nodeTrial');

        const line1 = document.getElementById('line1');
        const line2 = document.getElementById('line2');
        const line3 = document.getElementById('line3');
        const line4 = document.getElementById('line4');

        const allNodes = [nodeFir, nodeEvidence, nodeForensic, nodeChargeSheet, nodeTrial];
        const allLines = [line1, line2, line3, line4];

        allNodes.forEach(n => {
            if (n) {
                n.className = 'track-node';
                const circle = n.querySelector('.node-circle');
                if (circle) circle.innerHTML = '<i class="ph ph-circle"></i>';
            }
        });
        allLines.forEach(l => { if (l) l.className = 'track-line'; });

        if (status === 'active') {
            nodeFir.classList.add('completed');
            nodeFir.querySelector('.node-circle').innerHTML = '<i class="ph-fill ph-check"></i>';
            line1.classList.add('completed');

            nodeEvidence.classList.add('completed');
            nodeEvidence.querySelector('.node-circle').innerHTML = '<i class="ph-fill ph-check"></i>';
            line2.classList.add('completed');

            nodeForensic.classList.add('active');
            nodeForensic.querySelector('.node-circle').innerHTML = '<i class="ph ph-fingerprint"></i>';
        } else if (status === 'chargesheet') {
            [nodeFir, nodeEvidence, nodeForensic].forEach(n => {
                n.classList.add('completed');
                n.querySelector('.node-circle').innerHTML = '<i class="ph-fill ph-check"></i>';
            });
            [line1, line2, line3].forEach(l => l.classList.add('completed'));

            nodeChargeSheet.classList.add('active');
            nodeChargeSheet.querySelector('.node-circle').innerHTML = '<i class="ph ph-file-text"></i>';
        } else if (status === 'trial') {
            [nodeFir, nodeEvidence, nodeForensic, nodeChargeSheet].forEach(n => {
                n.classList.add('completed');
                n.querySelector('.node-circle').innerHTML = '<i class="ph-fill ph-check"></i>';
            });
            [line1, line2, line3, line4].forEach(l => l.classList.add('completed'));

            nodeTrial.classList.add('active');
            nodeTrial.querySelector('.node-circle').innerHTML = '<i class="ph ph-gavel"></i>';
        } else if (status === 'disposed') {
            allNodes.forEach(n => {
                n.classList.add('completed');
                n.querySelector('.node-circle').innerHTML = '<i class="ph-fill ph-check"></i>';
            });
            allLines.forEach(l => l.classList.add('completed'));
        }
    }

    document.querySelectorAll('.btn-open-dossier').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const row = e.target.closest('tr');
            if (!row) return;

            const caseId = row.getAttribute('data-case');
            const title = row.getAttribute('data-title');
            const sections = row.getAttribute('data-sections');
            const io = row.getAttribute('data-io');
            const date = row.getAttribute('data-date');
            const complainant = row.getAttribute('data-complainant');
            const accused = row.getAttribute('data-accused');
            const court = row.getAttribute('data-court');
            const status = row.getAttribute('data-status');

            if (dossierCaseId) dossierCaseId.textContent = caseId;
            if (dossierCaseTitle) dossierCaseTitle.textContent = title;
            if (dossierComplainant) dossierComplainant.textContent = complainant;
            if (dossierAccused) dossierAccused.textContent = accused;
            if (dossierOfficer) dossierOfficer.textContent = io;
            if (dossierCourt) dossierCourt.textContent = court;
            if (dossierSections) dossierSections.textContent = sections;
            if (dossierDate) dossierDate.textContent = date;

            updatePipelineTracker(status);

            if (dossierModal) dossierModal.classList.add('active');
        });
    });

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const printBtn = document.getElementById('btnPrintDocket');
    if (printBtn) {
        printBtn.addEventListener('click', () => {
            window.print();
        });
    }
});