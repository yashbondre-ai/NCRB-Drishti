document.addEventListener('DOMContentLoaded', () => {
    const artifactCards = document.querySelectorAll('.artifact-card');
    const categoryLinks = document.querySelectorAll('.cat-link');
    const searchInput = document.getElementById('vaultSearchInput');
    const filesCountLabel = document.getElementById('vaultFilesCount');

    const inspectorFormatBadge = document.getElementById('inspectorFormatBadge');
    const inspectorFileName = document.getElementById('inspectorFileName');
    const inspectorMime = document.getElementById('inspectorMime');
    const previewIcon = document.getElementById('previewIcon');
    const inspectorBanner = document.getElementById('inspectorBanner');
    const inspectorBannerIcon = document.getElementById('inspectorBannerIcon');
    const inspectorBannerTitle = document.getElementById('inspectorBannerTitle');
    const inspectorBannerDesc = document.getElementById('inspectorBannerDesc');
    const inspectorCaseId = document.getElementById('inspectorCaseId');
    const inspectorSize = document.getElementById('inspectorSize');
    const inspectorOfficer = document.getElementById('inspectorOfficer');
    const inspectorDate = document.getElementById('inspectorDate');
    const inspectorBlock = document.getElementById('inspectorBlock');
    const inspectorSeizureHash = document.getElementById('inspectorSeizureHash');
    const inspectorVaultHash = document.getElementById('inspectorVaultHash');
    const btnCopyFullHash = document.getElementById('btnCopyFullHash');

    function updateInspector(card) {
        if (!card) return;

        const file = card.getAttribute('data-file');
        const caseId = card.getAttribute('data-case');
        const size = card.getAttribute('data-size');
        const format = card.getAttribute('data-format');
        const date = card.getAttribute('data-date');
        const officer = card.getAttribute('data-officer');
        const block = card.getAttribute('data-block');
        const hash = card.getAttribute('data-hash');
        const status = card.getAttribute('data-status');
        const type = card.getAttribute('data-type');

        if (inspectorFileName) inspectorFileName.textContent = file;
        if (inspectorCaseId) inspectorCaseId.textContent = caseId;
        if (inspectorSize) inspectorSize.textContent = size;
        if (inspectorMime) inspectorMime.textContent = format;
        if (inspectorOfficer) inspectorOfficer.textContent = officer;
        if (inspectorDate) inspectorDate.textContent = date;
        if (inspectorBlock) inspectorBlock.textContent = block;
        if (inspectorSeizureHash) inspectorSeizureHash.textContent = hash;

        if (inspectorFormatBadge) {
            inspectorFormatBadge.textContent = type.toUpperCase();
        }

        if (previewIcon) {
            if (type === 'pdf') previewIcon.className = 'ph ph-file-pdf';
            else if (type === 'media') previewIcon.className = 'ph ph-video';
            else if (type === 'audio') previewIcon.className = 'ph ph-speaker-high';
            else previewIcon.className = 'ph ph-cpu';
        }

        if (status === 'flagged') {
            inspectorBanner.className = 'inspector-status-banner flagged';
            inspectorBannerIcon.className = 'ph-fill ph-warning-octagon';
            inspectorBannerTitle.textContent = 'Integrity Mismatch Quarantined';
            inspectorBannerDesc.textContent = 'Bit alteration detected. Hash fails TiDB ledger consensus.';
            if (inspectorVaultHash) {
                inspectorVaultHash.textContent = 'MISMATCH_CORRUPTED_BLOCK_INTEGRITY_FAIL';
                inspectorVaultHash.className = 'compare-box font-mono mismatch';
            }
        } else {
            inspectorBanner.className = 'inspector-status-banner intact';
            inspectorBannerIcon.className = 'ph-fill ph-shield-check';
            inspectorBannerTitle.textContent = 'Cryptographic Integrity Match';
            inspectorBannerDesc.textContent = 'Bit-level verification matches TiDB distributed ledger.';
            if (inspectorVaultHash) {
                inspectorVaultHash.textContent = hash;
                inspectorVaultHash.className = 'compare-box font-mono';
            }
        }
    }

    artifactCards.forEach(card => {
        card.addEventListener('click', () => {
            artifactCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            updateInspector(card);
        });
    });

    function filterArtifacts() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const activeCat = document.querySelector('.cat-link.active');
        const targetType = activeCat ? activeCat.getAttribute('data-filter') : 'all';

        let count = 0;
        let firstVisible = null;

        artifactCards.forEach(card => {
            const cardType = card.getAttribute('data-type');
            const cardStatus = card.getAttribute('data-status');
            const cardText = card.textContent.toLowerCase();

            let matchesCat = false;
            if (targetType === 'all') matchesCat = true;
            else if (targetType === 'flagged') matchesCat = (cardStatus === 'flagged');
            else matchesCat = (cardType === targetType);

            const matchesSearch = (!query || cardText.includes(query));

            if (matchesCat && matchesSearch) {
                card.style.display = 'flex';
                count++;
                if (!firstVisible) firstVisible = card;
            } else {
                card.style.display = 'none';
            }
        });

        if (filesCountLabel) {
            filesCountLabel.textContent = `${count} Artifacts Selected`;
        }

        if (firstVisible && !document.querySelector('.artifact-card.active:not([style*="display: none"])')) {
            artifactCards.forEach(c => c.classList.remove('active'));
            firstVisible.classList.add('active');
            updateInspector(firstVisible);
        }
    }

    if (searchInput) {
        searchInput.addEventListener('input', filterArtifacts);
    }

    categoryLinks.forEach(link => {
        link.addEventListener('click', () => {
            categoryLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            filterArtifacts();
        });
    });

    if (btnCopyFullHash && inspectorSeizureHash) {
        btnCopyFullHash.addEventListener('click', () => {
            navigator.clipboard.writeText(inspectorSeizureHash.textContent);
            btnCopyFullHash.innerHTML = '<i class="ph ph-check text-success"></i>';
            setTimeout(() => {
                btnCopyFullHash.innerHTML = '<i class="ph ph-copy"></i>';
            }, 1800);
        });
    }

    const firstCard = document.querySelector('.artifact-card.active');
    if (firstCard) {
        updateInspector(firstCard);
    }
});