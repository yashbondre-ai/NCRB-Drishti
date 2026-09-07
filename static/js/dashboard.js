document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('docChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = 70;
        const lineWidth = 18;
        const data = [
            { pct: 0.27, color: '#2563EB' },
            { pct: 0.21, color: '#6366F1' },
            { pct: 0.18, color: '#C9A227' },
            { pct: 0.16, color: '#0E7C86' },
            { pct: 0.12, color: '#38BDF8' },
            { pct: 0.06, color: '#64748B' }
        ];
        let startAngle = -Math.PI / 2;
        data.forEach(item => {
            const sliceAngle = item.pct * (2 * Math.PI);
            const endAngle = startAngle + sliceAngle;
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, startAngle, endAngle - 0.03);
            ctx.strokeStyle = item.color;
            ctx.lineWidth = lineWidth;
            ctx.lineCap = 'round';
            ctx.stroke();
            startAngle = endAngle;
        });
    }

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('active');
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('active');
    }

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modalId = btn.getAttribute('data-close');
            closeModal(modalId);
        });
    });

    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                backdrop.classList.remove('active');
            }
        });
    });

    const btnOpenUpload = document.getElementById('btnOpenUploadModal');
    if (btnOpenUpload) {
        btnOpenUpload.addEventListener('click', () => openModal('uploadModal'));
    }

    const btnTriggerCustody = document.getElementById('btnTriggerCustodyDemo');
    if (btnTriggerCustody) {
        btnTriggerCustody.addEventListener('click', () => openModal('custodyModal'));
    }

    const btnTriggerCert = document.getElementById('btnTriggerCertDemo');
    if (btnTriggerCert) {
        btnTriggerCert.addEventListener('click', () => openModal('certModal'));
    }

    async function computeFileSHA256(file) {
        const buffer = await file.arrayBuffer();
        const digestBuffer = await crypto.subtle.digest('SHA-256', buffer);
        const hashArray = Array.from(new Uint8Array(digestBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    const evidenceInput = document.getElementById('evidenceFileInput');
    const hashCard = document.getElementById('hashCalculationCard');
    const fileNameSpan = document.getElementById('selectedFileName');
    const fileSizeSpan = document.getElementById('selectedFileSize');
    const hashStringSpan = document.getElementById('calculatedHashString');

    if (evidenceInput) {
        evidenceInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            fileNameSpan.textContent = file.name;
            fileSizeSpan.textContent = (file.size / 1024).toFixed(1) + ' KB';
            hashStringSpan.textContent = 'Computing SHA-256 Digest...';
            hashCard.style.display = 'flex';

            try {
                const hash = await computeFileSHA256(file);
                hashStringSpan.textContent = hash;
            } catch (err) {
                hashStringSpan.textContent = 'Hashing error encountered.';
            }
        });
    }

    const btnCopy = document.getElementById('btnCopyHash');
    if (btnCopy) {
        btnCopy.addEventListener('click', () => {
            if (hashStringSpan) {
                navigator.clipboard.writeText(hashStringSpan.textContent);
                btnCopy.innerHTML = '<i class="ph ph-check"></i>';
                setTimeout(() => {
                    btnCopy.innerHTML = '<i class="ph ph-copy"></i>';
                }, 2000);
            }
        });
    }

    const uploadForm = document.getElementById('evidenceUploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('btnVaultSubmit');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="ph ph-check"></i> Sealed & Committed to Vault';
                submitBtn.style.background = 'var(--success)';
            }
            setTimeout(() => {
                closeModal('uploadModal');
                uploadForm.reset();
                if (hashCard) hashCard.style.display = 'none';
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="ph ph-lock-key"></i> Seal & Vault Evidence';
                    submitBtn.style.background = 'var(--primary-navy)';
                }
            }, 1200);
        });
    }

    const custodyLabel = document.getElementById('custodyDocLabel');
    document.querySelectorAll('.btn-view-custody').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const row = e.target.closest('tr');
            if (row && custodyLabel) {
                const doc = row.getAttribute('data-doc');
                custodyLabel.textContent = `Document: ${doc}`;
            }
            openModal('custodyModal');
        });
    });

    const certDocName = document.getElementById('certDocName');
    const certCaseId = document.getElementById('certCaseId');
    const certOfficer = document.getElementById('certOfficer');
    const certHashVal = document.getElementById('certHashVal');

    document.querySelectorAll('.btn-view-cert').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const row = e.target.closest('tr');
            if (row) {
                if (certDocName) certDocName.textContent = row.getAttribute('data-doc');
                if (certCaseId) certCaseId.textContent = row.getAttribute('data-case');
                if (certOfficer) certOfficer.textContent = row.getAttribute('data-officer');
                if (certHashVal) certHashVal.textContent = row.getAttribute('data-hash');
            }
            openModal('certModal');
        });
    });

    const btnPrint = document.getElementById('btnPrintCert');
    if (btnPrint) {
        btnPrint.addEventListener('click', () => {
            window.print();
        });
    }

    const filterChips = document.querySelectorAll('.filter-chip');
    const tableRows = document.querySelectorAll('#evidenceTable tbody tr');
    const countText = document.getElementById('tableCountText');

    filterChips.forEach(chip => {
        chip.addEventListener('click', () => {
            filterChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            const target = chip.getAttribute('data-filter');

            let visibleCount = 0;
            tableRows.forEach(row => {
                const status = row.getAttribute('data-status');
                if (target === 'all' || status === target) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            if (countText) {
                countText.textContent = `Showing ${visibleCount} of ${tableRows.length} records`;
            }
        });
    });

    const topbarSearch = document.querySelector('.search-container input');
    if (topbarSearch) {
        topbarSearch.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();
            let visibleCount = 0;

            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(term)) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            if (countText) {
                countText.textContent = `Showing ${visibleCount} of ${tableRows.length} records`;
            }
        });
    }
});